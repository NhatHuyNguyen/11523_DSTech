# app.py — the DSTS 11523 Course TA web page (Week 11, Part 8). TA = teaching assistant.
# How to start it: open a terminal in the Week 11 folder, make the Week 10 Python environment
# active, then type:
#     python -m streamlit run app.py
# It opens http://localhost:8501 in your browser; stop it with Ctrl+C in the terminal.
# Streamlit = the Python library that draws this page; it reruns this whole script after each click.
# How it answers: every message goes to the AGENT in course_ta.py (made from the notebook's code).
# The MODEL (LLM = large language model) decides what to do: it answers chat and general questions
# directly (with a label), or it calls the search_tutorials tool and writes a grounded answer (one
# based only on tutorial passages), which we then check (its quotes and its sources).
import os                                                 # to change the working folder
import sys                                                # to stop Python writing .pyc cache files
import time                                               # to time the warm-up
from pathlib import Path                                  # file paths that work on Windows and macOS

# Work inside this file's own folder, so paths such as corpus/ work wherever Streamlit was started.
HERE = Path(__file__).resolve().parent                    # the Week11_Student_Files folder (where this file is)
os.chdir(HERE)                                            # course_ta reads corpus/, gold/ and the replay files from here
sys.dont_write_bytecode = True                            # no __pycache__ folder in your student folder

# The libraries the page needs.
import base64                                             # to put the logo inside the page
import json                                               # chat history as text, for the cache key
import chromadb                                           # the vector database (the app keeps its own copy in memory)
import pandas as pd                                       # to read the gold questions
import requests                                           # to talk to Ollama (it runs the model)
import streamlit as st                                    # the web page library
from chromadb.config import Settings                      # Chroma settings (no telemetry)

# course_ta.py is generated from the notebook cells, so this page uses exactly the notebook's code.
import course_ta as ta                                    # the search, checked answer and agent

st.set_page_config(page_title="DSTS 11523 Course TA", layout="wide")   # the browser tab's title; use the full width

# The example buttons in the sidebar. They are all recorded, so Replay mode can answer them.
GOLD = pd.read_csv("gold/gold_questions.csv")             # the 11 gold questions: their answers are recorded
EXAMPLES = GOLD.set_index("id").loc[["Q03", "Q06", "Q08", "Q10", "Q11"], "question"].tolist()   # 5 clickable examples
# Add 4 more recorded questions: 3 more tutorial questions and one general question (the last one).
EXAMPLES += ["how do I handle missing values?", "how did we handle missing values in week 2?",
             "show me summary about week1 content", "what is overfitting?"]   # 9 examples in total
# The recorded demo for the "Try a demo conversation" button: one chat, asked in this order.
# "explain it" is a follow-up: it only makes sense together with the question before it.
DEMO = ["hi", "how are you today", "how do I apply pca", "explain it", "what about kubernetes", "what is overfitting?",
        "thanks"]                                         # 7 messages in total
# The chat models you can choose in Live mode (Live mode = ask Ollama for new, real replies).
# The default was chosen by the bake-off (the notebook's model comparison); the other is a fallback.
MODELS = {ta.TA_MODEL: "default — chosen by the bake-off", "qwen2.5:3b": "fallback — the Parts 1-7 model"}   # Live choices
# The one line shown when Replay mode has no recording for a message.
# Replay mode = reuse recorded real replies, so no Ollama is needed (only recorded messages work).
NO_RECORDING = "Replay mode can only answer the recorded messages — pick an example or the demo from the sidebar, or switch to Live mode."
# The label of the progress box for each step of the agent: deciding, searching, then writing.
STEP_LABEL = {"think": "Thinking…", "search": "Searching the tutorials…", "answer": "Writing the answer…"}   # progress


# get_index() builds the search index: tutorials, then chunks, then vectors (embeddings), then
# a Chroma collection plus a BM25 keyword index (Parts 2-7). cache_resource = keep one object for
# the whole server instead of rebuilding it on each rerun, so this slow step happens only once.
@st.cache_resource(show_spinner="Building the search index (only the first time) ...")   # built ONCE per server (speed)
def get_index():                                          # the search index of Parts 2-7
    # An in-memory Chroma database: nothing is written to disk, so there are no files and no locks.
    ta.client = chromadb.EphemeralClient(settings=Settings(anonymized_telemetry=False))   # in memory: no files, no locks
    mode_before = ta.USE_RECORDED                         # the sidebar's mode (Live or Replay), put back at the end
    # First try the recorded chunk vectors: no Ollama needed, and they are identical to live ones.
    ta.USE_RECORDED = True                                # True = replay: use recorded vectors
    try:                                                  # usually every vector is recorded
        return ta.build_ta_index("course_ta_app")         # exactly the function of notebook Exercise 19.1
    except KeyError:                                      # a chunk is not recorded (e.g. a corpus file was edited)
        ta.USE_RECORDED = False                           # False = live: then embed the chunks with Ollama (a few minutes)
        return ta.build_ta_index("course_ta_app")         # the same index, with live vectors
    finally:                                              # always, even after an error:
        ta.USE_RECORDED = mode_before                     # restore the sidebar's mode, so Live stays Live


# ollama_models() asks Ollama which models are downloaded. It returns a list of model names,
# or None when Ollama is not running (no answer, or none within 3 seconds).
def ollama_models():                                      # a list of names, or None
    try:                                                  # ask Ollama
        # /api/tags lists the downloaded models; keep only their names.
        return [m["name"] for m in requests.get(ta.OLLAMA_URL + "/api/tags", timeout=3).json()["models"]]   # names
    except requests.RequestException:                     # no answer at all
        return None                                       # not running


# warm_up() loads the chat model into memory once (cached for the whole server), so your first real
# question is not slow. It returns how many seconds the loading took.
@st.cache_resource(show_spinner="Warming up the model … (only once; loading it into memory can take a minute)")   # once
def warm_up(model):                                       # load the model once
    start = time.perf_counter()                           # start the stopwatch
    # An empty prompt means "just load the model"; keep_alive "30m" keeps it loaded for 30 minutes.
    requests.post(ta.OLLAMA_URL + "/api/generate", json={"model": model, "prompt": "", "keep_alive": "30m"},   # empty
                  timeout=600)                            # wait up to 10 minutes
    return round(time.perf_counter() - start, 1)          # seconds the loading took


# ask() answers ONE message. It sends the message, plus the chat so far if the history switch
# is on, to the agent. It always returns a result dict (a reply, or one "error" line), so it
# never crashes the page.
def ask(message, history, settings):                      # returns one result
    live, model, top_k, use_history = settings            # the sidebar settings
    sent = history if use_history else []                 # the turns we send with the message (the model has no memory)
    # A small cache: if the same message, history and settings were answered before in this session,
    # reuse that answer instead of calling the model again. session_state = what Streamlit remembers
    # between reruns of this script (here, a dict of earlier answers under the name "cache").
    key = (message, json.dumps(sent), settings)           # message, history as text, settings
    cache = st.session_state.setdefault("cache", {})      # the saved answers (empty at first)
    if key in cache:                                      # seen before? then reuse it
        return {**cache[key], "cached": True}             # marked as cached
    # Get the search index first (built once per server), so building it cannot reset the mode.
    index = get_index()                                   # the search index
    # Set the mode for course_ta: True = Replay (recorded real replies only, no Ollama),
    # False = Live (ask Ollama).
    ta.USE_RECORDED = not live                            # Replay unless Live is chosen
    # The progress box: an empty placeholder holds a status box that shows each step; the
    # placeholder is cleared when the reply is ready.
    box = st.empty()                                      # a placeholder for the progress box
    with box.container(), st.status(STEP_LABEL["think"], expanded=False) as status:   # progress steps
        # on_step() is called by course_ta with "think", then "search", then "answer".
        def on_step(step):                                # course_ta calls this at each step
            status.update(label=STEP_LABEL[step])         # show that step's label
        # Run the agent (notebook Exercise 20.1): the model decides, then it may search the
        # tutorials, and a grounded answer is checked.
        try:                                              # run the agent
            result = ta.ta_agent(message, index, sent, model, top_k, on_step)   # notebook Exercise 20.1
        # Each kind of failure below becomes ONE short error line instead of a crash.
        except KeyError:                                  # Replay mode: this was never recorded
            result = {"question": message, "error": NO_RECORDING}   # one short line
        except requests.HTTPError as e:                   # Ollama answered with an error
            missing = e.response is not None and e.response.status_code == 404   # 404 = the model is not downloaded
            # Model missing: say how to download it. Any other error: show the error itself.
            result = {"question": message, "error": f"{model} is not downloaded: run  ollama pull {model}  in a terminal."
                      if missing else f"Ollama returned an error ({e}). Try again, or use Replay mode."}   # one line
        except requests.RequestException as e:           # Live mode, but Ollama did not answer
            result = {"question": message, "error": "Ollama did not answer (" + type(e).__name__ + "). "   # why
                      "Open the Ollama app, or use Replay mode."}   # one short line
        status.update(label="Done", state="complete")     # mark the progress box as finished
    # Remove the progress box; the answer is drawn in the chat bubble in its place.
    box.empty()                                           # remove the box from the page
    # Extra facts for the screen: how many earlier turns were sent (one turn = 2 entries: the
    # question and its reply), and which mode this reply came from (for its timing line).
    result["history_sent"] = len(sent) // 2               # how many earlier turns went with this message
    result["replay"] = not live                           # the mode this reply came from (for its timing line)
    # Only real answers go in the cache: after an error the user must be able to try again.
    if "error" not in result:                             # cache real answers only
        cache[key] = result                               # remember it for the rest of the session
    return result                                         # one result for the screen


# check_caption() writes the one-line verdict under a tutorial answer: did the checks pass?
def check_caption(r):                                     # ONE short line: did the checks pass?
    # route = how a quote was verified: exact, relaxed, cleaned, matched (similar) or not found.
    routes = [x for x in r.get("evidence_route", []) if x != "not found"]   # the verified quotes
    if r.get("accepted") and routes and all(x == "matched" for x in routes):   # verified only by matching
        return "✓ quotes matched to the tutorial text"     # real lines, found by similarity
    if r.get("accepted"):                                 # passed every check
        return "✓ quotes verified"                        # exact, relaxed or cleaned quotes
    # Otherwise the answer failed a check: tell the user where to look.
    return "⚠ Couldn't verify this answer against the tutorials — open Show evidence and passages to check."   # failed


# timing_line() builds the timing text of one turn: how long each model call (and the search) took.
def timing_line(r):                                       # the measured steps of one turn, in one line
    if r.get("cached"):                                   # answered earlier in this chat
        return "cached (answered earlier in this chat)"   # no new call
    parts = []                                            # one piece per model call (and the search)
    # The steps: the "decide" call, then the grounded-answer call or (maybe) the label check.
    for s in r.get("steps", []):                          # one step = one model call
        # Reading and writing speed in tokens per second (tok/s), from Ollama's own counters;
        # empty text when the step has no speed numbers.
        speed = f", reads {s['prompt_tok_s']} tok/s, writes {s['output_tok_s']} tok/s" if s.get("output_tok_s") else ""
        parts.append(f"{s['call']} {s['seconds']} s ({s['output_tokens']} tokens{speed})")   # e.g. decide 6.1 s (...)
        if s["call"] == "decide" and "search_s" in r:     # the search runs between the two calls
            parts.append(f"search {r['search_s']} s")     # usually well under a second
    # Join all the pieces into one line and add the total time of the turn. In Replay mode, say that
    # these are the recorded live times.
    return " · ".join(parts) + f" · total {r.get('total_s', 0)} s" + (" (recorded live times)" if r.get("replay") else "")


# show() draws one TA reply: the answer, one short label line, then a fold-out with the evidence.
def show(r):                                              # draw one TA reply inside an assistant bubble
    if r.get("error"):                                    # no answer could be made
        st.markdown(r["error"])                           # ONE short line, no banner
        return                                            # nothing else to show
    meta = {p["chunk_id"]: p for p in r.get("passages", [])}   # passage details, looked up by chunk id
    # Show the reply as markdown (a simple text format), so bullet lists display properly.
    st.markdown(r.get("reply") or "*(the model gave no answer text)*")   # the model's own words
    # Under the reply, one label line that depends on the kind of reply.
    if r["kind"] == "grounded":                           # an answer from the tutorials
        names = [f"Week {meta[c]['week']} · {meta[c]['section']}" for c in r.get("sources", []) if c in meta]   # sources
        if names:                                         # at least one real source
            st.caption("Sources: " + " · ".join(dict.fromkeys(names)))   # one compact line, no duplicates
        st.caption(check_caption(r))                      # one short verdict line
    elif r["kind"] == "general":                          # the model answered from its own knowledge
        # The general label, and whether the tutorials were searched first (and had no answer).
        st.caption("ℹ " + ta.GENERAL_LABEL + (" (searched the tutorials: not found there)" if r.get("not_found") else ""))
    else:                                                 # chat, or a clarifying question
        st.caption(r["label"])                            # a lighter label
    with st.expander("Show evidence and passages"):       # everything else, folded away until clicked
        # First the details line: did the model call the search tool, which model, and how much
        # of the chat history it saw.
        how = (f"the model called search_tutorials(query={r['search_query']!r}, week={r.get('week_arg')})"   # the tool call
               if r.get("tool_called") else "the model answered directly (no search)")   # or not
        info = [how, f"model: {r['model']} ({'tool calling' if r['path'] == 'tools' else 'JSON decide call'})",   # how
                f"history sent: {r.get('history_sent', 0)} earlier turn(s)"]   # what the model saw of the chat
        if r.get("tool_called"):                          # the week filter that was really used
            # The week filter: the week the model passed (if you wrote a week), or none.
            info.append("filter: " + (f"week {r['filter']['week']}" if r.get("filter") else "none (all six tutorials)"))
        st.caption(" · ".join(info))                      # all of it in one line
        st.caption("timing: " + timing_line(r))           # speed, per step
        if r["kind"] == "grounded" and r.get("general_tip"):   # the model also wrote a general tip (not from the tutorials)
            st.markdown("**General tip** (" + ta.GENERAL_LABEL + "): " + r["general_tip"])   # labelled, kept out of the bubble
        if r.get("tool_called"):                          # a grounded answer: show how it was checked
            # The copy ratio: how much of the answer was copied from one passage.
            st.caption(f"copy ratio {r.get('copy_ratio')} (the longest stretch copied from a passage ÷ the answer length; "
                       f"above {ta.COPY_THRESHOLD} = mostly copied)")   # did it explain or paste?
        # The mark shown for each route: ✓ = verified, ≈ = matched by similarity, ✗ = not found.
        mark = {"exact": "✓ exact", "relaxed": "✓ relaxed match", "cleaned": "✓ cleaned", "matched": "≈ matched",   # route
                "not found": "✗ not found"}               # marks for each quote
        # For each quote: its mark, then the real tutorial line (or the model's text if not found).
        for quote, route, real in zip(r.get("evidence", []), r.get("evidence_route", []), r.get("evidence_verified", [])):   # each
            st.markdown(f"**Quote {mark.get(route, route)}**")   # how it was verified
            st.code(real if route != "not found" else quote, language="text")   # the real line (or the model's)
            if route == "matched":                        # matched: also show what the model wrote
                st.caption("the model wrote: " + quote)   # small grey text
        for p in meta.values():                           # every passage the model read, best first
            st.markdown(f"**Passage {p['chunk_id']}** · Week {p['week']} · {p['source_file']} · {p['section']}")   # header
            st.code(p["text"], language="markdown")       # the passage text


# run() handles one NEW message: it shows the message, answers it right below, and remembers both.
def run(message, settings):                               # handle one new message
    with st.chat_message("user"):                         # the user's bubble, at the end of the chat
        st.write(message)                                 # the message
    with st.chat_message("assistant"):                    # the TA's bubble, directly under the question
        r = ask(message, st.session_state["history"], settings)   # the progress box shows here, then disappears
        show(r)                                           # the reply takes its place, in the same bubble
    # Store both bubbles in session_state now; the next rerun draws them from there, so each bubble
    # is drawn only once.
    st.session_state["messages"].append({"role": "user", "text": message})   # stored now, drawn by the next rerun
    st.session_state["messages"].append({"role": "assistant", "result": r})   # (so each bubble is drawn only once)
    # A real reply (not an error) becomes part of the chat history that is sent with later messages.
    if not r.get("error"):                                # a real reply: it becomes part of the chat history
        st.session_state["history"] = ta.history_after(st.session_state["history"], r)   # + this question and reply


# ---- The page itself: this part runs from top to bottom on every rerun ----
# The logo file, turned into base64 text so that it can sit directly inside the page's HTML.
logo = base64.b64encode((HERE / "assets" / "logo.svg").read_bytes()).decode("ascii")   # the logo as text for HTML
# The two lists that Streamlit remembers between reruns: messages = the bubbles drawn on screen,
# history = the earlier turns we send to the model.
for name in ["messages", "history"]:                      # the first time the page runs
    st.session_state.setdefault(name, [])                 # an empty conversation and an empty history
# ---- The sidebar (the left panel): the mode, the model, the settings and the example buttons ----
with st.sidebar:                                          # everything in the left panel
    st.header("Settings")                                 # panel title
    # The mode switch: Replay (recorded real replies, no Ollama) or Live (new replies from Ollama).
    mode = st.radio("Mode", ["Replay (recorded answers)", "Live (Ollama)"])   # Replay works without Ollama
    live, model = mode.startswith("Live"), ta.TA_MODEL    # True for Live mode; the default model
    # Live mode: Ollama must be running and the chosen model downloaded; then it is loaded once.
    if live:                                              # Live mode: check Ollama first
        names = ollama_models()                           # what Ollama has
        # Choose the chat model: the default or the fallback (see MODELS at the top).
        model = st.selectbox("Chat model", list(MODELS), format_func=lambda m: f"{m} ({MODELS[m]})")   # default or fallback
        if names is None:                                 # Ollama does not answer
            st.error("Ollama is not running at " + ta.OLLAMA_URL + ". Open the Ollama app, or choose Replay.")   # say so
        elif model not in names:                          # the model is not downloaded
            st.warning(f"{model} is not downloaded: run  ollama pull {model}  in a terminal.")   # the fix
        else:                                             # ready: load the model once
            # warm_up is cached, so the time is measured only the first time and reused afterwards.
            took = warm_up(model)                         # seconds (measured only once)
            # A real load takes seconds, so under 0.5 seconds means the model was already in memory.
            loaded = "; it was already in memory" if took < 0.5 else ""   # fast = already loaded
            st.caption(f"model ready (warm-up took {took} s, once{loaded})")   # shown on every rerun
    else:                                                 # Replay mode: be honest about what it can do
        # What Replay mode can and cannot do.
        st.caption("Replay answers only the recorded messages (the examples, the demo and the gold questions), with the "
                   "default settings. Typing your own question needs Live mode.")   # what it can do
    # top-k = how many passages the model reads for a tutorial answer (a week summary reads 6).
    top_k = st.slider("Passages for a tutorial answer (top-k)", 1, 8, ta.TA_TOP_K)   # default 3 (a week summary reads 6)
    # History switch: on = send the last chat turns with each message; off = each message alone.
    use_history = st.toggle(f"Send the chat history (last {ta.HISTORY_TURNS} turns)", value=True)   # off = each message alone
    settings = (live, model, top_k, use_history)          # everything that changes an answer
    if st.button("Clear chat"):                           # forget the conversation shown on screen
        st.session_state["messages"], st.session_state["history"] = [], []   # and the history we send
    pending = []                                          # messages to ask (handled in the main area, below)
    if st.button("Try a demo conversation"):              # play the recorded demo (a new chat)
        st.session_state["messages"], st.session_state["history"] = [], []   # it starts from an empty chat
        pending = DEMO                                    # ask the 7 demo messages in order
    st.subheader("Example questions")                     # recorded, so they also work in Replay mode
    for i, example in enumerate(EXAMPLES):                # one button per example question
        if st.button(example, key=f"example_{i}"):        # True when this button was clicked
            st.session_state["messages"], st.session_state["history"] = [], []   # each example = a new chat
            pending = [example]                           # ask this one question

# ---- The main area: the logo, the title, the chat so far, then any new messages ----
st.markdown(f'<img src="data:image/svg+xml;base64,{logo}" width="260" alt="DSTS 11523 Course TA logo">',   # the logo
            unsafe_allow_html=True)                       # allow this one small piece of HTML
st.title("DSTS 11523 Course TA")                          # the page title
# One sentence that tells the user what the TA can do.
st.write("Ask about the Weeks 1–6 tutorials, or anything else. Tutorial answers come with sources and checks; "   # the
         "other answers are labelled *general*.")         # a one-line promise to the user
# One line that explains how the chat memory works on this page.
st.caption(f"The model has no memory of its own: with each message this page sends the last {ta.HISTORY_TURNS} turns "   # how
           "of the chat (if the history switch is on).")  # how the chat memory works
# The chat box at the bottom; message is the typed text, or None when nothing new was sent.
message = st.chat_input("Ask about the Weeks 1–6 tutorials, or just say hi ...")   # the chat box at the bottom
# First redraw the whole conversation so far (Streamlit rebuilds the page on every rerun).
for turn in st.session_state["messages"]:                 # first draw the conversation so far
    if turn["role"] == "user":                            # the user's bubble
        with st.chat_message("user"):                     # left-aligned bubble
            st.write(turn["text"])                        # the message
    else:                                                 # the TA's bubble
        with st.chat_message("assistant"):                # its bubble
            show(turn["result"])                          # the reply, its label, then the evidence fold-out
# Then handle the new messages: a clicked example, the demo, or a typed message.
for m in pending + ([message] if message else []):        # then the new messages
    run(m, settings)                                      # each goes below the last one, with its progress under it
