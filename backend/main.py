# from fastapi import FastAPI
# import joblib
# import pandas as pd

# app = FastAPI()

# model = joblib.load("model/attrition_model.pkl")
# scaler = joblib.load("model/scaler.pkl")
# columns = joblib.load("model/model_columns.pkl")


# @app.post("/predict")

# def predict(data: dict):

#     df = pd.DataFrame([data])

#     # Convert categorical to dummy
#     df = pd.get_dummies(df)

#     # Align columns
#     df = df.reindex(columns=columns,
#                     fill_value=0)

#     # Scale
#     df_scaled = scaler.transform(df)

#     prediction = model.predict(df_scaled)

#     if prediction[0] == 1:
#         return {"Prediction":"Attrition"}

#     else:
#         return {"Prediction":"No Attrition"}

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# ==============================
# Initialize API
# ==============================

app = FastAPI(
    title="Employee Attrition Prediction API",
    version="1.0"
)

# ==============================
# Load trained model
# ==============================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR,"models")

model = joblib.load(os.path.join(MODEL_DIR,"attrition_model.pkl"))

scaler = joblib.load(os.path.join(MODEL_DIR,"scaler.pkl"))

columns = joblib.load(os.path.join(MODEL_DIR,"model_columns.pkl"))

# ==============================
# Input schema
# ==============================

class EmployeeData(BaseModel):

    Age:int
    DailyRate:int
    DistanceFromHome:int
    Education:int
    EnvironmentSatisfaction:int
    HourlyRate:int
    JobInvolvement:int
    JobLevel:int
    JobSatisfaction:int
    MonthlyIncome:int
    MonthlyRate:int
    NumCompaniesWorked:int
    PercentSalaryHike:int
    PerformanceRating:int
    RelationshipSatisfaction:int
    StockOptionLevel:int
    TotalWorkingYears:int
    TrainingTimesLastYear:int
    WorkLifeBalance:int
    YearsAtCompany:int
    YearsInCurrentRole:int
    YearsSinceLastPromotion:int
    YearsWithCurrManager:int

    BusinessTravel:str
    Department:str
    EducationField:str
    Gender:str
    JobRole:str
    MaritalStatus:str
    OverTime:str


# ==============================
# Home route
# ==============================

@app.get("/")

def home():

    return {
        "Project":
        "Employee Attrition Prediction",

        "Model":
        "Logistic Regression",

        "Status":
        "Running"
    }

# ==============================
# Prediction route
# ==============================

@app.post("/predict")

def predict(data:EmployeeData):
    try:
        df = pd.DataFrame([data.dict()])

        # Convert categorical
        df = pd.get_dummies(df)

        # Align columns
        df = df.reindex(
            columns=columns,
            fill_value=0
        )

        # Scale
        df_scaled = scaler.transform(df)

        # Prediction
        prediction = model.predict(df_scaled)[0]
        probability = model.predict_proba(df_scaled)[0][1]
        result = "Attrition Risk" if prediction==1 else "No Attrition Risk"
        risk = "High" if probability>0.6 else "Medium" if probability>0.3 else "Low"

        return {
            "Prediction": result,
            "Probability":
            round(float(probability),3),
            "Risk Level":
            risk
        }

    except Exception as e:
        return {
            "error":str(e)
        }