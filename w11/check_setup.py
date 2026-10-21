"""DSTS 11523 Week 11 (RAG Foundations) - setup check. Run it in your activated Week 10 venv or conda env:
    python check_setup.py
No Ollama (replay mode)?
    python check_setup.py --replay
Prints OK / NOT OK for each requirement, with the fix next to every problem."""
import hashlib
import importlib
import platform
import shutil
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434"                     # 127.0.0.1, not localhost (faster on Windows)
CHAT_MODELS = ["qwen2.5:3b", "qwen2.5:1.5b"]              # Parts 1-7: either works live; replay matches qwen2.5:3b
TA_MODEL = "granite4:3b"                         # Part 8: the Course TA agent's model (chosen by a bake-off)
TA_MODEL_SIZE = "2.1 GB"                     # its download size
EMBED_MODEL = "nomic-embed-text"                          # the embedding model (274 MB)
CHROMA_VERSION = "1.5.9"                                  # pinned in requirements_week11.txt
REPLAY = "--replay" in sys.argv                           # replay mode: skip the Ollama checks
here = Path(__file__).resolve().parent                    # the Week11_Student_Files folder
problems = 0                                              # number of NOT OK lines


def check(name, ok, fix):                                 # print one OK / NOT OK line with its fix
    global problems
    problems += not ok
    print(("OK      " if ok else "NOT OK  ") + name + ("" if ok else "   ->  FIX: " + fix))


print("Python", sys.version.split()[0], "on", platform.system())
if sys.version_info[:2] == (3, 11):
    check("Python 3.11 (recommended; the lab was tested on 3.11)", True, "")
else:
    print("WARNING Python " + sys.version.split()[0] + " is not 3.11. Python 3.11 is recommended (as in Week 10).")

# any activated environment is fine: a venv (.venv) or a conda environment (e.g. dsts-week10)
prefix = Path(sys.prefix)
in_conda = (prefix / "conda-meta").exists()
in_venv = sys.prefix != sys.base_prefix
check("running inside an environment (" + ("conda: " + prefix.name if in_conda else "venv: " + prefix.name) + ")",
      in_conda or in_venv,
      "activate your Week 10 environment first (conda activate dsts-week10, or .venv\\Scripts\\Activate.ps1)")

# Week 10 packages: if any is missing, the Week 10 setup was not done in this environment
week10 = {"pandas": "pandas", "requests": "requests", "sklearn": "scikit-learn", "matplotlib": "matplotlib",
          "pydantic": "pydantic", "jupyterlab": "jupyterlab", "ipykernel": "ipykernel"}
missing10 = []
for module, dist in week10.items():
    try:
        importlib.import_module(module)
        check("package " + dist + " (Week 10)", True, "")
    except ImportError:
        missing10.append(dist)
        check("package " + dist + " (Week 10)", False,
              "do Week 10 Step 0 first (python -m pip install -r requirements_week10.txt), then run this check again")

# Week 11 packages (new this week)
try:
    importlib.import_module("numpy")
    check("package numpy (Week 11; comes with pandas)", True, "")
except ImportError:
    check("package numpy (Week 11)", False, "python -m pip install -r requirements_week11.txt")
try:
    importlib.import_module("chromadb")
    v = version("chromadb")
    check("package chromadb " + v + " (Week 11; tested with " + CHROMA_VERSION + ")", v == CHROMA_VERSION,
          "python -m pip install -r requirements_week11.txt")
except (ImportError, PackageNotFoundError):
    check("package chromadb (Week 11)", False, "python -m pip install -r requirements_week11.txt")
for module, dist, pinned in [("rank_bm25", "rank-bm25", "0.2.2"), ("streamlit", "streamlit", "1.66.0")]:   # Parts 7-8
    try:
        importlib.import_module(module)
        v = version(dist)
        check("package " + dist + " " + v + " (Week 11; tested with " + pinned + ")", v == pinned,
              "python -m pip install -r requirements_week11.txt")
    except (ImportError, PackageNotFoundError):
        check("package " + dist + " (Week 11)", False, "python -m pip install -r requirements_week11.txt")

# student files: corpus (6 tutorials, unchanged), gold files, replay files
CORPUS_SHA256 = {
    "week01_python_numpy_pandas_basics.md": "0325b54962b9d0bc80edbdeb23f264d4c9a17fb660038e96d92269fbea9c4983",
    "week02_eda_to_pca.md": "026f47db2ac8882e09f00f59fd2b9ec8ccfd87facd507139fdb78b2bb3e1581b",
    "week03_retail_and_weather_modelling.md": "c7dd1ce1f16f16ce03ce95ec4094ce4d46b4c5fe93a0b336e73aa1b43c98e8b5",
    "week04_model_evaluation_optimisation.md": "df72a895740bbd4bbcde18f0cc4e31d173281e015f6a9920d39aa9b1e8c7c044",
    "week05_version_control_collaboration.md": "e37ae25cb09238544546f9e34ca75ba37f4f7c3d0069338b145c06b199b88c33",
    "week06_containerisation_deployment.md": "ecbe9d98061d0d86da5be9b4961d8e19ae07a91fdff1ddcdafa98eadbc48610e",
}
ok_files = all((here / "corpus" / n).exists() and
               hashlib.sha256((here / "corpus" / n).read_bytes()).hexdigest() == h for n, h in CORPUS_SHA256.items())
check("corpus/ has the 6 unchanged tutorials", ok_files, "unzip Week11_Student_Files.zip again (do not edit corpus files)")
for name in ["gold/gold_questions.csv", "gold/gold_sections_week11.csv",
             "llm_replies_week11.json", "embeddings_week11.json", "app.py", "course_ta.py", "assets/logo.svg"]:
    check(name + " found", (here / name).exists(), "unzip Week11_Student_Files.zip again")

# where the folder is: Chroma writes a database, which OneDrive sync can lock
if "onedrive" in str(here).lower():
    print("WARNING this folder is inside OneDrive. Chroma's database can be locked by syncing: "
          "move Week11_Student_Files to e.g. C:\\dsts\\ (or ~/dsts on macOS).")
free_gb = shutil.disk_usage(here).free / 1e9
if free_gb < 6:
    print(f"WARNING only {free_gb:.1f} GB free on this drive; about 6 GB is recommended "
          "(models 1.9 GB + 2.1 GB + 0.27 GB, packages, Chroma).")

# Ollama and the three models
if REPLAY:
    print("SKIPPED (replay mode)  Ollama server at " + OLLAMA_URL)
    print("SKIPPED (replay mode)  chat model " + " or ".join(CHAT_MODELS))
    print("SKIPPED (replay mode)  embedding model " + EMBED_MODEL)
    print("SKIPPED (replay mode)  Course TA model " + TA_MODEL)
else:
    try:
        import requests
        names = [m["name"] for m in requests.get(OLLAMA_URL + "/api/tags", timeout=5).json().get("models", [])]
        check("Ollama server at " + OLLAMA_URL, True, "")
        chat = [m for m in CHAT_MODELS if m in names]
        check("chat model " + (chat[0] if chat else "qwen2.5:3b") + " is downloaded", bool(chat), "ollama pull qwen2.5:3b")
        if chat and chat[0] != "qwen2.5:3b":
            print("NOTE    replay files were recorded with qwen2.5:3b; with " + chat[0] + " use live mode")
        emb = any(n.split(":")[0] == EMBED_MODEL for n in names)
        check("embedding model " + EMBED_MODEL + " is downloaded", emb, "ollama pull " + EMBED_MODEL)
        check("Course TA model " + TA_MODEL + " is downloaded (Part 8, " + TA_MODEL_SIZE + ")", TA_MODEL in names,
              "ollama pull " + TA_MODEL + "   (or pick qwen2.5:3b in the app's sidebar)")
    except Exception:
        check("Ollama server at " + OLLAMA_URL, False,
              "open the Ollama app (or run `ollama serve`); no Ollama? run: python check_setup.py --replay")

if missing10:
    print("\nWeek 10 packages are missing (" + ", ".join(missing10) + "): do Week 10 Step 0 first.")
if problems:
    print(f"\n{problems} problem(s) - fix them, then run this check again.")
else:
    print("\nAll OK - open the notebook" + (" and set USE_RECORDED = True in Exercise 1 (replay mode: recorded replies, no Ollama)." if REPLAY else "."))
