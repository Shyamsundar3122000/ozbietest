# -*- coding: utf-8 -*-
"""lvadsusr120_snehao_lab4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vw5aOGp68RotfO0hDXpv2Ypa0EtT8_cf
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV
data = pd.read_csv('/content/anomaly_train.csv')

# Check data types and missing values
print(data.info())

# Compute basic statistical summaries
print(data.describe())



# Visualizations
# Histogram for 'Amount' column
plt.figure(figsize=(8, 6))
sns.histplot(data['Amount'], bins=30, kde=True)
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.title('Distribution of Amount')
plt.show()

# Count plot for 'Type' column
plt.figure(figsize=(8, 6))
sns.countplot(data['Type'])
plt.xlabel('Type')
plt.ylabel('Count')
plt.title('Count of Transactions by Type')
plt.show()

# Box plot for 'Amount' by 'Type'
plt.figure(figsize=(10, 6))
sns.boxplot(x='Type', y='Amount', data=data)
plt.xlabel('Type')
plt.ylabel('Amount')
plt.title('Distribution of Amount by Transaction Type')
plt.show()

# Label encode categorical columns
le = LabelEncoder()
data['Type'] = le.fit_transform(data['Type'])
data['Location'] = le.fit_transform(data['Location'])

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()



# Handle missing values by imputing with mean
data.fillna(data.mean(), inplace=True)

# Handle outliers using IQR method
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

# Standardize data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[['Amount', 'Time', 'User']])

# Isolation Forest for anomaly detection
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(data_scaled)

# Generate anomaly scores
anomaly_scores = model.decision_function(data_scaled)

# Calculate evaluation metric (average anomaly score)
avg_anomaly_score = anomaly_scores.mean()
print(f'Average Anomaly Score: {avg_anomaly_score:.2f}')

# Visualize anomaly scores
plt.figure(figsize=(8, 6))
plt.hist(anomaly_scores, bins=50, color='skyblue', edgecolor='black')
plt.xlabel('Anomaly Score')
plt.ylabel('Frequency')
plt.title('Distribution of Anomaly Scores')
plt.show()

# Visualize anomalies
colors = ['green' if score >= avg_anomaly_score else 'red' for score in anomaly_scores]

# Visualize anomalies
plt.figure(figsize=(10, 6))
plt.scatter(range(len(anomaly_scores)), anomaly_scores, c=colors, label='Anomalies', s=20)
plt.axhline(avg_anomaly_score, color='blue', linestyle='--', label='Average Anomaly Score')
plt.xlabel('Data Point Index')
plt.ylabel('Anomaly Score')
plt.title('Anomaly Detection with Isolation Forest')
plt.legend()
plt.show()

"""
Insights:The data comprises transaction details like 'Amount', 'Type', 'Time', 'Location', and 'User'. EDA visualizations include histograms, count plots, and box plots to depict distribution and correlations. Anomaly detection via Isolation Forest flags outliers based on features such as 'Amount', 'Time', and 'User'. Insights reveal transaction patterns, anomaly detection efficacy, and feature correlations."""

