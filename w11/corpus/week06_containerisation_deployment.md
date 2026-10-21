# DSTS 11523 · Week 6 Tutorial

## Containerisation & Deployment — hands-on lab (2 hours)

**How to use this tutorial.** Work top to bottom in a terminal. Every exercise has a **Goal**, a **Task**, some **Steps**, and a **▶ Solution** drop-down. *Try each exercise before you open the solution.* No Docker experience needed.

Inside the solutions, four labels tell you what to do with each block:

| Label | What you do |
|---|---|
| **Hint** | Read only — explains a command or a flag |
| **Command** | Type / paste **only** these lines |
| **Output** | Read only — what the tool prints back |
| **File content** | Create the file and paste this into it |

Two more appear on the steps that commonly go wrong: **Expected result** and **If it fails**.

---

## Why Docker?

**The problem.** Your model runs fine on your laptop. You send it to a classmate or a server and it breaks: they have a different Python version, missing packages, or a different OS. Nothing is wrong with your model — the *environment* is wrong.

**What Docker does.** It packs your code, your libraries, your Python version and your trained model into one bundle called an **image**. Any machine with Docker runs that image the same way, because the environment travels with the app.

**Concrete example — the API you are about to build:**

| | Without Docker | With Docker |
|---|---|---|
| Your classmate must | install Python, make a venv, `pip install` 6 pinned packages, find the model file, run the right uvicorn command | run **one** command |
| The command | *(about 6 steps)* | `docker run -d -p 8000:8000 rain-api:v1` |
| Time until it works | 10–30 min, if nothing goes wrong | seconds |

**This lab in four steps:** train a rain model → wrap it in a FastAPI service → package it into an image → run it as a container.

---

## Step 0 · Install Docker (do this first)

1. Install **Docker Desktop** (Windows/macOS) or **Docker for Linux** from [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/).
2. **Open Docker Desktop and wait until it says *running*.** Leave it open for the whole lab. If it is closed, later commands will fail.
3. Open a terminal. On Windows use **Git Bash** — `ls`, `touch` and `curl` all work there. (We use the terminal in this lab, not the Docker Desktop window.)

**Hint — command meaning:**
- `docker --version` = print the Docker version number
- `docker info` = check that Docker is **running and ready** (not only installed)

**Command (type this):**

```bash
docker --version
docker info
```

**Expected result:** a version number (**20 or newer is fine**), then many lines from `docker info` that include a **`Server:`** section. Seeing `Server:` means Docker is running.

**If it fails:**
- `Cannot connect to the Docker daemon` → Docker is installed but **not running**. The *daemon* is Docker’s background service (started by Docker Desktop). Open Docker Desktop, wait until it says *running*, then retry.
- `docker: command not found` → close the terminal, open a new one. If it persists, reinstall Docker Desktop.

---

## Quick concepts (read once)

### Words used when we build the rain API

**API**  
A simple “front door” for your model. Other programs — or your browser — send a request and get an answer back.  
Example: send humidity/temperature/… → get `will_rain: true/false`.

**Endpoint**  
One specific door on that API (a URL path).  
Examples: `/health` = “are you alive?”, `/predict` = “will it rain?”

**FastAPI**  
A Python library. You write endpoints in `app.py` (the rules of the API).

**uvicorn**  
The program that **starts** your FastAPI app and waits for requests on a port (like 8000).  
Think: `app.py` = the menu; **uvicorn** = the waiter who serves it. Without uvicorn, opening `http://localhost:8000` does nothing.

**`/docs`**  
A free clickable test page FastAPI creates for you (Swagger UI). Open `http://localhost:8000/docs` to try `/health` and `/predict` without writing curl.

### Docker ideas

**Image vs container**  
- **Image** = a packed box with everything needed (Python + packages + your code + model). It does not run by itself.  
- **Container** = that box **opened and running**.  
Analogy: image ≈ a recipe card; container ≈ cooking that recipe right now.

**Dockerfile → image → container**  
1. Write a **Dockerfile** (the recipe).  
2. `docker build` → makes an **image**.  
3. `docker run` → starts a **container** from that image.  
Important: **build ≠ run**. Building only creates the image; your API starts only when you run a container.

**Port mapping `-p HOST:CONTAINER`**  
Your app inside the container listens on a port (e.g. 8000). Your laptop needs a matching door.  
`-p 8000:8000` means: laptop port **8000** → container port **8000**.  
Rule: **left number = your laptop**, **right number = inside the container**.  
Then open `http://localhost:8000`.

**Why `--host 0.0.0.0` inside Docker**  
- On your laptop for a quick test: `--host 127.0.0.1` is fine (only you).  
- Inside a container: `127.0.0.1` means “only this container”, so your browser on the laptop gets *connection refused*.  
- Use `0.0.0.0` so requests from your laptop (via `-p`) can reach the app.

**The `.` at the end of `docker build -t rain-api:v1 .`**  
The `.` means “use **this folder**”. Docker looks here for the Dockerfile and the files to copy.  
So always run build from `rain-api/` (the folder that contains the Dockerfile).

**Layer cache (why order matters)**  
Each line in a Dockerfile is a **layer**. If a layer did not change, Docker reuses it (fast).  
Put `requirements.txt` + `pip install` **before** copying `app.py`. Then editing code does not reinstall all packages every time.

### Handy Docker commands (you will use these)

| Command | What it does (plain English) | When you use it |
|---|---|---|
| `docker ps` | Shows containers that are **running now** | “Is my API up?” |
| `docker ps -a` | Shows **all** containers, including stopped ones (`-a` = all) | After `hello-world` exits, or to find an old container |
| `docker images` | Shows images saved on your computer | After `docker build`, to check `rain-api:v1` exists |
| `docker logs <name>` | Prints what the app wrote (errors, “Uvicorn running…”) | Container looks broken or you want to see requests |
| `docker exec -it <name> bash` | Opens a terminal **inside** a running container (`-i` + `-t` = interactive) | Look at files inside, e.g. `ls /app` |
| `docker rm -f <name>` | **Force** stop and delete that container (`-f` = force) | Name already in use, or clean up `rain` / `mynginx` |

**Hint:** `<name>` means the **container name** you chose earlier (the `--name ...` value), for example `rain` or `mynginx` — not the image name.



---

## Setup

**Hint — command meaning:** `mkdir` = make a folder · `cd` = enter it · `&&` = only if the previous command worked · `pwd` = show which folder you are in.

**Command (type this):**

```bash
mkdir dsts-week6 && cd dsts-week6
pwd
```

**Expected result:** the path printed by `pwd` ends with `dsts-week6` (one line — that is all `pwd` shows).

**Folder map (not `pwd` output):** by the **end of the lab**, your folders will look like this. Right now you only have the empty `dsts-week6` folder — the files below appear later, exercise by exercise.

```text
dsts-week6/
└── rain-api/              <-- almost every command runs here
    ├── requirements.txt
    ├── train.py
    ├── app.py
    ├── model/rf.joblib    (created by train.py)
    ├── Dockerfile
    ├── .dockerignore
    └── docker-compose.yml
```

**Golden rule:** run `pwd` before each command block. Being in the wrong folder is the number-one cause of Docker errors.

---

## Part 1 · Docker basics *(≈ 15 min)*

**Notes.** Learn the commands on tiny throwaway examples first. Your own app comes in Part 2.

**Before Exercise 1 — make sure Docker Desktop is running**

1. Open **Docker Desktop** and wait until it says **running**.
2. In your terminal, check:

```bash
docker info
```

**Expected result:** you see a **`Server:`** section. Only then continue to Exercise 1.

**If you see** `failed to connect ... docker_engine` or `The system cannot find the file specified`: your `docker run` command is fine — Docker Desktop is just not available to the terminal yet. Open Docker Desktop, wait, run `docker info` again, then retry.

### Exercise 1 — Run your first container

**Goal:** confirm Docker is healthy and run something in a container.
**Task:** run the official `hello-world` image, then see what it left behind.

**Why this exercise?**  
It proves Docker really works on your machine, and it shows the difference you will rely on all lab: the **image** stays on your disk, while the **container** runs, prints its message and **exits**. Every later exercise is the same two ideas with a bigger app.

**Steps:**
1. Run `hello-world`.
2. List all containers, including stopped ones (`docker ps -a`).
3. List your images (`docker images`).

<details><summary>▶ Solution</summary>

**This exercise produces:** one exited `hello-world` container and one `hello-world` image on your machine.

#### Step 1 — Run `hello-world`

**Hint:** `docker run hello-world` = download the image if needed, then start a container from it.

**Command (type this):**

```bash
docker run hello-world
```

**Output (do not type — shortened):**

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
Hello from Docker!
```

**Hint:** `Unable to find image ... locally` is not an error — Docker just had to download it first.

**If it fails:**
- `failed to connect ... docker_engine` / `Cannot connect to the Docker daemon` → Docker Desktop is not running (see the note **before** this exercise). Open it, wait, run `docker info`, then retry.
- Slow first run → normal, it is downloading.

#### Step 2 — List all containers, including stopped ones

**Hint:** `docker ps -a` = show all containers (`-a` = all, not just running). Plain `docker ps` shows nothing here, because the container already finished.

**Command (type this):**

```bash
docker ps -a
```

**Output (do not type — shortened):**

```text
CONTAINER ID   IMAGE         STATUS                     NAMES
3f1b0c9d2a11   hello-world   Exited (0) 8 seconds ago   eager_bohr
```

**Expected result:** one row with image `hello-world` and status `Exited (0)`.

#### Step 3 — List your images

**Hint:** `docker images` = show images stored on your disk.

**Command (type this):**

```bash
docker images
```

**Output (do not type — shortened):**

```text
REPOSITORY    TAG      IMAGE ID       CREATED         SIZE
hello-world   latest   d2c94e258dcb   14 months ago   13.3kB
```

**Expected result:** `hello-world` is listed. The image stays on disk even after the container exits.

**Why:** Docker pulled an image, made a container, ran it, and the container **exited** because its only job was to print a message. A container lives exactly as long as its main process.
</details>

### Exercise 2 — Run a real service and look inside it

**Goal:** see a **long-running** container (stays up), open it in a browser, look inside it, then delete it.
**Task:** run Nginx in the background, open it, look inside, then clean up.

**What is Nginx?**  
Nginx is a **popular web server** (it shows web pages). We did **not** invent it for this lab — Docker Hub already has an official `nginx` image.  
We use it here as a **simple practice app** before your rain API: you learn `-d`, `-p`, `--name`, `exec`, `stop`, and `rm` on something easy.

**Why this exercise?**  
Exercise 1’s `hello-world` prints a message and **exits**. A real API (and Nginx) **keeps running**. This exercise teaches that difference, plus how to open a shell inside a running container — skills you need later for `rain-api`.

**Steps:**
1. Start Nginx with a name and a port mapping.
2. Open `http://localhost:8080` in your browser.
3. Open a shell inside, look around, exit.
4. Stop and remove it (so nothing is left running).

<details><summary>▶ Solution</summary>

**Brief:** you will start a throwaway Nginx container, visit it, peek inside, then delete it. Nothing from this exercise is needed later — it is practice only.

#### Step 1 — Start Nginx with a name and a port mapping

**Hint — command meaning:**
- `docker run` = create and start a container from an image
- `-d` = **detached mode** = the container keeps running in the background, and your terminal gives you the prompt back so you can type the next command. Without `-d`, the terminal would stay “busy” attached to Nginx.
- `-p 8080:80` = laptop port **8080** → container port **80** (Nginx listens on 80 **inside** the container)
- `--name mynginx` = give this container the name `mynginx` (easier than a random ID)
- `nginx` = the **image** name from Docker Hub (Docker downloads it if you do not have it yet)

**Command (type this):**

```bash
docker run -d -p 8080:80 --name mynginx nginx
```

**Command (type this — check it is running):**

```bash
docker ps
```

**Output (do not type):**

```text
CONTAINER ID   IMAGE   STATUS         PORTS                  NAMES
7a2c9f8e1b04   nginx   Up 3 seconds   0.0.0.0:8080->80/tcp   mynginx
```

**Expected result:** status says `Up ...` (still running). Unlike `hello-world`, this container stays up because a web server keeps waiting for visitors.

**If it fails:**
- `port is already allocated` → use `-p 8081:80` instead (then open `http://localhost:8081` in Step 2).
- name already in use → `docker rm -f mynginx`, then run the `docker run` command again.
- `failed to connect ... docker_engine` → Docker Desktop is not running (see the note before Exercise 1).

#### Step 2 — Open `http://localhost:8080` in your browser

Nothing to type in the terminal — paste that address into your browser.

**Expected result:** the **"Welcome to nginx!"** page. That page is served **from inside the container**. The `-p 8080:80` mapping is what lets your browser reach it.

#### Step 3 — Open a shell inside, look around, exit

**Hint — command meaning:**
- `docker exec` = run a command **inside** a container that is already running
- `-it` = interactive mode (so you can type commands inside)
- `bash` = start a Linux shell inside the container

**Command (type this):**

```bash
docker exec -it mynginx bash
```

Your prompt changes — you are **inside** the container now.

**Command (type these three lines inside the container):**

```bash
ls /
whoami
exit
```

**Hint — what each command does inside the container:**
- `ls /` = list the top-level folders **inside the container** (a tiny Linux system). These are **not** your Windows/Mac Desktop files.
- `whoami` = print the user name you are logged in as **inside the container** (usually `root` for this Nginx image).
- `exit` = leave the container shell and return to your normal laptop terminal.

**If it fails:** `bash: executable file not found` → use `docker exec -it mynginx sh` instead.

#### Step 4 — Stop and remove it (clean up)

**Hint:** we delete this practice container so it does not keep using port 8080. Your rain API work starts fresh in Part 2.

**Command (type this):**

```bash
docker stop mynginx && docker rm mynginx
```

**Expected result:** `docker ps -a` no longer lists `mynginx`, and `http://localhost:8080` stops working.

**Why:** you practiced a **long-running** container (like your future rain API), port mapping (`-p`), and debugging with `exec` — without installing Nginx on your laptop. Nginx was only a training example.
</details>

**Checkpoint:** you can run, list, enter, stop and remove containers.

---

## Part 2 · The rain app *(≈ 15 min)*

**Notes.** No Docker in this part. First you **train** a rain model (`train.py` → `model/rf.joblib`), then you **serve** it with FastAPI + uvicorn (`app.py`). Get that working on your laptop first, so later Docker problems are clearly Docker problems.

**Hint:** there is **no CSV to download**. `train.py` builds a small **synthetic** (fake) rain dataset itself: **4 input features** — `humidity`, `temperature`, `pressure`, `wind_speed` — and one yes/no label **`will_rain`**.

### Exercise 3 — Set up the project and train the model

**Goal:** create the project folder and produce a saved model file.
**Task:** create `rain-api/`, add `requirements.txt` and `train.py`, install, train.

**What are these two files?**  
- `requirements.txt` = the shopping list of Python packages, each pinned to an exact version. Both your laptop and the Docker image install from this same list.  
- `train.py` = the script that trains the rain model and saves it as `model/rf.joblib`.  
- **Synthetic data** = fake weather rows the script generates itself. There is **nothing to download** — this keeps everyone's data identical and the lab about Docker, not about CSV hunting.

**Why this exercise?**  
Docker packages something that already works. So you train the model **first**, on your laptop, and end up with one file (`rf.joblib`) that the image will later copy in. Train once, serve many times.

**Steps:**
1. Create the folders (`rain-api/` and `rain-api/model/`).
2. Create the two files and paste their content.
3. Install the packages and run the training.
4. Confirm `model/rf.joblib` exists.

<details><summary>▶ Solution</summary>

**This exercise produces:** the `rain-api/` folder, two source files, and a trained model saved at `model/rf.joblib`.

#### Step 1 — Create the folders

**Hint — command meaning:** `mkdir` = make a folder · `cd` = enter it · `pwd` = show where you are.

**Command (type this — you should be in `dsts-week6`):**

```bash
pwd
mkdir rain-api && cd rain-api && mkdir model
pwd
```

**Expected result:** the second `pwd` ends with `dsts-week6/rain-api`. **Stay here for the rest of the lab.**

#### Step 2 — Create the two files and paste their content

**Hint:** `touch <name>` creates an empty file, which you then open and paste into.  
In PowerShell `touch` does not exist — use Git Bash, or create the files with your editor (File → New).

**Command (type this):**

```bash
touch requirements.txt
touch train.py
ls
```

**Expected result:** `ls` shows `requirements.txt` and `train.py` (and the `model/` folder).

Now open each file in your editor. Select all → paste the matching **File content** below → **Save**.

**File content (`rain-api/requirements.txt`):**

```text
fastapi==0.115.0
uvicorn[standard]==0.32.0
scikit-learn==1.5.2
joblib==1.4.2
pandas==2.2.3
numpy==2.1.3
```

**Hint:** `==` pins an exact version, so your laptop and the Docker image install exactly the same thing.

**File content (`rain-api/train.py`):**

```python
"""Train a small rain-prediction model and save it to model/rf.joblib."""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FEATURES = ["humidity", "temperature", "pressure", "wind_speed"]

# 1) make a small synthetic weather dataset (no download needed)
rng = np.random.default_rng(42)
n = 2000

X = pd.DataFrame(
    {
        "humidity": rng.uniform(20, 100, n),      # %
        "temperature": rng.uniform(0, 40, n),     # degrees C
        "pressure": rng.uniform(980, 1040, n),    # hPa
        "wind_speed": rng.uniform(0, 60, n),      # km/h
    },
    columns=FEATURES,
)

# 2) rain is more likely when humidity is high and pressure is low
score = (
    0.06 * X["humidity"]
    - 0.05 * (X["pressure"] - 1010)
    + 0.02 * X["wind_speed"]
    - 0.03 * X["temperature"]
)
prob_rain = 1 / (1 + np.exp(-2.0 * (score - 3.6)))
y = (rng.uniform(0, 1, n) < prob_rain).astype(int)

# 3) train and score
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xtr, ytr)

# 4) save the trained model for the API to load
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/rf.joblib")
print(f"saved model/rf.joblib | features: {FEATURES} | test accuracy: {model.score(Xte, yte):.4f}")
```

**Hint — what this script does:**
- builds 2000 fake weather rows with 4 columns, then labels each one rainy or not — high humidity and low pressure make rain more likely
- `rng = np.random.default_rng(42)` = a fixed seed, so everyone gets the same data
- `joblib.dump(...)` = **saves the trained model to a file** — this is the line that matters for Docker, because the API will load that file

#### Step 3 — Install the packages and run the training

**Hint — command meaning:**
- `python -m pip install -r requirements.txt` = install the listed packages (`-m pip` is the reliable form on Windows, `-r` = read from this file)
- `python train.py` = run the training script

**Command (type this):**

```bash
python -m pip install -r requirements.txt
python train.py
```

**Output (do not type):**

```text
saved model/rf.joblib | features: ['humidity', 'temperature', 'pressure', 'wind_speed'] | test accuracy: 0.8650
```

**Expected result:** the `saved model/rf.joblib ...` line, with accuracy about **0.86**.

**If it fails:**
- `python: command not found` → on Windows try `py -m pip ...` and `py train.py`.
- `No such file or directory: 'requirements.txt'` → wrong folder. `pwd` must end with `rain-api`.
- The install takes a few minutes the first time — normal.

#### Step 4 — Confirm `model/rf.joblib` exists

**Command (type this):**

```bash
ls model/
```

**Output (do not type):**

```text
rf.joblib
```

**Expected result:** the file is listed. If `model/` is empty, Step 3 did not finish — read its error message.

**Why:** the trained model now lives in a **file**. That file gets copied into the image later — the container never retrains, it just loads `rf.joblib` and answers questions. "Train once, serve many times" is the standard production split.
</details>

### Exercise 4 — Write the API and run it locally

**Goal:** get a working HTTP service before adding Docker.
**Task:** write `app.py`, start uvicorn, test `/health` and `/predict`.

**What is FastAPI, uvicorn and `/docs`?**  
- **FastAPI** = the Python library you use in `app.py` to write the endpoints (`/health`, `/predict`).  
- **uvicorn** = the program that actually **starts** your app and listens on a port. `app.py` is the menu; uvicorn is the waiter. Without it, `http://localhost:8000` does nothing.  
- **`/docs`** = a clickable test page FastAPI generates for free (Swagger UI), so you can try the endpoints in your browser without writing curl.

**Why this exercise?**  
You get the API working **on your laptop, with no Docker involved**. That way, if something breaks in Part 3 or 4, you already know it is a Docker problem and not a Python one.

**Steps:**
1. Create `app.py` and paste the content.
2. Start the server with **uvicorn** and leave that terminal running.
3. In your browser, open `http://localhost:8000/docs` and test `/health` and `/predict`.

<details><summary>▶ Solution</summary>

**This exercise produces:** `app.py`, and a working API answering on `http://localhost:8000`.

#### Step 1 — Create `app.py` and paste the content

**Command (type this — still in `rain-api/`):**

```bash
pwd
touch app.py
```

Open `app.py` in your editor, paste the **File content** below, and **Save**.

**File content (`rain-api/app.py`):**

```python
"""Rain-prediction API: takes 4 weather numbers, returns will_rain."""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

FEATURES = ["humidity", "temperature", "pressure", "wind_speed"]

model = joblib.load("model/rf.joblib")
app = FastAPI(title="Rain Prediction API")


class Weather(BaseModel):
    humidity: float      # %
    temperature: float   # degrees C
    pressure: float      # hPa
    wind_speed: float    # km/h


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(w: Weather):
    row = pd.DataFrame(
        [[w.humidity, w.temperature, w.pressure, w.wind_speed]], columns=FEATURES
    )
    prob_rain = float(model.predict_proba(row)[0][1])
    return {"will_rain": bool(prob_rain >= 0.5), "prob_rain": round(prob_rain, 3)}
```

**Hint — what this file does:**
- `joblib.load(...)` loads the model **once** at startup, not on every request
- `class Weather(BaseModel)` describes the JSON we accept — the **same 4 features, in the same order** as training
- `/health` = a simple “are you alive?” check. Tools (and later Docker/cloud) call it to see if the API is up. You do **not** need a load balancer in this lab — that is just a real-world example of who uses `/health`.
- `/predict` = returns `will_rain` (true/false) and `prob_rain` (0 to 1)

#### Step 2 — Start the server with uvicorn and leave it running

**Hint:** this is the command that starts the server. It keeps the terminal busy on purpose.

**Hint — command meaning:**
- `python -m uvicorn` = start uvicorn through Python (reliable on Windows)
- `app:app` = file `app.py` → object named `app` (the `app = FastAPI(...)` line)
- `--host 127.0.0.1` = only your laptop can connect (local test; inside Docker we use `0.0.0.0` later)
- `--port 8000` = listen on port 8000 → open `http://localhost:8000`
- `--reload` = auto-restart when you edit code (handy while learning; usually off in production/Docker)

**Command (type this, then leave the terminal alone):**

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

**Expected result:** it prints `Application startup complete.` and does **not** return to the prompt. That is correct — the server is running. Stop it later with **Ctrl+C**.

**If it fails:**
- `FileNotFoundError: model/rf.joblib` → run `python train.py` inside `rain-api/` first (Exercise 3).
- Port 8000 busy → use `--port 8001` and open `http://localhost:8001/docs` in Step 3.
- `ModuleNotFoundError` → re-run `python -m pip install -r requirements.txt`.

#### Step 3 — Open `http://localhost:8000/docs` and test `/health` and `/predict`

Leave the server running and use a **browser** — Swagger UI is generated free by FastAPI.

1. **GET /health** → *Try it out* → *Execute* → you get `{"status":"ok"}`.
2. **POST /predict** → *Try it out* → paste the body below → *Execute*.

**File content (paste into the Swagger request body):**

```json
{"humidity": 92, "temperature": 18, "pressure": 995, "wind_speed": 25}
```

**Output (do not type):**

```text
{"will_rain":true,"prob_rain":0.98}
```

**Hint:** try a dry day too — `{"humidity": 35, "temperature": 30, "pressure": 1025, "wind_speed": 5}` returns `{"will_rain":false,"prob_rain":0.0}`.

Press **Ctrl+C** in the server terminal when you are done.

**Why:** if the API works here, any problem in Part 3 or 4 is a **Docker** problem, not a Python problem. Debugging one layer at a time is the most useful habit in deployment work.
</details>

**Checkpoint:** a trained model at `rain-api/model/rf.joblib` and a working API on your laptop.

---

## Part 3 · Dockerfile & build *(≈ 25 min)*

**Notes.** A **Dockerfile** is a plain text recipe with no file extension. `docker build` follows it and produces an image.

### Exercise 5 — Write the Dockerfile

**Goal:** write a small Dockerfile that rebuilds **quickly** when you only edit code (sometimes called “cache-friendly”).
**Task:** create `Dockerfile` inside `rain-api/` and paste the recipe.

**What is a Dockerfile?**  
A plain text file named exactly `Dockerfile` (**capital D**, **no** `.txt` extension).  
It is a **recipe** Docker follows **top to bottom** to build your image. Typical steps:
1. start from a base Python image  
2. install packages  
3. copy your files  
4. say which command to run when the container starts  

When you later run `docker build`, Docker reads this recipe and builds the image.

**What is a layer? What does “cached” mean?**  
- Each instruction in the Dockerfile (`FROM`, `COPY`, `RUN`, …) creates one **layer** = one saved step of the image.  
- **Cached** means: “this step did not change since last time, so Docker **reuses** the old result instead of doing the work again.”  
- That is why order matters: put slow steps that rarely change (install packages) **before** steps that change often (copy `app.py`).

**Why put dependencies before code?**  
- `requirements.txt` almost never changes.  
- `app.py` you edit often (“changes constantly” = you change it again and again while coding).  
- If packages are installed **first**, editing `app.py` does **not** force Docker to reinstall scikit-learn every time. You will see this in Exercise 7.

**Steps:**
1. Create the file (exact name `Dockerfile`, no extension).
2. Paste the recipe — dependencies first, code after.

<details><summary>▶ Solution</summary>

**This exercise produces:** a file named exactly `Dockerfile` (no extension) holding the build recipe.

#### Step 1 — Create the file (exact name, no extension)

**Command (type this — `pwd` must end with `rain-api`):**

```bash
touch Dockerfile
ls
```

**Expected result:** the listing shows `Dockerfile`, not `Dockerfile.txt`.

**If it fails:** your editor added an extension → rename it with `mv Dockerfile.txt Dockerfile`.

#### Step 2 — Paste the recipe — dependencies first, code after

Open `Dockerfile` in your editor, paste the **File content** below, and **Save**.

**File content (`rain-api/Dockerfile`):**

```dockerfile
# Dockerfile — rain-prediction API
FROM python:3.11-slim

WORKDIR /app

# 1) dependencies FIRST — this layer is cached across code edits
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) then the code and the model
COPY app.py .
COPY model/ ./model/

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Hint — plain English (each line ≈ one layer):**
- `FROM python:3.11-slim` = **layer 1** — start from a ready-made small Python 3.11 image (`-slim` = smaller download than the full Python image). This is its **own** layer because it is the base everything else sits on.
- `WORKDIR /app` = make `/app` the current folder inside the image
- `COPY requirements.txt .` then `RUN pip install ...` = **next layers** — copy the package list and install packages **while building**. `--no-cache-dir` tells pip not to keep extra download files, which keeps the image smaller
- `COPY app.py .` / `COPY model/ ./model/` = later layers — bring in the code and the trained model
- `EXPOSE 8000` = note for humans: the app will use port 8000 (you still need `-p` when you run)
- `CMD [...]` = the default command when a container starts — here it starts **uvicorn** (same web server as Exercise 4)
- **`--host 0.0.0.0` is mandatory inside Docker.** With `127.0.0.1` your laptop browser could not reach the app.

**Why this order (beginner version):**  
Imagine two rebuilds after you fix one line in `app.py`:
- **Good order (this file):** Docker sees `requirements.txt` unchanged → reuses the old “pip install” layer (**CACHED**, fast) → only re-copies `app.py`.  
- **Bad order** (`COPY . .` first): any tiny code edit looks like “everything changed” → Docker reinstalls all packages again (slow).

You will prove the good order works in Exercise 7.
</details>

### Exercise 6 — Build the image

**Goal:** turn the Dockerfile into an image named `rain-api:v1`.
**Task:** build it, then confirm it exists.

**What is `docker build`, and what is the tag `rain-api:v1`?**  
- `docker build` = run the Dockerfile once and save the result as an **image** on your disk. It does **not** start your API.  
- `rain-api:v1` = the image's **name** (`rain-api`) and **version tag** (`v1`), given with `-t`. Without a tag the image has no name and is awkward to run.

**Why this exercise?**  
This is the moment your code, packages and trained model get frozen into one shippable artefact. Everything after this (run, Compose, push) just uses the image you make here.

**Steps:**
1. Check you are in `rain-api/`.
2. Build with a tag (`-t rain-api:v1`).
3. Find `rain-api` in `docker images`.

<details><summary>▶ Solution</summary>

**This exercise produces:** a local image called `rain-api:v1`.

#### Step 1 — Check you are in `rain-api/`

**Command (type this):**

```bash
pwd
```

**Expected result:** the path ends with `rain-api`. If not, `cd` there first — the build reads the Dockerfile from the folder you are standing in.

#### Step 2 — Build with a tag

**Hint — command meaning:**
- `-t rain-api:v1` = tag it: name `rain-api`, version tag `v1`. Without `-t` the image has no name and is painful to use
- `.` = the build context = this folder, which is also where Docker looks for the Dockerfile

**Command (type this):**

```bash
docker build -t rain-api:v1 .
```

**Output (do not type — shortened):**

```text
[+] Building 45.2s (10/10) FINISHED
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => naming to docker.io/library/rain-api:v1
```

**Expected result:** the build ends with `FINISHED`.

**If it fails:**
- `failed to read dockerfile` → wrong folder, or the file is named `Dockerfile.txt` (rename it).
- `the Dockerfile cannot be empty` → you created the file but did **not** paste the recipe yet (go back to Exercise 5 Step 2, paste the File content, **Save**, then rebuild). Ignore “Debug this build failure with Gordon / docker ai …” suggestions unless your instructor uses them.
- `COPY failed: file not found ... model` → run `python train.py` first (Exercise 3) so `model/rf.joblib` exists.
- First build takes 2–5 minutes — normal: Docker is downloading the base image and installing packages.

#### Step 3 — Find `rain-api` in `docker images`

**Command (type this):**

```bash
docker images
```

**Output (do not type — shortened):**

```text
REPOSITORY   TAG   IMAGE ID       CREATED          SIZE
rain-api     v1    9b1f2c4e7a30   20 seconds ago   612MB
```

**Expected result:** a row with repository `rain-api` and tag `v1`.

**Why:** the image now holds Python, your packages, your code and your trained model, frozen together. Anyone with Docker can run it without installing Python or scikit-learn.
</details>

### Exercise 7 — Watch the layer cache work

**Goal:** see with your own eyes why Dockerfile order matters.
**Task:** change **only one line** in `app.py`, rebuild, and look for the word **`CACHED`**.

**The big idea (read this first):**  
Think of the Dockerfile as a stack of Lego blocks (layers), built from the bottom up:

1. base Python image  
2. copy `requirements.txt` + install packages ← **slow** (can take minutes)  
3. copy `app.py` and the model ← **fast**

Docker remembers finished blocks.  
If a block’s ingredients did **not** change, Docker **reuses** it and prints **`CACHED`** (skip the work).  
If a block **did** change, Docker rebuilds that block **and everything above it**.

So in this exercise you change only `app.py` (the top block). The slow “install packages” block should stay **CACHED**.

| | Exercise 6 (first build) | This exercise (after editing `app.py`) |
|---|---|---|
| Did `requirements.txt` change? | new / first time | **No** |
| Did `app.py` change? | yes (first copy) | **Yes** (title only) |
| What you should see | long `pip install` | `CACHED` on pip install |
| Typical time | minutes | a few seconds |

**Why this exercise?**  
So you believe the Exercise 5 order is useful: put slow, rarely changing steps first.

**Steps:**
1. Edit the FastAPI title in `app.py` and save (tiny change only).
2. Rebuild and look for `CACHED` on the pip install line.

<details><summary>▶ Solution</summary>

**Brief:** you are not adding a new feature — you are proving Docker is smart enough to skip unchanged work.

#### Step 1 — Edit one line in `app.py` (tiny change)

Open `rain-api/app.py`. Change **only** this line:

```python
app = FastAPI(title="Rain Prediction API")
```

to:

```python
app = FastAPI(title="Rain Prediction API v2")
```

**Save the file.** Do not change `requirements.txt`.

**Hint:** we change a title on purpose — a small edit that should **not** force a full package reinstall.

#### Step 2 — Rebuild and look for `CACHED`

**Command (type this — still in `rain-api/`):**

```bash
docker build -t rain-api:v1 .
```

**Output (do not type — look carefully for the word CACHED):**

```text
[+] Building 2.8s (10/10) FINISHED
 => CACHED [3/6] COPY requirements.txt .
 => CACHED [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => [5/6] COPY app.py .
 => [6/6] COPY model/ ./model/
```

**How to read this (beginner map):**
- **`CACHED` on `requirements.txt` / `pip install`** = “packages already installed last time; ingredients unchanged → reuse.”  
- **No `CACHED` on `COPY app.py`** = “`app.py` changed → do this step again.”  
- Total time should be **much shorter** than Exercise 6.

**Expected result:** you see **`CACHED`** next to the pip install step, and the build finishes in seconds (not minutes).

**Why (simple story):**  
You only moved one Lego on top (`app.py`). The big Lego underneath (install packages) was untouched, so Docker kept it.  

**What would go wrong with a bad Dockerfile?**  
If you had written `COPY . .` near the top (copy everything first), then editing `app.py` would make Docker think the early steps changed too → it would reinstall scikit-learn again. That is why we copy `requirements.txt` and install packages **before** copying `app.py`.
</details>

**Checkpoint:** you have a local image `rain-api:v1`, and you understand what **CACHED** means.

---

## Part 4 · Run & call the API *(≈ 20 min)*

**Notes.** Building does not start your app. `docker run` does. Today's flags: `-d` and `-p`.

### Exercise 8 — Run the container and call it

**Goal:** start your API inside Docker and talk to it from your laptop.
**Task:** run it in the background, test `/health` and `/predict`, read the logs.

**Why run the image? (plain English)**  
So far you only **built** an image (`docker build`). That is like packing a lunchbox and putting it in the fridge — the food is ready, but nobody is eating yet.

- **`docker build`** = make the packed box (image). Your API is **not** answering browsers yet.  
- **`docker run`** = open the box and start using it (container). Now the API is **actually running**.

In Exercise 4 you ran the API with uvicorn **on your laptop** (Python + packages installed locally).  
In this exercise the **same** API runs **inside Docker**. Your browser still opens `http://localhost:8000/docs`, but the work happens in the container — another computer would not need to install Python or scikit-learn to run it, only Docker.


**Before you start:** if the uvicorn server from Exercise 4 is still running, press **Ctrl+C** in that terminal — otherwise port 8000 is already taken and the container cannot use it.

**Steps:**
1. Run with a port mapping and a name (`-p 8000:8000 --name rain`).
2. Confirm it is up with `docker ps`.
3. Test both endpoints in your browser via `/docs`.
4. View the logs.

<details><summary>▶ Solution</summary>

**This exercise produces:** a container named `rain` serving your model on `http://localhost:8000`.

#### Step 1 — Run with a port mapping and a name

**Hint:** if uvicorn from Exercise 4 is still running, press **Ctrl+C** there first, or port 8000 is taken.

**Hint — command meaning:**
- `-d` = **detached** = run the container **in the background**.  
  - **With `-d` (what we use here):** the container starts, then your terminal prompt comes back, so you can type `docker ps`, open `/docs`, etc. The API keeps running behind the scenes.  
  - **Without `-d`:** the terminal stays attached to the container (you see live logs and no prompt). The API still runs, but you cannot easily type the next commands in that same window until you press Ctrl+C — and Ctrl+C would **stop** the container.  
  - So for this exercise: **yes, use `-d`** so you can test the API in your browser while the container keeps running.
- `-p 8000:8000` = laptop port 8000 → container port 8000
- `--name rain` = container name
- `rain-api:v1` = the image to start


**Command (type this):**

```bash
docker run -d -p 8000:8000 --name rain rain-api:v1
```

**Expected result:** Docker prints a long container ID and gives your prompt straight back — that is what `-d` does.

**If it fails:**
- `port is already allocated` → stop the old process, or use `-p 8001:8000` and use `http://localhost:8001/docs` in Step 3.
- name already in use → `docker rm -f rain`, then run again.

#### Step 2 — Confirm it is up

**Command (type this):**

```bash
docker ps
```

**Output (do not type):**

```text
CONTAINER ID   IMAGE         STATUS         PORTS                    NAMES
8f2ac1b30d5e   rain-api:v1   Up 4 seconds   0.0.0.0:8000->8000/tcp   rain
```

**Expected result:** status `Up ...`.

**If it fails:** status `Exited` means the app crashed. Run `docker logs rain`; if it says `FileNotFoundError: model/rf.joblib`, the model was not in the image — retrain, rebuild, run again.

#### Step 3 — Test both endpoints via `/docs`

Open **`http://localhost:8000/docs`** in your browser and use it exactly as in Exercise 4: `GET /health` → *Try it out* → *Execute*, then `POST /predict` with this body.

**File content (paste into the Swagger request body):**

```json
{"humidity": 92, "temperature": 18, "pressure": 995, "wind_speed": 25}
```

**Output (do not type):**

```text
{"will_rain":true,"prob_rain":0.98}
```

**Command (optional — same call with curl in Git Bash):**

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"humidity":92,"temperature":18,"pressure":995,"wind_speed":25}'
```

**Hint — curl flags:** `-X POST` = send a POST request · `-H` = set a header · `-d` = the JSON body.

**Important (Windows / Git Bash):**
1. Use **`127.0.0.1`**, not `localhost`. On some Windows machines `localhost` goes via IPv6 and curl sits there with **no output**.
2. Put the JSON in **single quotes** as shown (`'{"humidity":...}'`). Do **not** use `\"...\"` — that often breaks the body.
3. If curl still fails, use `/docs` in the browser — that is the recommended test for this lab.

#### Step 4 — View the logs

**Command (type this):**

```bash
docker logs rain
```

**Output (do not type):**

```text
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     172.17.0.1:52350 - "POST /predict HTTP/1.1" 200 OK
```

**Expected result:** you see the request you just made in Step 3 recorded as `200 OK`.

**Why:** `-p 8000:8000` forwards your laptop’s port 8000 into the container’s port 8000 — that is how browser/`curl` traffic reaches the app. The log line `Uvicorn running on http://0.0.0.0:8000` shows the app is listening on all interfaces inside the container (from `--host 0.0.0.0` in your Dockerfile), so that forwarded traffic can actually be accepted.
</details>

### Exercise 9 — Debug from inside the container

**Goal:** learn the two commands that solve most container problems.
**Task:** follow the logs, open a shell inside, then clean up.

**What are `logs` and `exec` for?**  
- `docker logs` = read what the app **printed** (startup messages, errors, each request). First thing to check when a container misbehaves.  
- `docker exec -it <name> bash` = open a terminal **inside** the running container, so you can check which files actually made it into the image.

**Why this exercise?**  
A container is a black box until you know these two commands. You used them on Nginx in Exercise 2; now you use them on your own API, which is what you will do every time a deployment does not work.

**Steps:**
1. Follow the logs live (`-f`).
2. Open a shell inside and look at the files.
3. Stop and remove the container, then run `docker ps` to confirm it is gone (and remember: code changes need a rebuild).

<details><summary>▶ Solution</summary>

**This exercise produces:** no new files — it teaches the two commands you will reach for whenever a container misbehaves.

#### Step 1 — Follow the logs live

**Hint — command meaning:** `docker logs -f rain` = follow the logs live (`-f` = follow). **Ctrl+C** stops following but leaves the container running.

**Command (type this):**

```bash
docker logs -f rain
```

**Expected result:** the log lines appear and the prompt does not come back. Reload `http://localhost:8000/docs` in your browser and watch new lines arrive. Press **Ctrl+C** to stop following.

#### Step 2 — Open a shell inside and look at the files

**Command (type this):**

```bash
docker exec -it rain bash
```

**Command (type these three lines inside the container):**

```bash
pwd
ls
exit
```

**Output (do not type):**

```text
/app
app.py  model  requirements.txt
```

**Hint:** notice `train.py` is **not** there — the Dockerfile never copied it. The image contains only what you asked for, which is what you want in production.

**If it fails:** `bash` missing → use `docker exec -it rain sh`.

#### Step 3 — Stop and remove the container

**Command (type this):**

```bash
docker stop rain && docker rm rain
```

**Command (type this next — check it is gone):**

```bash
docker ps
```

**Expected result:** `rain` is **not** in the list (running containers only). Port 8000 is free again.

**Optional check:** `docker ps -a` also shows stopped containers. After a successful `rm`, `rain` should not appear there either.

**Why `stop` then `rm`?**  
`docker stop` shuts the process down; `docker rm` deletes the container. Until you `rm`, the old container still exists (you would see it with `docker ps -a`), and the name `rain` stays taken.

---

**Important — when you change the app, rebuild the image**

Editing `app.py` (or the Dockerfile, or retraining the model) does **not** update a container that is already running. A container is a frozen copy of an **image**. To pick up your changes you must:

1. Stop and remove the old container: `docker stop rain && docker rm rain`
2. **Rebuild the image:** `docker build -t rain-api:v1 .`
3. **Run a new container** from that new image: `docker run -d --name rain -p 8000:8000 rain-api:v1`

**Why:** `docker run` starts from the image that already exists. If you skip `docker build`, you keep serving yesterday’s code even though your laptop files look updated.

---

**Why this exercise?**  
`docker logs` tells you what the app *said*; `docker exec` lets you walk around inside the running environment. Together they turn a container from a black box into something you can debug.
</details>

**Checkpoint:** you built an image, ran it, called it from your browser, read its logs and got a shell inside it.

---

### Exercise 10 — Share your image with a classmate

**Goal:** give someone else your working API **without** asking them to install Python or retrain the model.
**Task:** try **one** sharing path below (file share **or** online registry). Both end the same way: your friend runs one `docker run` and opens `/docs`.

**What are you sharing?**  
Not the source folder — the **image**. The image already holds Python, packages, `app.py`, and the trained model. That is the whole point of Docker.

**Why this exercise?**  
Right now `rain-api:v1` lives only on your laptop. Sharing the image is how a classmate, a marker, or a server gets the **exact** thing you tested.

**Two easy paths (pick one):**

| Path | Best when… | You need… |
|---|---|---|
| **A — File** (`docker save` / `docker load`) | USB stick, OneDrive, email, lab PCs with no login | Nothing online |
| **B — Online** (Docker Hub **or** GHCR) | Your friend is on another network | A free account + login |

**What is a registry? What is GHCR?**  
A **registry** is an online store for Docker images. You `push` an image up; anyone with access can `pull` it down and run it.

| Registry | Full name | Who runs it | Image address looks like… |
|---|---|---|---|
| **Docker Hub** | Docker Hub | Docker | `your-name/rain-api:v1` |
| **GHCR** | **G**it**H**ub **C**ontainer **R**egistry | GitHub | `ghcr.io/your-name/rain-api:v1` |

Same job as Docker Hub — store and share images — but GHCR lives on **GitHub** (you find published images under your profile → **Packages**). Use Docker Hub if you want the simplest login; use GHCR if you already use GitHub (Week 5) and want the image next to your repo.

**Steps:**
1. Confirm the image still exists on your machine.
2. Share it with Path A **or** Path B.
3. Your friend loads/pulls it and runs the container.

<details><summary>▶ Solution</summary>

**This exercise produces:** a shareable copy of `rain-api:v1` (a `.tar` file, or a copy on Docker Hub / GHCR) that a friend can run with Docker alone.

**Hint:** Exercise 9 removed the **container** named `rain`, but the **image** `rain-api:v1` is still on your laptop. Check with `docker images`. If it is missing, rebuild first: `docker build -t rain-api:v1 .` from `rain-api/`.

#### Step 1 — Confirm the image exists

**Command (type this):**

```bash
docker images
```

**Expected result:** a row for `rain-api` with tag `v1`.

---

#### Path A — Share as a file (USB / OneDrive / email)

**You (export the image):**

**Hint — command meaning:** `docker save` writes the whole image into one archive file. `-o` = output file name.

**Command (type this — from any folder):**

```bash
docker save -o rain-api-v1.tar rain-api:v1
```

**Expected result:** a file `rain-api-v1.tar` appears (often a few hundred MB). Send that file to your friend (USB, OneDrive, etc.).

**Your friend (import and run):**

They need Docker Desktop installed and running. Then:

**Command (friend types these):**

```bash
docker load -i rain-api-v1.tar
docker run -d --name rain -p 8000:8000 rain-api:v1
```

**Expected result:** `docker load` prints `Loaded image: rain-api:v1`. Then open **`http://127.0.0.1:8000/docs`** and try `/predict`.

**Why Path A?** No account, no internet push — just a file. Good for class when everyone is offline or blocked from registries.

---

#### Path B — Publish online (Docker Hub *or* GHCR)

Pick **one** registry (see the table above). **Docker Hub** is usually simplest for beginners. **GHCR** is GitHub’s image store — same idea, different website and login (`ghcr.io` + a GitHub token).

##### B1 — Docker Hub (simple)

1. Create a free account at [https://hub.docker.com](https://hub.docker.com).
2. Log in from the terminal.

**Command (type this):**

```bash
docker login
```

**Expected result:** `Login Succeeded` (enter your Docker Hub username and password/token when asked).

3. Tag the image with **your** Docker Hub username, then push.

**Hint:** replace `your-dockerhub-username` with your real username (usually lowercase).

**Command (type this pattern):**

```bash
docker tag rain-api:v1 your-dockerhub-username/rain-api:v1
docker push your-dockerhub-username/rain-api:v1
```

**Expected result:** layers upload. The image appears on your Docker Hub profile under **Repositories**.

**Your friend (download and run):**

**Command (friend types these — use *your* username):**

```bash
docker pull your-dockerhub-username/rain-api:v1
docker run -d --name rain -p 8000:8000 your-dockerhub-username/rain-api:v1
```

Then they open **`http://127.0.0.1:8000/docs`**.

**If it fails:** `denied` / `unauthorized` → not logged in, or the repo is private (make it **Public** on Docker Hub for a classmate to pull without login).

##### B2 — GitHub Container Registry (GHCR)

**Reminder:** GHCR = GitHub’s place to host Docker images. You push to `ghcr.io/...`; the package shows up on GitHub under **Packages**. Your friend does not clone your repo — they only `docker pull` the image.

**You:**

1. Create a GitHub **Personal access token (classic)** with **`write:packages`** (Settings → Developer settings → Personal access tokens). Never commit the token.
2. Log in, tag, push (replace `your-username` with your GitHub username in **lowercase**):

```bash
export TOKEN=ghp_your_token_here
echo $TOKEN | docker login ghcr.io -u your-username --password-stdin
docker tag rain-api:v1 ghcr.io/your-username/rain-api:v1
docker push ghcr.io/your-username/rain-api:v1
```

3. On GitHub: open the package → **Package settings** → set visibility to **Public** if your friend should pull without a token.

**Your friend:**

```bash
docker pull ghcr.io/your-username/rain-api:v1
docker run -d --name rain -p 8000:8000 ghcr.io/your-username/rain-api:v1
```

Then **`http://127.0.0.1:8000/docs`**.

**Hint:** more GHCR detail (and common errors) is also in **Exercise 14 · BONUS** later.

---

**Why share the image, not the folder?**  
Your friend would otherwise need Python, the right packages, and your model file. With the image they only need Docker — that is the “it works on my machine” fix from the start of this lab.
</details>

**Checkpoint:** you can hand a classmate a running rain API using either a `.tar` file or a registry pull.

**The core lab ends here (Exercises 1–10).** Parts 5–6 below are optional extras.

<div class="home-optional" markdown="1">

**Optional — try at home**  
Exercises **11–14** (`.dockerignore`, multi-stage build, Compose, GHCR) are **not required in class**. Skip them for now if you are out of time. You can come back and try them at home when you want to go further — nothing in the concept check depends on finishing them today.

</div>

---

## Part 5 · Optimise the image *(optional · ≈ 15 min at home)*

### Exercise 11 — Add a `.dockerignore`

**Goal:** keep junk and secrets out of the build.
**Task:** create `.dockerignore` in `rain-api/`, then rebuild.

**What is `.dockerignore`?**  
The same idea as `.gitignore` from Week 5, but for builds: a list of files Docker must **not** send into the build. Anything listed can never end up inside your image.

**Why this exercise?**  
Without it, `docker build` ships your whole folder — `.git`, notebooks, datasets, even a `.env` full of secrets. That makes builds slow, images fat, and secrets leakable to anyone who pulls the image.

**Steps:**
1. Create the file (the name starts with a dot).
2. Paste the list and rebuild.

<details><summary>▶ Solution</summary>

**This exercise produces:** `.dockerignore` (name starts with a dot), which keeps junk and secrets out of every future build.

#### Step 1 — Create the file (name starts with a dot)

**Command (type this — `ls -a` shows dot-files):**

```bash
touch .dockerignore
ls -a
```

**Expected result:** `ls -a` lists `.dockerignore`. Plain `ls` will not show it, because names starting with a dot are hidden.

#### Step 2 — Paste the list and rebuild

Open `.dockerignore`, paste the **File content** below, and **Save**.

**File content (`rain-api/.dockerignore`):**

```text
# python
__pycache__
*.pyc
.venv

# dev/git noise
.git
.vscode
*.md

# data & notebooks
data/
*.csv
*.ipynb

# secrets — never copy these into an image
.env
*.pem
```

Then rebuild so the new rules take effect.

**Command (type this):**

```bash
docker build -t rain-api:v1 .
```

**Expected result:** the build finishes as before. The first line, `transferring context`, should report a **smaller** size than in Exercise 6, because the ignored files were never sent.

**Why:** it works like `.gitignore` from Week 5 — matching files are never sent to Docker, so they can never end up inside your image. Three reasons this matters: **security** (a stray `.env` baked into a layer can be extracted by anyone who pulls the image, and deleting it in a later layer does not remove it), **speed** (Docker sends the whole context before building, so a big `data/` folder slows every build), and **size**.
</details>

### Exercise 12 — Multi-stage build · **BONUS**

*Optional — skip it and keep using `rain-api:v1`. Nothing later depends on this.*

**Goal:** build a **smaller runtime image** that still runs the API, but does **not** carry the heavy build tooling.
**Task:** rewrite the Dockerfile with two stages, build as `rain-api:v2`, compare sizes with `v1`.

**What is a multi-stage build?**  
One Dockerfile with **two `FROM` lines** (two stages):

| Stage | Nickname | Job | Kept in the final image? |
|---|---|---|---|
| 1 | `builder` | Install / compile packages (needs compilers and build tools) | **No** — thrown away after the build |
| 2 | runtime | Run the API (needs Python + the finished packages + your code + model) | **Yes** — this is what you ship |

Stage 2 **copies only the finished result** from stage 1 (here: pre-built package wheels), then installs those into the slim image and copies `app.py` and `model/`.

**Important — what you remove vs what you keep**

- You are **not** deleting the libraries the app needs to run (FastAPI, scikit-learn, etc.). Those still get installed into stage 2.
- You **are** deleting the *build workshop*: compilers, temporary build files, and the fat builder image. They helped *create* the packages; they are not needed to *run* them.
- If the final image were missing a **runtime** library, that would be a broken Dockerfile (you forgot to copy/install something) — not the goal of multi-stage.

**Why this exercise?**  
Smaller images pull faster and contain less extra software that could carry a vulnerability. This is the usual pattern for production Dockerfiles: build in a heavy stage, ship a slim stage.

**Steps:**
1. Keep a backup of your current Dockerfile.
2. Replace the Dockerfile with the two-stage version.
3. Build it as `rain-api:v2` and compare the sizes in `docker images`.

<details><summary>▶ Solution</summary>

**This exercise produces:** a second image, `rain-api:v2`, smaller than `v1`, that still answers `/health` and `/predict` the same way.

#### Step 1 — Keep a backup of your current Dockerfile

**Hint:** the next step replaces your whole Dockerfile, so save the working one first. `cp` = copy.

**Command (type this — in `rain-api/`):**

```bash
cp Dockerfile Dockerfile.single
```

**Expected result:** `ls` shows both `Dockerfile` and `Dockerfile.single`. To go back later: `cp Dockerfile.single Dockerfile`.

#### Step 2 — Replace the Dockerfile with the two-stage version

Open `Dockerfile`, select all, paste the **File content** below, and **Save**.

**File content (replace everything in `rain-api/Dockerfile`):**

```dockerfile
# ---- stage 1: builder (tools stay here and are discarded) ----
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- stage 2: runtime (only what is needed to run) ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index /wheels/*
COPY app.py .
COPY model/ ./model/
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Hint — how the libraries still arrive in stage 2:**
- `FROM python:3.11 AS builder` = fat image with compilers; nickname `builder`
- `pip wheel --wheel-dir /wheels ...` = build every package into finished `.whl` files (still in stage 1)
- `COPY --from=builder /wheels /wheels` = copy **only those wheels** into the slim stage (not the compilers)
- `pip install --no-index /wheels/*` = install the real libraries into stage 2 from those wheels
- `COPY app.py` and `COPY model/` = your code and trained model (runtime files)

So stage 2 ends up with: slim Python + installed packages + app + model. It does **not** keep the builder’s compilers.

#### Step 3 — Build it as `rain-api:v2` and compare the sizes

**Hint:** `-t rain-api:v2` gives it a **new tag**, so `v1` stays on disk and you can compare the two.

**Command (type this):**

```bash
docker build -t rain-api:v2 .
docker images
```

**Output (do not type — example):**

```text
rain-api   v2   ...   190MB
rain-api   v1   ...   285MB
```

**Expected result:** both tags are listed, and the `v2` row has the smaller SIZE.

**Optional check — it still runs:**

```bash
docker rm -f rain || true
docker run -d --name rain -p 8000:8000 rain-api:v2
```

Open **`http://127.0.0.1:8000/docs`** and try `/health` and `/predict`. Same API as `v1` — just a smaller image.

**Why:** stage 1 needs compilers; stage 2 only needs to run the app. The **runtime libraries are installed into stage 2**; only the **build tooling** is thrown away with the builder stage.
</details>

---

## Part 6 · Ship the image *(optional · ≈ 20 min at home)*

### Exercise 13 — Run it with Docker Compose

**Goal:** start and stop the service with one short command.
**Task:** create `docker-compose.yml` in `rain-api/` and use it.

**What is Docker Compose?**  
A tool that reads a small YAML file describing your containers, so you write the settings down **once** instead of retyping a long `docker run` line. `docker compose up -d` starts everything in the file; `docker compose down` stops and removes it.

**Why this exercise?**  
Your run command becomes a file you can commit and review. And when a project grows to an API **plus** a database, the same one command starts both, already networked together.

**Steps:**
1. Remove any leftover `rain` container (it would hold port 8000).
2. Create the file.
3. Start with Compose, test in your browser, shut down.

<details><summary>▶ Solution</summary>

**This exercise produces:** `docker-compose.yml`, which replaces the long `docker run` line with `docker compose up -d`.

#### Step 1 — Remove any leftover `rain` container

**Hint:** `docker rm -f rain` force-removes it; `|| true` means "carry on even if there was nothing to remove".

**Command (type this — clear anything holding port 8000):**

```bash
docker rm -f rain || true
```

**Expected result:** either the name `rain` is printed, or an "No such container" message you can ignore. Port 8000 is now free.

#### Step 2 — Create the file

**Command (type this — in `rain-api/`):**

```bash
touch docker-compose.yml
```

Open `docker-compose.yml`, paste the **File content** below, and **Save**.

**File content (`rain-api/docker-compose.yml`):**

```yaml
services:
  api:
    build: .
    image: rain-api:v1
    ports:
      - "8000:8000"
    restart: unless-stopped
```

**Hint — plain English:**
- `services:` = the containers Compose manages; ours has one, called `api`
- `build: .` = build from the Dockerfile in this folder
- `ports: - "8000:8000"` = the same idea as `-p 8000:8000`
- `restart: unless-stopped` = restart automatically if the app crashes
- YAML is indentation-sensitive: **spaces, never tabs**

#### Step 3 — Start with Compose, test, shut down

**Hint — command meaning:** `docker compose up -d` = build if needed, then start everything in the file, detached · `docker compose ps` = show the services · `docker compose down` = stop **and** remove them.

**Command (type this — start it):**

```bash
docker compose up -d
docker compose ps
```

**Expected result:** the `api` service shows `Up`.

Now test it: open **`http://127.0.0.1:8000/docs`** and call `/health` and `/predict` — exactly as in Exercise 8. Same API, shorter command.

**Command (type this when finished — shut down):**

```bash
docker compose down
```

**Expected result:** Compose reports the container and network removed, and `docker ps` no longer shows the service.

**If it fails:**
- `'compose' is not a docker command` → old Docker; try `docker-compose up -d` or update Docker Desktop.
- `did not find expected key` → an indentation problem. Re-paste the file, check for tabs.

**Why:** the long `docker run -d -p 8000:8000 --name rain rain-api:v1` is now written down, version-controlled and reviewable. When your project grows to an API plus a database, `docker compose up -d` starts both, already networked together.
</details>

### Exercise 14 — Push to a registry · **BONUS**

*Optional — needs a GitHub account and a token. Skip it freely. If you already pushed with Path B2 in Exercise 10, treat this as extra practice.*

**Goal:** publish your image so another machine can pull and run it.
**Task:** tag and push to the GitHub Container Registry (GHCR).

**What is a registry, and what is GHCR?**  
A **registry** is an online store for images — Docker Hub is the one you already pulled `hello-world` and `nginx` from. You `push` an image up, and any machine can `pull` it down and run it. **GHCR** is GitHub's registry, so your image lives beside your repo.

**Why this exercise?**  
Right now your image exists only on your laptop. Pushing it is how a server, a teammate or a GitHub Actions pipeline gets exactly the artefact you tested.

**Steps:**
1. Create a GitHub token and log in to GHCR.
2. Tag your image with the GHCR address.
3. Push it and check it under **Packages** on GitHub.

<details><summary>▶ Solution</summary>

**This exercise produces:** a copy of your image hosted on GitHub that anyone (or any server) can `docker pull`.

**Hint:** in every command below, replace `your-username` with your GitHub username in **lowercase** — GHCR rejects capitals.

#### Step 1 — Create a GitHub token and log in to GHCR

Create a token at **Settings → Developer settings → Personal access tokens (classic)** with the **`write:packages`** scope. Never commit a token.

**Hint — command meaning:** `--password-stdin` = feed the token through a pipe so it never appears in your shell history.

**Command (type this pattern):**

```bash
export TOKEN=ghp_your_token_here
echo $TOKEN | docker login ghcr.io -u your-username --password-stdin
```

**Expected result:** `Login Succeeded`.

**If it fails:** `unauthorized` → the token was copied incompletely, or it has expired.

#### Step 2 — Tag your image with the GHCR address

**Hint:** `docker tag` does not copy anything — it gives the **same** image a second name, and that name tells Docker where to push it.

**Command (type this pattern):**

```bash
docker tag rain-api:v1 ghcr.io/your-username/rain-api:v1
```

**Expected result:** `docker images` now lists `ghcr.io/your-username/rain-api` alongside `rain-api`, both with the same IMAGE ID.

#### Step 3 — Push it and check it on GitHub

**Command (type this pattern):**

```bash
docker push ghcr.io/your-username/rain-api:v1
```

**Expected result:** the layers upload, and the package appears under **Packages** on your GitHub profile.

**If it fails:** `denied: permission_denied` → the token lacks `write:packages`, or your username has a capital letter.

**Why:** this closes the loop with Week 5. GitHub Actions can build and push this image on every merge to `main`, and a server can `docker pull` exactly the artefact that was tested. That is continuous delivery in one sentence.
</details>

**Checkpoint:** you can describe a service in `docker-compose.yml` and start it with one command.

---

## Concept check

Answer in one line, then check.

1. What is the difference between an image and a container?
2. Your container is up, but `http://localhost:8000/health` is refused. Name **two** likely causes.
3. You changed one line in `app.py` and the build reinstalled every package. What is wrong with your Dockerfile?
4. Why should you never copy `.env` into an image?
5. What does `docker exec -it <name> bash` do, and when would you use it?

<details><summary>▶ Answers</summary>

1. An **image** is a frozen blueprint; a **container** is a running or stopped instance of it. Image ≈ class, container ≈ object.
2. Either you forgot `-p 8000:8000`, or the app bound to `127.0.0.1` instead of `0.0.0.0` inside the container. A third option: it crashed — check `docker ps` and `docker logs`.
3. The code was copied **before** `pip install`, so any code change invalidates that layer and everything after it. Copy `requirements.txt` and install first, then copy the code.
4. Secrets baked into a layer can be extracted by anyone who pulls the image, and deleting the file in a later layer does not remove it from the earlier one. Use runtime environment variables, and list `.env` in `.dockerignore`.
5. Opens a shell inside a **running** container — use it to check which files actually made it in, and to inspect the environment when the logs are not enough.
</details>

---

## Capstone challenge *(optional, ~20 min)*

Containerise a different small ML app of your own, from scratch:

1. `train.py` plus a pinned `requirements.txt`.
2. `app.py` with `/health` and `/predict`.
3. A cache-friendly `Dockerfile`: `-slim` base, dependencies before code, `--host 0.0.0.0`.
4. A `.dockerignore` and a `docker-compose.yml`.
5. **Bonus:** a multi-stage build with the sizes compared, and a push to GHCR.

You have now built and shipped a real ML service the same way production teams do — and this is the workflow your **Final Project** can follow.

---

*DSTS 11523 · University of Canberra · Dr Ibrahim Radwan — Docker commands use standard syntax (Docker Desktop 4.x / Docker Engine 24+); the Python flow was run end to end with FastAPI 0.115 and scikit-learn.*
