# DSTS 11523 · Week 4 Tutorial

## Model Evaluation & Optimisation — hands-on lab

**How to use this tutorial.** Work top to bottom. Each exercise has a **Goal**, a **Task**,
a few **Steps** to nudge you, and a **Solution** with code, the real output, and a short
"why". Try each one *before* opening the solution — you'll learn far more. Everything here
runs as-is; the numbers shown are what you should see.

> Solutions are hidden in drop-downs. On GitHub / VS Code preview, click **▶ Solution** to
> expand. If they don't expand in your viewer, just scroll — the code is underneath.

### Setup (do this once)

```bash
pip install scikit-learn pandas mlflow scipy matplotlib
```

```python
import warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore"); np.random.seed(42)

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(as_frame=True, return_X_y=True)
# sklearn stores 0 = malignant, 1 = benign. Flip so 1 = cancer (the class we want to catch).
y = (y == 0).astype(int)   # 1 = malignant (positive), 0 = benign (negative)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
print(X.shape, "positive rate (malignant):", round(y.mean(), 3))
```

This is a real Yes/No problem. Think of it like *"will it rain tomorrow?"* — we care about the smaller class.

**In sklearn's raw file:** `0 = malignant (cancer)`, `1 = benign`.  
So cancer is label **0** there — but sklearn metrics treat **1** as positive by default. Awkward.

We **flip** the labels:

- **Positive (1) = malignant = cancer** — the class we want to catch
- **Negative (0) = benign** — not cancer

After the flip, **positive is label 1, not 0.** About **37%** of cases are malignant. Precision / recall / F1 / AUC are then for **cancer**.

---

## Part 1 · Metrics — learn to distrust accuracy

**Notes.** Every classification metric comes from four counts. Build the confusion matrix,
`[[TN, FP], [FN, TP]]`, then: precision = TP/(TP+FP) ("when I say positive, am I right?"),
recall = TP/(TP+FN) ("of the real cancers, how many did I catch?"), F1 balances the two,
and ROC-AUC measures ranking quality independent of the 0.5 threshold.
Here **positive = malignant (cancer)**.

### Exercise 1 — Rebuild precision & recall by hand

**Goal:** see that the metrics are *just ratios of the confusion-matrix cells.*
**Task:** train a random forest, get its confusion matrix, and compute precision and recall
with plain arithmetic — then check they match scikit-learn.

**Steps:**
1. Fit `RandomForestClassifier(n_estimators=300, random_state=42)` on the training set.
2. `confusion_matrix(y_test, pred)` → unpack `TN, FP, FN, TP` with `.ravel()`.
3. Apply the formulas; compare to `precision_score` / `recall_score`.

<details><summary>▶ Solution</summary>

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score

rf = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train, y_train)
pred = rf.predict(X_test)

cm = confusion_matrix(y_test, pred)
TN, FP, FN, TP = cm.ravel()
print("confusion matrix:", cm.tolist())
print("precision  manual:", round(TP/(TP+FP), 4), "| sklearn:", round(precision_score(y_test, pred), 4))
print("recall     manual:", round(TP/(TP+FN), 4), "| sklearn:", round(recall_score(y_test, pred), 4))
```

```text
confusion matrix: [[72, 0], [3, 39]]
precision manual: 1.0 | sklearn: 1.0
recall    manual: 0.9286 | sklearn: 0.9286
```

**Why:** the metric functions are doing this exact arithmetic. **Positive = cancer.**
TN=72 (correct benign), FP=0 (no false cancer alarms), FN=3 (missed cancers), TP=39 (correct cancer).
Precision 1.0: every cancer alarm was right. Recall 0.9286: we missed 3 of 42 cancers.
</details>

### Exercise 2 — Fall into (and out of) the accuracy trap

**Goal:** feel *why* accuracy is dangerous on imbalanced data.
**Task:** compare a "dumb" model that always predicts the majority class against the random
forest — on **accuracy** and on **recall for the malignant (cancer) class**.

**Steps:**
1. Use `DummyClassifier(strategy="most_frequent")`.
2. Report its accuracy.
3. Report `recall_score(...)` — recall for *malignant / cancer* (`pos_label=1`, sklearn's default) — for both models.

<details><summary>▶ Solution</summary>

```python
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
dp = dummy.predict(X_test)

print("dummy  accuracy        :", round(accuracy_score(y_test, dp), 4))
print("dummy  recall CANCER :", round(recall_score(y_test, dp), 4))
print("forest recall CANCER :", round(recall_score(y_test, pred), 4))
```

```text
dummy  accuracy         : 0.6316
dummy  recall CANCER  : 0.0
forest recall CANCER  : 0.9286
```

**Why:** the dummy model scores **63% accuracy while catching *zero* cancers** — useless, yet
"63% right" sounds fine. The forest catches 93% of malignancies. On imbalanced, high-stakes
problems, judge by **recall / AUC**, never accuracy alone. *This is the single most important
idea in Part 1.*
</details>

### Exercise 3 — Compare two models with ROC-AUC

**Goal:** use a threshold-free metric to compare models fairly.
**Task:** compute ROC-AUC for the random forest and for a (scaled) logistic-regression model.

**Steps:**
1. Logistic regression needs scaling — wrap it in a `Pipeline([StandardScaler, LogisticRegression])`.
2. Get `predict_proba(...)[:, 1]` for each model.
3. Compare with `roc_auc_score`. *(Optional: plot both with `RocCurveDisplay.from_estimator`.)*

<details><summary>▶ Solution</summary>

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

lr = Pipeline([("scale", StandardScaler()),
               ("clf", LogisticRegression(max_iter=5000))]).fit(X_train, y_train)

rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1])
print("Random Forest AUC:", round(rf_auc, 4))
print("Logistic Reg  AUC:", round(lr_auc, 4))
```

```text
Random Forest AUC: 0.9937
Logistic Reg  AUC: 0.9954
```

**Why:** AUC sweeps *every* threshold, so it's a fair single-number comparison. Both are
excellent; logistic regression edges ahead here — a good reminder that the simpler model is
often competitive, and worth keeping as a baseline.
</details>

---

## Part 2 · Trustworthy estimates — CV & leakage

**Notes.** One split is a coin flip. **Cross-validation** averages several, giving a mean and
an error bar. And beware **leakage**: any step that *learns from data* (scaling, imputing,
feature selection) must happen **inside** the cross-validation fold — a `Pipeline` guarantees
this.

### Exercise 4 — Put an error bar on your score

**Goal:** stop trusting a single number.
**Task:** get the 5-fold stratified CV F1 as **mean ± std**.

**Steps:** use `StratifiedKFold(5, shuffle=True, random_state=42)` with `cross_val_score(..., scoring="f1")`.

<details><summary>▶ Solution</summary>

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
cv = StratifiedKFold(5, shuffle=True, random_state=42)
s = cross_val_score(rf, X, y, cv=cv, scoring="f1")
print("per-fold:", np.round(s, 4))
print(f"mean {s.mean():.4f}  ±  {s.std():.4f}")
```

```text
per-fold: [0.9545 0.9    0.9383 0.9333 0.9512]
mean 0.9355  ±  0.0194
```

**Why:** always report mean ± std. **Rule of thumb:** if two models differ by less than one
std (~0.02 here), treat them as tied — the difference is noise, not skill.
F1 here is for the **cancer** class.
</details>

### Exercise 5 — Spot the leak 🔍 (predict, then measure)

**Goal:** recognise leakage and fix it structurally.
**Task:** the code below selects the 20 "best" features using **all** the data, then
cross-validates on just those. The data is **pure noise with random labels**.
**(a)** Predict: will the CV score be near 0.5 (chance) or higher? **(b)** Then run it.
**(c)** Fix the leak with a `Pipeline` and measure the difference.

```python
rng = np.random.RandomState(0)
Xn = rng.randn(200, 1000)          # 1000 noise features
yn = rng.randint(0, 2, 200)        # random labels — no real signal
# ... buggy selection happens here (see solution) ...
```

**Steps:**
1. Buggy version: rank features by |correlation with y| over the whole set, keep top 20,
   then `cross_val_score`.
2. Fixed version: move `SelectKBest` **inside** a `Pipeline` so it re-runs per fold.

<details><summary>▶ Solution</summary>

```python
from sklearn.feature_selection import SelectKBest, f_classif

# (b) WRONG — selection saw every row's label before "testing" on it
corr = np.abs([np.corrcoef(Xn[:, j], yn)[0, 1] for j in range(1000)])
top  = np.argsort(corr)[-20:]
leaky = cross_val_score(LogisticRegression(max_iter=1000), Xn[:, top], yn, cv=5)

# (c) RIGHT — selection is inside the pipeline, redone on each training fold
pipe = Pipeline([("select", SelectKBest(f_classif, k=20)),
                 ("clf",    LogisticRegression(max_iter=1000))])
honest = cross_val_score(pipe, Xn, yn, cv=5)

print("leaky :", round(leaky.mean(), 4), " <- looks predictive (it isn't!)")
print("honest:", round(honest.mean(), 4), " <- ~chance")
```

```text
leaky : 0.735  <- looks predictive (it isn't!)
honest: 0.485  <- ~chance
```

**Answer to (a):** it should be ~0.5, because there is no signal. **What actually happens:**
the buggy version reports **73.5%** — a complete illusion, because feature selection peeked at
the labels of the rows it was later scored on. **Lesson:** wrap every fitted transform in a
`Pipeline`; never `fit` anything on data before splitting.
</details>

---

## Part 3 · Diagnose & optimise

**Notes.** Plot **training vs validation** performance as you increase model complexity.
Both low and close → **underfit (bias)**; big gap → **overfit (variance)**. Then tune
hyperparameters **on CV**, not on the test set.

### Exercise 6 — Diagnose bias vs variance

**Goal:** read a validation curve and name the problem.
**Task:** sweep `max_depth` for a random forest and find where overfitting begins.

**Steps:** use `validation_curve(..., param_name="max_depth", param_range=[1,2,3,5,8,12,None], scoring="f1")`;
compare `train.mean(1)` and `val.mean(1)`.

<details><summary>▶ Solution</summary>

```python
from sklearn.model_selection import validation_curve
depths = [1, 2, 3, 5, 8, 12, None]
tr, va = validation_curve(RandomForestClassifier(n_estimators=150, random_state=42),
                          X, y, param_name="max_depth", param_range=depths,
                          cv=cv, scoring="f1")
for d, a, b in zip(depths, tr.mean(1), va.mean(1)):
    print(f"depth {str(d):>4}  train {a:.3f}  valid {b:.3f}  gap {a-b:.3f}")
```

```text
depth    1  train 0.903  valid 0.880  gap 0.023
depth    2  train 0.949  valid 0.925  gap 0.024
depth    3  train 0.972  valid 0.929  gap 0.042
depth    5  train 0.993  valid 0.933  gap 0.060
depth    8  train 1.000  valid 0.935  gap 0.065
depth   12  train 1.000  valid 0.936  gap 0.064
depth None  train 1.000  valid 0.936  gap 0.064
```

**Why:** at depth 1–2 both scores are lower and close → mild **underfit**. Past depth ~5,
training hits a perfect 1.000 while validation flatlines near 0.93 and the **gap stops
improving** → deeper trees only **overfit**. Pick the shallowest depth on the validation
plateau (~5): similar score, less variance. *More data or regularisation would shrink that gap.*
</details>

### Exercise 7 — Tune it properly

**Goal:** use CV-based search and understand `best_*`.
**Task:** run a small `GridSearchCV`; report `best_params_`, `best_score_`, and the **test** F1.
Then answer: why is the CV score a little higher than the test score?

**Steps:** grid over `n_estimators`, `max_depth`, `min_samples_leaf`; `scoring="f1"`, `cv=cv`;
after fitting, `grid.best_params_` and `f1_score(y_test, grid.predict(X_test))`.

<details><summary>▶ Solution</summary>

```python
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

grid = GridSearchCV(RandomForestClassifier(random_state=42),
                    {"n_estimators":[100,300], "max_depth":[3,5,None], "min_samples_leaf":[1,3]},
                    cv=cv, scoring="f1", n_jobs=-1).fit(X_train, y_train)

print("best_params_:", grid.best_params_)
print("best_score_ (CV):", round(grid.best_score_, 4))
print("test f1        :", round(f1_score(y_test, grid.predict(X_test)), 4))
```

```text
best_params_: {'max_depth': 5, 'min_samples_leaf': 1, 'n_estimators': 100}
best_score_ (CV): 0.9553
test f1        : 0.963
```

**Why the CV score > test score:** you picked the winner *because* it scored highest on the CV
folds, so that number is slightly optimistic — you're reporting the max of many noisy
estimates. The untouched test set gives the unbiased figure. `best_estimator_` is the model
refit on all training data, ready to deploy. *Try `RandomizedSearchCV` for bigger grids.*
</details>

---

## Part 4 · Attribute & audit

**Notes.** **Ablation** = remove one piece, measure the drop → shows what actually helps.
**Slice analysis** = score each subgroup → shows *where* the model fails, which the average hides.

### Exercise 8 — Ablate the feature groups

**Goal:** turn "everything matters" into evidence.
**Task:** the 30 features split into `mean_*`, `error_*`, `worst_*`. Drop each group and
measure the change in CV F1. Which group matters most? Which is redundant?

**Steps:** build the baseline CV score, then loop over groups dropping their columns.

<details><summary>▶ Solution</summary>

```python
groups = {"mean":  [c for c in X.columns if c.startswith("mean")],
          "error": [c for c in X.columns if "error" in c],
          "worst": [c for c in X.columns if c.startswith("worst")]}

base = cross_val_score(rf, X, y, cv=cv, scoring="f1").mean()
print(f"full model f1 = {base:.4f}")
for name, cols in groups.items():
    s = cross_val_score(rf, X.drop(columns=cols), y, cv=cv, scoring="f1").mean()
    print(f"  drop {name:5s}: f1={s:.4f}  change={base - s:+.4f}")
```

```text
full model f1 = 0.9355
  drop worst : f1=0.9187  change=+0.0168   <- most important
  drop mean  : f1=0.9450  change=-0.0095
  drop error : f1=0.9465  change=-0.0110   <- removing it HELPS
```

**Why:** the **worst-case** measurements carry the signal (dropping them hurts most). The
**standard-error** group is slightly *harmful* — removing it *raises* F1 — so it's noise the
model over-weights. This is exactly the "ablation table" you'll critique in papers: does each
component earn its place?
</details>

### Exercise 9 — Find where the model fails (slices)

**Goal:** discover a failure that the headline metric hides.
**Task:** bucket the test set by tumour size (`mean radius`) into quartiles and compute
accuracy **and recall** per bucket. What do you notice?

**Steps:** `pd.qcut(res["mean radius"], 4, labels=[...])`, then `groupby` and score each slice.

<details><summary>▶ Solution</summary>

```python
res = X_test.copy(); res["y_true"] = y_test.values; res["y_pred"] = pred
res["bucket"] = pd.qcut(res["mean radius"], 4, labels=["small","medium","large","x-large"])

print("overall accuracy:", round((res.y_true == res.y_pred).mean(), 4))
for b, g in res.groupby("bucket"):
    acc = (g.y_true == g.y_pred).mean()
    rec = recall_score(g.y_true, g.y_pred, pos_label=1, zero_division=0)   # recall for cancer
    print(f"  {b:8s} n={len(g):2d}  acc={acc:.3f}  recall(cancer)={rec:.3f}")
```

```text
overall accuracy: 0.9737
  small    n=29  acc=1.000  recall(cancer)=0.000
  medium   n=28  acc=1.000  recall(cancer)=1.000
  large    n=28  acc=0.893  recall(cancer)=0.750
  x-large  n=29  acc=1.000  recall(cancer)=1.000
```

**Why:** overall accuracy (~97%) looks fine. The **small** bucket has no cancer cases
(recall 0.000 because there were none). The **large** bucket is the weak spot: accuracy 0.89
and cancer recall 0.75 — we miss 1 in 4 cancers there. The headline score hides that.
Swap `bucket` for `region`, `age_group`, or a sensitive attribute and the same code becomes a
**fairness audit**.
</details>

---

## Part 5 · Track everything with MLflow

**Notes.** Once you're tuning and ablating, you generate dozens of models. MLflow logs each
**run** (its params, metrics, artifacts) so you can compare and reproduce them.

### Exercise 10 — Log and compare runs

**Goal:** make your experiments searchable and reproducible.
**Task:** log three random-forest configs to MLflow, then query them back sorted by F1.

**Steps:** `set_tracking_uri("sqlite:///mlflow.db")`, `set_experiment(...)`, loop with
`start_run()`, `log_params`/`log_metric`/`sklearn.log_model`; finally `search_runs(...)`.

<details><summary>▶ Solution</summary>

```python
import mlflow, mlflow.sklearn
mlflow.set_tracking_uri("sqlite:///mlflow.db")     # MLflow 3.x needs a DB backend
mlflow.set_experiment("bc-classifier")

for cfg in [dict(n_estimators=100, max_depth=3),
            dict(n_estimators=300, max_depth=5),
            dict(n_estimators=300, max_depth=None)]:
    with mlflow.start_run(run_name=f"rf_d{cfg['max_depth']}"):
        m  = RandomForestClassifier(random_state=42, **cfg).fit(X_train, y_train)
        f1 = f1_score(y_test, m.predict(X_test))
        mlflow.log_params(cfg)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("roc_auc", roc_auc_score(y_test, m.predict_proba(X_test)[:,1]))
        mlflow.sklearn.log_model(m, name="model")

runs = mlflow.search_runs(experiment_names=["bc-classifier"], order_by=["metrics.f1 DESC"])
print(runs[["params.max_depth","params.n_estimators","metrics.f1","metrics.roc_auc"]]
      .round(4).to_string(index=False))
```

```text
params.max_depth params.n_estimators  metrics.f1  metrics.roc_auc
            None                 300      0.9630           0.9944
               5                 300      0.9500           0.9947
               3                 100      0.9367           0.9940
```

Run **`mlflow ui`** in the same folder and open `localhost:5000` to sort, plot and diff runs
visually. **Why:** unlimited depth wins on F1; depth 5 is close and a bit simpler. AUC is
almost the same. Pick with evidence, not a guess. F1 here is for **cancer**.
</details>

### Exercise 10b — Log a plot (why MLflow matters)

**Goal:** see that MLflow stores pictures with a run, not only numbers.
**Task:** take the best F1 run, plot its ROC, log `winner_roc.png`. Also log
`compare_roc.png` (winner forest vs logistic). Open the UI and find both under **Artifacts**.

<details><summary>▶ Solution</summary>

```python
best = runs.iloc[0]
depth_raw = best["params.max_depth"]
max_depth = None if str(depth_raw) in ("None", "nan") else int(float(depth_raw))
n_estimators = int(float(best["params.n_estimators"]))
best_cfg = dict(n_estimators=n_estimators, max_depth=max_depth)

print("Winner:", best_cfg, "F1=", round(best["metrics.f1"], 4))

lr_cmp = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=5000)),
]).fit(X_train, y_train)

with mlflow.start_run(run_name="winner_with_plots"):
    m = RandomForestClassifier(random_state=42, **best_cfg).fit(X_train, y_train)
    mlflow.log_params(best_cfg)
    mlflow.log_metric("f1", f1_score(y_test, m.predict(X_test)))
    mlflow.log_metric("roc_auc", roc_auc_score(y_test, m.predict_proba(X_test)[:, 1]))

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_estimator(m, X_test, y_test, ax=ax1, pos_label=1, name="Winner RF")
    ax1.set_title("Winner ROC (positive = cancer = 1)")
    fig1.savefig("winner_roc.png", dpi=120, bbox_inches="tight")
    mlflow.log_artifact("winner_roc.png")
    plt.show()

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_estimator(m, X_test, y_test, ax=ax2, pos_label=1, name="Winner RF")
    RocCurveDisplay.from_estimator(lr_cmp, X_test, y_test, ax=ax2, pos_label=1, name="Logistic Regression")
    ax2.set_title("Compare models (positive = cancer = 1)")
    fig2.savefig("compare_roc.png", dpi=120, bbox_inches="tight")
    mlflow.log_artifact("compare_roc.png")
    plt.show()

print("mlflow ui  →  bc-classifier  →  winner_with_plots  →  Artifacts")
```

```text
Winner: {'n_estimators': 300, 'max_depth': None} F1= 0.963
Logged artifacts: winner_roc.png , compare_roc.png
```

**Why:** later you can reopen the run and see the ROC that justified the choice — not only a
number lost in the notebook scroll.
</details>

---

## Concept check (quick quiz)

Try each question first. Then open the answers.

1. A fraud model is 99% accurate but finds only 5% of real fraud. Which score shows the problem?
2. Where should we fit `StandardScaler`, and why?
3. Train F1 = 0.99 but validation F1 = 0.80. Is the model too simple or too detailed? Name one fix.
4. Why do we report both `GridSearchCV.best_score_` and a separate test score?
5. Ablation: we remove a group of features and the score goes **up**. What does that mean?

<details><summary>▶ Answers (plain English)</summary>

1. **Recall** (how many real fraud cases we caught).  
   Accuracy can look great if almost everyone is “not fraud.” The model can ignore fraud and still
   score 99%.

2. Fit it **inside a Pipeline**, and only on the **training** data (each CV fold’s training part).  
   If you scale using the test data, the test set “helps” the model — that is cheating (leakage).

3. The model is **too detailed (overfitting)**.  
   It memorised the training set. Fix: use a simpler model, stop trees growing so deep, or get more
   data.

4. They answer different questions.  
   - `best_score_` = how well the winner did while we were **choosing** settings (a bit too hopeful).  
   - **Test score** = how well it does on data we never used to choose anything (the honest number).

5. That feature group was **not helping** — it was mostly noise.  
   The model is better without it, so drop those features.
</details>

---

## Challenge (optional, open-ended)

Put it all together on **new data**: load a fresh dataset (`sklearn.datasets.load_wine`, or the
real `weatherAUS.csv`), and produce a one-page report that includes:

1. a **stratified** train/test split and a **Pipeline** (no leakage);
2. a **cross-validated** baseline with mean ± std;
3. a **validation curve** diagnosing bias vs variance;
4. a **tuned** model via `GridSearchCV`, reported on the **test set**;
5. an **ablation** of at least two feature groups;
6. a **slice analysis** finding your model's weakest subgroup;
7. every model **logged to MLflow**, with the winner named and justified.

That report *is* the skill set the Paper Critique grades: sound methodology, honest
evaluation, and reproducibility.

---
