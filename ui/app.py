#########################################
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# st.set_page_config(
#     page_title="HR Attrition Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("HR Attrition Analytics Platform")

# st.caption(
# "AI driven workforce analytics and attrition prediction system"
# )

# # Sidebar

# st.sidebar.title("Dashboard")

# page = st.sidebar.radio(

# "Navigation",

# ["Prediction","Analytics Dashboard"]

# )

# st.sidebar.divider()

# st.sidebar.success(
# "Model: Logistic Regression"
# )

# # Load model

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# model = joblib.load(
# os.path.join(BASE_DIR,"models","attrition_model.pkl")
# )

# scaler = joblib.load(
# os.path.join(BASE_DIR,"models","scaler.pkl")
# )

# columns = joblib.load(
# os.path.join(BASE_DIR,"models","columns.pkl")
# )

# # ======================
# # PREDICTION
# # ======================

# if page=="Prediction":

#     st.subheader("Employee Risk Prediction")

#     col1,col2,col3,col4 = st.columns(4)

#     age = col1.slider("Age",18,60,30)

#     income = col2.number_input(
#     "Monthly Income",
#     1000,20000,5000
#     )

#     job_level = col3.selectbox(
#     "Job Level",
#     [1,2,3,4,5]
#     )

#     years = col4.slider(
#     "Years at Company",
#     0,40,5
#     )

#     col1,col2,col3,col4 = st.columns(4)

#     job_sat = col1.selectbox(
#     "Job Satisfaction",
#     [1,2,3,4]
#     )

#     worklife = col2.selectbox(
#     "Work Life Balance",
#     [1,2,3,4]
#     )

#     overtime = col3.selectbox(
#     "Overtime",
#     ["Yes","No"]
#     )

#     department = col4.selectbox(

#     "Department",

#     ["Sales",
#     "Research & Development",
#     "Human Resources"]

#     )

#     if st.button("Predict"):

#         data = {

#         "Age":age,
#         "DailyRate":800,
#         "DistanceFromHome":5,
#         "Education":3,
#         "EnvironmentSatisfaction":3,
#         "HourlyRate":60,
#         "JobInvolvement":3,
#         "JobLevel":job_level,
#         "JobSatisfaction":job_sat,
#         "MonthlyIncome":income,
#         "MonthlyRate":15000,
#         "NumCompaniesWorked":2,
#         "PercentSalaryHike":13,
#         "PerformanceRating":3,
#         "RelationshipSatisfaction":3,
#         "StockOptionLevel":1,
#         "TotalWorkingYears":10,
#         "TrainingTimesLastYear":2,
#         "WorkLifeBalance":worklife,
#         "YearsAtCompany":years,
#         "YearsInCurrentRole":3,
#         "YearsSinceLastPromotion":1,
#         "YearsWithCurrManager":3,

#         "BusinessTravel":"Travel_Rarely",
#         "Department":department,
#         "EducationField":"Life Sciences",
#         "Gender":"Male",
#         "JobRole":"Sales Executive",
#         "MaritalStatus":"Single",
#         "OverTime":overtime

#         }

#         response = requests.post(
#         "http://127.0.0.1:8000/predict",
#         json=data
#         )

#         result=response.json()

#         st.divider()

#         col1,col2,col3 = st.columns(3)

#         if result["Prediction"]=="Attrition Risk":

#             col1.error("High Risk")

#         else:

#             col1.success("Low Risk")

#         col2.metric(
#         "Probability",
#         result["Probability"]
#         )

#         col3.metric(
#         "Risk Level",
#         result["Risk Level"]
#         )

# # ======================
# # ANALYTICS
# # ======================

# if page=="Analytics Dashboard":
    
#     st.subheader("Workforce Analytics")

#     file = st.file_uploader(
#     "Upload HR Dataset",
#     type=["csv"]
#     )

#     if file:

#         df = pd.read_csv(file)

#         st.subheader("Dataset Preview")

#         st.dataframe(df.head())

#         st.write("Dataset Shape:",df.shape)

#         if model:

#             df_original = df.copy()

#             df_encoded = pd.get_dummies(df)

#             df_encoded = df_encoded.reindex(
#             columns=columns,
#             fill_value=0
#             )

#             df_scaled = scaler.transform(df_encoded)

#             df_original['Prediction']=model.predict(df_scaled)

#             df_original['Probability']=model.predict_proba(df_scaled)[:,1]

#             df_original['Prediction']=df_original[
#             'Prediction'
#             ].map({

#             0:"No Attrition",
#             1:"Attrition"

#             })

#             st.subheader("Prediction Results")

#             st.dataframe(df_original.head())

#             # KPI

#             col1,col2,col3,col4 = st.columns(4)

#             col1.metric(
#             "Employees",
#             len(df_original)
#             )

#             col2.metric(
#             "Attrition",
#             (df_original['Prediction']=="Attrition").sum()
#             )

#             col3.metric(

#             "Attrition Rate",

#             str(

#             round(

#             (df_original['Prediction']=="Attrition")
#             .mean()*100,2

#             ))+"%"

#             )

#             col4.metric(

#             "Avg Salary",

#             int(df_original['MonthlyIncome'].mean())

#             )

#             st.divider()

#             # Charts

#             fig = px.histogram(

#             df_original,

#             x="Prediction",

#             color="Prediction",

#             title="Attrition Distribution"

#             )

#             st.plotly_chart(fig,
#             use_container_width=True)

#             fig2 = px.box(

#             df_original,

#             x="Prediction",

#             y="MonthlyIncome",

#             color="Prediction",

#             title="Income Impact"

#             )

#             st.plotly_chart(fig2,
#             use_container_width=True)

#             fig3 = px.histogram(

#             df_original,

#             x="Department",

#             color="Prediction",

#             title="Department Impact"

#             )

#             st.plotly_chart(fig3,
#             use_container_width=True)

#             st.divider()

#             st.subheader("Insights")

#             st.info("""

# Overtime strongly impacts attrition.

# Lower salary employees are higher risk.

# Job satisfaction affects retention.

# """)

#             st.subheader("Recommendations")

#             st.success("""

# Reduce overtime.

# Improve engagement.

# Review salary structure.

# Provide career growth.

# """)

#             st.download_button(

#             "Download Results",

#             df_original.to_csv(index=False),

#             "attrition_results.csv"

#             )


# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# st.set_page_config(
#     page_title="HR Attrition Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("HR Attrition Analytics Platform")

# st.caption(
# "AI driven workforce analytics and attrition prediction system"
# )

# st.divider()

# # Sidebar

# st.sidebar.title("Dashboard")

# page = st.sidebar.radio(
# "Navigation",
# ["Prediction","Analytics Dashboard"]
# )

# st.sidebar.divider()

# st.sidebar.success("Model Active")
# st.sidebar.info("Algorithm: Logistic Regression")

# # Load model

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# model = joblib.load(
# os.path.join(BASE_DIR,"models","attrition_model.pkl")
# )

# scaler = joblib.load(
# os.path.join(BASE_DIR,"models","scaler.pkl")
# )

# columns = joblib.load(
# os.path.join(BASE_DIR,"models","columns.pkl")
# )

# # ======================
# # PREDICTION
# # ======================

# if page=="Prediction":

#     st.subheader("Employee Risk Prediction")

#     container = st.container(border=True)

#     with container:

#         col1,col2,col3,col4 = st.columns(4)

#         age = col1.slider("Age",18,60,30)

#         income = col2.number_input(
#         "Monthly Income",
#         1000,20000,5000
#         )

#         job_level = col3.selectbox(
#         "Job Level",
#         [1,2,3,4,5]
#         )

#         years = col4.slider(
#         "Years at Company",
#         0,40,5
#         )

#         col1,col2,col3,col4 = st.columns(4)

#         job_sat = col1.selectbox(
#         "Job Satisfaction",
#         [1,2,3,4]
#         )

#         worklife = col2.selectbox(
#         "Work Life Balance",
#         [1,2,3,4]
#         )

#         overtime = col3.selectbox(
#         "Overtime",
#         ["Yes","No"]
#         )

#         department = col4.selectbox(

#         "Department",

#         ["Sales",
#         "Research & Development",
#         "Human Resources"]

#         )

#     if st.button("Predict Risk"):

#         with st.spinner("Running prediction model..."):

#             data = {

#             "Age":age,
#             "DailyRate":800,
#             "DistanceFromHome":5,
#             "Education":3,
#             "EnvironmentSatisfaction":3,
#             "HourlyRate":60,
#             "JobInvolvement":3,
#             "JobLevel":job_level,
#             "JobSatisfaction":job_sat,
#             "MonthlyIncome":income,
#             "MonthlyRate":15000,
#             "NumCompaniesWorked":2,
#             "PercentSalaryHike":13,
#             "PerformanceRating":3,
#             "RelationshipSatisfaction":3,
#             "StockOptionLevel":1,
#             "TotalWorkingYears":10,
#             "TrainingTimesLastYear":2,
#             "WorkLifeBalance":worklife,
#             "YearsAtCompany":years,
#             "YearsInCurrentRole":3,
#             "YearsSinceLastPromotion":1,
#             "YearsWithCurrManager":3,

#             "BusinessTravel":"Travel_Rarely",
#             "Department":department,
#             "EducationField":"Life Sciences",
#             "Gender":"Male",
#             "JobRole":"Sales Executive",
#             "MaritalStatus":"Single",
#             "OverTime":overtime

#             }

#             try:

#                 response = requests.post(
#                 "http://127.0.0.1:8000/predict",
#                 json=data
#                 )

#                 result=response.json()

#                 st.divider()

#                 st.subheader("Prediction Result")

#                 col1,col2,col3 = st.columns(3)

#                 if result["Prediction"]=="Attrition Risk":

#                     col1.error("High Risk Employee")

#                 else:

#                     col1.success("Low Risk Employee")

#                 col2.metric(
#                 "Attrition Probability",
#                 result["Probability"]
#                 )

#                 col3.metric(
#                 "Risk Level",
#                 result["Risk Level"]
#                 )

#             except:

#                 st.error("API not running")

# # ======================
# # ANALYTICS
# # ======================

# if page=="Analytics Dashboard":
    
#     st.subheader("Workforce Analytics Dashboard")

#     file = st.file_uploader(
#     "Upload HR Dataset",
#     type=["csv"]
#     )

#     if file:

#         df = pd.read_csv(file)

#         required_cols=[
#         'Age',
#         'MonthlyIncome',
#         'Department'
#         ]

#         missing=[]

#         for col in required_cols:

#             if col not in df.columns:

#                 missing.append(col)

#         if missing:

#             st.error(
#             "Missing columns: "+str(missing)
#             )

#             st.stop()

#         st.subheader("Dataset Preview")

#         st.dataframe(df.head())

#         st.write("Dataset Shape:",df.shape)

#         if model:

#             with st.spinner("Analyzing workforce data..."):

#                 df_original = df.copy()

#                 df_encoded = pd.get_dummies(df)

#                 df_encoded = df_encoded.reindex(
#                 columns=columns,
#                 fill_value=0
#                 )

#                 df_scaled = scaler.transform(df_encoded)

#                 df_original['Prediction']=model.predict(df_scaled)

#                 df_original['Probability']=model.predict_proba(df_scaled)[:,1]

#                 df_original['Prediction']=df_original[
#                 'Prediction'
#                 ].map({

#                 0:"No Attrition",
#                 1:"Attrition"

#                 })

#             st.success("Analysis Completed")

#             # KPI

#             st.subheader("HR Summary")

#             col1,col2,col3,col4 = st.columns(4)

#             col1.metric(
#             "Total Employees",
#             len(df_original)
#             )

#             col2.metric(
#             "Attrition Count",
#             (df_original['Prediction']=="Attrition").sum()
#             )

#             col3.metric(

#             "Attrition Rate",

#             str(

#             round(

#             (df_original['Prediction']=="Attrition")
#             .mean()*100,2

#             ))+"%"

#             )

#             col4.metric(

#             "Average Salary",

#             int(df_original['MonthlyIncome'].mean())

#             )

#             st.divider()

#             # Risk indicator

#             high_risk = (
#             df_original['Prediction']=="Attrition"
#             ).sum()

#             if high_risk>50:

#                 st.error(
#                 "High Attrition Risk Workforce"
#                 )

#             else:

#                 st.success(
#                 "Workforce Stability Good"
#                 )

#             # Charts

#             st.subheader("Attrition Insights")

#             col1,col2 = st.columns(2)

#             fig = px.histogram(
#             df_original,
#             x="Prediction",
#             color="Prediction",
#             title="Attrition Distribution"
#             )

#             col1.plotly_chart(
#             fig,
#             use_container_width=True
#             )

#             fig2 = px.box(
#             df_original,
#             x="Prediction",
#             y="MonthlyIncome",
#             color="Prediction",
#             title="Income Impact"
#             )

#             col2.plotly_chart(
#             fig2,
#             use_container_width=True
#             )

#             fig3 = px.histogram(
#             df_original,
#             x="Department",
#             color="Prediction",
#             title="Department Impact"
#             )

#             st.plotly_chart(
#             fig3,
#             use_container_width=True
#             )

#             st.divider()

#             # Expandable table

#             with st.expander("View Full Prediction Data"):

#                 st.dataframe(df_original)

#             # Insights

#             st.subheader("Key Insights")

#             st.info("""

# Employees working overtime show higher attrition.

# Lower salary employees show higher risk.

# Job satisfaction affects retention.

# Early tenure employees show higher turnover.

# """)

#             # Recommendations

#             st.subheader("HR Recommendations")

#             st.success("""

# Reduce overtime workload.

# Improve employee engagement.

# Review salary structure.

# Provide career growth.

# Improve work life balance.

# """)

#             # Download

#             st.subheader("Export Results")

#             st.download_button(

#             "Download Predictions",

#             df_original.to_csv(index=False),

#             "attrition_results.csv"

#             )

# st.divider()

# st.caption(
# "Employee Attrition Analytics Platform | Built with FastAPI & Streamlit"
# )



#### claude verwsion
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import joblib
# import os

# st.set_page_config(
#     page_title="PeopleIQ — HR Attrition Analytics",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─────────────────────────────────────────────────────────────────────────────
# # GLOBAL CSS  — carefully scoped so Streamlit native inputs stay fully visible
# # ─────────────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

# html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
# .stApp { background: #f0f2f8 !important; }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 1.5rem 2rem 4rem 2rem !important; max-width: 100% !important; }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: #ffffff !important;
#     border-right: 1px solid #dde1ee !important;
# }
# [data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
# [data-testid="stSidebar"] .stRadio > label {
#     font-size: 11px !important;
#     font-weight: 600 !important;
#     text-transform: uppercase !important;
#     letter-spacing: 0.8px !important;
#     color: #9aa0b8 !important;
# }
# [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
#     font-size: 13px !important;
#     font-weight: 400 !important;
#     text-transform: none !important;
#     letter-spacing: 0 !important;
#     color: #3d4563 !important;
#     padding: 6px 10px !important;
#     border-radius: 7px !important;
# }

# /* ── Form labels ── */
# .stSlider label p,
# .stSelectbox label p,
# .stNumberInput label p {
#     font-size: 11px !important;
#     font-weight: 600 !important;
#     text-transform: uppercase !important;
#     letter-spacing: 0.8px !important;
#     color: #6b7491 !important;
# }

# /* ── Selectbox — CRITICAL: makes text visible ── */
# div[data-baseweb="select"] > div {
#     background-color: #ffffff !important;
#     border: 1.5px solid #dde1ee !important;
#     border-radius: 9px !important;
#     color: #1a1f36 !important;
#     font-size: 13px !important;
#     font-family: 'Inter', sans-serif !important;
#     min-height: 42px !important;
# }
# div[data-baseweb="select"] > div:hover { border-color: #4f6ef7 !important; }
# div[data-baseweb="select"] > div:focus-within {
#     border-color: #4f6ef7 !important;
#     box-shadow: 0 0 0 3px rgba(79,110,247,0.12) !important;
# }
# /* The selected value text */
# div[data-baseweb="select"] [data-testid="stSelectbox"] span,
# div[data-baseweb="select"] span {
#     color: #1a1f36 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
# }
# /* SVG arrow icon */
# div[data-baseweb="select"] svg { fill: #6b7491 !important; }

# /* Dropdown list */
# [data-baseweb="popover"] [data-baseweb="menu"] {
#     background: #ffffff !important;
#     border: 1px solid #dde1ee !important;
#     border-radius: 10px !important;
#     box-shadow: 0 8px 30px rgba(0,0,0,0.10) !important;
# }
# [data-baseweb="popover"] li {
#     font-size: 13px !important;
#     color: #1a1f36 !important;
#     font-family: 'Inter', sans-serif !important;
# }
# [data-baseweb="popover"] li:hover { background: #f0f2f8 !important; }
# [data-baseweb="popover"] li[aria-selected="true"] {
#     background: #eef1fd !important;
#     color: #4f6ef7 !important;
#     font-weight: 500 !important;
# }

# /* ── Number input — CRITICAL: makes text visible ── */
# .stNumberInput input {
#     background: #ffffff !important;
#     border: 1.5px solid #dde1ee !important;
#     border-radius: 9px !important;
#     color: #1a1f36 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     font-family: 'Inter', sans-serif !important;
#     height: 42px !important;
# }
# .stNumberInput input:focus {
#     border-color: #4f6ef7 !important;
#     box-shadow: 0 0 0 3px rgba(79,110,247,0.12) !important;
#     outline: none !important;
# }
# .stNumberInput button {
#     background: #f0f2f8 !important;
#     border: 1px solid #dde1ee !important;
#     color: #3d4563 !important;
#     border-radius: 7px !important;
# }

# /* ── Slider track & thumb ── */
# .stSlider [data-baseweb="slider"] div[role="slider"] { background: #4f6ef7 !important; }
# .stSlider [data-baseweb="slider"] div { background: #4f6ef7 !important; }

# /* ── Primary button ── */
# .stButton > button {
#     background: linear-gradient(135deg, #4f6ef7 0%, #3a56d4 100%) !important;
#     color: #ffffff !important;
#     border: none !important;
#     border-radius: 10px !important;
#     font-weight: 600 !important;
#     font-size: 14px !important;
#     padding: 12px 28px !important;
#     font-family: 'Inter', sans-serif !important;
#     box-shadow: 0 4px 14px rgba(79,110,247,0.35) !important;
#     transition: all .2s !important;
#     height: auto !important;
# }
# .stButton > button:hover {
#     opacity: 0.90 !important;
#     box-shadow: 0 6px 20px rgba(79,110,247,0.45) !important;
#     transform: translateY(-1px) !important;
# }

# /* ── Download button ── */
# .stDownloadButton > button {
#     background: #ffffff !important;
#     color: #4f6ef7 !important;
#     border: 1.5px solid #4f6ef7 !important;
#     border-radius: 9px !important;
#     font-weight: 500 !important;
#     font-size: 13px !important;
#     font-family: 'Inter', sans-serif !important;
#     box-shadow: none !important;
#     padding: 9px 20px !important;
# }
# .stDownloadButton > button:hover { background: #eef1fd !important; }

# /* ── st.metric cards ── */
# [data-testid="stMetric"] {
#     background: #ffffff !important;
#     border: 1px solid #dde1ee !important;
#     border-radius: 14px !important;
#     padding: 18px 20px !important;
# }
# [data-testid="stMetricLabel"] p {
#     font-size: 10px !important;
#     font-weight: 600 !important;
#     text-transform: uppercase !important;
#     letter-spacing: 1px !important;
#     color: #9aa0b8 !important;
# }
# [data-testid="stMetricValue"] {
#     font-size: 26px !important;
#     font-weight: 700 !important;
#     letter-spacing: -1px !important;
#     color: #1a1f36 !important;
# }
# [data-testid="stMetricDelta"] {
#     font-size: 11px !important;
#     font-family: 'JetBrains Mono', monospace !important;
# }

# /* ── File uploader ── */
# [data-testid="stFileUploader"] {
#     background: #ffffff !important;
#     border: 2px dashed #c8ceea !important;
#     border-radius: 14px !important;
# }

# /* ── Expander ── */
# .streamlit-expanderHeader {
#     background: #ffffff !important;
#     border: 1px solid #dde1ee !important;
#     border-radius: 10px !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     color: #3d4563 !important;
# }

# /* ── Divider ── */
# hr { border: none !important; border-top: 1px solid #dde1ee !important; margin: 20px 0 !important; }

# /* ────────────────────────────────
#    CUSTOM HTML COMPONENT STYLES
#    ──────────────────────────────── */
# .topbar {
#     background: #ffffff;
#     border: 1px solid #dde1ee;
#     border-radius: 14px;
#     padding: 18px 24px;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     margin-bottom: 24px;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.05);
# }
# .topbar h1 {
#     font-size: 19px; font-weight: 700; color: #1a1f36;
#     letter-spacing: -0.5px; margin: 0 0 3px;
# }
# .topbar p { font-size: 12px; color: #9aa0b8; margin: 0; font-family: 'JetBrains Mono', monospace; }
# .badge-active {
#     display: inline-flex; align-items: center; gap: 7px;
#     background: #ecfdf5; color: #059669; font-size: 12px; font-weight: 600;
#     padding: 6px 14px; border-radius: 20px; border: 1px solid #a7f3d0;
#     font-family: 'JetBrains Mono', monospace; white-space: nowrap;
# }
# .badge-dot { width: 7px; height: 7px; border-radius: 50%; background: #10b981; box-shadow: 0 0 0 3px rgba(16,185,129,0.2); display: inline-block; }

# .form-section {
#     background: #ffffff; border: 1px solid #dde1ee; border-radius: 14px;
#     padding: 20px 22px; margin-bottom: 20px;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.05);
# }
# .form-section-title { font-size: 14px; font-weight: 700; color: #1a1f36; margin-bottom: 3px; }
# .form-section-sub { font-size: 12px; color: #9aa0b8; }

# .kpi-row {
#     display: grid; grid-template-columns: repeat(4, 1fr);
#     gap: 14px; margin-bottom: 24px;
# }
# .kpi-card {
#     background: #ffffff; border: 1px solid #dde1ee; border-radius: 14px;
#     padding: 20px 22px; position: relative; overflow: hidden;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.05);
# }
# .kpi-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #9aa0b8; margin-bottom: 10px; }
# .kpi-value { font-size: 30px; font-weight: 700; letter-spacing: -1.5px; line-height: 1; margin-bottom: 8px; }
# .kpi-badge { display: inline-block; font-size: 10px; font-family: 'JetBrains Mono', monospace; font-weight: 500; padding: 3px 9px; border-radius: 20px; }
# .kpi-card.danger .kpi-value  { color: #dc2626; }
# .kpi-card.danger .kpi-badge  { background: #fee2e2; color: #dc2626; }
# .kpi-card.danger::after  { content:''; position:absolute; top:-12px; right:-12px; width:72px; height:72px; background:#dc2626; opacity:.06; border-radius:50%; }
# .kpi-card.success .kpi-value { color: #059669; }
# .kpi-card.success .kpi-badge { background: #d1fae5; color: #059669; }
# .kpi-card.success::after { content:''; position:absolute; top:-12px; right:-12px; width:72px; height:72px; background:#059669; opacity:.06; border-radius:50%; }
# .kpi-card.warn .kpi-value    { color: #d97706; }
# .kpi-card.warn .kpi-badge    { background: #fef3c7; color: #d97706; }
# .kpi-card.warn::after    { content:''; position:absolute; top:-12px; right:-12px; width:72px; height:72px; background:#d97706; opacity:.06; border-radius:50%; }
# .kpi-card.info .kpi-value    { color: #4f6ef7; }
# .kpi-card.info .kpi-badge    { background: #eef1fd; color: #4f6ef7; }
# .kpi-card.info::after    { content:''; position:absolute; top:-12px; right:-12px; width:72px; height:72px; background:#4f6ef7; opacity:.06; border-radius:50%; }

# .section-hdr {
#     display: flex; align-items: center; gap: 10px;
#     margin: 28px 0 14px; padding-bottom: 12px; border-bottom: 1px solid #dde1ee;
# }
# .section-hdr-title { font-size: 14px; font-weight: 700; color: #1a1f36; letter-spacing: -0.3px; }
# .section-hdr-sub   { font-size: 12px; color: #9aa0b8; margin-left: auto; }

# .chart-card {
#     background: #ffffff; border: 1px solid #dde1ee; border-radius: 14px;
#     padding: 16px 18px 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 14px;
# }

# .alert-danger {
#     background: #fff1f1; border: 1px solid #fca5a5; border-left: 4px solid #dc2626;
#     color: #7f1d1d; border-radius: 10px; padding: 13px 16px;
#     font-size: 13px; font-weight: 500; margin-bottom: 20px;
# }
# .alert-success {
#     background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a;
#     color: #14532d; border-radius: 10px; padding: 13px 16px;
#     font-size: 13px; font-weight: 500; margin-bottom: 20px;
# }

# .result-card-high {
#     background: #fff; border: 1.5px solid #fca5a5; border-left: 5px solid #dc2626;
#     border-radius: 14px; padding: 22px; box-shadow: 0 2px 8px rgba(220,38,38,0.08);
# }
# .result-card-low {
#     background: #fff; border: 1.5px solid #86efac; border-left: 5px solid #16a34a;
#     border-radius: 14px; padding: 22px; box-shadow: 0 2px 8px rgba(22,163,74,0.08);
# }
# .result-prob { font-size: 52px; font-weight: 700; font-family: 'JetBrains Mono', monospace; letter-spacing: -3px; line-height: 1; margin-bottom: 8px; }
# .result-prob.high { color: #dc2626; }
# .result-prob.low  { color: #059669; }
# .result-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #9aa0b8; margin-bottom: 14px; }
# .risk-pill { display: inline-block; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; padding: 5px 14px; border-radius: 20px; font-family: 'JetBrains Mono', monospace; }
# .risk-pill.high { background: #fee2e2; color: #dc2626; }
# .risk-pill.med  { background: #fef3c7; color: #d97706; }
# .risk-pill.low  { background: #d1fae5; color: #059669; }
# .result-heading { font-size: 16px; font-weight: 700; color: #1a1f36; margin-bottom: 6px; letter-spacing: -0.3px; }
# .result-sub     { font-size: 12px; color: #6b7491; line-height: 1.6; margin-bottom: 14px; }
# .result-meta    { font-size: 12px; color: #9aa0b8; }
# .result-meta strong { color: #1a1f36; font-weight: 600; }

# .rec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px; }
# .rec-item { background: #f7f8ff; border: 1px solid #e0e4f8; border-radius: 10px; padding: 12px 14px; font-size: 12px; color: #3d4563; line-height: 1.5; }
# .rec-item strong { color: #1a1f36; font-weight: 600; display: block; margin-bottom: 3px; }
# .rec-panel { background: #fff; border: 1px solid #dde1ee; border-radius: 14px; padding: 22px; }
# .rec-panel-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; color: #9aa0b8; margin-bottom: 12px; }

# .insight-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
# .insight-item { background: #f0f4ff; border: 1px solid #c7d2fa; border-radius: 10px; padding: 12px 14px; font-size: 12px; color: #3d4563; line-height: 1.5; display: flex; gap: 10px; align-items: flex-start; }
# .insight-icon { font-size: 14px; flex-shrink: 0; margin-top: 1px; }
# .hrec-item { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px 14px; font-size: 12px; color: #14532d; line-height: 1.5; display: flex; gap: 10px; align-items: flex-start; }
# .hrec-icon { font-size: 14px; flex-shrink: 0; margin-top: 1px; }

# .sidebar-logo { font-size: 17px; font-weight: 700; color: #1a1f36; letter-spacing: -0.5px; margin-bottom: 2px; }
# .sidebar-sub { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: #9aa0b8; background: #f0f2f8; padding: 2px 8px; border-radius: 20px; display: inline-block; margin-bottom: 18px; }
# .sidebar-status { display: inline-flex; align-items: center; gap: 6px; background: #ecfdf5; color: #059669; font-size: 11px; font-weight: 600; padding: 5px 12px; border-radius: 20px; border: 1px solid #a7f3d0; font-family: 'JetBrains Mono', monospace; }
# .sidebar-status-dot { width: 6px; height: 6px; border-radius: 50%; background: #10b981; display: inline-block; }
# .sidebar-info { font-size: 11px; color: #9aa0b8; font-family: 'JetBrains Mono', monospace; margin-top: 8px; }

# .empty-state { text-align: center; padding: 70px 0; color: #9aa0b8; }
# .empty-state-icon { font-size: 40px; margin-bottom: 14px; }
# .empty-state-title { font-size: 15px; font-weight: 600; color: #3d4563; margin-bottom: 6px; }
# .empty-state-sub { font-size: 13px; }

# .page-footer { text-align: center; padding: 36px 0 0; font-size: 11px; color: #c4c9de; font-family: 'JetBrains Mono', monospace; }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("""
#     <div class="sidebar-logo">PeopleIQ</div>
#     <span class="sidebar-sub">HR Analytics · v2.4</span>
#     """, unsafe_allow_html=True)

#     page = st.radio("Navigation", ["Prediction", "Analytics Dashboard"])

#     st.markdown("---")
#     st.markdown("""
#     <div class="sidebar-status">
#         <span class="sidebar-status-dot"></span>&nbsp;Model Active
#     </div>
#     <div class="sidebar-info" style="margin-top:10px">Algorithm: Logistic Regression</div>
#     <div class="sidebar-info">Last sync: just now</div>
#     """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # LOAD MODEL
# # ─────────────────────────────────────────────
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# try:
#     model   = joblib.load(os.path.join(BASE_DIR, "models", "attrition_model.pkl"))
#     scaler  = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
#     columns = joblib.load(os.path.join(BASE_DIR, "models", "columns.pkl"))
#     model_loaded = True
# except Exception:
#     model = scaler = columns = None
#     model_loaded = False


# # ─────────────────────────────────────────────
# # PLOTLY THEME HELPER
# # ─────────────────────────────────────────────
# def plot_layout(title=""):
#     return dict(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(family="Inter, sans-serif", color="#6b7491", size=12),
#         margin=dict(l=4, r=4, t=44 if title else 10, b=4),
#         title=dict(text=title, font=dict(size=13, color="#1a1f36", family="Inter", weight=600), x=0),
#         xaxis=dict(gridcolor="#edf0f7", linecolor="#edf0f7", showgrid=False, tickfont=dict(size=11)),
#         yaxis=dict(gridcolor="#edf0f7", linecolor="#edf0f7", tickfont=dict(size=11)),
#         hoverlabel=dict(bgcolor="#fff", font_size=12, font_family="Inter", bordercolor="#dde1ee"),
#     )


# # ─────────────────────────────────────────────
# # PAGE: PREDICTION
# # ─────────────────────────────────────────────
# if page == "Prediction":

#     st.markdown("""
#     <div class="topbar">
#         <div>
#             <h1>Employee Risk Prediction</h1>
#             <p>AI-powered attrition risk assessment · Logistic Regression v3</p>
#         </div>
#         <div class="badge-active"><span class="badge-dot"></span> Model Active</div>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div class="form-section">
#         <div class="form-section-title">Employee Details</div>
#         <div class="form-section-sub">Fill in the attributes below to generate a risk assessment</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3, col4 = st.columns(4)
#     age       = col1.slider("Age", 18, 60, 30)
#     income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
#     job_level = col3.selectbox("Job Level", [1, 2, 3, 4, 5],
#                     format_func=lambda x: {1:"1 — Entry",2:"2 — Junior",3:"3 — Mid",4:"4 — Senior",5:"5 — Director"}[x])
#     years     = col4.slider("Years at Company", 0, 40, 5)

#     col1, col2, col3, col4 = st.columns(4)
#     job_sat    = col1.selectbox("Job Satisfaction", [1, 2, 3, 4],
#                     format_func=lambda x: {1:"1 — Very Low",2:"2 — Low",3:"3 — Medium",4:"4 — High"}[x])
#     worklife   = col2.selectbox("Work-Life Balance", [1, 2, 3, 4],
#                     format_func=lambda x: {1:"1 — Poor",2:"2 — Fair",3:"3 — Good",4:"4 — Excellent"}[x])
#     overtime   = col3.selectbox("Overtime", ["No", "Yes"])
#     department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

#     st.markdown("<br>", unsafe_allow_html=True)
#     _, btn_col, _ = st.columns([4, 2, 4])
#     predict_clicked = btn_col.button("Run Risk Assessment →", use_container_width=True)

#     if predict_clicked:
#         with st.spinner("Analysing employee profile..."):
#             payload = {
#                 "Age": age, "DailyRate": 800, "DistanceFromHome": 5,
#                 "Education": 3, "EnvironmentSatisfaction": 3, "HourlyRate": 60,
#                 "JobInvolvement": 3, "JobLevel": job_level, "JobSatisfaction": job_sat,
#                 "MonthlyIncome": income, "MonthlyRate": 15000, "NumCompaniesWorked": 2,
#                 "PercentSalaryHike": 13, "PerformanceRating": 3, "RelationshipSatisfaction": 3,
#                 "StockOptionLevel": 1, "TotalWorkingYears": 10, "TrainingTimesLastYear": 2,
#                 "WorkLifeBalance": worklife, "YearsAtCompany": years, "YearsInCurrentRole": 3,
#                 "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 3,
#                 "BusinessTravel": "Travel_Rarely", "Department": department,
#                 "EducationField": "Life Sciences", "Gender": "Male",
#                 "JobRole": "Sales Executive", "MaritalStatus": "Single", "OverTime": overtime
#             }
#             try:
#                 resp        = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
#                 result      = resp.json()
#                 prediction  = result["Prediction"]
#                 probability = result["Probability"]
#                 risk_level  = result["Risk Level"]
#                 api_ok      = True
#             except Exception:
#                 api_ok = False

#         if not api_ok:
#             st.markdown('<div class="alert-danger">⚠ <strong>API Unavailable</strong> — Cannot reach FastAPI server at <code>localhost:8000</code>. Make sure your backend is running.</div>', unsafe_allow_html=True)
#         else:
#             is_high  = prediction == "Attrition Risk"
#             card_cls = "result-card-high" if is_high else "result-card-low"
#             prob_cls = "high" if is_high else "low"
#             pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
#             heading  = "⚠ High Attrition Risk" if is_high else "✓ Low Attrition Risk"
#             desc     = ("Multiple risk signals detected. Immediate HR intervention is recommended "
#                         "to retain this employee.") if is_high else \
#                        ("This profile appears stable. Continue regular check-ins "
#                         "and career development planning.")

#             c1, c2, c3 = st.columns([1, 1.6, 1.6])
#             with c1:
#                 st.markdown(f"""
#                 <div class="{card_cls}" style="text-align:center">
#                     <div class="result-label">Risk Probability</div>
#                     <div class="result-prob {prob_cls}">{probability}</div>
#                     <span class="risk-pill {pill_cls}">{risk_level} Risk</span>
#                 </div>""", unsafe_allow_html=True)

#             with c2:
#                 st.markdown(f"""
#                 <div class="{card_cls}">
#                     <div class="result-heading">{heading}</div>
#                     <div class="result-sub">{desc}</div>
#                     <div class="result-meta">
#                         <strong>Prediction:</strong> {prediction}<br>
#                         <strong>Risk Level:</strong> {risk_level}
#                     </div>
#                 </div>""", unsafe_allow_html=True)

#             with c3:
#                 recs = []
#                 if overtime == "Yes":
#                     recs.append(("Reduce Overtime", "Excessive overtime is the #1 driver of attrition in this model."))
#                 if job_sat <= 2:
#                     recs.append(("Satisfaction Review", "Schedule a 1:1 — low job satisfaction is a strong exit signal."))
#                 if income < 4000:
#                     recs.append(("Salary Benchmark", "Pay is below market. A compensation review is recommended."))
#                 if years < 3:
#                     recs.append(("Onboarding Support", "Early-tenure employees carry the highest flight risk."))
#                 if not recs:
#                     recs.append(("Maintain Engagement", "Profile is healthy. Keep regular check-ins and recognition."))

#                 rec_html = "".join([
#                     f'<div class="rec-item"><strong>{t}</strong>{d}</div>'
#                     for t, d in recs
#                 ])
#                 st.markdown(f"""
#                 <div class="rec-panel">
#                     <div class="rec-panel-label">HR Recommendations</div>
#                     <div class="rec-grid">{rec_html}</div>
#                 </div>""", unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # PAGE: ANALYTICS DASHBOARD
# # ─────────────────────────────────────────────
# if page == "Analytics Dashboard":

#     st.markdown("""
#     <div class="topbar">
#         <div>
#             <h1>Workforce Analytics Dashboard</h1>
#             <p>Upload your HR dataset to generate predictions and insights</p>
#         </div>
#         <div class="badge-active"><span class="badge-dot"></span> Ready</div>
#     </div>
#     """, unsafe_allow_html=True)

#     file = st.file_uploader("Upload HR Dataset (CSV)", type=["csv"])

#     if not file:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="empty-state-icon">📂</div>
#             <div class="empty-state-title">No Dataset Loaded</div>
#             <div class="empty-state-sub">Upload an IBM HR-format CSV file above to begin analysis</div>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         df = pd.read_csv(file)
#         required_cols = ['Age', 'MonthlyIncome', 'Department']
#         missing = [c for c in required_cols if c not in df.columns]
#         if missing:
#             st.markdown(f'<div class="alert-danger">⚠ <strong>Missing columns:</strong> {", ".join(missing)}</div>', unsafe_allow_html=True)
#             st.stop()

#         if not model_loaded:
#             st.warning("Model files not found — showing dataset preview only.")
#             st.dataframe(df.head(), use_container_width=True, hide_index=True)
#             st.stop()

#         with st.spinner("Running predictions across workforce..."):
#             df_orig  = df.copy()
#             df_enc  = pd.get_dummies(df)
#             df_enc  = df_enc.reindex(columns=columns, fill_value=0)
#             df_sc   = scaler.transform(df_enc)
#             df_orig['Prediction'] = model.predict(df_sc)
#             df_orig['Probability'] = model.predict_proba(df_sc)[:, 1]
#             df_orig['Prediction'] = df_orig['Prediction'].map({0: "No Attrition", 1: "Attrition"})

#         att_count = (df_orig['Prediction'] == "Attrition").sum()
#         att_rate  = (df_orig['Prediction'] == "Attrition").mean() * 100
#         avg_sal   = int(df_orig['MonthlyIncome'].mean())
#         avg_risk  = df_orig['Probability'].mean() * 100

#         if att_count > 50:
#             st.markdown(f'<div class="alert-danger">🔴 <strong>High Attrition Risk:</strong> {att_count} employees ({att_rate:.1f}%) are predicted to leave. Immediate action required.</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="alert-success">✅ <strong>Workforce Stable:</strong> Attrition is within an acceptable range — {att_count} employees ({att_rate:.1f}%).</div>', unsafe_allow_html=True)

#         # ── KPI Row
#         st.markdown(f"""
#         <div class="kpi-row">
#             <div class="kpi-card info">
#                 <div class="kpi-label">Total Employees</div>
#                 <div class="kpi-value">{len(df_orig):,}</div>
#                 <span class="kpi-badge">Loaded</span>
#             </div>
#             <div class="kpi-card danger">
#                 <div class="kpi-label">Attrition Count</div>
#                 <div class="kpi-value">{att_count:,}</div>
#                 <span class="kpi-badge">↑ Predicted</span>
#             </div>
#             <div class="kpi-card warn">
#                 <div class="kpi-label">Attrition Rate</div>
#                 <div class="kpi-value">{att_rate:.1f}%</div>
#                 <span class="kpi-badge">Avg risk {avg_risk:.0f}%</span>
#             </div>
#             <div class="kpi-card success">
#                 <div class="kpi-label">Avg Monthly Income</div>
#                 <div class="kpi-value">${avg_sal:,}</div>
#                 <span class="kpi-badge">Per employee</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown('<div class="section-hdr"><span class="section-hdr-title">Attrition Insights</span><span class="section-hdr-sub">Model predictions across your workforce</span></div>', unsafe_allow_html=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             fig1 = px.histogram(df_orig, x="Prediction", color="Prediction",
#                 color_discrete_map={"Attrition":"#dc2626","No Attrition":"#10b981"})
#             fig1.update_layout(**plot_layout("Attrition Distribution"), showlegend=False)
#             fig1.update_traces(marker_line_width=0)
#             st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#             st.plotly_chart(fig1, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         with col2:
#             fig2 = px.box(df_orig, x="Prediction", y="MonthlyIncome", color="Prediction",
#                 color_discrete_map={"Attrition":"#dc2626","No Attrition":"#10b981"})
#             fig2.update_layout(**plot_layout("Income vs Attrition"), showlegend=False)
#             st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#             st.plotly_chart(fig2, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         fig3 = px.histogram(df_orig, x="Department", color="Prediction", barmode="group",
#             color_discrete_map={"Attrition":"#dc2626","No Attrition":"#4f6ef7"})
#         fig3.update_layout(**plot_layout("Attrition by Department"),
#             legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1, font=dict(size=11)))
#         fig3.update_traces(marker_line_width=0)
#         st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#         st.plotly_chart(fig3, use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#         col1, col2 = st.columns(2)
#         with col1:
#             fig4 = px.histogram(df_orig, x="Probability", nbins=30,
#                 color_discrete_sequence=["#4f6ef7"])
#             fig4.update_layout(**plot_layout("Risk Probability Distribution"), showlegend=False)
#             fig4.update_traces(marker_line_width=0)
#             st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#             st.plotly_chart(fig4, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         with col2:
#             if 'Age' in df_orig.columns:
#                 fig5 = px.scatter(df_orig, x="Age", y="Probability", color="Prediction", opacity=0.55,
#                     color_discrete_map={"Attrition":"#dc2626","No Attrition":"#10b981"})
#                 fig5.update_layout(**plot_layout("Age vs Attrition Risk"),
#                     legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1, font=dict(size=11)))
#                 st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#                 st.plotly_chart(fig5, use_container_width=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#         st.markdown('<div class="section-hdr"><span class="section-hdr-title">Prediction Table</span><span class="section-hdr-sub">{:,} total records</span></div>'.format(len(df_orig)), unsafe_allow_html=True)
#         with st.expander("View full prediction data", expanded=False):
#             st.dataframe(df_orig, use_container_width=True, hide_index=True)

#         st.markdown('<div class="section-hdr" style="margin-top:4px"><span class="section-hdr-title">Key Insights</span></div>', unsafe_allow_html=True)
#         st.markdown("""
#         <div class="insight-grid">
#             <div class="insight-item"><span class="insight-icon">📊</span>Employees working overtime show significantly higher attrition rates across all departments.</div>
#             <div class="insight-item"><span class="insight-icon">💰</span>Lower salary bands (&lt;$4k/mo) correlate with 2–3× elevated attrition probability.</div>
#             <div class="insight-item"><span class="insight-icon">😔</span>Job satisfaction score ≤ 2 is the strongest individual predictor of departure.</div>
#             <div class="insight-item"><span class="insight-icon">🕐</span>Employees with tenure &lt; 3 years represent the highest-risk cohort for early turnover.</div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown('<div class="section-hdr" style="margin-top:20px"><span class="section-hdr-title">HR Recommendations</span></div>', unsafe_allow_html=True)
#         st.markdown("""
#         <div class="insight-grid">
#             <div class="hrec-item"><span class="hrec-icon">✅</span>Audit and reduce overtime allocation, particularly in Sales and R&D teams.</div>
#             <div class="hrec-item"><span class="hrec-icon">✅</span>Benchmark compensation against market — prioritise adjustments for Level 1–2 roles.</div>
#             <div class="hrec-item"><span class="hrec-icon">✅</span>Launch a targeted engagement program for employees with satisfaction scores below 3.</div>
#             <div class="hrec-item"><span class="hrec-icon">✅</span>Strengthen onboarding and mentorship for employees in their first 2 years.</div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown('<div class="section-hdr" style="margin-top:20px"><span class="section-hdr-title">Export</span></div>', unsafe_allow_html=True)
#         st.download_button(
#             "⬇  Download Prediction Report (CSV)",
#             df_orig.to_csv(index=False),
#             "attrition_predictions.csv",
#             mime="text/csv"
#         )

# # ── Footer
# st.markdown('<div class="page-footer">PeopleIQ · Employee Attrition Analytics · Built with FastAPI &amp; Streamlit</div>', unsafe_allow_html=True)




########Version 3.0
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# st.set_page_config(
#     page_title="HR Attrition Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# st.markdown("""
# <style>

# /* Background */
# .stApp{
# background:#f5f7fb;
# font-family: Inter;
# }

# /* KPI cards */
# .kpi-row{
# display:grid;
# grid-template-columns:repeat(4,1fr);
# gap:16px;
# margin-top:15px;
# margin-bottom:20px;
# }

# .kpi-card{
# background:white;
# padding:22px;
# border-radius:14px;
# border:1px solid #e6e8f0;
# box-shadow:0 2px 6px rgba(0,0,0,0.04);
# }

# .kpi-label{
# font-size:11px;
# font-weight:600;
# letter-spacing:1px;
# color:#8b93a7;
# margin-bottom:10px;
# }

# .kpi-value{
# font-size:28px;
# font-weight:700;
# }

# .kpi-card.info .kpi-value{color:#4f6ef7;}
# .kpi-card.danger .kpi-value{color:#dc2626;}
# .kpi-card.warn .kpi-value{color:#d97706;}
# .kpi-card.success .kpi-value{color:#059669;}

# .kpi-badge{
# font-size:10px;
# background:#eef2ff;
# padding:4px 10px;
# border-radius:20px;
# margin-top:8px;
# display:inline-block;
# }

# /* Insight boxes */

# .insight-grid{
# display:grid;
# grid-template-columns:1fr 1fr;
# gap:12px;
# margin-top:10px;
# }

# .insight-item{
# background:#f3f6ff;
# border:1px solid #cfd7ff;
# padding:14px;
# border-radius:10px;
# font-size:13px;
# color:#2f365f;
# }

# .insight-item-title{
# font-weight:600;
# margin-bottom:4px;
# }

# .insight-item-body{
# font-size:13px;
# }

# /* HR recommendation cards */

# .hrec-grid{
# display:grid;
# grid-template-columns:1fr 1fr;
# gap:14px;
# margin-top:10px;
# }

# .hrec-item{
# background:#ecfdf5;
# border:1px solid #bbf7d0;
# padding:16px;
# border-radius:10px;
# font-size:13px;
# color:#14532d;
# }

# .hrec-item-title{
# font-weight:600;
# margin-bottom:5px;
# }

# .hrec-item-body{
# font-size:13px;
# }

# .hrec-priority-pill{
# padding:3px 10px;
# border-radius:20px;
# font-size:11px;
# margin-left:10px;
# }

# /* Prediction result cards */

# .result-card-high{
# background:white;
# border:2px solid #fecaca;
# border-left:6px solid #dc2626;
# padding:20px;
# border-radius:14px;
# }

# .result-card-low{
# background:white;
# border:2px solid #bbf7d0;
# border-left:6px solid #16a34a;
# padding:20px;
# border-radius:14px;
# }

# .result-prob{
# font-size:46px;
# font-weight:700;
# }

# .result-prob.high{
# color:#dc2626;
# }

# .result-prob.low{
# color:#16a34a;
# }

# .result-label{
# font-size:11px;
# color:#8b93a7;
# margin-bottom:10px;
# }

# .risk-pill{
# padding:5px 12px;
# border-radius:20px;
# font-size:11px;
# font-weight:600;
# }

# .risk-pill.high{
# background:#fee2e2;
# color:#dc2626;
# }

# .risk-pill.med{
# background:#fef3c7;
# color:#d97706;
# }

# .risk-pill.low{
# background:#d1fae5;
# color:#059669;
# }

# /* Section headers */

# .section-hdr{
# display:flex;
# justify-content:space-between;
# margin-top:25px;
# margin-bottom:10px;
# border-bottom:1px solid #e6e8f0;
# padding-bottom:8px;
# }

# .section-hdr-title{
# font-weight:600;
# font-size:15px;
# }

# .section-hdr-sub{
# font-size:12px;
# color:#8b93a7;
# }

# /* Alerts */

# .alert-danger{
# background:#fff1f1;
# border-left:5px solid #dc2626;
# padding:14px;
# border-radius:10px;
# margin-bottom:15px;
# }

# .alert-success{
# background:#f0fdf4;
# border-left:5px solid #16a34a;
# padding:14px;
# border-radius:10px;
# margin-bottom:15px;
# }

# /* Buttons */

# .stButton button{

# background:linear-gradient(135deg,#4f6ef7,#3a56d4);

# border:none;

# color:white;

# border-radius:10px;

# padding:12px;

# font-weight:600;

# }

# .stButton button:hover{

# opacity:.9;

# }

# /* Tables */

# [data-testid="stDataFrame"]{

# background:white;

# border-radius:12px;

# padding:10px;

# border:1px solid #e6e8f0;

# }

# /* Footer */

# footer{

# visibility:hidden;

# }

# </style>
# """,unsafe_allow_html=True)

# st.title("HR Attrition Analytics Platform")

# st.caption(
# "AI driven workforce analytics and attrition prediction system"
# )

# st.divider()

# # Sidebar

# st.sidebar.title("Dashboard")

# page = st.sidebar.radio(
# "Navigation",
# ["Prediction","Analytics Dashboard"]
# )

# st.sidebar.divider()

# st.sidebar.success("Model Active")
# st.sidebar.info("Algorithm: Logistic Regression")

# # Load model

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# model = joblib.load(
# os.path.join(BASE_DIR,"models","attrition_model.pkl")
# )

# scaler = joblib.load(
# os.path.join(BASE_DIR,"models","scaler.pkl")
# )

# columns = joblib.load(
# os.path.join(BASE_DIR,"models","columns.pkl")
# )

# # ======================
# # SINGLE PREDICTION
# # ======================

# if page=="Prediction":

#     st.subheader("Employee Risk Prediction")

#     container = st.container(border=True)

#     with container:

#         col1,col2,col3,col4 = st.columns(4)

#         age = col1.slider("Age",18,60,30)

#         income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)

#         job_level = col3.selectbox("Job Level", [1, 2, 3, 4, 5],
#                     format_func=lambda x: {1:"Entry",2:"Junior",3:"Mid",4:"Senior",5:"Director"}[x])

#         years     = col4.slider("Years at Company", 0, 40, 5)

#         col1,col2,col3,col4 = st.columns(4)

#         job_sat    = col1.selectbox("Job Satisfaction", [1, 2, 3, 4],
#                     format_func=lambda x: {1:"Very Low",2:"Low",3:"Medium",4:"High"}[x])

#         worklife   = col2.selectbox("Work-Life Balance", [1, 2, 3, 4],
#                     format_func=lambda x: {1:"Poor",2:"Fair",3:"Good",4:"Excellent"}[x])

#         overtime   = col3.selectbox("Overtime", ["No", "Yes"])

#         department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

#     st.markdown("<br>", unsafe_allow_html=True)
#     _, btn_col, _ = st.columns([4, 2, 4])
#     predict_clicked = btn_col.button("Run Risk Assessment →", use_container_width=True)
 
#     if predict_clicked:
#         with st.spinner("Analysing employee profile..."):
#             payload = {
#                 "Age": age, "DailyRate": 800, "DistanceFromHome": 5,
#                 "Education": 3, "EnvironmentSatisfaction": 3, "HourlyRate": 60,
#                 "JobInvolvement": 3, "JobLevel": job_level, "JobSatisfaction": job_sat,
#                 "MonthlyIncome": income, "MonthlyRate": 15000, "NumCompaniesWorked": 2,
#                 "PercentSalaryHike": 13, "PerformanceRating": 3, "RelationshipSatisfaction": 3,
#                 "StockOptionLevel": 1, "TotalWorkingYears": 10, "TrainingTimesLastYear": 2,
#                 "WorkLifeBalance": worklife, "YearsAtCompany": years, "YearsInCurrentRole": 3,
#                 "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 3,
#                 "BusinessTravel": "Travel_Rarely", "Department": department,
#                 "EducationField": "Life Sciences", "Gender": "Male",
#                 "JobRole": "Sales Executive", "MaritalStatus": "Single", "OverTime": overtime
#             }
#             try:
#                 resp        = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
#                 result      = resp.json()
#                 prediction  = result["Prediction"]
#                 probability = result["Probability"]
#                 risk_level  = result["Risk Level"]
#                 api_ok      = True
#             except Exception:
#                 api_ok = False
 
#         if not api_ok:
#             st.markdown('<div class="alert-danger">⚠ <strong>API Unavailable</strong> — Cannot reach FastAPI server at <code>localhost:8000</code>. Make sure your backend is running.</div>', unsafe_allow_html=True)
#         else:
#             is_high  = prediction == "Attrition Risk"
#             card_cls = "result-card-high" if is_high else "result-card-low"
#             prob_cls = "high" if is_high else "low"
#             pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
#             heading  = "⚠ High Attrition Risk" if is_high else "✓ Low Attrition Risk"
#             desc     = ("Multiple risk signals detected. Immediate HR intervention is recommended "
#                         "to retain this employee.") if is_high else \
#                        ("This profile appears stable. Continue regular check-ins "
#                         "and career development planning.")
 
#             c1, c2, c3 = st.columns([1, 1.6, 1.6])
#             with c1:
#                 st.markdown(f"""
#                 <div class="{card_cls}" style="text-align:center">
#                     <div class="result-label">Risk Probability</div>
#                     <div class="result-prob {prob_cls}">{probability}</div>
#                     <span class="risk-pill {pill_cls}">{risk_level} Risk</span>
#                 </div>""", unsafe_allow_html=True)
 
#             with c2:
#                 st.markdown(f"""
#                 <div class="{card_cls}">
#                     <div class="result-heading">{heading}</div>
#                     <div class="result-sub">{desc}</div>
#                     <div class="result-meta">
#                         <strong>Prediction:</strong> {prediction}<br>
#                         <strong>Risk Level:</strong> {risk_level}
#                     </div>
#                 </div>""", unsafe_allow_html=True)
 
#             with c3:
#                 recs = []
#                 if overtime == "Yes":
#                     recs.append(("Reduce Overtime", "Excessive overtime is the #1 driver of attrition in this model."))
#                 if job_sat <= 2:
#                     recs.append(("Satisfaction Review", "Schedule a 1:1 — low job satisfaction is a strong exit signal."))
#                 if income < 4000:
#                     recs.append(("Salary Benchmark", "Pay is below market. A compensation review is recommended."))
#                 if years < 3:
#                     recs.append(("Onboarding Support", "Early-tenure employees carry the highest flight risk."))
#                 if not recs:
#                     recs.append(("Maintain Engagement", "Profile is healthy. Keep regular check-ins and recognition."))
 
#                 rec_html = "".join([
#                     f'<div class="rec-item"><strong>{t}</strong>{d}</div>'
#                     for t, d in recs
#                 ])
#                 st.markdown(f"""
#                 <div class="rec-panel">
#                     <div class="rec-panel-label">HR Recommendations</div>
#                     <div class="rec-grid">{rec_html}</div>
#                 </div>""", unsafe_allow_html=True)

# # ======================
# # ANALYTICS DASHBOARD
# # ======================

# if page=="Analytics Dashboard":

#     st.markdown("""
#     <div class="topbar">
#         <div>
#             <h1>Workforce Analytics Dashboard</h1>
#             <p>Upload your HR dataset to generate predictions and insights</p>
#         </div>
#         <div class="badge-active"><span class="badge-dot"></span> Ready</div>
#     </div>
#     """, unsafe_allow_html=True)

#     file = st.file_uploader(
#     "Upload HR Dataset",
#     type=["csv"]
#     )

#     if file:
#         df = pd.read_csv(file)

#         required_cols=[
#         'Age',
#         'MonthlyIncome',
#         'Department'
#         ]

#         missing=[c for c in required_cols if c not in df.columns]

#         for col in required_cols:

#             if col not in df.columns:

#                 missing.append(col)

#         if missing:
#             st.markdown(f'<div class="alert-danger">⚠ <strong>Missing columns:</strong> {", ".join(missing)}</div>', unsafe_allow_html=True)
#             st.stop()

#         st.subheader("Dataset Preview")

#         st.dataframe(df.head())

#         if model:
    
#             with st.spinner("Analyzing workforce data..."):

#                 df_original = df.copy()
#             df_enc  = pd.get_dummies(df)
#             df_enc  = df_enc.reindex(columns=columns, fill_value=0)
#             df_sc   = scaler.transform(df_enc)
#             df_original['Prediction'] = model.predict(df_sc)
#             df_original['Probability'] = model.predict_proba(df_sc)[:, 1]
#             df_original['Prediction'] = df_original['Prediction'].map({0: "No Attrition", 1: "Attrition"})
 
#         att_count = (df_original['Prediction'] == "Attrition").sum()
#         att_rate  = (df_original['Prediction'] == "Attrition").mean() * 100
#         avg_sal   = int(df_original['MonthlyIncome'].mean())
#         avg_risk  = df_original['Probability'].mean() * 100
 
#         if att_count > 50:
#             st.markdown(f'<div class="alert-danger">🔴 <strong>High Attrition Risk:</strong> {att_count} employees ({att_rate:.1f}%) are predicted to leave. Immediate action required.</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="alert-success">✅ <strong>Workforce Stable:</strong> Attrition is within an acceptable range — {att_count} employees ({att_rate:.1f}%).</div>', unsafe_allow_html=True)
 

#         # ================= KPI SUMMARY =================

#         st.markdown(f"""
#         <div class="kpi-row">
#             <div class="kpi-card info">
#                 <div class="kpi-label">Total Employees</div>
#                 <div class="kpi-value">{len(df_original):,}</div>
#                 <span class="kpi-badge">Loaded</span>
#             </div>
#             <div class="kpi-card danger">
#                 <div class="kpi-label">Attrition Count</div>
#                 <div class="kpi-value">{att_count:,}</div>
#                 <span class="kpi-badge">↑ Predicted</span>
#             </div>
#             <div class="kpi-card warn">
#                 <div class="kpi-label">Attrition Rate</div>
#                 <div class="kpi-value">{att_rate:.1f}%</div>
#                 <span class="kpi-badge">Avg risk {avg_risk:.0f}%</span>
#             </div>
#             <div class="kpi-card success">
#                 <div class="kpi-label">Avg Monthly Income</div>
#                 <div class="kpi-value">${avg_sal:,}</div>
#                 <span class="kpi-badge">Per employee</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # ================= FILTERS =================

#         st.subheader("Filters")

#         col = st.columns(2)

#         dept_filter = col[0].multiselect(
#         "Department",
#         df_original['Department'].unique(),
#         default=df_original['Department'].unique()
#         )

#         filtered_df=df_original[
#         (df_original['Department'].isin(dept_filter))
#         ]

#         # ================= DATASET HEALTH =================

#         st.subheader("Dataset Health")

#         col1,col2 = st.columns(2)

#         col1.metric(
#         "Missing Values",
#         filtered_df.isnull().sum().sum()
#         )

#         col2.metric(
#         "Features",
#         filtered_df.shape[1]
#         )

#         st.divider()

#         # ================= CHARTS =================

#         st.subheader("Workforce Insights")

#         col1,col2 = st.columns(2)

#         fig=px.histogram(
#         filtered_df,
#         x="Prediction",
#         color="Prediction",
#         title="Attrition Distribution"
#         )

#         col1.plotly_chart(fig,
#         use_container_width=True)

#         fig2=px.box(
#         filtered_df,
#         x="Prediction",
#         y="MonthlyIncome",
#         color="Prediction",
#         title="Income Impact"
#         )

#         col2.plotly_chart(fig2,
#         use_container_width=True)
        

#         col3,col4 = st.columns(2)

#         fig3=px.histogram(
#         filtered_df,
#         x="Department",
#         color="Prediction",
#         title="Department Impact"
#         )

#         col3.plotly_chart(fig3,
#         use_container_width=True)

#         fig4=px.pie(
#         filtered_df,
#         names="Prediction",
#         title="Risk Breakdown"
#         )

#         col4.plotly_chart(fig4,
#         use_container_width=True)

#         # ================= PROBABILITY =================

#         # st.subheader("Risk Probability Distribution")

#         # fig5=px.histogram(
#         # filtered_df,
#         # x="Probability"
#         # )

#         # st.plotly_chart(fig5,
#         # use_container_width=True)

#         # ================= HIGH RISK TABLE =================

#         st.subheader("Top High Risk Employees")

#         high_risk=filtered_df[
#         filtered_df['Prediction']=="Attrition"
#         ].sort_values(

#         "Probability",

#         ascending=False

#         ).head(10)

#         st.dataframe(high_risk)

#         with st.expander("View Full Prediction Data"):

#                 st.dataframe(df_original)

#         # ================= INSIGHTS =================

#         insights = []
 
#         if 'OverTime' in df_original.columns:
#             ot_att  = df_original[df_original['OverTime'] == 'Yes']['Prediction'].eq('Attrition').mean() * 100
#             not_att = df_original[df_original['OverTime'] == 'No']['Prediction'].eq('Attrition').mean() * 100
#             lift    = ot_att - not_att
#             insights.append(("📊", "Overtime Impact",
#                 f"{ot_att:.1f}% attrition among overtime employees vs {not_att:.1f}% for others — a <strong>{lift:.1f}pp lift</strong>."))
 
#         if 'MonthlyIncome' in df_original.columns:
#             low_sal = df_original[df_original['MonthlyIncome'] < 4000]['Prediction'].eq('Attrition').mean() * 100
#             hi_sal  = df_original[df_original['MonthlyIncome'] >= 4000]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("💰", "Salary Band Risk",
#                 f"Employees earning &lt;$4k/mo have <strong>{low_sal:.1f}%</strong> attrition vs {hi_sal:.1f}% for higher earners."))
 
#         if 'JobSatisfaction' in df_original.columns:
#             low_js = df_original[df_original['JobSatisfaction'] <= 2]['Prediction'].eq('Attrition').mean() * 100
#             hi_js  = df_original[df_original['JobSatisfaction'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("😔", "Satisfaction vs Retention",
#                 f"Low satisfaction (≤2) employees show <strong>{low_js:.1f}%</strong> attrition vs {hi_js:.1f}% for satisfied staff."))
 
#         if 'YearsAtCompany' in df_original.columns:
#             early  = df_original[df_original['YearsAtCompany'] < 3]['Prediction'].eq('Attrition').mean() * 100
#             senior = df_original[df_original['YearsAtCompany'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🕐", "Early Tenure Risk",
#                 f"Employees with &lt;3 years tenure have <strong>{early:.1f}%</strong> predicted attrition vs {senior:.1f}% for veterans."))
 
#         if 'Department' in df_original.columns:
#             top_dept = (df_original[df_original['Prediction'] == 'Attrition']
#                         .groupby('Department').size()
#                         .idxmax())
#             top_pct  = df_original[df_original['Department'] == top_dept]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🏢", "Highest-Risk Department",
#                 f"<strong>{top_dept}</strong> has the most predicted attrition at <strong>{top_pct:.1f}%</strong> of its headcount."))
 
#         if 'WorkLifeBalance' in df_original.columns:
#             poor_wlb = df_original[df_original['WorkLifeBalance'] == 1]['Prediction'].eq('Attrition').mean() * 100
#             good_wlb = df_original[df_original['WorkLifeBalance'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("⚖️", "Work-Life Balance",
#                 f"Poor WLB (score 1) employees: <strong>{poor_wlb:.1f}%</strong> attrition vs {good_wlb:.1f}% for good WLB."))
 
#         insight_html = "".join([
#             f"""<div class="insight-item">
#                     <div class="insight-item-icon">{icon}</div>
#                     <div>
#                         <div class="insight-item-title">{title}</div>
#                         <div class="insight-item-body">{body}</div>
#                     </div>
#                 </div>"""
#             for icon, title, body in insights
#         ])
 
#         st.markdown(f"""
#         <div class="section-hdr" style="margin-top:4px">
#             <span class="section-hdr-title">Key Insights</span>
#             <span class="section-hdr-sub">Derived from your dataset · {len(insights)} findings</span>
#         </div>
#         <div class="insight-grid">{insight_html}</div>
#         """, unsafe_allow_html=True)
 
#         # ── Dynamic Recommendations from actual data ──
#         recommendations = []
 
#         if 'OverTime' in df_original .columns:
#             ot_count = (df_original ['OverTime'] == 'Yes').sum()
#             ot_att_n = df_original [(df_original ['OverTime'] == 'Yes') & (df_original ['Prediction'] == 'Attrition')].shape[0]
#             recommendations.append(("🔴", "High", "Reduce Overtime Load",
#                 f"<strong>{ot_att_n} at-risk employees</strong> are on overtime. Redistribute workloads to bring OT headcount below 20%."))
 
#         if 'MonthlyIncome' in df_original .columns:
#             below_market = (df_original ['MonthlyIncome'] < 4000).sum()
#             recommendations.append(("🟠", "Medium", "Compensation Review",
#                 f"<strong>{below_market} employees</strong> earn below $4k/mo. Benchmark Level 1–2 roles against market rates immediately."))
 
#         if 'JobSatisfaction' in df_original .columns:
#             low_sat_n = (df_original ['JobSatisfaction'] <= 2).sum()
#             recommendations.append(("🟠", "Medium", "Engagement Program",
#                 f"<strong>{low_sat_n} employees</strong> have satisfaction ≤ 2. Launch pulse surveys and targeted 1:1 check-ins this quarter."))
 
#         if 'YearsAtCompany' in df_original .columns:
#             new_hires = (df_original ['YearsAtCompany'] < 3).sum()
#             recommendations.append(("🟡", "Low", "Onboarding Reinforcement",
#                 f"<strong>{new_hires} employees</strong> have under 3 years tenure. Assign mentors and strengthen the 90-day onboarding plan."))
 
#         if 'Department' in df_original .columns:
#             top_dept = (df_original [df_original ['Prediction'] == 'Attrition']
#                         .groupby('Department').size().idxmax())
#             recommendations.append(("🔴", "High", f"{top_dept} — Urgent Review",
#                 f"This department has the highest predicted attrition. Schedule an all-hands HR review and exit risk assessment."))
 
#         priority_color = {"High": "#dc2626", "Medium": "#d97706", "Low": "#059669"}
#         priority_bg    = {"High": "#fee2e2",  "Medium": "#fef3c7", "Low": "#d1fae5"}
 
#         rec_html = "".join([
#             f"""<div class="hrec-item">
#                     <div class="hrec-item-top">
#                         <span class="hrec-item-icon">{icon}</span>
#                         <span class="hrec-item-title">{title}</span>
#                         <span class="hrec-priority-pill" style="background:{priority_bg[priority]};color:{priority_color[priority]}">{priority}</span>
#                     </div>
#                     <div class="hrec-item-body">{body}</div>
#                 </div>"""
#             for icon, priority, title, body in recommendations
#         ])
 
#         st.markdown(f"""
#         <div class="section-hdr" style="margin-top:20px">
#             <span class="section-hdr-title">HR Recommendations</span>
#             <span class="section-hdr-sub">{len(recommendations)} action items identified</span>
#         </div>
#         <div class="hrec-grid">{rec_html}</div>
#         """, unsafe_allow_html=True)


#         # ================= DOWNLOAD =================

#         st.subheader("Export Results")

#         st.download_button(
#             "Download Predictions",
#             filtered_df.to_csv(index=False),
#             "attrition_results.csv"
#         )

# st.divider()

# st.caption(
# "HR Attrition Analytics Platform | Built with FastAPI & Streamlit"
# )









###########Final version 4.0
######
# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# st.set_page_config(
#     page_title="HR Attrition Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# st.markdown("""
# <style>

# /* ── Force dark mode base ── */
# html, body, [class*="css"] {
#     color-scheme: dark !important;
#     font-family: 'Inter', sans-serif !important;
# }

# /* Background */
# .stApp {
#     background: #0f1117 !important;
#     color: #e2e8f0 !important;
# }

# /* Main content area */
# .block-container {
#     padding: 1.5rem 2rem 4rem 2rem !important;
#     max-width: 100% !important;
# }

# /* ── Page title & text ── */
# h1, h2, h3,
# .stApp h1, .stApp h2, .stApp h3,
# [data-testid="stMarkdownContainer"] h1,
# [data-testid="stMarkdownContainer"] h2,
# [data-testid="stMarkdownContainer"] h3 {
#     color: #f1f5f9 !important;
# }
# .stApp p,
# [data-testid="stMarkdownContainer"] p {
#     color: #94a3b8 !important;
# }
# .stCaption, [data-testid="stCaptionContainer"] p {
#     color: #64748b !important;
# }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: #1e2130 !important;
#     border-right: 1px solid #2d3348 !important;
# }
# [data-testid="stSidebar"] * {
#     color: #cbd5e1 !important;
# }
# [data-testid="stSidebar"] h1,
# [data-testid="stSidebar"] h2,
# [data-testid="stSidebar"] h3 {
#     color: #f1f5f9 !important;
#     font-weight: 700 !important;
# }
# [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
#     color: #94a3b8 !important;
#     padding: 6px 10px !important;
#     border-radius: 7px !important;
#     font-size: 13px !important;
# }
# [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
#     background: #2d3348 !important;
# }

# /* Sidebar success/info boxes — brighter */
# [data-testid="stSidebar"] [data-testid="stAlert"] {
#     background: #1e3a5f !important;
#     border-color: #3b82f6 !important;
#     color: #93c5fd !important;
#     font-size: 13px !important;
#     font-weight: 600 !important;
# }
# [data-testid="stSidebar"] [data-testid="stAlert"] p {
#     color: #e2e8f0 !important;
#     font-size: 13px !important;
#     font-weight: 600 !important;
# }
# /* success alert in sidebar */
# [data-testid="stSidebar"] [data-testid="stAlert"][data-baseweb="notification"] {
#     color: #6ee7b7 !important;
# }

# /* ── Divider ── */
# hr {
#     border: none !important;
#     border-top: 1px solid #2d3348 !important;
# }

# /* ── Form labels ── */
# .stSlider label p,
# .stSelectbox label p,
# .stNumberInput label p,
# .stMultiSelect label p {
#     font-size: 11px !important;
#     font-weight: 600 !important;
#     text-transform: uppercase !important;
#     letter-spacing: 0.7px !important;
#     color: #64748b !important;
# }

# /* ── Selectbox — dark bg, light text ── */
# div[data-baseweb="select"] > div {
#     background-color: #1e2130 !important;
#     border: 1.5px solid #2d3348 !important;
#     border-radius: 9px !important;
#     color: #e2e8f0 !important;
#     font-size: 13px !important;
#     font-family: 'Inter', sans-serif !important;
#     min-height: 42px !important;
# }
# div[data-baseweb="select"] > div:hover {
#     border-color: #4f6ef7 !important;
# }
# div[data-baseweb="select"] > div:focus-within {
#     border-color: #4f6ef7 !important;
#     box-shadow: 0 0 0 3px rgba(79,110,247,0.18) !important;
# }
# div[data-baseweb="select"] span {
#     color: #e2e8f0 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
# }
# div[data-baseweb="select"] svg { fill: #64748b !important; }

# /* Dropdown list */
# [data-baseweb="popover"] [data-baseweb="menu"] {
#     background: #1e2130 !important;
#     border: 1px solid #2d3348 !important;
#     border-radius: 10px !important;
#     box-shadow: 0 8px 24px rgba(0,0,0,0.40) !important;
# }
# [data-baseweb="popover"] li {
#     font-size: 13px !important;
#     color: #e2e8f0 !important;
#     font-family: 'Inter', sans-serif !important;
# }
# [data-baseweb="popover"] li:hover {
#     background: #2d3348 !important;
# }
# [data-baseweb="popover"] li[aria-selected="true"] {
#     background: #1e3a6e !important;
#     color: #7c9ef5 !important;
#     font-weight: 600 !important;
# }

# /* ── Number input ── */
# .stNumberInput input {
#     background: #1e2130 !important;
#     border: 1.5px solid #2d3348 !important;
#     border-radius: 9px !important;
#     color: #e2e8f0 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     font-family: 'Inter', sans-serif !important;
#     height: 42px !important;
# }
# .stNumberInput input:focus {
#     border-color: #4f6ef7 !important;
#     box-shadow: 0 0 0 3px rgba(79,110,247,0.18) !important;
#     outline: none !important;
# }
# .stNumberInput button {
#     background: #2d3348 !important;
#     border: 1px solid #3d4563 !important;
#     color: #94a3b8 !important;
#     border-radius: 7px !important;
# }
# .stNumberInput button:hover {
#     background: #3d4563 !important;
# }

# /* ── Multi-select ── */
# [data-baseweb="tag"] {
#     background: #1e3a6e !important;
#     color: #7c9ef5 !important;
# }

# /* ── Slider ── */
# [data-testid="stSlider"] [role="slider"] {
#     background: #4f6ef7 !important;
#     border-color: #4f6ef7 !important;
# }
# [data-testid="stSlider"] [data-testid="stTickBarMin"],
# [data-testid="stSlider"] [data-testid="stTickBarMax"] {
#     color: #64748b !important;
# }

# /* ── Container border (st.container border=True) ── */
# [data-testid="stVerticalBlockBorderWrapper"] > div {
#     background: #1e2130 !important;
#     border: 1px solid #2d3348 !important;
#     border-radius: 14px !important;
#     padding: 20px !important;
# }

# /* ── Primary button ── */
# .stButton > button {
#     background: linear-gradient(135deg, #4f6ef7 0%, #3a56d4 100%) !important;
#     color: #ffffff !important;
#     border: none !important;
#     border-radius: 10px !important;
#     font-weight: 600 !important;
#     font-size: 14px !important;
#     padding: 12px 28px !important;
#     font-family: 'Inter', sans-serif !important;
#     box-shadow: 0 4px 14px rgba(79,110,247,0.30) !important;
#     transition: all .2s !important;
#     height: auto !important;
# }
# .stButton > button:hover {
#     opacity: 0.90 !important;
#     transform: translateY(-1px) !important;
#     box-shadow: 0 6px 20px rgba(79,110,247,0.45) !important;
# }

# /* ── Download button ── */
# .stDownloadButton > button {
#     background: transparent !important;
#     color: #7c9ef5 !important;
#     border: 1.5px solid #4f6ef7 !important;
#     border-radius: 9px !important;
#     font-weight: 500 !important;
#     box-shadow: none !important;
# }
# .stDownloadButton > button:hover {
#     background: #1e3a6e !important;
# }

# /* ── Metric ── */
# [data-testid="stMetric"] {
#     background: #1e2130 !important;
#     border: 1px solid #2d3348 !important;
#     border-radius: 12px !important;
#     padding: 16px 18px !important;
# }
# [data-testid="stMetricLabel"] p {
#     color: #64748b !important;
#     font-size: 11px !important;
#     font-weight: 600 !important;
#     text-transform: uppercase !important;
#     letter-spacing: 1px !important;
# }
# [data-testid="stMetricValue"] {
#     color: #f1f5f9 !important;
#     font-size: 24px !important;
#     font-weight: 700 !important;
# }

# /* ── File uploader — better aligned ── */
# [data-testid="stFileUploader"] {
#     background: #1e2130 !important;
#     border: 2px dashed #3d4563 !important;
#     border-radius: 12px !important;
#     padding: 4px !important;
# }
# [data-testid="stFileUploader"] * {
#     color: #94a3b8 !important;
# }
# [data-testid="stFileUploader"] section {
#     display: flex !important;
#     align-items: center !important;
#     justify-content: space-between !important;
#     gap: 16px !important;
# }
# [data-testid="stFileUploader"] button {
#     background: #2d3348 !important;
#     color: #e2e8f0 !important;
#     border: 1px solid #3d4563 !important;
#     border-radius: 8px !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     white-space: nowrap !important;
#     flex-shrink: 0 !important;
# }
# [data-testid="stFileUploader"]:hover {
#     border-color: #4f6ef7 !important;
# }

# /* ── Expander ── */
# .streamlit-expanderHeader {
#     background: #1e2130 !important;
#     border: 1px solid #2d3348 !important;
#     border-radius: 10px !important;
#     color: #e2e8f0 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
# }
# .streamlit-expanderContent {
#     background: #1e2130 !important;
#     border: 1px solid #2d3348 !important;
# }

# /* ── Dataframe ── */
# [data-testid="stDataFrame"] {
#     background: #1e2130 !important;
#     border-radius: 12px !important;
#     border: 1px solid #2d3348 !important;
#     overflow: hidden !important;
# }

# /* ── Spinner ── */
# .stSpinner > div { border-top-color: #4f6ef7 !important; }

# /* ── Subheaders — all bigger & brighter ── */
# [data-testid="stHeading"],
# [data-testid="stHeadingWithActionElements"],
# .stSubheader {
#     color: #f1f5f9 !important;
# }
# [data-testid="stHeadingWithActionElements"] h2,
# [data-testid="stHeading"] h2,
# .stApp h2 {
#     font-size: 22px !important;
#     font-weight: 700 !important;
#     color: #f1f5f9 !important;
#     letter-spacing: -0.3px !important;
# }
# .stApp h3 {
#     font-size: 18px !important;
#     font-weight: 700 !important;
#     color: #f1f5f9 !important;
# }

# /* ═══════════════════════════════════
#    CUSTOM HTML COMPONENT STYLES — DARK
#    ═══════════════════════════════════ */

# /* KPI row */
# .kpi-row {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 16px;
#     margin-top: 15px;
#     margin-bottom: 20px;
# }
# .kpi-card {
#     background: #1e2130;
#     padding: 22px;
#     border-radius: 14px;
#     border: 1px solid #2d3348;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.25);
#     position: relative;
#     overflow: hidden;
#     min-height: 130px;
#     display: flex;
#     flex-direction: column;
#     justify-content: space-between;
# }
# .kpi-card::after {
#     content: '';
#     position: absolute;
#     top: -12px; right: -12px;
#     width: 70px; height: 70px;
#     border-radius: 50%;
#     opacity: 0.10;
# }
# .kpi-label {
#     font-size: 13px;
#     font-weight: 700;
#     letter-spacing: 0.8px;
#     text-transform: uppercase;
#     color: #94a3b8;
#     margin-bottom: 10px;
# }
# .kpi-value {
#     font-size: 32px;
#     font-weight: 700;
#     line-height: 1;
#     margin-bottom: 10px;
# }
# .kpi-badge {
#     font-size: 11px;
#     padding: 4px 10px;
#     border-radius: 20px;
#     display: inline-block;
#     font-weight: 500;
# }
# .kpi-card.info .kpi-value   { color: #7c9ef5; }
# .kpi-card.info .kpi-badge   { background: #1e3a6e; color: #7c9ef5; }
# .kpi-card.info::after       { background: #4f6ef7; }
# .kpi-card.danger .kpi-value { color: #f87171; }
# .kpi-card.danger .kpi-badge { background: #3f1515; color: #f87171; }
# .kpi-card.danger::after     { background: #dc2626; }
# .kpi-card.warn .kpi-value   { color: #fbbf24; }
# .kpi-card.warn .kpi-badge   { background: #3d2b08; color: #fbbf24; }
# .kpi-card.warn::after       { background: #d97706; }
# .kpi-card.success .kpi-value { color: #34d399; }
# .kpi-card.success .kpi-badge { background: #0d3321; color: #34d399; }
# .kpi-card.success::after     { background: #059669; }

# /* Section header */
# .section-hdr {
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#     margin-top: 25px;
#     margin-bottom: 10px;
#     border-bottom: 1px solid #2d3348;
#     padding-bottom: 8px;
# }
# .section-hdr-title {
#     font-weight: 700;
#     font-size: 18px;
#     color: #f1f5f9;
# }
# .section-hdr-sub {
#     font-size: 13px;
#     color: #64748b;
# }

# /* Alerts */
# .alert-danger {
#     background: #2a1215;
#     border: 1px solid #7f1d1d;
#     border-left: 5px solid #dc2626;
#     padding: 13px 16px;
#     border-radius: 10px;
#     margin-bottom: 15px;
#     font-size: 13px;
#     color: #fca5a5;
#     font-weight: 500;
# }
# .alert-success {
#     background: #0d2818;
#     border: 1px solid #14532d;
#     border-left: 5px solid #16a34a;
#     padding: 13px 16px;
#     border-radius: 10px;
#     margin-bottom: 15px;
#     font-size: 13px;
#     color: #86efac;
#     font-weight: 500;
# }

# /* Topbar */
# .topbar {
#     background: #1e2130;
#     border: 1px solid #2d3348;
#     border-radius: 14px;
#     padding: 18px 24px;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     margin-bottom: 20px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.25);
# }
# .topbar h1 {
#     font-size: 18px;
#     font-weight: 700;
#     color: #f1f5f9 !important;
#     margin: 0 0 3px;
#     letter-spacing: -0.4px;
# }
# .topbar p {
#     font-size: 12px;
#     color: #64748b;
#     margin: 0;
#     font-family: 'JetBrains Mono', monospace;
# }
# .badge-active {
#     display: inline-flex;
#     align-items: center;
#     gap: 7px;
#     background: #0d2818;
#     color: #34d399;
#     font-size: 12px;
#     font-weight: 600;
#     padding: 6px 14px;
#     border-radius: 20px;
#     border: 1px solid #166534;
#     white-space: nowrap;
# }
# .badge-dot {
#     width: 7px; height: 7px;
#     border-radius: 50%;
#     background: #34d399;
#     box-shadow: 0 0 0 3px rgba(52,211,153,0.2);
#     display: inline-block;
# }

# /* Insight cards */
# .insight-grid {
#     display: grid;
#     grid-template-columns: 1fr 1fr;
#     gap: 12px;
#     margin-top: 10px;
# }
# .insight-item {
#     background: #1e2130;
#     border: 1px solid #2d3348;
#     border-radius: 12px;
#     padding: 16px;
#     display: flex;
#     gap: 12px;
#     align-items: flex-start;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.20);
#     transition: border-color .15s, box-shadow .15s;
# }
# .insight-item:hover {
#     border-color: #4f6ef7;
#     box-shadow: 0 3px 12px rgba(79,110,247,0.15);
# }
# .insight-item-icon { font-size: 26px; flex-shrink: 0; margin-top: 1px; }
# .insight-item-title {
#     font-size: 14px;
#     font-weight: 700;
#     color: #e2e8f0;
#     margin-bottom: 5px;
# }
# .insight-item-body {
#     font-size: 13.5px;
#     color: #94a3b8;
#     line-height: 1.6;
# }
# .insight-item-body strong { color: #7c9ef5; font-weight: 600; }

# /* HR recommendation cards */
# .hrec-grid {
#     display: grid;
#     grid-template-columns: 1fr 1fr;
#     gap: 14px;
#     margin-top: 10px;
# }
# .hrec-item {
#     background: #1e2130;
#     border: 1px solid #2d3348;
#     border-radius: 12px;
#     padding: 16px;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.20);
#     transition: border-color .15s, box-shadow .15s;
# }
# .hrec-item:hover {
#     border-color: #166534;
#     box-shadow: 0 3px 12px rgba(52,211,153,0.10);
# }
# .hrec-item-top {
#     display: flex;
#     align-items: center;
#     gap: 8px;
#     margin-bottom: 8px;
# }
# .hrec-item-icon  { font-size: 20px; flex-shrink: 0; }
# .hrec-item-title { font-size: 14.5px; font-weight: 700; color: #e2e8f0; flex: 1; }
# .hrec-item-body  { font-size: 13.5px; color: #94a3b8; line-height: 1.6; }
# .hrec-item-body strong { color: #e2e8f0; font-weight: 600; }
# .hrec-priority-pill {
#     font-size: 11px;
#     font-weight: 700;
#     text-transform: uppercase;
#     letter-spacing: .7px;
#     padding: 4px 10px;
#     border-radius: 20px;
#     flex-shrink: 0;
# }

# /* Prediction result cards */
# .result-card-high {
#     background: #1e2130;
#     border: 1.5px solid #7f1d1d;
#     border-left: 5px solid #dc2626;
#     padding: 24px;
#     border-radius: 14px;
#     box-shadow: 0 2px 10px rgba(220,38,38,0.12);
#     height: 100%;
#     min-height: 200px;
#     display: flex;
#     flex-direction: column;
#     justify-content: center;
# }
# .result-card-low {
#     background: #1e2130;
#     border: 1.5px solid #166534;
#     border-left: 5px solid #16a34a;
#     padding: 24px;
#     border-radius: 14px;
#     box-shadow: 0 2px 10px rgba(22,163,74,0.12);
#     height: 100%;
#     min-height: 200px;
#     display: flex;
#     flex-direction: column;
#     justify-content: center;
# }
# .result-prob {
#     font-size: 58px;
#     font-weight: 700;
#     font-family: 'JetBrains Mono', monospace;
#     letter-spacing: -2px;
#     line-height: 1;
# }
# .result-prob.high { color: #f87171; }
# .result-prob.low  { color: #34d399; }
# .result-label {
#     font-size: 12px;
#     color: #64748b;
#     margin-bottom: 10px;
#     text-transform: uppercase;
#     letter-spacing: .8px;
#     font-weight: 600;
# }
# .result-heading { font-size: 18px; font-weight: 700; color: #f1f5f9; margin-bottom: 6px; }
# .result-sub     { font-size: 13.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 12px; }
# .result-meta    { font-size: 13px; color: #64748b; }
# .result-meta strong { color: #e2e8f0; font-weight: 600; }

# .risk-pill {
#     display: inline-block;
#     padding: 6px 14px;
#     border-radius: 20px;
#     font-size: 12px;
#     font-weight: 700;
#     text-transform: uppercase;
#     letter-spacing: .8px;
# }
# .risk-pill.high { background: #3f1515; color: #f87171; }
# .risk-pill.med  { background: #3d2b08; color: #fbbf24; }
# .risk-pill.low  { background: #0d3321; color: #34d399; }

# /* Recommendation panel (prediction page) */
# .rec-panel {
#     background: #1e2130;
#     border: 1px solid #2d3348;
#     border-radius: 14px;
#     padding: 20px;
#     height: 100%;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.20);
# }
# .rec-panel-label {
#     font-size: 11px;
#     font-weight: 700;
#     text-transform: uppercase;
#     letter-spacing: .8px;
#     color: #64748b;
#     margin-bottom: 12px;
# }
# .rec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
# .rec-item {
#     background: #252b3b;
#     border: 1px solid #2d3348;
#     border-radius: 10px;
#     padding: 12px 14px;
#     font-size: 12px;
#     color: #94a3b8;
#     line-height: 1.5;
# }
# .rec-item strong { color: #e2e8f0; font-weight: 600; display: block; margin-bottom: 3px; }

# /* Footer */
# footer { visibility: hidden; }

# </style>
# """, unsafe_allow_html=True)

# st.title("HR Attrition Analytics Platform")
# st.caption("AI driven workforce analytics and attrition prediction system")
# st.divider()

# # Sidebar
# st.sidebar.title("Dashboard")
# page = st.sidebar.radio("Navigation", ["Prediction", "Analytics Dashboard"])
# st.sidebar.divider()
# st.sidebar.success("Model Active")
# st.sidebar.info("Algorithm: Logistic Regression")

# # Load model
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# model   = joblib.load(os.path.join(BASE_DIR, "models", "attrition_model.pkl"))
# scaler  = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
# columns = joblib.load(os.path.join(BASE_DIR, "models", "columns.pkl"))

# # ======================
# # SINGLE PREDICTION
# # ======================
# if page == "Prediction":

#     st.subheader("Employee Risk Prediction")

#     container = st.container(border=True)
#     with container:
#         col1, col2, col3, col4 = st.columns(4)
#         age       = col1.slider("Age", 18, 60, 30)
#         income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
#         job_level = col3.selectbox("Job Level", [1, 2, 3, 4, 5],
#                         format_func=lambda x: {1:"Entry",2:"Junior",3:"Mid",4:"Senior",5:"Director"}[x])
#         years     = col4.slider("Years at Company", 0, 40, 5)

#         col1, col2, col3, col4 = st.columns(4)
#         job_sat    = col1.selectbox("Job Satisfaction", [1, 2, 3, 4],
#                         format_func=lambda x: {1:"Very Low",2:"Low",3:"Medium",4:"High"}[x])
#         worklife   = col2.selectbox("Work-Life Balance", [1, 2, 3, 4],
#                         format_func=lambda x: {1:"Poor",2:"Fair",3:"Good",4:"Excellent"}[x])
#         overtime   = col3.selectbox("Overtime", ["No", "Yes"])
#         department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

#     st.markdown("<br>", unsafe_allow_html=True)
#     _, btn_col, _ = st.columns([4, 2, 4])
#     predict_clicked = btn_col.button("Run Risk Assessment →", use_container_width=True)

#     if predict_clicked:
#         with st.spinner("Analysing employee profile..."):
#             payload = {
#                 "Age": age, "DailyRate": 800, "DistanceFromHome": 5,
#                 "Education": 3, "EnvironmentSatisfaction": 3, "HourlyRate": 60,
#                 "JobInvolvement": 3, "JobLevel": job_level, "JobSatisfaction": job_sat,
#                 "MonthlyIncome": income, "MonthlyRate": 15000, "NumCompaniesWorked": 2,
#                 "PercentSalaryHike": 13, "PerformanceRating": 3, "RelationshipSatisfaction": 3,
#                 "StockOptionLevel": 1, "TotalWorkingYears": 10, "TrainingTimesLastYear": 2,
#                 "WorkLifeBalance": worklife, "YearsAtCompany": years, "YearsInCurrentRole": 3,
#                 "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 3,
#                 "BusinessTravel": "Travel_Rarely", "Department": department,
#                 "EducationField": "Life Sciences", "Gender": "Male",
#                 "JobRole": "Sales Executive", "MaritalStatus": "Single", "OverTime": overtime
#             }
#             try:
#                 resp        = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
#                 result      = resp.json()
#                 prediction  = result["Prediction"]
#                 probability = result["Probability"]
#                 risk_level  = result["Risk Level"]
#                 api_ok      = True
#             except Exception:
#                 api_ok = False

#         if not api_ok:
#             st.markdown('<div class="alert-danger">⚠ <strong>API Unavailable</strong> — Cannot reach FastAPI server at <code>localhost:8000</code>. Make sure your backend is running.</div>', unsafe_allow_html=True)
#         else:
#             is_high  = prediction == "Attrition Risk"
#             card_cls = "result-card-high" if is_high else "result-card-low"
#             prob_cls = "high" if is_high else "low"
#             pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
#             heading  = "⚠ High Attrition Risk" if is_high else "✓ Low Attrition Risk"
#             desc     = ("Multiple risk signals detected. Immediate HR intervention is recommended "
#                         "to retain this employee.") if is_high else \
#                        ("This profile appears stable. Continue regular check-ins "
#                         "and career development planning.")

#             c1, c2, c3 = st.columns([1, 1.6, 1.6])
#             with c1:
#                 st.markdown(f"""
#                 <div class="{card_cls}" style="text-align:center">
#                     <div class="result-label">Risk Probability</div>
#                     <div class="result-prob {prob_cls}">{probability}</div>
#                     <br><span class="risk-pill {pill_cls}">{risk_level} Risk</span>
#                 </div>""", unsafe_allow_html=True)

#             with c2:
#                 st.markdown(f"""
#                 <div class="{card_cls}">
#                     <div class="result-heading">{heading}</div>
#                     <div class="result-sub">{desc}</div>
#                     <div class="result-meta">
#                         <strong>Prediction:</strong> {prediction}<br>
#                         <strong>Risk Level:</strong> {risk_level}
#                     </div>
#                 </div>""", unsafe_allow_html=True)

#             with c3:
#                 recs = []
#                 if overtime == "Yes":
#                     recs.append(("Reduce Overtime", "Excessive overtime is the #1 driver of attrition in this model."))
#                 if job_sat <= 2:
#                     recs.append(("Satisfaction Review", "Schedule a 1:1 — low job satisfaction is a strong exit signal."))
#                 if income < 4000:
#                     recs.append(("Salary Benchmark", "Pay is below market. A compensation review is recommended."))
#                 if years < 3:
#                     recs.append(("Onboarding Support", "Early-tenure employees carry the highest flight risk."))
#                 if not recs:
#                     recs.append(("Maintain Engagement", "Profile is healthy. Keep regular check-ins and recognition."))

#                 rec_html = "".join([
#                     f'<div class="rec-item"><strong>{t}</strong>{d}</div>'
#                     for t, d in recs
#                 ])
#                 st.markdown(f"""
#                 <div class="rec-panel">
#                     <div class="rec-panel-label">HR Recommendations</div>
#                     <div class="rec-grid">{rec_html}</div>
#                 </div>""", unsafe_allow_html=True)

# # ======================
# # ANALYTICS DASHBOARD
# # ======================
# if page == "Analytics Dashboard":

#     st.markdown("""
#     <div class="topbar">
#         <div>
#             <h1>Workforce Analytics Dashboard</h1>
#             <p>Upload your HR dataset to generate predictions and insights</p>
#         </div>
#         <div class="badge-active"><span class="badge-dot"></span> Ready</div>
#     </div>
#     """, unsafe_allow_html=True)

#     file = st.file_uploader("Upload HR Dataset", type=["csv"])

#     if file:
#         df = pd.read_csv(file)

#         required_cols = ['Age', 'MonthlyIncome', 'Department']
#         missing = [c for c in required_cols if c not in df.columns]
#         for col in required_cols:
#             if col not in df.columns:
#                 missing.append(col)

#         if missing:
#             st.markdown(f'<div class="alert-danger">⚠ <strong>Missing columns:</strong> {", ".join(missing)}</div>', unsafe_allow_html=True)
#             st.stop()

#         st.subheader("Dataset Preview")
#         st.dataframe(df.head())

#         if model:
#             with st.spinner("Analyzing workforce data..."):
#                 df_original = df.copy()
#                 df_enc = pd.get_dummies(df)
#                 df_enc = df_enc.reindex(columns=columns, fill_value=0)
#                 df_sc  = scaler.transform(df_enc)
#                 df_original['Prediction'] = model.predict(df_sc)
#                 df_original['Probability'] = model.predict_proba(df_sc)[:, 1]
#                 df_original['Prediction'] = df_original['Prediction'].map({0: "No Attrition", 1: "Attrition"})

#         att_count = (df_original['Prediction'] == "Attrition").sum()
#         att_rate  = (df_original['Prediction'] == "Attrition").mean() * 100
#         avg_sal   = int(df_original['MonthlyIncome'].mean())
#         avg_risk  = df_original['Probability'].mean() * 100

#         if att_count > 50:
#             st.markdown(f'<div class="alert-danger">🔴 <strong>High Attrition Risk:</strong> {att_count} employees ({att_rate:.1f}%) are predicted to leave. Immediate action required.</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="alert-success">✅ <strong>Workforce Stable:</strong> Attrition is within an acceptable range — {att_count} employees ({att_rate:.1f}%).</div>', unsafe_allow_html=True)

#         # ================= KPI SUMMARY =================
#         st.markdown(f"""
#         <div class="kpi-row">
#             <div class="kpi-card info">
#                 <div class="kpi-label">Total Employees</div>
#                 <div class="kpi-value">{len(df_original):,}</div>
#                 <span class="kpi-badge">Loaded</span>
#             </div>
#             <div class="kpi-card danger">
#                 <div class="kpi-label">Attrition Count</div>
#                 <div class="kpi-value">{att_count:,}</div>
#                 <span class="kpi-badge">↑ Predicted</span>
#             </div>
#             <div class="kpi-card warn">
#                 <div class="kpi-label">Attrition Rate</div>
#                 <div class="kpi-value">{att_rate:.1f}%</div>
#                 <span class="kpi-badge">Avg risk {avg_risk:.0f}%</span>
#             </div>
#             <div class="kpi-card success">
#                 <div class="kpi-label">Avg Monthly Income</div>
#                 <div class="kpi-value">${avg_sal:,}</div>
#                 <span class="kpi-badge">Per employee</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # ================= FILTERS + DATASET HEALTH SIDE BY SIDE =================
#         col_left, col_right = st.columns(2)

#         with col_left:
#             st.subheader("Filters")
#             dept_filter = st.multiselect(
#                 "Department",
#                 df_original['Department'].unique(),
#                 default=df_original['Department'].unique()
#             )

#         filtered_df = df_original[df_original['Department'].isin(dept_filter)]

#         with col_right:
#             st.subheader("Dataset Health")
#             h1, h2 = st.columns(2)
#             h1.metric("Missing Values", filtered_df.isnull().sum().sum())
#             h2.metric("Features", filtered_df.shape[1])

#         st.divider()

#         # ================= CHARTS =================
#         st.subheader("Workforce Insights")

#         DARK_PLOT = dict(
#             paper_bgcolor="rgba(0,0,0,0)",
#             plot_bgcolor="rgba(0,0,0,0)",
#             font=dict(family="Inter, sans-serif", color="#94a3b8", size=13),
#             margin=dict(l=4, r=4, t=50, b=4),
#             xaxis=dict(gridcolor="#2d3348", linecolor="#2d3348", showgrid=False, tickfont=dict(color="#64748b", size=12)),
#             yaxis=dict(gridcolor="#2d3348", linecolor="#2d3348", tickfont=dict(color="#64748b", size=12)),
#             hoverlabel=dict(bgcolor="#1e2130", font_size=13, bordercolor="#2d3348", font_color="#e2e8f0"),
#         )

#         col1, col2 = st.columns(2)
#         fig = px.histogram(filtered_df, x="Prediction", color="Prediction",
#             title="Attrition Distribution",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig.update_layout(**DARK_PLOT, showlegend=False, title_font=dict(color="#f1f5f9", size=16, family="Inter"))
#         fig.update_traces(marker_line_width=0)
#         col1.plotly_chart(fig, use_container_width=True)

#         fig2 = px.box(filtered_df, x="Prediction", y="MonthlyIncome", color="Prediction",
#             title="Income Impact",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig2.update_layout(**DARK_PLOT, showlegend=False, title_font=dict(color="#f1f5f9", size=16, family="Inter"))
#         col2.plotly_chart(fig2, use_container_width=True)

#         col3, col4 = st.columns(2)
#         fig3 = px.histogram(filtered_df, x="Department", color="Prediction",
#             title="Department Impact",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#7c9ef5"})
#         fig3.update_layout(**DARK_PLOT, title_font=dict(color="#f1f5f9", size=16, family="Inter"),
#             legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1,
#                         font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
#         fig3.update_traces(marker_line_width=0)
#         col3.plotly_chart(fig3, use_container_width=True)

#         fig4 = px.pie(filtered_df, names="Prediction", title="Risk Breakdown",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig4.update_layout(**DARK_PLOT, title_font=dict(color="#f1f5f9", size=16, family="Inter"),
#             legend=dict(font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
#         fig4.update_traces(textfont_color="#f1f5f9", textfont_size=13)
#         col4.plotly_chart(fig4, use_container_width=True)

#         # ================= HIGH RISK TABLE =================
#         st.subheader("Top High Risk Employees")
#         high_risk = filtered_df[filtered_df['Prediction'] == "Attrition"] \
#             .sort_values("Probability", ascending=False).head(10)
#         st.dataframe(high_risk, use_container_width=True, hide_index=True)

#         with st.expander("View Full Prediction Data"):
#             st.dataframe(df_original, use_container_width=True, hide_index=True)

#         # ================= INSIGHTS =================
#         insights = []

#         if 'OverTime' in df_original.columns:
#             ot_att  = df_original[df_original['OverTime'] == 'Yes']['Prediction'].eq('Attrition').mean() * 100
#             not_att = df_original[df_original['OverTime'] == 'No']['Prediction'].eq('Attrition').mean() * 100
#             lift    = ot_att - not_att
#             insights.append(("📊", "Overtime Impact",
#                 f"{ot_att:.1f}% attrition among overtime employees vs {not_att:.1f}% for others — a <strong>{lift:.1f}pp lift</strong>."))

#         if 'MonthlyIncome' in df_original.columns:
#             low_sal = df_original[df_original['MonthlyIncome'] < 4000]['Prediction'].eq('Attrition').mean() * 100
#             hi_sal  = df_original[df_original['MonthlyIncome'] >= 4000]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("💰", "Salary Band Risk",
#                 f"Employees earning &lt;$4k/mo have <strong>{low_sal:.1f}%</strong> attrition vs {hi_sal:.1f}% for higher earners."))

#         if 'JobSatisfaction' in df_original.columns:
#             low_js = df_original[df_original['JobSatisfaction'] <= 2]['Prediction'].eq('Attrition').mean() * 100
#             hi_js  = df_original[df_original['JobSatisfaction'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("😔", "Satisfaction vs Retention",
#                 f"Low satisfaction (≤2) employees show <strong>{low_js:.1f}%</strong> attrition vs {hi_js:.1f}% for satisfied staff."))

#         if 'YearsAtCompany' in df_original.columns:
#             early  = df_original[df_original['YearsAtCompany'] < 3]['Prediction'].eq('Attrition').mean() * 100
#             senior = df_original[df_original['YearsAtCompany'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🕐", "Early Tenure Risk",
#                 f"Employees with &lt;3 years tenure have <strong>{early:.1f}%</strong> predicted attrition vs {senior:.1f}% for veterans."))

#         if 'Department' in df_original.columns:
#             top_dept = (df_original[df_original['Prediction'] == 'Attrition']
#                         .groupby('Department').size().idxmax())
#             top_pct  = df_original[df_original['Department'] == top_dept]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🏢", "Highest-Risk Department",
#                 f"<strong>{top_dept}</strong> has the most predicted attrition at <strong>{top_pct:.1f}%</strong> of its headcount."))

#         if 'WorkLifeBalance' in df_original.columns:
#             poor_wlb = df_original[df_original['WorkLifeBalance'] == 1]['Prediction'].eq('Attrition').mean() * 100
#             good_wlb = df_original[df_original['WorkLifeBalance'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("⚖️", "Work-Life Balance",
#                 f"Poor WLB (score 1): <strong>{poor_wlb:.1f}%</strong> attrition vs {good_wlb:.1f}% for good WLB."))

#         insight_html = "".join([
#             f"""<div class="insight-item">
#                     <div class="insight-item-icon">{icon}</div>
#                     <div>
#                         <div class="insight-item-title">{title}</div>
#                         <div class="insight-item-body">{body}</div>
#                     </div>
#                 </div>"""
#             for icon, title, body in insights
#         ])
#         st.markdown(f"""
#         <div class="section-hdr" style="margin-top:4px">
#             <span class="section-hdr-title">Key Insights</span>
#             <span class="section-hdr-sub">Derived from your dataset · {len(insights)} findings</span>
#         </div>
#         <div class="insight-grid">{insight_html}</div>
#         """, unsafe_allow_html=True)

#         # ================= RECOMMENDATIONS =================
#         recommendations = []

#         if 'OverTime' in df_original.columns:
#             ot_att_n = df_original[(df_original['OverTime'] == 'Yes') & (df_original['Prediction'] == 'Attrition')].shape[0]
#             recommendations.append(("🔴", "High", "Reduce Overtime Load",
#                 f"<strong>{ot_att_n} at-risk employees</strong> are on overtime. Redistribute workloads to bring OT headcount below 20%."))

#         if 'MonthlyIncome' in df_original.columns:
#             below_market = (df_original['MonthlyIncome'] < 4000).sum()
#             recommendations.append(("🟠", "Medium", "Compensation Review",
#                 f"<strong>{below_market} employees</strong> earn below $4k/mo. Benchmark Level 1–2 roles against market rates immediately."))

#         if 'JobSatisfaction' in df_original.columns:
#             low_sat_n = (df_original['JobSatisfaction'] <= 2).sum()
#             recommendations.append(("🟠", "Medium", "Engagement Program",
#                 f"<strong>{low_sat_n} employees</strong> have satisfaction ≤ 2. Launch pulse surveys and targeted 1:1 check-ins this quarter."))

#         if 'YearsAtCompany' in df_original.columns:
#             new_hires = (df_original['YearsAtCompany'] < 3).sum()
#             recommendations.append(("🟡", "Low", "Onboarding Reinforcement",
#                 f"<strong>{new_hires} employees</strong> have under 3 years tenure. Assign mentors and strengthen the 90-day onboarding plan."))

#         if 'Department' in df_original.columns:
#             top_dept = (df_original[df_original['Prediction'] == 'Attrition']
#                         .groupby('Department').size().idxmax())
#             recommendations.append(("🔴", "High", f"{top_dept} — Urgent Review",
#                 f"This department has the highest predicted attrition. Schedule an all-hands HR review and exit risk assessment."))

#         priority_color = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
#         priority_bg    = {"High": "#3f1515",  "Medium": "#3d2b08", "Low": "#0d3321"}

#         rec_html = "".join([
#             f"""<div class="hrec-item">
#                     <div class="hrec-item-top">
#                         <span class="hrec-item-icon">{icon}</span>
#                         <span class="hrec-item-title">{title}</span>
#                         <span class="hrec-priority-pill" style="background:{priority_bg[priority]};color:{priority_color[priority]}">{priority}</span>
#                     </div>
#                     <div class="hrec-item-body">{body}</div>
#                 </div>"""
#             for icon, priority, title, body in recommendations
#         ])
#         st.markdown(f"""
#         <div class="section-hdr" style="margin-top:20px">
#             <span class="section-hdr-title">HR Recommendations</span>
#             <span class="section-hdr-sub">{len(recommendations)} action items identified</span>
#         </div>
#         <div class="hrec-grid">{rec_html}</div>
#         """, unsafe_allow_html=True)

#         # ================= DOWNLOAD =================
#         st.subheader("Export Results")
#         st.download_button(
#             "⬇ Download Predictions",
#             filtered_df.to_csv(index=False),
#             "attrition_results.csv"
#         )

# st.divider()
# st.caption("HR Attrition Analytics Platform | Built with FastAPI & Streamlit")

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import joblib
import os

st.set_page_config(
    page_title="HR Attrition Analytics",
    page_icon="📊",
    layout="wide"
)

# ─────────────────────────────────────────────
# LOAD CSS FROM SEPARATE FILE
# Edit styles.css to change any UI styling.
# Each section in that file has a clear heading
# telling you exactly which component it controls.
# ─────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.title("HR Attrition Analytics Platform")
st.caption("AI driven workforce analytics and attrition prediction system")
st.divider()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("Dashboard")
page = st.sidebar.radio("Navigation", ["Prediction", "Analytics Dashboard"])
st.sidebar.divider()
st.sidebar.success("Model Active")
st.sidebar.info("Algorithm: Logistic Regression")


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model   = joblib.load(os.path.join(BASE_DIR, "models", "attrition_model.pkl"))
scaler  = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
columns = joblib.load(os.path.join(BASE_DIR, "models", "columns.pkl"))


# ─────────────────────────────────────────────
# PLOTLY DARK THEME  (shared across all charts)
# To change chart appearance edit these values.
# ─────────────────────────────────────────────
DARK_PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=13),
    margin=dict(l=4, r=4, t=50, b=4),
    xaxis=dict(
        gridcolor="#2d3348", linecolor="#2d3348",
        showgrid=False, tickfont=dict(color="#64748b", size=12)
    ),
    yaxis=dict(
        gridcolor="#2d3348", linecolor="#2d3348",
        tickfont=dict(color="#64748b", size=12)
    ),
    hoverlabel=dict(
        bgcolor="#1e2130", font_size=13,
        bordercolor="#2d3348", font_color="#e2e8f0"
    ),
)


# ══════════════════════════════════════════════
# PAGE: PREDICTION
# ══════════════════════════════════════════════
if page == "Prediction":

    st.subheader("Employee Risk Prediction")

    # ── Input form ──────────────────────────
    container = st.container(border=True)
    with container:
        col1, col2, col3, col4 = st.columns(4)
        age       = col1.slider("Age", 18, 60, 30)
        income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
        job_level = col3.selectbox(
            "Job Level", [1, 2, 3, 4, 5],
            format_func=lambda x: {1:"Entry", 2:"Junior", 3:"Mid", 4:"Senior", 5:"Director"}[x]
        )
        years = col4.slider("Years at Company", 0, 40, 5)

        col1, col2, col3, col4 = st.columns(4)
        job_sat    = col1.selectbox(
            "Job Satisfaction", [1, 2, 3, 4],
            format_func=lambda x: {1:"Very Low", 2:"Low", 3:"Medium", 4:"High"}[x]
        )
        worklife   = col2.selectbox(
            "Work-Life Balance", [1, 2, 3, 4],
            format_func=lambda x: {1:"Poor", 2:"Fair", 3:"Good", 4:"Excellent"}[x]
        )
        overtime   = col3.selectbox("Overtime", ["No", "Yes"])
        department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([4, 2, 4])
    predict_clicked = btn_col.button("Run Risk Assessment →", use_container_width=True)

    # ── Run prediction ───────────────────────
    if predict_clicked:
        with st.spinner("Analysing employee profile..."):
            payload = {
                "Age": age, "DailyRate": 800, "DistanceFromHome": 5,
                "Education": 3, "EnvironmentSatisfaction": 3, "HourlyRate": 60,
                "JobInvolvement": 3, "JobLevel": job_level, "JobSatisfaction": job_sat,
                "MonthlyIncome": income, "MonthlyRate": 15000, "NumCompaniesWorked": 2,
                "PercentSalaryHike": 13, "PerformanceRating": 3, "RelationshipSatisfaction": 3,
                "StockOptionLevel": 1, "TotalWorkingYears": 10, "TrainingTimesLastYear": 2,
                "WorkLifeBalance": worklife, "YearsAtCompany": years, "YearsInCurrentRole": 3,
                "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 3,
                "BusinessTravel": "Travel_Rarely", "Department": department,
                "EducationField": "Life Sciences", "Gender": "Male",
                "JobRole": "Sales Executive", "MaritalStatus": "Single", "OverTime": overtime
            }
            try:
                resp        = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
                result      = resp.json()
                prediction  = result["Prediction"]
                probability = result["Probability"]
                risk_level  = result["Risk Level"]
                api_ok      = True
            except Exception:
                api_ok = False

        if not api_ok:
            st.markdown(
                '<div class="alert-danger">⚠ <strong>API Unavailable</strong> — '
                'Cannot reach FastAPI server at <code>localhost:8000</code>. '
                'Make sure your backend is running.</div>',
                unsafe_allow_html=True
            )
        else:
            # ── Determine card style based on result
            is_high  = prediction == "Attrition Risk"
            card_cls = "result-card-high" if is_high else "result-card-low"
            prob_cls = "high" if is_high else "low"
            pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
            heading  = "⚠ High Attrition Risk" if is_high else "✓ Low Attrition Risk"
            desc     = (
                "Multiple risk signals detected. Immediate HR intervention is recommended "
                "to retain this employee."
            ) if is_high else (
                "This profile appears stable. Continue regular check-ins "
                "and career development planning."
            )

            # ── Result: 3 columns
            c1, c2, c3 = st.columns([1, 1.6, 1.6])

            # Col 1 — probability score
            with c1:
                st.markdown(f"""
                <div class="{card_cls}" style="text-align:center">
                    <div class="result-label">Risk Probability</div>
                    <div class="result-prob {prob_cls}">{probability}</div>
                    <br><span class="risk-pill {pill_cls}">{risk_level} Risk</span>
                </div>""", unsafe_allow_html=True)

            # Col 2 — heading + description
            with c2:
                st.markdown(f"""
                <div class="{card_cls}">
                    <div class="result-heading">{heading}</div>
                    <div class="result-sub">{desc}</div>
                    <div class="result-meta">
                        <strong>Prediction:</strong> {prediction}<br>
                        <strong>Risk Level:</strong> {risk_level}
                    </div>
                </div>""", unsafe_allow_html=True)

            # Col 3 — HR recommendations
            with c3:
                recs = []
                if overtime == "Yes":
                    recs.append(("Reduce Overtime",
                                 "Excessive overtime is the #1 driver of attrition in this model."))
                if job_sat <= 2:
                    recs.append(("Satisfaction Review",
                                 "Schedule a 1:1 — low job satisfaction is a strong exit signal."))
                if income < 4000:
                    recs.append(("Salary Benchmark",
                                 "Pay is below market. A compensation review is recommended."))
                if years < 3:
                    recs.append(("Onboarding Support",
                                 "Early-tenure employees carry the highest flight risk."))
                if not recs:
                    recs.append(("Maintain Engagement",
                                 "Profile is healthy. Keep regular check-ins and recognition."))

                rec_html = "".join([
                    f'<div class="rec-item"><strong>{t}</strong>{d}</div>'
                    for t, d in recs
                ])
                st.markdown(f"""
                <div class="rec-panel">
                    <div class="rec-panel-label">HR Recommendations</div>
                    <div class="rec-grid">{rec_html}</div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: ANALYTICS DASHBOARD
# ══════════════════════════════════════════════
if page == "Analytics Dashboard":

    # ── Top bar ─────────────────────────────
    st.markdown("""
    <div class="topbar">
        <div>
            <h1>Workforce Analytics Dashboard</h1>
            <p>Upload your HR dataset to generate predictions and insights</p>
        </div>
        <div class="badge-active"><span class="badge-dot"></span> Ready</div>
    </div>
    """, unsafe_allow_html=True)

    # ── File upload ──────────────────────────
    file = st.file_uploader("Upload HR Dataset", type=["csv"])

    if file:
        df = pd.read_csv(file)

        # Validate required columns
        required_cols = ['Age', 'MonthlyIncome', 'Department']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.markdown(
                f'<div class="alert-danger">⚠ <strong>Missing columns:</strong> {", ".join(missing)}</div>',
                unsafe_allow_html=True
            )
            st.stop()

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True, hide_index=True)

        # ── Run model predictions ─────────────
        if model:
            with st.spinner("Analyzing workforce data..."):
                df_original = df.copy()
                df_enc = pd.get_dummies(df)
                df_enc = df_enc.reindex(columns=columns, fill_value=0)
                df_sc  = scaler.transform(df_enc)
                df_original['Prediction'] = model.predict(df_sc)
                df_original['Probability'] = model.predict_proba(df_sc)[:, 1]
                df_original['Prediction'] = df_original['Prediction'].map(
                    {0: "No Attrition", 1: "Attrition"}
                )

        # ── Summary stats ────────────────────
        att_count = (df_original['Prediction'] == "Attrition").sum()
        att_rate  = (df_original['Prediction'] == "Attrition").mean() * 100
        avg_sal   = int(df_original['MonthlyIncome'].mean())
        avg_risk  = df_original['Probability'].mean() * 100

        # ── Alert banner ─────────────────────
        if att_count > 50:
            st.markdown(
                f'<div class="alert-danger">🔴 <strong>High Attrition Risk:</strong> '
                f'{att_count} employees ({att_rate:.1f}%) are predicted to leave. '
                f'Immediate action required.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="alert-success">✅ <strong>Workforce Stable:</strong> '
                f'Attrition is within an acceptable range — '
                f'{att_count} employees ({att_rate:.1f}%).</div>',
                unsafe_allow_html=True
            )

        # ── KPI Cards ────────────────────────
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card info">
                <div class="kpi-label">Total Employees</div>
                <div class="kpi-value">{len(df_original):,}</div>
                <span class="kpi-badge">Loaded</span>
            </div>
            <div class="kpi-card danger">
                <div class="kpi-label">Attrition Count</div>
                <div class="kpi-value">{att_count:,}</div>
                <span class="kpi-badge">↑ Predicted</span>
            </div>
            <div class="kpi-card warn">
                <div class="kpi-label">Attrition Rate</div>
                <div class="kpi-value">{att_rate:.1f}%</div>
                <span class="kpi-badge">Avg risk {avg_risk:.0f}%</span>
            </div>
            <div class="kpi-card success">
                <div class="kpi-label">Avg Monthly Income</div>
                <div class="kpi-value">${avg_sal:,}</div>
                <span class="kpi-badge">Per employee</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Dataset Health (standalone, compact) ──
        st.markdown("""
        <div class="section-hdr" style="margin-top:10px">
            <span class="section-hdr-title">Dataset Health</span>
        </div>
        """, unsafe_allow_html=True)
        h1, h2 = st.columns(2)
        h1.metric("Missing Values", df_original.isnull().sum().sum())
        h2.metric("Features", df_original.shape[1])

        st.divider()

        # ── Workforce Insights heading + inline Department filter ──
        ins_col, filt_col = st.columns([1, 1])
        with ins_col:
            st.markdown("""
            <div class="workforce-heading">
                <div class="workforce-heading-title">Workforce Insights</div>
                <div class="workforce-heading-sub">Charts filtered by department selection</div>
            </div>
            """, unsafe_allow_html=True)
        with filt_col:
            st.markdown("""
            <div style="font-size:10px;font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;color:#3d4563;margin-bottom:4px;
                        font-family:'JetBrains Mono',monospace;">
                Filter by Department
            </div>
            """, unsafe_allow_html=True)
            dept_filter = st.multiselect(
                "Filter by Department",
                df_original['Department'].unique(),
                default=df_original['Department'].unique(),
                label_visibility="collapsed",
                placeholder="All departments"
            )

        filtered_df = df_original[df_original['Department'].isin(dept_filter)]

        col1, col2 = st.columns(2)

        fig = px.histogram(filtered_df, x="Prediction", color="Prediction",
            title="Attrition Distribution",
            color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
        fig.update_layout(**DARK_PLOT, showlegend=False,
                          title_font=dict(color="#f1f5f9", size=16, family="Inter"))
        fig.update_traces(marker_line_width=0)
        col1.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(filtered_df, x="Prediction", y="MonthlyIncome", color="Prediction",
            title="Income Impact",
            color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
        fig2.update_layout(**DARK_PLOT, showlegend=False,
                           title_font=dict(color="#f1f5f9", size=16, family="Inter"))
        col2.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)

        fig3 = px.histogram(filtered_df, x="Department", color="Prediction",
            title="Department Impact",
            color_discrete_map={"Attrition": "#f87171", "No Attrition": "#7c9ef5"})
        fig3.update_layout(**DARK_PLOT,
            title_font=dict(color="#f1f5f9", size=16, family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1,
                        font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
        fig3.update_traces(marker_line_width=0)
        col3.plotly_chart(fig3, use_container_width=True)

        fig4 = px.pie(filtered_df, names="Prediction", title="Risk Breakdown",
            color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
        fig4.update_layout(**DARK_PLOT,
            title_font=dict(color="#f1f5f9", size=16, family="Inter"),
            legend=dict(font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
        fig4.update_traces(textfont_color="#f1f5f9", textfont_size=13)
        col4.plotly_chart(fig4, use_container_width=True)

        # ── High Risk Table ───────────────────
        st.subheader("Top High Risk Employees")
        high_risk = (
            filtered_df[filtered_df['Prediction'] == "Attrition"]
            .sort_values("Probability", ascending=False)
            .head(10)
        )
        st.dataframe(high_risk, use_container_width=True, hide_index=True)

        with st.expander("View Full Prediction Data"):
            st.dataframe(df_original, use_container_width=True, hide_index=True)

        # ── Key Insights ─────────────────────
        insights = []

        if 'OverTime' in df_original.columns:
            ot_att  = df_original[df_original['OverTime'] == 'Yes']['Prediction'].eq('Attrition').mean() * 100
            not_att = df_original[df_original['OverTime'] == 'No']['Prediction'].eq('Attrition').mean() * 100
            lift    = ot_att - not_att
            insights.append(("📊", "Overtime Impact",
                f"{ot_att:.1f}% attrition among overtime employees vs {not_att:.1f}% "
                f"for others — a <strong>{lift:.1f}pp lift</strong>."))

        if 'MonthlyIncome' in df_original.columns:
            low_sal = df_original[df_original['MonthlyIncome'] < 4000]['Prediction'].eq('Attrition').mean() * 100
            hi_sal  = df_original[df_original['MonthlyIncome'] >= 4000]['Prediction'].eq('Attrition').mean() * 100
            insights.append(("💰", "Salary Band Risk",
                f"Employees earning &lt;$4k/mo have <strong>{low_sal:.1f}%</strong> "
                f"attrition vs {hi_sal:.1f}% for higher earners."))

        if 'JobSatisfaction' in df_original.columns:
            low_js = df_original[df_original['JobSatisfaction'] <= 2]['Prediction'].eq('Attrition').mean() * 100
            hi_js  = df_original[df_original['JobSatisfaction'] >= 3]['Prediction'].eq('Attrition').mean() * 100
            insights.append(("😔", "Satisfaction vs Retention",
                f"Low satisfaction (≤2) employees show <strong>{low_js:.1f}%</strong> "
                f"attrition vs {hi_js:.1f}% for satisfied staff."))

        if 'YearsAtCompany' in df_original.columns:
            early  = df_original[df_original['YearsAtCompany'] < 3]['Prediction'].eq('Attrition').mean() * 100
            senior = df_original[df_original['YearsAtCompany'] >= 3]['Prediction'].eq('Attrition').mean() * 100
            insights.append(("🕐", "Early Tenure Risk",
                f"Employees with &lt;3 years tenure have <strong>{early:.1f}%</strong> "
                f"predicted attrition vs {senior:.1f}% for veterans."))

        if 'Department' in df_original.columns:
            top_dept = (df_original[df_original['Prediction'] == 'Attrition']
                        .groupby('Department').size().idxmax())
            top_pct  = df_original[df_original['Department'] == top_dept]['Prediction'].eq('Attrition').mean() * 100
            insights.append(("🏢", "Highest-Risk Department",
                f"<strong>{top_dept}</strong> has the most predicted attrition "
                f"at <strong>{top_pct:.1f}%</strong> of its headcount."))

        if 'WorkLifeBalance' in df_original.columns:
            poor_wlb = df_original[df_original['WorkLifeBalance'] == 1]['Prediction'].eq('Attrition').mean() * 100
            good_wlb = df_original[df_original['WorkLifeBalance'] >= 3]['Prediction'].eq('Attrition').mean() * 100
            insights.append(("⚖️", "Work-Life Balance",
                f"Poor WLB (score 1): <strong>{poor_wlb:.1f}%</strong> "
                f"attrition vs {good_wlb:.1f}% for good WLB."))

        insight_html = "".join([
            f"""<div class="insight-item">
                    <div class="insight-item-icon">{icon}</div>
                    <div>
                        <div class="insight-item-title">{title}</div>
                        <div class="insight-item-body">{body}</div>
                    </div>
                </div>"""
            for icon, title, body in insights
        ])
        st.markdown(f"""
        <div class="section-hdr" style="margin-top:4px">
            <span class="section-hdr-title">Key Insights</span>
            <span class="section-hdr-sub">Derived from your dataset · {len(insights)} findings</span>
        </div>
        <div class="insight-grid">{insight_html}</div>
        """, unsafe_allow_html=True)

        # ── HR Recommendations ────────────────
        recommendations = []

        if 'OverTime' in df_original.columns:
            ot_att_n = df_original[
                (df_original['OverTime'] == 'Yes') &
                (df_original['Prediction'] == 'Attrition')
            ].shape[0]
            recommendations.append(("🔴", "High", "Reduce Overtime Load",
                f"<strong>{ot_att_n} at-risk employees</strong> are on overtime. "
                f"Redistribute workloads to bring OT headcount below 20%."))

        if 'MonthlyIncome' in df_original.columns:
            below_market = (df_original['MonthlyIncome'] < 4000).sum()
            recommendations.append(("🟠", "Medium", "Compensation Review",
                f"<strong>{below_market} employees</strong> earn below $4k/mo. "
                f"Benchmark Level 1–2 roles against market rates immediately."))

        if 'JobSatisfaction' in df_original.columns:
            low_sat_n = (df_original['JobSatisfaction'] <= 2).sum()
            recommendations.append(("🟠", "Medium", "Engagement Program",
                f"<strong>{low_sat_n} employees</strong> have satisfaction ≤ 2. "
                f"Launch pulse surveys and targeted 1:1 check-ins this quarter."))

        if 'YearsAtCompany' in df_original.columns:
            new_hires = (df_original['YearsAtCompany'] < 3).sum()
            recommendations.append(("🟡", "Low", "Onboarding Reinforcement",
                f"<strong>{new_hires} employees</strong> have under 3 years tenure. "
                f"Assign mentors and strengthen the 90-day onboarding plan."))

        if 'Department' in df_original.columns:
            top_dept = (df_original[df_original['Prediction'] == 'Attrition']
                        .groupby('Department').size().idxmax())
            recommendations.append(("🔴", "High", f"{top_dept} — Urgent Review",
                f"This department has the highest predicted attrition. "
                f"Schedule an all-hands HR review and exit risk assessment."))

        priority_color = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
        priority_bg    = {"High": "#3f1515",  "Medium": "#3d2b08", "Low": "#0d3321"}

        rec_html = "".join([
            f"""<div class="hrec-item">
                    <div class="hrec-item-top">
                        <span class="hrec-item-icon">{icon}</span>
                        <span class="hrec-item-title">{title}</span>
                        <span class="hrec-priority-pill"
                              style="background:{priority_bg[priority]};
                                     color:{priority_color[priority]}">{priority}</span>
                    </div>
                    <div class="hrec-item-body">{body}</div>
                </div>"""
            for icon, priority, title, body in recommendations
        ])
        st.markdown(f"""
        <div class="section-hdr" style="margin-top:20px">
            <span class="section-hdr-title">HR Recommendations</span>
            <span class="section-hdr-sub">{len(recommendations)} action items identified</span>
        </div>
        <div class="hrec-grid">{rec_html}</div>
        """, unsafe_allow_html=True)

        # ── Export ────────────────────────────
        st.subheader("Export Results")
        st.download_button(
            "⬇ Download Predictions",
            filtered_df.to_csv(index=False),
            "attrition_results.csv"
        )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption("HR Attrition Analytics Platform | Built with FastAPI & Streamlit")