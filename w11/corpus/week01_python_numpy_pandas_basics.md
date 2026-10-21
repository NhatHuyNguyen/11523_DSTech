# **Data Science Technology and Systems (2-Hour Tutorial)**

**Week 1**  

---

**Objectives:**  
This tutorial introduces the foundational tools and skills for data science. By the end, learners will be able to:  

1) Set up Jupyter Notebooks / JupyterLab and run Python code,  
2) Review Python basics (lists, NumPy arrays) and Pandas for data manipulation,  
3) Perform basic operations on real datasets, like calculating summary statistics,  
4) Perform basic data cleaning and visualisation operations.

*(Prepares students for upcoming data cleaning and visualisation topics.)*

## **Part 1: Environment Setup (20 mins)**

### **1. Installations**

To get started with Data Science, we need to set up our environment with the necessary tools.  

#### **A. Install Anaconda**

Anaconda is a distribution that includes Python, Jupyter Notebook / JupyterLab, and essential libraries for Data Science.  

**Steps:**  

1. Download Anaconda from: [https://www.anaconda.com/download](https://www.anaconda.com/download)  

2. Follow the installation instructions for your OS (Windows/macOS/Linux).  

3. Verify installation by running in **Terminal (macOS/Linux) or Anaconda Prompt (Windows)**:  

```bash
conda --version  # Should return something like: conda 24.1.2
jupyter --version  # Should return Jupyter version (e.g., 7.1.2)
```

#### **B. Set up Jupyter Notebook / JupyterLab (Anaconda command line)**

1. Open **Anaconda Prompt** (Windows) or **Terminal** (macOS/Linux).  

2. Install Jupyter Notebook and/or JupyterLab with pip:

```bash
pip install jupyter
pip install jupyterlab
```

3. Launch either interface:

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

4. Your browser should open. Create a notebook with **New → Python 3** (Notebook) or **File → New → Notebook** (JupyterLab).  

To stop the server later, press **Ctrl+C** in the same terminal/prompt.

**Troubleshooting (Windows):** If `jupyter lab` (or install/launch) fails with an SSL / certificate error such as `ASN1: NOT_ENOUGH_DATA`, see [`README_JupyterLab_SSL_Windows.md`](README_JupyterLab_SSL_Windows.md) for the fix.

#### **C. Install VS Code (Optional but Recommended)**

VS Code is a powerful code editor with Python support.  

**Steps:**  

1. Download VS Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)  
2. Install the **Python extension** (Guide: [VS Code Python Setup](https://code.visualstudio.com/docs/python/python-tutorial))  

---

### **2. Jupyter Notebook Basics**

Jupyter Notebook is an interactive environment for writing and running Python code. JupyterLab is the next-generation interface for the Jupyter ecosystem — both work with the same `.ipynb` notebook files.

| | **Jupyter Notebook** | **JupyterLab** |
|---|---|---|
| **Interface** | Simple, one notebook per browser tab | Flexible IDE-like layout (tabs, side panels) |
| **Best for** | Quick labs and learning | Multi-file work and larger projects |
| **Launch** | `jupyter notebook` | `jupyter lab` |

For this tutorial, either tool is fine; the cell and Markdown concepts below apply to both.

#### **A. Launching Jupyter Notebook**

Run in Terminal/Anaconda Prompt:  

```bash
jupyter notebook
```

This will open Jupyter in your default browser. (For JupyterLab, use `jupyter lab` as in section **1B** above.)

#### **B. Creating a Notebook**

1. In classic Jupyter Notebook: click **New → Python 3**. In JupyterLab: **File → New → Notebook**.  
2. **Cells** can be:  
   - **Code cells** (execute Python code)  
   - **Markdown cells** (for text/documentation)  

**Demo:**  

- Type in a cell:  

```python
print("Hello, Data Science!")
```

- Press **Shift+Enter** to run.  

**Exercise:**  

- Create a new cell, type `5 + 7`, and run it.  

---

## **Part 2: Python for Data Science (90 mins)**

### **1. Variables & Data Structures**

#### **A. Lists vs. NumPy Arrays**

- **Lists**: Basic Python data structure.  
- **NumPy Arrays**: Optimized for numerical operations.  

**Example:**  

```python
import numpy as np

my_list = [1, 2, 3]  # Python list
my_array = np.array(my_list)  # NumPy array
print(my_array * 2)  # Output: [2 4 6] (element-wise operation)
```

**Exercise:**  
Convert a list of temperatures in °C to °F.  
Formula: `°F = (°C × 9/5) + 32`  

**Solution:**  

```python
celsius = [0, 10, 20, 30]
fahrenheit = np.array(celsius) * 9/5 + 32
print(fahrenheit)  # Output: [32. 50. 68. 86.]
```

---

### **2. Pandas Introduction**

Pandas is a library for data manipulation and analysis.  

#### **A. Loading Data**

We’ll use the **Iris dataset** (a classic dataset in Data Science).  

**Example:**  

```python
import pandas as pd

# Load dataset from URL
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
print(df.head())  # Shows first 5 rows
```

**Output Preview (First 5 rows):**

|     | sepal_length | sepal_width | petal_length | petal_width | species |
| --- | ------------ | ----------- | ------------ | ----------- | ------- |
| 0   | 5.1          | 3.5         | 1.4          | 0.2         | setosa  |
| 1   | 4.9          | 3.0         | 1.4          | 0.2         | setosa  |
| 2   | 4.7          | 3.2         | 1.3          | 0.2         | setosa  |
| 3   | 4.6          | 3.1         | 1.5          | 0.2         | setosa  |
| 4   | 5.0          | 3.6         | 1.4          | 0.2         | setosa  |

#### **B. Basic Operations**

- **Selecting columns**: `df['column_name']`  
- **Grouping & Aggregation**: `df.groupby().mean()`  

**Exercise:**  
Calculate the **mean sepal length** for each species.  

**Solution:**  

```python
mean_sepal = df.groupby('species')['sepal_length'].mean()
print(mean_sepal)
```

**Expected Output:**  

```
species
setosa        5.006
versicolor    5.936
virginica     6.588
Name: sepal_length, dtype: float64
```

---

### **3. Exercise: Sensor Data Analysis with NumPy**

**Scenario:**  
You’re analyzing temperature sensor data from a weather station. The raw data is collected as Python lists and needs processing using NumPy.

#### **Dataset**

```python
import numpy as np

# Raw data (hourly temperatures over 5 days in °C)
day1 = [12.1, 12.5, 13.0, 14.2, 15.1, 16.0, 15.8, 15.3]
day2 = [11.9, 12.2, 12.8, 14.0, 15.2, 16.1, 15.9, 15.2]
day3 = [10.8, 11.5, 12.3, 13.1, 14.9, 15.8, 15.5, 14.9]
day4 = [9.7, 10.1, 11.0, 12.2, 13.8, 14.7, 14.3, 13.5]
day5 = [8.9, 9.5, 10.3, 11.7, 12.9, 13.8, 13.2, 12.6]
```

#### **Tasks**

1. **Data Conversion**  
   
   - Combine all days into a single NumPy array (`shape = (5, 8)`).  
   - Convert temperatures to Fahrenheit (°F = °C × 9/5 + 32).  

2. **Statistical Analysis**  
   
   - Calculate the mean temperature for each day.  
   - Find the daily temperature range (max - min) for all days.  
   - Identify which hour had the highest average temperature across all days.  

3. **Data Filtering**  
   
   - Create a masked array showing only temperatures > 15°C in the original data.  
   - Count how many measurements exceeded 14°C each day.  

4. **Visualisation (Bonus)**  
   
   - Use `matplotlib` to plot hourly temperature trends for all days.  

Solution: see `solutions/exercise3_sensor_numpy.py`

---

### **4. Exercise: Student Performance Analysis**

**Dataset:**  
We’ll use a simulated dataset of student exam scores (copy this into a CSV file named `scores.csv`):  

```csv
student_id,name,math_score,physics_score,chemistry_score,attendance
1,Alex,85,76,90,0.92
2,Brian,72,88,74,0.85
3,Clara,90,82,95,0.96
4,Diana,68,71,62,0.78
5,Ethan,78,75,80,0.88
```

#### **Tasks:**

1. **Data Loading & Inspection**  
   
   - Load the CSV file into a Pandas DataFrame.  
   - Display:  
     - First 3 rows  
     - Data types of each column  
     - Summary statistics (mean, min, max) for numerical columns  

2. **Data Cleaning**  
   
   - Check for missing values.  
   - Convert `attendance` from decimal (0.92) to percentage (92%).  

3. **Calculations**  
   
   - Add a new column `average_score` that calculates the mean of all three subjects.  
   - Add another column `performance_rating` with these categories:  
     - "Excellent" if average ≥ 85  
     - "Good" if 70 ≤ average < 85  
     - "Needs Improvement" if average < 70  

4. **Analysis**  
   
   - Find which student has the highest math score.  
   - Calculate the overall class average for each subject.  
   - Group students by `performance_rating` and count how many are in each category.  

5. **Visualisation (Bonus)**  
   
   - Plot a bar chart of `average_score` for all students (use `matplotlib` or `seaborn`).  

Solution: see `solutions/exercise4_student_performance.py`

---

**Extension Idea:**  

- Add a "pass/fail" column where students fail if any score is < 50.  
- Calculate the correlation between attendance and average scores.  

## **Summary**

✔ Installed Anaconda, JupyterLab (command line), and optional VS Code  
✔ Learned Jupyter Notebook / JupyterLab basics  
✔ Refreshed Python (lists, NumPy arrays)  
✔ Introduced Pandas (loading data, grouping)  
✔ Practised analysis (aggregations, filtering, grouping)  
✔ Practised visualisation (basic plotting with Pandas/Matplotlib)

**Next week:** more detailed data cleaning, visualisation, and machine learning. 

---

**Optional practice at home:**  

1. Load the Iris dataset and find the **median petal_width** per species.  
2. Create a NumPy array of numbers 1-10 and compute its mean.  