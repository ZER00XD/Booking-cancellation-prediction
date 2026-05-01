# 🧠 Data Analysis & Machine Learning Project

## 📌 Overview
This project focuses on building a complete data analysis and machine learning pipeline.  
It starts from raw data, goes through preprocessing and cleaning, and ends with training and evaluating a machine learning model.

The goal of this project is to extract insights from data and build a predictive model with good performance.

---

## 🎯 Objectives
- Clean and prepare raw data for analysis  
- Perform Exploratory Data Analysis (EDA)  
- Build a machine learning model  
- Evaluate model performance  

---

## 📊 Dataset
(Write details about your dataset here)

The dataset Cleaned_data.csv contains 109,372 entries related to hotel bookings,specifically for City and Resort hotels.
It is designed for analyzing booking behaviors, cancellations,and customer demographics.

---

## 🔍 Data Preprocessing
In `Cleaning.ipynb`, the following steps were performed:

- Handling missing values  
- Removing duplicates  
- Encoding categorical variables  
- Feature scaling (if applied)  
- Data visualization  

---

## 🤖 Model Building
In `Model.ipynb`, the following steps were implemented:

- Splitting the dataset into training and testing sets  
- Choosing the appropriate machine learning algorithm  
- Training the model  
- Hyperparameter tuning
  
---

## 📈 Model Evaluation
The model was evaluated using:

- Accuracy / RMSE / MAE (حسب مشروعك)  
- Confusion Matrix (لو classification)  
- Visualization of predictions  

👉 **Results:**  

Roc_auc_score : 0.867938852805745
              precision    recall  f1-score   support

           0       0.90      0.90      0.90     13749
           1       0.83      0.84      0.83      8126

    accuracy                           0.87     21875
   macro avg       0.87      0.87      0.87     21875
weighted avg       0.88      0.87      0.88     21875

---

## 🛠️ Technologies Used
- Python 🐍  
- Jupyter Notebook  
- Pandas  
- NumPy  
- Scikit-learn  
- Matplotlib / Seaborn  

---

## 📂 Project Structure

Hotel_Cancellation_Project/
│
├── data/                       # Data storage (not synced to GitHub if large)
│   ├── raw/                   # Original, immutable data (hotel_bookings.csv)
│   └── processed/             # Cleaned data ready for modeling (Cleaned_data.csv)
│
├── notebooks/                  # Jupyter Notebooks for experimentation
│   ├── 01_EDA.ipynb           # Exploratory Data Analysis & Visualizations
│   ├── 02_Cleaning.ipynb      # Data preprocessing & feature engineering
│   └── 03_Modeling.ipynb      # Model training (Random Forest) & evaluation
│
├── src/                        # Source code for modularity
│   ├── __init__.py
│   ├── preprocess.py          # Scripts to automate data cleaning
│   └── train_model.py         # Scripts for training and saving the model
│
├── models/                     # Saved model artifacts
│   └── hotel_model.pkl        # The final trained Random Forest model[cite: 1]
│
├── app/                        # Deployment files (e.g., Streamlit or Flask)
│   └── hotel_app.py           # The application script[cite: 1]
│
├── requirements.txt            # Project dependencies (pandas, scikit-learn, etc.)[cite: 1]
└── README.md                   # Project overview, results, and setup instructions[cite: 1]

