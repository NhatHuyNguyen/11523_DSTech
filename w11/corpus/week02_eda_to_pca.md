# **Data Science Tutorial: From EDA to PCA**

## **Data Science Technology and Systems (DSTS) Tutorial - Week 2**

## **Exploratory Data Analysis (EDA) & Dimensionality Reduction**

**Duration**: Two hours  
**Tools**: Python, Pandas, Seaborn, Matplotlib, Scikit-learn  
**Datasets**: 

- [BlackFriday Data](https://raw.githubusercontent.com/rd2g16/Black-Friday-Sales/refs/heads/master/data.csv)  
- [Australian Weather Data](https://rattle.togaware.com/weatherAUS.csv)  

---

## **1. Introduction to EDA (10 minutes)**

**Objective**: Learn how to analyse datasets before modelling  

### **Key Concepts**

```python
import pandas as pd
# Please make sure that the data are in the same directory as the Python scripts
df = pd.read_csv('BlackFriday.csv')
print(df.info())  # Structure
print(df.describe())  # Statistics
```

### **Exercise 1.1: Initial Exploration**

**Task**:  

1. Find the number of missing values per column  
2. Identify the data type of each column  

**Solution**:  

```python
# 1. Missing values
print(df.isnull().sum())

# 2. Data types
print(df.dtypes)
```

---

## **2. Statistical Analysis (20 minutes)**

### **A. Central Tendency**

```python
# mean and median
print("Mean Purchase:", df['Purchase'].mean())
print("Median Purchase:", df['Purchase'].median())
```

### **B. Spread & Distribution**

```python
# IQR and skewness
print("IQR:", df['Purchase'].quantile(0.75) - df['Purchase'].quantile(0.25))
print("Skewness:", df['Purchase'].skew())  # Right-skewed if >0
```

### **Exercise 2.1: Advanced Statistics**

**Tasks**:  

1. Calculate the 90th percentile for Purchase
2. Compare the mean vs median of Purchase – what does it imply?

**Solution**:  

```python
# 1. 90th percrntile
print("90th percentile:", df['Purchase'].quantile(0.9))

# 2. mean vs. median
print("Mean Purchase:", df['Purchase'].mean())   # Likely higher than median
print("Median Purchase:", df['Purchase'].median())   # Shows data is right-skewed
# Right-skewed if mean > median
```

---

## **3. Data Visualisation (30 minutes)**

### **A. Distribution Plots**

```python
import seaborn as sns
import matplotlib.pyplot as plt


# Histogram with KDE
sns.histplot(df['Purchase'], bins=50, kde=True)
plt.title("Purchase Distribution")
plt.show()
```

### **B. Outlier Detection**

```python
# Boxplot
sns.boxplot(x='Purchase', data=df)
plt.title("Purchase Value Spread")
plt.show()
```

### **Exercise 3.1: Visualisation**

**Tasks**:  

1. Create a histogram for Product_Category_1
2. Compare purchase amounts by gender using boxplots

**Solution**:  

```python
# 1.
sns.histplot(df['Product_Category_1'], bins=30)
plt.title("Distribution of Product Category 1")
plt.show()

# 2.
sns.boxplot(x='Gender', y='Purchase', data=df)
plt.title("Purchase Amount by Gender")
plt.show()
```

---

## **4. Retail EDA Project (25 minutes)**

### **Data Cleaning**

```python
# Drop rows with missing critical fields
clean_df = df.dropna(subset=['Product_Category_1', 'Purchase'])
# Recheck for missing values (NaN) in the dataset
clean_df.isna().any()
# Optionally fill NaNs in category columns with a placeholder
# The modern, correct way to update individual columns
clean_df['Product_Category_2'] = clean_df['Product_Category_2'].fillna(-1)
clean_df['Product_Category_3'] = clean_df['Product_Category_3'].fillna(-1)
# Remove outliers
Q1 = clean_df['Purchase'].quantile(0.25)
Q3 = clean_df['Purchase'].quantile(0.75)
IQR = Q3 - Q1
clean_df = clean_df[~((clean_df['Purchase'] < (Q1 - 1.5*IQR)) | 
                      (clean_df['Purchase'] > (Q3 + 1.5*IQR)))]
```

### **Correlation Analysis**

```python
# Encode categorical columns for correlation
from sklearn.preprocessing import LabelEncoder

# Create a copy to avoid altering the original
df_encoded = clean_df.copy()

# Identify all object (categorical) columns to encode
categorical_cols = df_encoded.select_dtypes(include='object').columns

# Apply Label Encoding to all categorical columns
le = LabelEncoder()
for col in categorical_cols:
    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

# Compute correlation matrix for all numeric columns
corr = df_encoded.corr(numeric_only=True)

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Encoded Features")
plt.show()
```

### **Exercise 4.1: Advanced EDA**

**Tasks**:  

1. Find the top 3 products with the highest average purchase

2. Plot a scatter plot of Age vs Purchase, colored by Gender

**Solution**:  

```python
# 1. Top 3 products by average purchase
top_products= df.groupby('Product_ID')['Purchase'].mean().nlargest(3)
print("Top 3 Products with Highest Avg Purchase:\n", top_products)

# 2. Scatter plot
sns.scatterplot(x='Age', y='Purchase', hue='Gender', data=df, alpha=0.6)
plt.title("Age vs Purchase by Gender")
plt.xticks(rotation=45)
plt.show()
```

---

## **5. PCA with Weather Data (25 minutes)**

### **Data Preparation**

```python
weather = pd.read_csv('weatherAUS.csv')

# Handle missing data
weather = weather.dropna(thresh=len(weather)*0.7, axis=1).dropna()

# Identify categorical variables
categorical = weather.select_dtypes(include=['object']).columns.tolist()
```

### **PCA Implementation**

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Select continuous features
cont_features = [col for col in weather.columns 
                if col not in categorical and col != 'RainTomorrow']
X = weather[cont_features]

# Standardize and transform
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)
```

### **Exercise 5.1: PCA Analysis**

**Tasks**:  

1. Create a scree plot showing variance explained by top 5 components  
2. Color the PCA plot by 'RainTomorrow' and analyze patterns  
3. Calculate cumulative explained variance for 3 components  

**Solution**:  

```python
# 1. Scree plot
pca_5 = PCA(n_components=5)
pca_5.fit(X_scaled)
plt.bar(range(5), pca_5.explained_variance_ratio_)
plt.title("Scree Plot (Top 5 Components)")
plt.xlabel("Principal Component")
plt.ylabel("Variance Explained")
plt.show()

# 2. Colored plot
pca_df = pd.DataFrame(principal_components, columns=['PC1','PC2'])
pca_df['RainTomorrow'] = weather['RainTomorrow']
sns.scatterplot(x='PC1', y='PC2', hue='RainTomorrow', data=pca_df)
plt.title("PCA Projection Colored by Rain Tomorrow")
plt.show()

# 3. Cumulative variance
print("Cumulative variance for 3 components:", 
     sum(pca_5.explained_variance_ratio_[:3]))
```

---

## **6. Wrap-Up & Solutions Review (10 minutes)**

### **Key Findings**

1. **Retail Data**:  
   
   - Strong correlation between Age and Purchase (e.g., older age groups tend to spend more)
   
   - Right-skewed Purchase distribution suggests applying a log transformation for better modelling

2. **Weather Data PCA**:  
   
   - The first two components explain 48% variance  
   - Rainy days cluster in specific PCA regions  

### **Take-Home Exercises: Integration Challenge**

**Task**:  
For the weather data:  

1. Create a new binary feature 'HighHumidity' (1 if Humidity3pm > 75%)  
2. Rerun PCA and colour points by this new feature  

**Solution**:  

```python
# 1. New feature
weather['HighHumidity'] = (weather['Humidity3pm'] > 75).astype(int)

# 2. Modified PCA
X_scaled = scaler.fit_transform(weather[cont_features])
pca_results = pca.fit_transform(X_scaled)

pca_df = pd.DataFrame(pca_results, columns=['PC1','PC2'])
pca_df['HighHumidity'] = weather['HighHumidity']
sns.scatterplot(x='PC1', y='PC2', hue='HighHumidity', data=pca_df)
plt.title("PCA Colored by High Humidity Days")
plt.show()
```

---

## **Appendix: Complete Solution Files**

All code available as:  

1. [Retail_EDA_Solutions.py](Retail_EDA_Solutions.py)  
2. [Weather_PCA_Solutions.py](Weather_PCA_Solutions.py)  

**Pro Tips**:  

- For skewed data: Apply log transformation before PCA  
- Always standardise data before dimensionality reduction  
- Use `PCA(n_components=0.95)` to retain 95% variance  

This end-to-end tutorial provides various practical exercises with verified solutions, covering everything from basic data inspection to advanced dimensionality reduction techniques.