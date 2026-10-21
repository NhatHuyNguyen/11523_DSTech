DSTS 11523 - Week 11 Lab - RAG Foundations: a Course TA for the Weeks 1-6 tutorials - student files
====================================================================================================
Start with the tutorial DSTS_11523_Week11_Lab_RAG_Foundations.html (one file; it works offline).
The required lab (Parts 1-7) takes about 2 hours 40 minutes: Parts 1-6 in the 2-hour class, then Part 7 (improve the
search, ~40 min), which is required too. Part 8 (your Course TA web page, ~60 min) is OPTIONAL but important for
your final project app: complete it at home.

Week11_RAG_Foundations.ipynb            the lab notebook (PREPARED cells + TODO cells you complete)
Week11_RAG_Foundations_COMPLETE.ipynb   the finished notebook, for checking (it writes to complete_run\)
app.py                                  the Course TA web page (Part 8):  python -m streamlit run app.py
course_ta.py                            the pipeline that app.py uses, made from the notebook's code (do not edit)
assets\logo.svg                         the web page's logo
corpus\                                 the six Week 1-6 tutorials you will search (see corpus\README_CORPUS.txt)
gold\                                   gold questions and labels used to check the pipeline (see gold\README_GOLD.txt)
llm_replies_week11.json                 recorded real LLM replies, for replay mode
embeddings_week11.json                  recorded real embedding vectors, for replay mode
requirements_week11.txt                 the three new packages (chromadb, rank-bm25, streamlit), for your Week 10 environment
check_setup.py                          setup check:  python check_setup.py   (no Ollama: python check_setup.py --replay)

Setup (once, at home, about 10 minutes; tutorial "Step 0"). This lab REUSES your Week 10 environment.
No Week 10 setup yet? First do Step 0 of the Week 10 lab (DSTS_11523_Week10_Lab_Prompt_Engineering_Sentiment.html,
Week10_Student_Files.zip), then come back. Run these one at a time:
  1. Activate the Week 10 environment:
       venv, PowerShell:  C:\dsts\week10\Week10_Student_Files\.venv\Scripts\Activate.ps1
       venv, cmd:         C:\dsts\week10\Week10_Student_Files\.venv\Scripts\activate.bat
       venv, macOS:       source ~/dsts/week10/Week10_Student_Files/.venv/bin/activate
       Anaconda:          conda activate dsts-week10
  2. cd C:\dsts\week11\Week11_Student_Files          (macOS: cd ~/dsts/week11/Week11_Student_Files)
  3. python -m pip install -r requirements_week11.txt
  4. ollama pull nomic-embed-text          (the embedding model, 274 MB)
     ollama pull granite4:3b              (the Course TA's model, Part 8 only, 2.1 GB; optional)
     Disk: about 2.9 GB more in total (about 0.8 GB without granite4:3b).
     ollama list
  5. python check_setup.py
Then open the notebook:  jupyter lab   (VS Code / Cursor: Select Kernel -> the Week 10 .venv or dsts-week10).

The web page (Part 8): with the environment active, in this folder:  python -m streamlit run app.py
It opens http://localhost:8501 (http://127.0.0.1:8501 also works). Stop it with Ctrl+C in the terminal.
The model decides: it chats, answers general questions (labelled "General answer"), or searches the tutorials and
answers with sources and checks. The page sends the last 3 turns, so a follow-up ("explain it") works. Replay mode
answers the recorded examples and the demo conversation; Live mode (Ollama running) answers any message.

Replay mode (no Ollama, or a slow laptop): set USE_RECORDED = True in Exercise 1, the first code cell
(True = replay mode: the recorded real replies, no Ollama needed, NOT live; False = live calls to Ollama).
The notebook then uses the recorded real replies and vectors, so you get exactly our results, offline.
Live, the metadata extraction (Exercise 7) took about 45 minutes on our laptop, the TA answers (Exercise 19) about
36 minutes and the Course TA agent (Exercise 20) about 22 minutes: in class, run Exercises 7, 19 and 20 in replay mode.

Keep this folder OUTSIDE OneDrive (C:\dsts\week11\Week11_Student_Files, or ~/dsts/week11/Week11_Student_Files).
Your notebook writes outputs\ and chroma_week11\ in this folder.
Corpus: DSTS 11523 tutorials, for enrolled students only. Do not redistribute.
