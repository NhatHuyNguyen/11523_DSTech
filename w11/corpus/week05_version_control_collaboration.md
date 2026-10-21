# DSTS 11523 · Week 5 Tutorial

## Version Control & Collaboration — hands-on lab (2 hours)

**How to use this tutorial.** Work top to bottom in a terminal. Every exercise has a **Goal**, a **Task**, some **Steps**, and a **▶ Solution** drop-down. *Try each exercise before you open the solution.*

### Install Git (do this first)

Install **Git** from [https://git-scm.com](https://git-scm.com), then open a terminal (**Git Bash** on Windows).

**Hint — command meaning:**
- `git --version` = ask Git to print its version number
- `--version` = “show version” flag

**Command (type this):**

```bash
git --version
```

**Hint:** any version 2.30 or newer is fine.

**Note — GitHub Desktop:** [GitHub Desktop](https://desktop.github.com) is only an **optional GUI alternative**. We will **not** use GitHub Desktop in this tutorial. Use the terminal (Git Bash / command line) for every step.

Useful link:
- Git basics (handbook): [https://docs.github.com/en/get-started/git-basics](https://docs.github.com/en/get-started/git-basics)

**Attached starter files (Exercises 11–12).** This tutorial package includes ready-made files. Put each one in the **exact** place below (or create them with the Solution commands):

| File | Put it here (project root = same folder as `prediction.py`) |
|---|---|
| `ci.yml` | `.github/workflows/ci.yml` |
| `requirements.txt` | `requirements.txt` (project root) |
| `test_prediction.py` | `test_prediction.py` (project root) |
| `.pre-commit-config.yaml` | `.pre-commit-config.yaml` (project root) |

### How to read the solutions (important)

In every solution you will see three kinds of text. Do not mix them up:

| Label | Meaning | What you do |
|---|---|---|
| **Hint** | Explains a command and its parameters | Read only — do **not** type it |
| **Command** | What you type in the terminal | Type / paste these lines only |
| **Output** | What Git prints after a command | Read only — do **not** type it |

### Quick concepts (read once before Part 1)

**1. Global vs local Git identity**

Global = for **all** projects on this computer:

```bash
git config --global user.name "Ada Student"
git config --global user.email "ada@uni.edu.au"
git config --list | grep user
```

Local = for **this repo only** (run inside the project folder; no `--global`):

```bash
git config user.name "Ada Student"
git config user.email "ada@uni.edu.au"
git config --local --list | grep user
```

**Hint:** local settings override global ones inside that repository.

**2. `git init`**  
Turns the current folder into a Git project by creating a hidden `.git/` folder. History stays local until you connect GitHub later. Do **not** run `git init` inside a project you already got with `git clone`.

**3. `git status` basics**
- `Untracked files` = Git sees the file but is not saving it yet → use `git add`
- `nothing to commit, working tree clean` = all saved; no new edits waiting

**4. `git add` then `git commit`**
- `git add prediction.py` = put the file in the **staging** area (ready to save)
- `git commit -m "initial commit"` = save a permanent snapshot with a message (`-m`)
- Staging holds the version from the moment you ran `git add` — if you edit again, run `git add` again

**5. Harmless Windows note**  
`LF will be replaced by CRLF` is usually safe on Windows. Optional:

```bash
git config --global core.autocrlf true
```

**6. `create mode 100644`**  
Means a normal file (not a password/key). `644` = you can read/write; others can read.

**7. Commit IDs and `HEAD`**  
Codes like `e63c1af` are short commit IDs (not secrets). `HEAD` = the commit you are on right now.

**8. Exit a long `git log` screen**  
If you see `(END)` or `~`, press **`q`** to quit.

We follow one project the whole session — the **rain-prediction model** (`prediction.py`) from Weeks 3–4 — taking it from an empty folder to an automated GitHub repository. Suggested time budget:

| Part | Time | Covers |
|---|---|---|
| 1 · Setup & first commit | 15 min | config, init, add, commit, status |
| 2 · Track & inspect | 30 min | diff, .gitignore, log family |
| 3 · Branching & conflicts | 30 min | branch/switch/merge; resolving a real conflict |
| 4 · Publish & collaborate on GitHub | 30 min | remotes, push, pull requests, branch protection |
| 5 · Automate | 15 min | GitHub Actions + pre-commit |

### Setup (do this once)

Create a workspace folder:

**Hint — command meaning:**
- `mkdir dsts-week5` = make a new folder named `dsts-week5`
- `cd dsts-week5` = change directory into that folder
- `&&` = run the next command only if the previous one succeeded

**Command (type this):**

```bash
mkdir dsts-week5 && cd dsts-week5
```

---

## Part 1 · Setup & first commit *(≈ 15 min)*

**Notes.** Git needs your name and email so it can label every commit with “who made this change.” Set them once on your computer with `--global`. When you run `git init` inside a folder, that folder becomes a Git project. Git creates a hidden `.git/` folder to store the project history.

### Exercise 1 — Introduce yourself to Git

**Goal:** every commit you make from now on will show your name.  
**Task:** tell Git your name and email for this computer, then check it worked.

**Steps:**
1. `git config --global user.name "Your Name"`
2. `git config --global user.email "you@uni.edu.au"`
3. `git config --list | grep user` to confirm.

<details><summary>▶ Solution</summary>

**Hint:** use your real name (not your GitHub username). Use your uni email, or the email linked to GitHub.

**Hint — command meaning:**
- `git config` = set or read a Git setting
- `--global` = apply this setting for **all** projects on this computer
- `user.name "Ada Student"` = set the author name shown on commits
- `user.email "ada@uni.edu.au"` = set the author email shown on commits
- `git config --list` = show all Git settings
- `|` = pipe = send output of the left command into the right command
- `grep user` = keep only lines that contain the word `user`

**Command (type this):**

```bash
git config --global user.name "Ada Student"
git config --global user.email "ada@uni.edu.au"
git config --list | grep user
```

**Output (do not type — Git prints this):**

```text
user.name=Ada Student
user.email=ada@uni.edu.au
```

**Why:** Git puts this name and email on every commit as the author.  
Use `--global` so it applies to all projects on this computer.  
If you need a different name for one project only, run the same command **without** `--global` inside that project folder.
</details>

### Exercise 2 — Create the repo and make your first commit

**Goal:** turn a normal folder into a Git project and save the first snapshot.  
**Task:** create `python_project/`, add a starter `prediction.py`, and commit it.

**Steps:**
1. `mkdir python_project && cd python_project`
2. `git init`
3. Create `prediction.py` with a few lines of Python.
4. Run `git status` — read what Git says about the new file.
5. `git add prediction.py`, then `git commit -m "initial commit"`.

<details><summary>▶ Solution</summary>

**Hint:** create the folder, start Git, then create `prediction.py` with this content:

```python
import numpy as np
import pandas as pd
def predict():
    print("baseline")
```

**Hint — command meaning:**
- `mkdir python_project` = create a new folder
- `cd python_project` = enter that folder
- `git init` = start a new Git repository in the current folder
- `git status` = show which files are new / changed / staged
- `git add prediction.py` = put `prediction.py` into staging (ready for the next commit)
- `git commit` = save a snapshot
- `-m "initial commit"` = set the commit message (`-m` = message)

**Command (type this):**

```bash
mkdir python_project && cd python_project
git init
git status
git add prediction.py
git commit -m "initial commit"
```

**Output (do not type — example of `git status` before commit):**

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        prediction.py

nothing added to commit but untracked files present (use "git add" to track)
```

**Hint:** “Untracked” means Git sees the file but has not saved it yet.

**Why:** Think of Git in 3 simple steps:
1. **Working folder** — your normal files  
2. **Staging** — files you chose with `git add`  
3. **Commit** — a saved snapshot with `git commit`  

`git status` is the most useful command: it tells you where each file is right now.
</details>

---

## Part 2 · Track & inspect *(≈ 30 min)*

**Notes.** After your first commit, you will often repeat this loop: edit a file → `git status` → `git diff` → `git add` → `git commit`.

A special file called `.gitignore` tells Git: “do **not** track these files.” Use it for things you should not save in the repo, such as:
- big datasets (`data/`)
- secret keys (`.env`)
- temporary files (`__pycache__/`, `*.pyc`)

Then use `git log` to read the project’s history (past commits).

### Exercise 3 — Edit, diff, stage, commit

**Goal:** see why `git diff` and `git diff --staged` show different things.  
**Task:** change one line in `prediction.py`. Check the diff *before* you stage, then *after*, then commit.

**Steps:**
1. Open `prediction.py` and change `"baseline"` to `"main version"`.
2. Run `git diff` — shows edits not staged yet.
3. `git add prediction.py`.
4. Run `git diff` again (should be empty) and `git diff --staged` (shows what will go into the next commit).
5. `git commit -m "update message"`.

<details><summary>▶ Solution</summary>

**Hint:** first edit `prediction.py` in your editor. Change `print("baseline")` to `print("main version")`. Save the file. Then type only the command below.

**Hint — command meaning:**
- `git diff` = show unstaged changes (edited file vs staging area)

**Command (type this):**

```bash
git diff
```

**Output (do not type — Git prints this):**

```text
diff --git a/prediction.py b/prediction.py
index 6c74eee..2c7334e 100644
--- a/prediction.py
+++ b/prediction.py
@@ -1,4 +1,4 @@
 import numpy as np
 import pandas as pd
 def predict():
-    print("baseline")
+    print("main version")
```

**Hint:** in the output, `-` means removed line, `+` means added line. The lines starting with `diff --git` are **not** commands.

**Hint — command meaning:**
- `git add prediction.py` = stage this file
- `git diff` = show unstaged changes (should be empty after `git add`)
- `git diff --staged` = show staged changes (what the next commit will save)
- `--staged` = look at staging area vs last commit
- `git commit -m "update message"` = save snapshot with message `update message`

**Command (type this next):**

```bash
git add prediction.py
git diff
git diff --staged
git commit -m "update message"
```

**Why:**  
- `git diff` shows changes you made in the file but have **not** staged yet.  
- `git diff --staged` shows changes you already staged with `git add`.  

About `@@ -1,4 +1,4 @@`: it just means “look near line 1 for about 4 lines.” You do not need to memorize it.  
Focus on: Red `-` = removed, Green `+` = added.
</details>

### Exercise 4 — Keep data and secrets out of the repo

**Goal:** learn `.gitignore` so Git ignores files you never want to commit.  
**Task:** make a small data-science style mess — a `data/` folder with a CSV, and a `.env` file with a fake secret. Both should stay out of Git.

**Steps:**
1. `mkdir -p data && echo "day,rain" > data/weather.csv`
2. `echo "SECRET=xyz" > .env`
3. Run `git status` — Git should list both as untracked.
4. Create `.gitignore` and list: `data/`, `.env`, `__pycache__/`, `*.pyc`.
5. Stage and commit **only** `.gitignore`, then check that `git status` is clean.

<details><summary>▶ Solution</summary>

**Hint:** we create fake data and a fake secret only to practice ignoring them. Do not commit real secrets.

**Hint — command meaning:**
- `mkdir -p data` = create folder `data` (`-p` = also create parents if needed; no error if it exists)
- `echo "day,rain"` = print this text
- `>` = write that text into a file (overwrite)
- `data/weather.csv` = the file being created
- `echo "SECRET=xyz" > .env` = create a fake secret file named `.env`

**Command (type this):**

```bash
mkdir -p data && echo "day,rain" > data/weather.csv
echo "SECRET=xyz" > .env
```

**Hint — command meaning:**
- `cat > .gitignore << 'EOF' ... EOF` = create/overwrite `.gitignore` with the lines between the two `EOF` markers
- `'EOF'` = end marker for the text block
- each line inside = a pattern Git should ignore

**Command (type this):**

```bash
cat > .gitignore << 'EOF'
data/
.env
__pycache__/
*.pyc
EOF
```

**Hint — command meaning:**
- `git add .gitignore` = stage only the ignore rules file
- `git commit -m "add gitignore"` = save it (`-m` = message)
- `git status` = confirm the working tree is clean

**Command (type this):**

```bash
git add .gitignore
git commit -m "add gitignore"
git status
```

**Output (do not type — Git prints this):**

```text
On branch main
nothing to commit, working tree clean
```

**Hint:** “clean” means Git is ignoring `data/` and `.env`, as we wanted.

**Why:** `.gitignore` does **not** delete files from your computer. It only tells Git to ignore them. Add `.gitignore` early. If you commit a secret by mistake, deleting the file later is **not** enough — treat the key as leaked and replace it.
</details>

### Exercise 5 — Read the story so far

**Goal:** learn the `git log` variants you'll actually use.  
**Task:** make one more small change and commit it, then explore the log.

**Steps:**
1. Append any line to `prediction.py` (e.g. `print(2+2)`) and `git commit -am "small tweak"`.
2. Try `git log --oneline`, `git log --stat -1`, and `git log --oneline --graph --all`.
3. Copy a SHA from the output and inspect that single commit with `git show <SHA>`.

<details><summary>▶ Solution</summary>

**Hint:** first add a small line to `prediction.py` (for example `print(2+2)`), save it, then run the commands below.

**Hint — command meaning:**
- `git commit -am "small tweak"` = stage changed **tracked** files and commit in one step
- `-a` = auto-stage modified tracked files
- `-m "small tweak"` = commit message
- `git log` = show commit history
- `--oneline` = short view (one line per commit)

**Command (type this):**

```bash
git commit -am "small tweak"
git log --oneline
```

**Output (do not type — example):**

```text
e63c1af small tweak
b95ec55 add gitignore
9e20d45 update message
42bd3f2 initial commit
```

**Hint:** left side is a short commit ID (SHA), right side is the message.

**Hint — command meaning:**
- `git log --stat -1` = show the newest commit with file-change stats
- `--stat` = list which files changed and how much
- `-1` = show only the latest 1 commit
- optional later: `git log --oneline --graph --all`
  - `--graph` = draw branch lines
  - `--all` = show all branches
- optional: `git show e63c1af` = show full details of one commit ID

**Command (type this):**

```bash
git log --stat -1
```

**Output (do not type — example):**

```text
commit e63c1afcc36a638d151f1749a9996a4e3f43f068
Author: Ada Student <ada@uni.edu.au>
Date:   Tue Sep 8 06:21:44 2026 +0000

    small tweak

 prediction.py | 1 +
 1 file changed, 1 insertion(+)
```

**Why:**  
- Each commit has an ID (like `e63c1af`).  
- `HEAD` means “the commit you are on right now.”  
- `-am` does **not** add brand-new files — for a new file, still use `git add`.

(End of solution.)
</details>

---

## Part 3 · Branching & conflicts *(≈ 30 min)*

**Notes.** A **branch** is a separate line of work. Good habit: keep `main` safe and working. Do new work on a feature branch, then merge it back into `main`.

If two branches change the **same line** in the same file, Git cannot choose automatically. That is called a **merge conflict**. You must open the file and choose what to keep.

### Exercise 6 — Branch, edit, merge (the clean case)

**Goal:** practice the normal branch → edit → merge flow (no conflict).  
**Task:** add a new metric function on a branch, then merge it into `main`.  
**Also check:** look at `prediction.py` on `main` **before** the merge and **after** the merge, so you can see what changed.

**Steps:**
1. `git checkout -b feature/add-metric` (create AND switch in one step).
2. Append an `rmse` function to `prediction.py`, then `git commit -am "add rmse metric"`.
3. `git checkout main`.
4. **Show the file on `main` before merge:** `cat prediction.py` (or open it in your editor). Notice: there is **no** `rmse` function yet.
5. `git merge feature/add-metric`.
6. **Show the file on `main` after merge:** `cat prediction.py` again. Notice: the `rmse` function is now there.
7. `git log --oneline --graph --all` to see the shape of history.

<details><summary>▶ Solution</summary>

**Hint — command meaning:**
- `git checkout -b feature/add-metric` = create a new branch and switch to it
- `-b` = create branch
- `feature/add-metric` = branch name (you can choose another name)

**Command (type this):**

```bash
git checkout -b feature/add-metric
```

**Hint — command meaning:**
- `cat >> prediction.py << 'EOF' ... EOF` = **append** text to the end of `prediction.py`
- `>>` = append (do not overwrite the whole file)
- `'EOF'` = end marker for the pasted text

**Command (type this to append the function):**

```bash
cat >> prediction.py << 'EOF'

def rmse(y, yhat):
    return ((y - yhat) ** 2).mean() ** 0.5
EOF
```

**Hint — command meaning:**
- `git commit -am "add rmse metric"` = stage tracked changes + commit (`-a` stage, `-m` message)

**Command (type this):**

```bash
git commit -am "add rmse metric"
```

**Hint — command meaning:**
- `git checkout main` = switch to the `main` branch
- `cat prediction.py` = print the file content in the terminal (so you can inspect it)

**Command (type this) — switch to main and show file BEFORE merge:**

```bash
git checkout main
cat prediction.py
```

**Output (do not type — example of `prediction.py` on `main` BEFORE merge):**

```text
import numpy as np
import pandas as pd
def predict():
    print("main version")
print(2+2)
```

**Hint:** on `main` before the merge, there is **no** `rmse` function. That function exists only on the feature branch so far.

**Hint — command meaning:**
- `git merge feature/add-metric` = bring the feature branch changes into the current branch (`main`)

**Command (type this) — merge, then show file AFTER merge:**

```bash
git merge feature/add-metric
cat prediction.py
```

**Output (do not type — example merge message):**

```text
Updating e63c1af..efd3de0
Fast-forward
 prediction.py | 3 +++
 1 file changed, 3 insertions(+)
```

**Output (do not type — example of `prediction.py` on `main` AFTER merge):**

```text
import numpy as np
import pandas as pd
def predict():
    print("main version")
print(2+2)

def rmse(y, yhat):
    return ((y - yhat) ** 2).mean() ** 0.5
```

**Hint:** after the merge, `main` now includes the `rmse` function. That is the point of merging.

**Hint — command meaning:**
- `git log --oneline --graph --all` = short history with a branch graph for all branches

**Command (type this):**

```bash
git log --oneline --graph --all
```

**Hint:** “Fast-forward” means a clean, simple merge (no conflict).

**Why:** While you worked on the feature branch, `main` did not change, so Git can move `main` forward easily. Comparing the file **before** and **after** merge proves the feature landed on `main`. Tip: `git switch` can also change branches.
</details>

### Exercise 7 — Team conflict: two members edit the same function

**Story (what this simulates):**  
Imagine **two team members** work at the same time:

| Person | Branch | What they change |
|---|---|---|
| **Ada** | `feature/ada-threshold` | edits the same `predict()` line to `print("ada threshold 0.7")` |
| **Bob** | `feature/bob-threshold` | edits the same `predict()` line to `print("bob threshold 0.5")` |

Both want their work on `main`.  
1. Ada merges first → **no conflict** (clean).  
2. Bob merges next → **conflict**, because `main` and Bob both changed the **same line** of the **same function**.  
3. You resolve it (choose one version), then finish the merge.

**Goal:** feel a real team conflict, then fix it safely.  
**Task:** create two branches, change the same `predict()` line on each, merge both into `main`, resolve the conflict.

**Steps:**
1. From `main`, create Ada’s branch: `git checkout -b feature/ada-threshold`. Edit `predict()` to `print("ada threshold 0.7")`. Commit.
2. Go back to `main`. Create Bob’s branch: `git checkout -b feature/bob-threshold`. Edit the **same** `predict()` line to `print("bob threshold 0.5")`. Commit.
3. Switch to `main`. Show the file: `cat prediction.py`.
4. Merge Ada first: `git merge feature/ada-threshold` (should succeed). Show the file again.
5. Merge Bob next: `git merge feature/bob-threshold` (should conflict).
6. Open `prediction.py`, read the `<<<<<<<` / `=======` / `>>>>>>>` markers, keep **one** version, delete markers.
7. `git add prediction.py`, then `git commit -m "merge: resolve predict() conflict"`. Show the final file and the graph.

<details><summary>▶ Solution</summary>

**Hint:** you play both teammates on one computer by switching branches.

---

#### Step 1 — Ada’s branch (team member 1)

**Hint — command meaning:**
- `git checkout -b feature/ada-threshold` = create + switch to Ada’s branch

**Command (type this):**

```bash
git checkout -b feature/ada-threshold
```

**Hint — how to edit (same file, not a new file):**
1. Open the existing `prediction.py` in your project folder (VS Code / Cursor / Notepad).
2. Find the line inside `predict()` that looks like `print("...")`.
3. Change **only that line** to:

```python
    print("ada threshold 0.7")
```

4. **Save** the file (`Ctrl+S`).
5. Do **not** create a second `prediction.py`.

Then run the commit command below.

**Hint — command meaning:**
- `git commit -am "..."` = `-a` stage tracked edits, `-m` message

**Command (type this):**

```bash
git commit -am "ada: set threshold 0.7"
```

---

#### Step 2 — Bob’s branch (team member 2)

**Hint:** start Bob’s branch from the original `main` (not from Ada’s branch).

**Hint — command meaning:**
- `git checkout main` = go back to `main`
- `git checkout -b feature/bob-threshold` = create Bob’s branch from `main`

**Command (type this):**

```bash
git checkout main
git checkout -b feature/bob-threshold
```

**Hint — how to edit (same file, not a new file):**
1. Open the existing `prediction.py` again.
2. Change the **same** `print(...)` line inside `predict()` to:

```python
    print("bob threshold 0.5")
```

3. **Save** the file (`Ctrl+S`).
4. You are on Bob’s branch now, so this edit belongs to Bob only.

**Command (type this):**

```bash
git commit -am "bob: set threshold 0.5"
```

---

#### Step 3 — Merge Ada into `main` first (clean)

**Command (type this) — show file BEFORE any merge:**

```bash
git checkout main
cat prediction.py
```

**Hint:** before merges, `main` still has the old print line (for example `"main version"`). No Ada/Bob text yet.

**Hint — command meaning:**
- `git merge feature/ada-threshold` = bring Ada’s commits into `main`

**Command (type this):**

```bash
git merge feature/ada-threshold
cat prediction.py
```

**Output (do not type — example):**

```text
Updating ....
Fast-forward
 prediction.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Hint:** after Ada’s merge, `predict()` on `main` shows `print("ada threshold 0.7")`. No conflict yet.

---

#### Step 4 — Merge Bob into `main` (conflict happens)

**Command (type this):**

```bash
git merge feature/bob-threshold
```

**Output (do not type — Git prints this):**

```text
Auto-merging prediction.py
CONFLICT (content): Merge conflict in prediction.py
Automatic merge failed; fix conflicts and then commit the result.
```

**Hint:** conflict = both branches changed the **same line** of `predict()`, and Git cannot choose.

Open `prediction.py`. You will see markers like this (**file content**, not a command):

```python
<<<<<<< HEAD
    print("ada threshold 0.7")
=======
    print("bob threshold 0.5")
>>>>>>> feature/bob-threshold
```

**Hint — how to read the markers:**
- `<<<<<<< HEAD` … above `=======` = current branch (`main`, which already has Ada’s change)
- below `=======` … `>>>>>>> feature/bob-threshold` = Bob’s incoming change

**Decide (example):** keep Bob’s line. Delete the markers and Ada’s line, so the function ends up as:

```python
def predict():
    print("bob threshold 0.5")
```

**Hint:** you may keep Ada’s line instead — either choice is fine. The important part is: remove `<<<<<<<`, `=======`, `>>>>>>>`.

---

#### Step 5 — Finish the merge and check the result

**Hint — command meaning:**
- `git add prediction.py` = mark conflict as resolved
- `git commit -m "..."` = save the merge commit
- `cat prediction.py` = show final file content
- `git log --oneline --graph --all` = show history graph
- bail-out: `git merge --abort` = cancel the merge if you want to restart

**Command (type this):**

```bash
git add prediction.py
git commit -m "merge: resolve predict() conflict (keep bob)"
cat prediction.py
git log --oneline --graph --all
```

**Output (do not type — example final file):**

```text
import numpy as np
import pandas as pd
def predict():
    print("bob threshold 0.5")
print(2+2)

def rmse(y, yhat):
    return ((y - yhat) ** 2).mean() ** 0.5
```

**Output (do not type — example graph):**

```text
*   a1b2c3d merge: resolve predict() conflict (keep bob)
|\
| * b0b1111 bob: set threshold 0.5
* | a0a1111 ada: set threshold 0.7
|/
* efd3de0 add rmse metric
...
```

**Why:** this is normal team work. Two people edited the same function → Git asks a human to choose. Conflicts are not “Git broken”; they are “Git needs a decision.” In VS Code you can click **Accept Current / Incoming / Both**.
</details>

---

## Part 4 · Publish & collaborate on GitHub *(≈ 30 min)*

**Notes.** A **remote** is a copy of your project on the internet (usually GitHub).  
- `git push` = send your commits to GitHub  
- `git pull` = download new commits from GitHub  

On GitHub, teams usually use a **Pull Request (PR)**: you push a branch, open a PR into `main`, others can review it, checks can run, then you merge.

### Exercise 8 — Publish the repo to GitHub

**Goal:** upload your local project to GitHub.  
**Task:** follow the numbered example below from start to finish.

**Before you start (very important):**  
GitHub does **not** accept your normal password for `git push`.  
In this exercise we use **GitHub CLI (`gh`)** so login is easy.

**Where to run commands:**  
Open Git Bash (or your terminal), then go into **your** project folder — the folder that already contains both `prediction.py` and `.git`.

**Command (type this — change the path to yours):**

```bash
cd /path/to/your/python_project
```

**Hint — how to know you are in the right folder:**

```bash
ls
```

You should see `prediction.py` (and maybe `.gitignore`, `data`, etc.).  
Also check Git is active here:

```bash
git status
```

If that works (no “not a git repository” error), you are in the correct folder.  
Do **not** copy someone else’s full Desktop path — every student’s folder location can be different.

---

#### Example — do these steps in order

<details><summary>▶ Solution (follow Step 1 → Step 7)</summary>

##### Step 1 — Check that GitHub CLI is installed

**Hint — command meaning:**  
`gh --version` = show if GitHub CLI is installed.

**Command (type this):**

```bash
gh --version
```

**What good looks like:** you see a version number, for example `gh version 2.x.x`.

**If it fails (“command not found”):**
1. Install GitHub CLI from [https://cli.github.com](https://cli.github.com)
2. Close the terminal
3. Open a new Git Bash
4. Run `gh --version` again

---

##### Step 2 — Log in to GitHub from the terminal

**Hint — command meaning:**  
`gh auth login` = sign in to your GitHub account in the terminal.

**Command (type this):**

```bash
gh auth login
```

**What to choose on the screen (use arrow keys + Enter):**
1. `GitHub.com`
2. `HTTPS`
3. `Login with a web browser`
4. Copy the one-time code shown in the terminal
5. Press Enter, then paste/confirm the code in the browser
6. Allow access

**Then check login:**

**Command (type this):**

```bash
gh auth status
```

**Output (do not type — example):**

```text
✓ Logged in to github.com as YOUR_USERNAME
```

**Hint:** replace in your mind `YOUR_USERNAME` with your real GitHub username.

---

##### Step 3 — Make sure your branch is called `main`

**Hint — command meaning:**
- `git branch -M main` = rename current branch to `main`
- `-M` = force rename

**Command (type this):**

```bash
git branch -M main
```

**Check:**

```bash
git branch
```

**Output (do not type — example):**

```text
* main
```

**Hint:** the `*` means you are on that branch.

---

##### Step 4 — Create the GitHub repo, then link + push (separate commands)

**Do this in 3 small parts.**

###### 4A — Create the empty repo on GitHub (command line)

**Hint — command meaning:**
- `gh repo create prediction` = create a new GitHub repository named `prediction`
- `--public` = public repo (use `--private` if your tutor asks)
- do **not** use `--push` here — we will push in a later command

**Command (type this):**

```bash
gh repo create prediction --public
```

**Output (do not type — example):**

```text
✓ Created repository YOUR_USERNAME/prediction on github.com
https://github.com/YOUR_USERNAME/prediction
```

**Hint:** copy your real URL from the output (change `YOUR_USERNAME` to yours).  
Example shape:

```text
https://github.com/YOUR_USERNAME/prediction.git
```

**If the name already exists online:** use another name, for example `prediction-week5`.

###### 4B — Link your local folder to that GitHub repo

**Short note:** if `origin` already exists from an earlier try, remove it first:

```bash
git remote remove origin
```

**Hint — command meaning:**
- `git remote add origin <URL>` = save the GitHub URL as local nickname `origin`
- replace the URL with **your** repo URL from Step 4A

**Command (type this — use your username):**

```bash
git remote add origin https://github.com/YOUR_USERNAME/prediction.git
```

**Check:**

```bash
git remote -v
```

**Output (do not type — example):**

```text
origin  https://github.com/YOUR_USERNAME/prediction.git (fetch)
origin  https://github.com/YOUR_USERNAME/prediction.git (push)
```

###### 4C — Push your code to GitHub

**Hint — command meaning:**
- `git push -u origin main` = upload local `main` to GitHub
- `-u` = remember this link so later `git push` / `git pull` are shorter
- `origin` = the remote nickname
- `main` = the branch to upload

**Command (type this):**

```bash
git push -u origin main
```

**Output (do not type — example):**

```text
Enumerating objects: ...
To https://github.com/YOUR_USERNAME/prediction.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

**If push fails with authentication error:** go back to Step 2 (`gh auth login`), or use a Personal Access Token as the password (not your GitHub account password).

**If push says `fetch first`:**  
Meaning: GitHub has commits your computer does not have yet.  
Download them first, then push again:

```bash
git pull
git push
```

**Hint:** if Git asks you to create a merge commit message, save and close the editor, then run `git push` again.  
If `git pull` shows a merge conflict, fix the file (same as Exercise 7), then:

```bash
git add .
git commit -m "merge remote main"
git push
```

---

##### Step 5 — Confirm the remote link

**Hint — command meaning:**  
`git remote -v` = show where Git uploads/downloads (`-v` = verbose).

**Command (type this):**

```bash
git remote -v
```

**Output (do not type — example):**

```text
origin  https://github.com/YOUR_USERNAME/prediction.git (fetch)
origin  https://github.com/YOUR_USERNAME/prediction.git (push)
```

---

##### Step 6 — Open your repo in the browser

Open this URL (change `YOUR_USERNAME`):

```text
https://github.com/YOUR_USERNAME/prediction
```

**What good looks like:** you can see files such as `prediction.py`.

---

##### Step 7 — Done checklist

- [ ] `gh auth status` shows you are logged in
- [ ] `git branch` shows `* main`
- [ ] `git remote -v` shows `origin` pointing to github.com
- [ ] Browser page shows your project files

**Why (simple and clear):**

1. **What `-u` means**  
   In `git push -u origin main`, the `-u` means “remember this link.”  
   After that, you can usually type just:
   - `git push` (upload)
   - `git pull` (download)  
   without writing `origin main` every time.

2. **Why password fails**  
   GitHub no longer accepts your normal account password for Git.  
   You must use one of these:
   - **GitHub CLI login** (`gh auth login`), or  
   - a **Personal Access Token (PAT)** as the password, or  
   - **SSH keys**  
   If you type your normal password, GitHub rejects it.

3. **If push says `fetch first`**  
   Example error: `[rejected] main -> main (fetch first)`  
   Meaning: GitHub has new commits that your computer does not have yet.  
   Fix (complete basic commands):
   ```bash
   git pull
   git push
   ```
   First download the new commits, then upload yours.  
   If `git pull` creates a conflict, resolve it, then `git add` + `git commit`, then `git push`.

**Why this exercise works:**  
`gh auth login` handles authentication.  
Then we use **separate commands**:
1. `gh repo create ...` = create the empty GitHub repo  
2. `git remote add origin ...` = link your local folder to that repo  
3. `git push -u origin main` = upload your code  

You do **not** need to type your GitHub account password.

---

##### Backup plan (only if `gh` cannot be installed)

1. Create a token: [https://github.com/settings/tokens](https://github.com/settings/tokens) → classic token → tick **`repo`** → copy token  
2. On github.com create empty repo `prediction` (no README)  
3. Then type:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prediction.git
git push -u origin main
```

**Hint — command meaning for the backup push:**
- `git remote add origin <URL>` = save GitHub address as name `origin`
- `git push -u origin main` = upload branch `main` to `origin`
- `-u` = remember this remote/branch pair for later shorter `git push` / `git pull`

4. When asked for password, paste the **token** (not your GitHub password)

**If you see this error:**

```text
Password authentication is not supported for Git operations
```

you typed a normal password. Use the token, or go back to the main steps with `gh auth login`.

**If you see this error:**

```text
! [rejected] main -> main (fetch first)
```

GitHub is ahead of your computer. Fix with:

```bash
git pull
git push
```
</details>

### Exercise 9 — Open a Pull Request

**Goal:** practice the normal team review flow.  
**Task:** create a branch, add a docstring to `predict()` in `prediction.py`, push it, open a PR into `main`, review it, and merge it.

**Steps:**
1. `git checkout -b feature/add-docstring`.
2. Add a docstring to `predict()` in `prediction.py`, save, then commit.
3. `git push -u origin feature/add-docstring`.
4. On GitHub you'll see a **Compare & pull request** banner — click it. Add a title and a short description of *what and why*, then **Create pull request**.
5. Review your own diff line-by-line (imagine you're a teammate). When happy, **Merge pull request** → **Delete branch**.
6. Locally: `git checkout main && git pull` to sync the merged change.

<details><summary>▶ Solution (what to watch for)</summary>

**Hint — command meaning:**
- `git checkout -b feature/add-docstring` = create + switch to this feature branch

**Command (type this):**

```bash
git checkout -b feature/add-docstring
```

#### How to add a docstring to `prediction.py`

**Hint:** a **docstring** is a short text inside `"""..."""` that explains what a function does.  
Put it on the first line **inside** the function.

1. Open the existing `prediction.py` (same file, do not create a new one).
2. Find your `predict()` function. It may look like this:

```python
def predict():
    print("bob threshold 0.5")
```

3. Change it to this (add the docstring line, keep your current print text):

```python
def predict():
    """Return a simple rain-prediction message."""
    print("bob threshold 0.5")
```

**Hint:**
- Keep the indentation (4 spaces) the same as the `print` line
- Use three quotes: `"""` at the start and end
- **Save** the file (`Ctrl+S`)

4. Optional check — show the file:

```bash
cat prediction.py
```

You should see the docstring inside `predict()`.

#### Commit and push the branch

**Hint — command meaning:**
- `git commit -am "..."` = `-a` stage tracked edits, `-m` message
- `git push -u origin feature/add-docstring` = upload this branch and set upstream
- `-u` = remember this branch’s remote tracking
- `origin` = GitHub remote
- `feature/add-docstring` = branch name to upload

**Command (type this):**

```bash
git commit -am "docs: add docstring to predict()"
git push -u origin feature/add-docstring
```

**Hint (on GitHub — click, do not type):**
- Open your repo on github.com
- Click the **Compare & pull request** banner (or **Pull requests** → **New pull request**)
- Title example: `Add docstring to predict()`
- Description example: `Adds a short docstring so the function purpose is clearer.`
- Click **Create pull request**
- The PR page shows **the diff** (same idea as `git diff`)
- **Files changed** is where reviewers leave comments on lines
- **Conversation** shows discussion and check status (green tick = OK)
- Click **Merge pull request** → **Confirm** → **Delete branch**

**Hint — command meaning:**
- `git checkout main` = switch back to `main`
- `git pull` = download + merge newest commits from GitHub into your current branch
- `git branch -d feature/add-docstring` = delete the local branch (`-d` = safe delete if already merged)

**Command (type this locally after the PR is merged):**

```bash
git checkout main
git pull
git branch -d feature/add-docstring
```

**Optional check after pull:**

```bash
cat prediction.py
```

You should now see the docstring on `main` too.

**Why:** A Pull Request gives you a diff to review, a place to discuss, and a place for CI checks.
</details>

### Exercise 10 — Protect `main`

**Goal:** stop anyone (including you) from pushing straight to `main`, so changes go through a PR.  
**Task:** turn on branch protection on GitHub.

**Steps:**
1. On the repo page: **Settings** → **Branches** → **Add branch protection rule**.
2. Branch name pattern: `main`.
3. Tick **Require a pull request before merging**, and **Require approvals** (set to `1` for a small team, or leave `0` for solo work but keep the PR requirement).
4. If you'll add CI in Part 5, also tick **Require status checks to pass before merging** later.
5. **Save.** Try to push a commit directly to `main` — GitHub will refuse.

<details><summary>▶ Solution</summary>

#### A) Test: push directly to `main` (GitHub should refuse)

**Hint — command meaning:**  
- `git checkout main` = switch to the `main` branch  
- `git pull` = download the latest `main` from GitHub  
- `git commit -am "..."` = stage tracked file edits (`-a`) and commit with message (`-m`)  
- `git push origin main` = try to upload `main` straight to GitHub (this should fail after protection)

**Command (type this):**

```bash
git checkout main
git pull
```

**Hint:** edit `prediction.py` a little (for example add a comment `# protection test`), save the file, then:

**Command (type this):**

```bash
git commit -am "test: try direct push to main"
git push origin main
```

**Output (do not type — example of a refused push):**

```text
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Changes must be made through a pull request.
To https://github.com/YOUR_USERNAME/prediction.git
 ! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs ...
```

**Hint:** this error is **good**. It means Exercise 10 worked. Direct pushes to `main` are blocked.

#### B) Correct way after protection (branch + PR)

**Command (type this):**

```bash
git checkout -b feature/protected-main-test
git push -u origin feature/protected-main-test
```

Then on GitHub: **Compare & pull request** → review → **Merge pull request**.

**After merge, sync locally:**

```bash
git checkout main
git pull
```

**Why:** Branch protection turns “use a PR” into a real rule, not just advice. Use this on your Final Project group repo early.
</details>

---

## Part 5 · Automate *(≈ 15 min)*

**Notes — two different tools (do not mix them up):**

| Tool | Where it runs | When it runs | Exercise |
|---|---|---|---|
| **GitHub Actions** | On GitHub (in the cloud) | After you `git push`, or when you open a **Pull Request (PR)** | Exercise 11 |
| **pre-commit** | On **your computer** | Right before `git commit` saves a snapshot | Exercise 12 |

**Simple picture:**
1. You edit code on your laptop.
2. **pre-commit** (Exercise 12) can check it *before* the commit is saved.
3. You push to GitHub.
4. **GitHub Actions** (Exercise 11) checks it again *on GitHub*.

**What is a PR?**  
**PR** = **Pull Request**. It is a GitHub page where you ask to merge a branch into `main`.  
So “every PR” means: “every time a Pull Request is opened or updated on GitHub.”

### Mini glossary (read this first)

| Word / tool | Simple meaning |
|---|---|
| **CI** | Continuous Integration = automatic checks on GitHub |
| **workflow** | A recipe GitHub runs (the `ci.yml` file) |
| **lint / linter** | A tool that checks code style and common mistakes |
| **formatter** | A tool that rewrites code to a clean, shared style |
| **test** | A small program that checks your code still works |
| **hook** | A tiny script that runs automatically at a Git moment (for example: before commit) |
| **flake8** | A Python **linter** — finds style issues and simple bugs |
| **black** | A Python **formatter** — auto-fixes spacing/layout |
| **pytest** | A Python **test runner** — runs your `test_*.py` files |
| **nbstripout** | Removes Jupyter notebook outputs before commit |
| **pre-commit** | A tool that installs and runs hooks before each `git commit` |
| **rev** | The version of a hook tool to use (like a version number) |
| **id** | The name of the specific check to run |

**Hint:** keep this table open while you do Exercises 11–12.

### Exercise 11 — Add a GitHub Actions workflow

**Goal:** make GitHub automatically check your code after you upload it.  
**In plain English:** after `git push`, and also when someone opens a Pull Request (PR), GitHub should:
1. install your packages  
2. run **flake8** (style check)  
3. run **pytest** (tests)

**Task:** add one special file: `.github/workflows/ci.yml`.  
This file is the “recipe” GitHub follows. Students often call this a **workflow** or **CI file**.

**Attached with this tutorial (Exercise 11):** `ci.yml`, `requirements.txt`, `test_prediction.py`.  
Create the folder first, then create each file in the correct place (see Solution commands), or copy the attached files into those same paths.

**Steps (do them in order):**
1. Create a feature branch (because `main` is protected from Exercise 10).
2. Create the folder `.github/workflows`.
3. Inside it, create a file named `ci.yml` (copy the content from the Solution).
4. Also add `requirements.txt` and `test_prediction.py` if needed.
5. Commit and push the **feature branch**.
6. Open a Pull Request into `main`, wait for the CI check, then merge.
7. On github.com, open **Actions** to watch the run.

<details><summary>▶ Solution</summary>

**Hint:** Exercise 11 is about GitHub (cloud checks). Exercise 12 is about your laptop. Do not put pre-commit settings in `ci.yml`.

**Important:** `main` is protected (Exercise 10), so do **not** push CI files straight to `main`. Use a feature branch + PR.

**Step 0 — start from `main`, then create a feature branch**

**Command (type this):**

```bash
git checkout main
git pull
git checkout -b feature/add-ci
```

**Hint — command meaning:**
- `git checkout main` = switch to `main`
- `git pull` = get the latest `main` from GitHub
- `git checkout -b feature/add-ci` = create and switch to a new branch for this CI work

**Step A — create the folder + empty files in the correct places**

**Hint — where each file must live:**
- folder: `.github/workflows/`
- CI file: `.github/workflows/ci.yml` (**not** in the project root)
- packages file: `requirements.txt` (project root)
- test file: `test_prediction.py` (project root, next to `prediction.py`)

**Hint — command meaning:**
- `mkdir -p .github/workflows` = create nested folders
- `-p` = create parents as needed; do not error if folders already exist
- `touch <path>` = create an empty file at that exact path (then paste content into it)

**Command (type this):**

```bash
mkdir -p .github/workflows
touch .github/workflows/ci.yml
touch requirements.txt
touch test_prediction.py
```

**Hint:** check the paths look right:

```bash
ls .github/workflows/
ls requirements.txt test_prediction.py
```

You should see `ci.yml` inside `.github/workflows/`, and the other two files in the project root.

**Optional (if attached files are provided):** copy them into those exact paths instead of using `touch` + paste, for example:

```bash
mkdir -p .github/workflows
cp /path/to/attached/ci.yml .github/workflows/ci.yml
cp /path/to/attached/requirements.txt requirements.txt
cp /path/to/attached/test_prediction.py test_prediction.py
```

**Step B — fill `requirements.txt` (project root)**

**Hint:** GitHub will install packages listed in this file.  
Open `requirements.txt` in your editor and paste the content below (or keep the attached copy).

**File content (create/save `requirements.txt`):**

```text
numpy
pandas
pytest
flake8
pre-commit
```

**Step C — fill the workflow file (`.github/workflows/ci.yml`)**

**Hint:** open `.github/workflows/ci.yml` (the file you created with `touch`) and paste this content.  
This is **file content**. It is **not** something you type into the terminal line by line.

**Important (Windows):** the file name must be exactly `ci.yml` — **not** `ci.yml.txt`.  
If Notepad saved `ci.yml.txt`, rename it:

```bash
mv .github/workflows/ci.yml.txt .github/workflows/ci.yml
```

Check the real file name:

```bash
ls .github/workflows/
```

You should see `ci.yml`.

**File content (create/save this file):**

```yaml
# .github/workflows/ci.yml
# Hint: this recipe runs on GitHub, not on your laptop
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install flake8 pytest
      - run: flake8 . --max-line-length=100
      - run: pytest -q
```

**Hint — what each line / parameter means:**
- `name: CI` → label shown in the GitHub **Actions** tab
- `on: [push, pull_request]` → run after a push **and** when a Pull Request (PR) is opened/updated
- `runs-on: ubuntu-latest` → use a free Linux computer on GitHub
- `actions/checkout@v4` → download your project code (`@v4` = version 4 of that action)
- `actions/setup-python@v5` → install Python (`@v5` = version 5 of that action)
- `python-version: '3.11'` → which Python version to install
- `pip install -r requirements.txt` → install packages listed in the file (`-r` = from requirements file)
- `pip install flake8 pytest` → install the linter and test runner
- `flake8 . --max-line-length=100` → lint current folder (`.`); allow lines up to 100 characters
- `pytest -q` → run tests; `-q` = quiet (less text)

**Step D — fill `test_prediction.py` (project root)**

**Hint:** open `test_prediction.py` in the **same folder as** `prediction.py` (your project root), not inside `data/` or `.github/`. Paste the content below.

**File content (create/save `test_prediction.py`):**

```python
from prediction import predict

def test_predict_runs():
    predict()
```

**Step E — commit on the feature branch and push**

**Hint:** you should still be on `feature/add-ci`. If not, switch with:

```bash
git checkout feature/add-ci
```

**Hint — command meaning:**
- `git add <files>` = stage these files
- `git commit -m "..."` = save snapshot with message
- `git push -u origin feature/add-ci` = upload this feature branch (`-u` remembers the link)

**Command (type this):**

```bash
git add .github/ requirements.txt test_prediction.py
git status
git commit -m "ci: add lint + tests workflow"
git push -u origin feature/add-ci
```

**Hint:** prefer `git add .github/` (whole folder). That still works if the nested path is awkward.  
If you see `pathspec ... did not match any files`, check the file name with `ls .github/workflows/` — Windows may have saved `ci.yml.txt` instead of `ci.yml`.

**Step F — open a Pull Request (because `main` is protected)**

**Hint (on GitHub — click, do not type):**
1. Open your repository on github.com
2. Click **Compare & pull request** (or **Pull requests** → **New pull request**)
3. Base: `main` ← compare: `feature/add-ci`
4. Title example: `Add CI workflow`
5. Click **Create pull request**
6. Wait for the CI status check (green tick / red X)
7. When happy, click **Merge pull request** → **Confirm** → **Delete branch**

**Step G — sync `main` locally and watch Actions**

**Command (type this):**

```bash
git checkout main
git pull
```

**Hint (on GitHub — click, do not type):**
1. Open the **Actions** tab
2. Click the newest run
3. Green tick = checks passed  
   Red X = something failed (open the failed step to read the error)

**Why:** Because branch protection is on, CI files must enter `main` through a PR. The PR also triggers the workflow (`on: [push, pull_request]`), so you can see the green tick before merging.

</details>

### Exercise 12 — Add pre-commit hooks

**Goal:** auto-format code and clean notebooks *before* each commit.  
**Task:** install pre-commit and enable three hooks: `black` (formatter), `flake8` (linter), `nbstripout` (removes notebook outputs).

**Attached with this tutorial (Exercise 12):** `.pre-commit-config.yaml`.  
Create it in the **project root** (same folder as `prediction.py`), not inside `.github/`.

**Steps:**
1. Because **main is protected**, create a **new** feature branch and make sure it is **active** (do this **before** any `git add` / `git commit` / `git push`).
2. Install pre-commit with `python -m …` (make sure `python` works in your terminal).
3. Create `.pre-commit-config.yaml` in the project root (see Solution command), then paste the hooks list.
4. Enable the Git hook — this drops a hook into `.git/hooks/pre-commit`.
5. Run hooks once on the whole project.
6. Only then: `git add` → `git commit` → `git push` on that new branch, then open a PR into `main`.

<details><summary>▶ Solution</summary>

**Hint:** a **hook** is an automatic check that runs when you try to commit.  
`pre-commit` is the manager that installs those checks for you.

**Important:** `main` is protected (Exercise 10), so create a **new branch** for this work (better than reusing an old branch).  
Do **Step 0 first**. The new branch must already be **created and active** before you run `git add` / `git commit` / `git push` later.

**Step 0 — create a new feature branch (do this first)**

**Hint — command meaning:**
- `git checkout main` = switch to `main` first (start from the protected default branch)
- `git pull` = get the latest `main` from GitHub
- `git checkout -b feature/add-pre-commit` = create + switch to a new branch for this exercise

**Command (type this):**

```bash
git checkout main
git pull
git checkout -b feature/add-pre-commit
```

**Hint:** stay on `feature/add-pre-commit` for the rest of Exercise 12.

**Hint — create vs switch:**
- First time (branch does **not** exist yet): use `git checkout -b feature/add-pre-commit`
- Later (branch **already** exists): use `git checkout feature/add-pre-commit`
- If you see `error: pathspec 'feature/add-pre-commit' did not match`, the branch was never created — go back and run Step 0 with `-b`.

**Step A — create the config file in the project root**

**Hint — where this file must live:**
- `.pre-commit-config.yaml` goes in the **project root** (same folder as `prediction.py`)
- do **not** put it inside `.github/`

**Hint — command meaning:**
- `touch .pre-commit-config.yaml` = create an empty config file at the correct path

**Command (type this):**

```bash
touch .pre-commit-config.yaml
ls .pre-commit-config.yaml
```

**Optional (if attached file is provided):**

```bash
cp /path/to/attached/.pre-commit-config.yaml .pre-commit-config.yaml
```

**Hint:** open `.pre-commit-config.yaml` and paste the content below (unless you copied the attached file).  
This is **file content**, not a terminal command.

**File content (create/save this file):**

```yaml
# .pre-commit-config.yaml
# Hint: this file lists the automatic checks to run before each commit
repos:
  # 1) black = formatter (fixes code layout automatically)
  - repo: https://github.com/psf/black
    rev: 24.4.2          # Hint: rev = tool version (keep as shown)
    hooks:
      - id: black        # Hint: id = which check to run from that repo

  # 2) flake8 = linter (reports style problems; does not auto-fix everything)
  - repo: https://github.com/pycqa/flake8
    rev: 7.1.0
    hooks:
      - id: flake8

  # 3) nbstripout = clean Jupyter notebooks (remove cell outputs)
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
```

**Hint — plain English for this file:**
- `repos:` = list of tools to download
- each `- repo:` block = one tool
- `rev:` = which version of that tool to use
- `hooks:` / `id:` = which check from that tool to turn on
- **black** → makes spacing/style consistent
- **flake8** → warns about messy or risky Python code
- **nbstripout** → removes notebook outputs so Git history stays small and readable

**Hint — command meaning:**
- `python -m pip install pre-commit` = install the pre-commit Python package
- `python` = the Python command (must be on your PATH)
- `-m pip` = run the pip module
- `install pre-commit` = download and install the package
- `python -m pre_commit install` = turn on the Git hook in this repo (writes into `.git/hooks/`)
- Note the underscore: module name is `pre_commit`, not `pre-commit`

**Hint:** if `python` is not found, close and reopen the terminal after adding Python to PATH, then check with `python --version`.

**Command (type this):**

```bash
python -m pip install pre-commit
python -m pre_commit install
```

**Hint:** if `pip` and `pre-commit` already work in your terminal, you can use the short form instead:  
`pip install pre-commit` then `pre-commit install`.

**Hint — command meaning:**
- `python -m pre_commit run --all-files` = run all hooks now on every file in the project
- `run` = execute hooks once
- `--all-files` = check the whole project (not only staged files)

**Command (type this once to check the whole project now):**

```bash
python -m pre_commit run --all-files
```

**Hint — how to read the result:**
- `Passed` = that check is OK
- `Failed` = fix the reported issue, then run the command again
- If **black** changes files, that is normal: run `git add` on the changed files, then commit again

**Hint — command meaning:**
- `git add .pre-commit-config.yaml` = stage the config file
- `git commit -m "..."` = save it (`-m` = message)
- `git push -u origin feature/add-pre-commit` = upload the **new** branch (`-u` remembers the link)

**Hint:** because **main is protected** (Exercise 10), do **not** push this straight to `main`.  
You should already be on `feature/add-pre-commit` from Step 0.  
If you are not, switch with `git checkout feature/add-pre-commit` (only works if Step 0 already created it).  
If that pathspec error appears, create it now with `git checkout -b feature/add-pre-commit`.

**Command (type this after the checks pass — you must already be on `feature/add-pre-commit`):**

```bash
git add .pre-commit-config.yaml
git commit -m "chore: enable pre-commit hooks"
git push -u origin feature/add-pre-commit
```

**Hint:** then open a pull request on GitHub: `feature/add-pre-commit` → `main`.

**Hint:** from now on, when you run `git commit`, these hooks run automatically.  
If a hook fails, the commit is stopped. Fix → `git add` → commit again.

**Why:** Local hooks catch problems *before* code reaches GitHub.  
CI (Exercise 11) catches problems *after* push. Using both is best practice.
</details>

---

## Concept check (5-minute self-quiz)

Answer in one line, then check.

1. What's the difference between `git add` and `git commit`?
2. Where does `git diff` look, and where does `git diff --staged` look?
3. Committing a `.env` file with an API key by mistake — is deleting the file enough to fix it?
4. Two branches change the same line. What happens on merge, and what do you do?
5. You made a fresh clone but the push is rejected with `[rejected] main -> main (fetch first)`. Why, and how do you fix it?

<details><summary>▶ Answers</summary>

1. `git add` chooses which files go into the next save. `git commit` actually saves that snapshot with a message.
2. `git diff` shows edits not staged yet. `git diff --staged` shows edits already staged (what the next commit will include).
3. **No.** Deleting the file is not enough. The secret can still be in old commits. Change/revoke the key, and add `.env` to `.gitignore` so it does not happen again.
4. Git shows a **merge conflict**. Open the file, keep the correct lines, delete the conflict markers, then `git add` and `git commit`. Use `git merge --abort` if you want to cancel.
5. GitHub has commits that your computer does not have yet. Run `git pull` first, then `git push`.

(End of answers.)
</details>

---

## Capstone challenge (optional, ~15 min)

Do the whole nine-step case study again on a **new** project of your own — a small script (calculator, greeting bot, anything). Include:

1. `git init`, first commit, `.gitignore` that keeps out `data/` and `.env`.
2. A `feature/*` branch with a real change, merged back into `main`.
3. **A deliberate conflict** — edit the same line on two branches, merge, resolve it, and note *which* version you kept and why.
4. Push to a fresh GitHub repo; **protect `main`**.
5. Open a PR from a second branch and merge it via the PR (not on the command line).
6. Add `ci.yml` so the PR gets a green tick.
7. Add `.pre-commit-config.yaml` with at least `black` and `flake8`.

You've now done, unaided, the exact workflow expected in your **Final Project** — and the reproducibility hallmarks the **Paper Critique** asks you to look for in others' work.

---

*DSTS 11523 · University of Canberra · Dr Ibrahim Radwan — all commands verified on Git 2.43, running end-to-end on a real repo.*
