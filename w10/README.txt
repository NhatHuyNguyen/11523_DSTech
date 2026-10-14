DSTS 11523 - Week 10 Lab (Option: Sentiment) - student files
=============================================================
Week10_Prompt_Engineering.ipynb           the lab notebook (PREPARED cells + TODO cells you complete)
Week10_Prompt_Engineering_COMPLETE.ipynb  the finished notebook (Option 3, for checking; writes to complete_run\)
data\amazon_cells_labelled.txt            the dataset: 1,000 Amazon review sentences (see data\README_DATA.txt)
llm_replies_week10.json                   recorded real LLM replies, for replay mode (USE_RECORDED = True)
requirements_week10.txt                   the Python packages:  python -m pip install -r requirements_week10.txt
check_setup.py                            setup check:  python check_setup.py   (no Ollama: python check_setup.py --replay)

Python: Python 3.11 (recommended; the lab was tested on 3.11.3). 3.9+ may work but was not tested.
No Anaconda: follow tutorial Steps 0.1, 0.2 (venv in this folder) and 0.3.
Anaconda already installed: in Anaconda Prompt (Windows) or Terminal (macOS), inside this folder, run one at a time:
  conda create -n dsts-week10 python=3.11 -y
  conda activate dsts-week10
  python -m   python -m pip install -r requirements_week10.txt
then SKIP tutorial Steps 0.1-0.3 and continue with Step 0.4 (Ollama). Next time, run  conda activate dsts-week10  first.

Three ways to work:
- Option 1 (recommended): open Week10_Prompt_Engineering.ipynb, run the PREPARED cells and complete the TODO cells.
- Option 2: create an empty notebook in this folder and paste each solution code block from the tutorial, in order.
- Option 3 (run the finished version): open Week10_Prompt_Engineering_COMPLETE.ipynb and choose Kernel -> Restart
  Kernel and Run All Cells. Use it to see the whole pipeline working, or to compare with your own notebook when you
  are stuck. You learn most from Option 1 or 2; Option 3 is for checking. It saves its files in complete_run\outputs\
  and complete_run\figures\, so it never overwrites yours.

What to do first: follow "Step 0 - Install everything" in the tutorial
DSTS_11523_Week10_Lab_Prompt_Engineering_Sentiment.html, then run check_setup.py, then open the notebook.
Keep this folder OUTSIDE OneDrive (e.g. C:\dsts\week10\Week10_Student_Files\ or ~/dsts/week10/Week10_Student_Files/).
