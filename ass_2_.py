# -*- coding: utf-8 -*-
"""ASS 2 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13gOnipZCPCcMWfnOKQiO26qSwVaAcY-D
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv('HAM10000_metadata.csv')

# Drop unnecessary columns
data = data.drop(['lesion_id', 'image_id'], axis=1)

# Handling missing values (e.g., age)
data['age'] = data['age'].fillna(data['age'].median())

# Convert categorical data
categorical_features = ['sex', 'localization', 'dx_type']
numerical_features = ['age']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Define target (dx) and features (X)
X = data.drop('dx', axis=1)
y = data['dx']  # Target (diagnosis)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM Model Pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', SVC(kernel='rbf', random_state=42))])

# Train the model
pipeline.fit(X_train, y_train)

# Predict on the test set
y_pred = pipeline.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

from sklearn.model_selection import GridSearchCV

# Define hyperparameter grid
param_grid = {
    'classifier__C': [0.1, 1, 10],
    'classifier__gamma': [1, 0.1, 0.01],
    'classifier__kernel': ['linear', 'rbf']
}

# Use GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters and accuracy
print("Best parameters:", grid_search.best_params_)
print("Best accuracy:", grid_search.best_score_)

pip install streamlit

import streamlit as st
import pandas as pd

# Define the Streamlit app
def main():
    st.title("Skin Lesion Risk Prediction Tool")

    # Input features from the user
    age = st.slider("Age", 0, 100, 30)
    sex = st.selectbox("Sex", ["Male", "Female"])
    localization = st.selectbox("Localization", X['localization'].unique())
    dx_type = st.selectbox("Diagnosis Type", X['dx_type'].unique())

    # Preprocess input
    input_data = pd.DataFrame([[age, sex, localization, dx_type]], columns=X.columns)

    if st.button("Predict"):
        prediction = pipeline.predict(input_data)
        st.write(f"Predicted Diagnosis: {prediction[0]}")

# Run the app
if __name__ == "__main__":
    main()