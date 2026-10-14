"""DSTS 11523 Week 10 - setup check. Run it in the activated venv (or conda env):   python check_setup.py
No Ollama (replay mode)?                                          python check_setup.py --replay
Prints OK / NOT OK for each requirement, with the fix next to every problem."""
import importlib
import platform
import sys
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:3b"
REPLAY = "--replay" in sys.argv
problems = 0


def check(name, ok, fix):
    global problems
    problems += not ok
    print(("OK      " if ok else "NOT OK  ") + name + ("" if ok else "   ->  FIX: " + fix))


print("Python", sys.version.split()[0], "on", platform.system())
if sys.version_info[:2] == (3, 11):
    check("Python 3.11 (recommended; the lab was tested on 3.11.3)", True, "")
else:
    print("WARNING Python " + sys.version.split()[0] + " is not 3.11. Python 3.11 is recommended (the lab was tested "
          "on 3.11.3); 3.9+ may work but was not tested. Install 3.11.9 from "
          "https://www.python.org/downloads/release/python-3119/ if anything below fails.")
prefix = Path(sys.prefix)
if (prefix / "conda-meta").exists():
    # conda's base environment has condabin/; a separate environment (e.g. dsts-week10) does not
    check("running inside a conda environment (" + prefix.name + ")", not (prefix / "condabin").exists(),
          "activate the lab environment first: conda activate dsts-week10")
else:
    check("running inside a virtual environment (.venv)", sys.prefix != sys.base_prefix,
          "activate it first: Windows .\\.venv\\Scripts\\Activate.ps1 | macOS/Linux source .venv/bin/activate")
for pkg in ["pandas", "requests", "sklearn", "matplotlib", "pydantic", "jupyterlab", "ipykernel"]:
    try:
        importlib.import_module(pkg)
        check("package " + pkg, True, "")
    except ImportError:
        check("package " + pkg, False, "python -m pip install -r requirements_week10.txt")

here = Path(__file__).resolve().parent
check("data/amazon_cells_labelled.txt found", (here / "data" / "amazon_cells_labelled.txt").exists(),
      "unzip Week10_Student_Files.zip again; the data/ folder must sit next to this script")
check("llm_replies_week10.json found (replay mode)", (here / "llm_replies_week10.json").exists(),
      "unzip Week10_Student_Files.zip again")

if REPLAY:
    print("SKIPPED (replay mode)  Ollama server at " + OLLAMA_URL)
    print("SKIPPED (replay mode)  model " + MODEL)
else:
    try:
        import requests
        tags = requests.get(OLLAMA_URL + "/api/tags", timeout=5).json()
        names = [m["name"] for m in tags.get("models", [])]
        check("Ollama server at " + OLLAMA_URL, True, "")
        check("model " + MODEL + " is downloaded", MODEL in names, "ollama pull " + MODEL)
    except Exception:
        check("Ollama server at " + OLLAMA_URL, False,
              "open the Ollama app (or run `ollama serve`); no Ollama? run: python check_setup.py --replay")

if problems:
    print(f"\n{problems} problem(s) - fix them, then run this check again.")
else:
    print("\nAll OK - open the notebook" + (" and set USE_RECORDED = True in Exercise 1." if REPLAY else "."))
