# -*- coding: utf-8 -*-
"""lvadsusr120_snehao_lab2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DqDINUYlQ6iYdiVYLCPeHzP0XFvpiNAM
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectFromModel
from sklearn.impute import SimpleImputer
from scipy import stats

# Load the dataset
df = pd.read_csv('/content/penguins_classification.csv')

# Label Encoding for the target variable
le = LabelEncoder()
df['species'] = le.fit_transform(df['species'])
df['island'] = le.fit_transform(df['island'])

# Impute missing values
imputer = SimpleImputer(strategy='mean')
numerical_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'year']
df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

# Detect and remove outliers using Z-score method
z_scores = np.abs(stats.zscore(df[numerical_cols]))
threshold = 3
outliers_indices = np.where(z_scores > threshold)
df_clean = df.drop(outliers_indices[0])

# EDA: Visualization
sns.pairplot(df_clean, hue='species')
plt.show()
plt.figure(figsize=(10, 8))
sns.heatmap(df_clean.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# Standardize numerical features
scaler = StandardScaler()
df_scaled = df_clean.copy()
df_scaled[numerical_cols] = scaler.fit_transform(df_clean[numerical_cols])

# Feature selection
X = df_scaled[numerical_cols]
y = df_scaled['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
sfm = SelectFromModel(clf, threshold=0.1)
sfm.fit(X_train, y_train)
selected_features = X.columns[sfm.get_support()]

# Train Random Forest Classifier using selected features
clf.fit(X_train[selected_features], y_train)
y_pred = clf.predict(X_test[selected_features])

# Evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

"""Insights : The Random Forest Classifier's accurate classification of penguin species using physical attributes like bill dimensions and body mass underscores the significance of these traits in species differentiation. This suggests that subtle variations in morphology play a crucial role in the evolution and adaptation of penguin species to their environments. Understanding these distinctions can aid conservation efforts by providing insights into population dynamics and habitat preferences, ultimately contributing to the preservation of these iconic seabirds."""

