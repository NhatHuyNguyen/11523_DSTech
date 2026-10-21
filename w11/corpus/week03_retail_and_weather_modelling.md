# Data Science Technology and Systems

## Tutorial and Lab Notes - Week 3

### **Learning Objectives**

By the end of this tutorial, you will be able to:

1. Implement the data science pipeline in Jupyter notebooks
2. Compare different modelling approaches for regression and classification
3. Generate actionable insights from model results
4. Transfer skills between different problem domains

### **Session Structure** (2 Hours)

**First Hour**: Guided Retail Sales Analysis  
**Second Hour**: Independent Weather Prediction Challenge

---

### Required Tasks

1. **Data Preparation**:
   
   - Load data from `weatherAUS.csv`
   
   - Handle missing values (remove or impute)
   
   - Convert date features

2. **Feature Engineering**:
   
   - Categorical variables vs. Continuous ones.
   
   - Create visualisations for key features

3. **Modelling** (Implement various classifiers/regressors):
   
   - Logistic Regression (baseline)
   
   - Random Forest
   
   - Gradient Boosting (XGBoost)
   
   - *Bonus*: Neural Network

4. **Evaluation**:
   
   - Use precision-recall metrics (imbalanced classes)
   
   - Generate confusion matrices
   
   - Identify the most important features
   
   - Hyperparameter tuning (GridSearch)
   
   - Feature importance analysis (SHAP)

-----

## Section 1: Retail Sales Analysis (Guided)

**Dataset**: Black Friday sales data (`Retail_Working_NB.ipynb`)

### Activity Objectives

1. Understand the complete data science workflow:
   - Data Preparation → Exploration → Modeling → Insights
2. Analyse a regression problem (predicting purchase amounts)
3. Compare three model types:
   - Random Forest
   - Support Vector Regression
   - Neural Networks

### Step-by-Step Tasks

1. Download the `BlackFriday.csv` dataset from week 2's tutorial

2. Download the `Retail_Working_NB.ipynb` notebook from this week's content on the Canvas website

3. **Run the notebook** from start to finish

4. **Focus on key transitions**:
   
   - How categorical variables are encoded
   - Outlier treatment using IQR
   - Feature scaling importance
   - Hyperparameter tuning using GridSearchCV
   - Feature importance analysis using SHAP

5. **Discussion Points**:
   
   - Why did Random Forest outperform other models?
   - Business implications of feature importance
   - Limitations of the current approach

**Deliverable**: 

- Run the notebook and prepare 2 questions about any unclear steps

---

## Section 2: Weather Prediction Challenge (Independent)

**Dataset**: Australian weather data (`WeatherAU_Working_NB.ipynb`)

**Task**: Please download the dataset and the Jupyter notebook from this week's content on Canvas, then complete the required tasks in the notebook. 

### Objectives:

1. Identify key weather patterns preceding rainfall
2. Build classification models with >75% accuracy
3. Compare model performance metrics for various ML techniques
4. Tune a classifier with GridSearchCV
5. Interpret the most important features with SHAP

---

## **Final Discussion Questions**

1. How did feature importance differ between regression and classification?

2. Which evaluation metrics were most appropriate for each problem?

3. What data quality issues appeared in both datasets?

4. How would you improve either analysis, given more time
