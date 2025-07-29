# Upi_fraud_detection_ML
A machine learning model to detect UPI fraud using features like amount, time, and user behavior. Models like Random Forest and XGBoost are used with SMOTE. Built with Python, Flask for real-time detection, and SQL for storing and retrieving transaction data.
Project Overview:
The rise in UPI (Unified Payments Interface) usage has increased the risk of digital fraud. This project aims to build a machine learning-based system that detects fraudulent UPI transactions using transaction history, behavioral patterns, and contextual data. It also features a Flask-based web app and uses SQL to store and retrieve transaction records for analysis and real-time detection.

✅ Key Features:
📊 Data Preprocessing:

Cleaned and structured UPI transaction data (synthetic or anonymized real datasets)

Extracted features such as amount, transaction time, location, frequency, device ID, etc.

🧠 Machine Learning Model:

Algorithms used: Random Forest, XGBoost, Logistic Regression

Tackled class imbalance with SMOTE (Synthetic Minority Oversampling)

Evaluated using Accuracy, Precision, Recall, F1-score, and ROC-AUC

🛠️ Technologies Used:

Programming: Python

Libraries: Scikit-learn, Pandas, NumPy, XGBoost, Imbalanced-learn

Database: MySQL or SQLite for storing user transactions

Backend: Flask (Python)

Frontend: HTML, CSS (optional dashboard)

Deployment: Localhost or cloud-based platform

🌐 Flask Web Interface:

Users can input transaction details manually or upload CSV

Backend processes the input and predicts if the transaction is “Fraud” or “Legit”

SQL database stores the result along with input features for audit/tracking

🧪 Outcome:
The system successfully flags high-risk transactions with high accuracy. It can be integrated into real-time UPI systems to prevent fraud before it occurs. The solution is scalable, customizable, and can serve as the foundation for enterprise-level fraud monitoring tools.

💡 Possible Extensions:
Integrate OTP/email alerts for flagged transactions

Add a user authentication system

Visualize fraud patterns on a dashboard (e.g., Streamlit, Power BI)

Deploy on Heroku, Render, or AWS for public access
