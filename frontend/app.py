# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px
# import joblib
# import os

# st.set_page_config(
#     page_title="PeopleIQ | AI Workforce Intelligence",
#     page_icon="🧠",
#     layout="wide"
# )

# # ─────────────────────────────────────────────
# # LOAD CSS FROM SEPARATE FILE
# # Edit styles.css to change any UI styling.
# # Each section in that file has a clear heading
# # telling you exactly which component it controls.
# # ─────────────────────────────────────────────
# css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
# with open(css_path, encoding="utf-8") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # PAGE HEADER
# # ─────────────────────────────────────────────
# st.title("PeopleIQ – AI Workforce Intelligence Platform")
# st.caption("Predict employee attrition and generate HR intelligence using machine learning")
# st.divider()


# # ─────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────
# st.sidebar.title("Dashboard")
# page = st.sidebar.radio("Navigation", ["Prediction", "Analytics Dashboard"])
# st.sidebar.divider()
# st.sidebar.success("Model Active")
# st.sidebar.info("Algorithm: Logistic Regression")


# # ─────────────────────────────────────────────
# # LOAD MODEL
# # ─────────────────────────────────────────────
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# model   = joblib.load(os.path.join(BASE_DIR, "models", "attrition_model.pkl"))
# scaler  = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
# columns = joblib.load(os.path.join(BASE_DIR, "models", "columns.pkl"))


# # ─────────────────────────────────────────────
# # PLOTLY DARK THEME  (shared across all charts)
# # To change chart appearance edit these values.
# # ─────────────────────────────────────────────
# DARK_PLOT = dict(
#     paper_bgcolor="rgba(0,0,0,0)",
#     plot_bgcolor="rgba(0,0,0,0)",
#     font=dict(family="Inter, sans-serif", color="#94a3b8", size=13),
#     margin=dict(l=4, r=4, t=50, b=4),
#     xaxis=dict(
#         gridcolor="#2d3348", linecolor="#2d3348",
#         showgrid=False, tickfont=dict(color="#64748b", size=12)
#     ),
#     yaxis=dict(
#         gridcolor="#2d3348", linecolor="#2d3348",
#         tickfont=dict(color="#64748b", size=12)
#     ),
#     hoverlabel=dict(
#         bgcolor="#1e2130", font_size=13,
#         bordercolor="#2d3348", font_color="#e2e8f0"
#     ),
# )


# # ══════════════════════════════════════════════
# # PAGE: PREDICTION
# # ══════════════════════════════════════════════
# if page == "Prediction":

#     st.subheader("Employee Risk Prediction")

#     # ── Input form ──────────────────────────
#     container = st.container(border=True)
#     with container:
#         col1, col2, col3, col4 = st.columns(4)
#         age       = col1.slider("Age", 18, 60, 30)
#         income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
#         job_level = col3.selectbox(
#             "Job Level", [1, 2, 3, 4, 5],
#             format_func=lambda x: {1:"Entry", 2:"Junior", 3:"Mid", 4:"Senior", 5:"Director"}[x]
#         )
#         years = col4.slider("Years at Company", 0, 40, 5)

#         col1, col2, col3, col4 = st.columns(4)
#         job_sat    = col1.selectbox(
#             "Job Satisfaction", [1, 2, 3, 4],
#             format_func=lambda x: {1:"Very Low", 2:"Low", 3:"Medium", 4:"High"}[x]
#         )
#         worklife   = col2.selectbox(
#             "Work-Life Balance", [1, 2, 3, 4],
#             format_func=lambda x: {1:"Poor", 2:"Fair", 3:"Good", 4:"Excellent"}[x]
#         )
#         overtime   = col3.selectbox("Overtime", ["No", "Yes"])
#         department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

#     st.markdown("<br>", unsafe_allow_html=True)
#     _, btn_col, _ = st.columns([4, 2, 4])
#     predict_clicked = btn_col.button("Run Risk Assessment →", use_container_width=True)

#     # ── Run prediction ───────────────────────
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
#             st.markdown(
#                 '<div class="alert-danger">⚠ <strong>API Unavailable</strong> — '
#                 'Cannot reach FastAPI server at <code>localhost:8000</code>. '
#                 'Make sure your backend is running.</div>',
#                 unsafe_allow_html=True
#             )
#         else:
#             # ── Determine card style based on result
#             is_high  = prediction == "Attrition Risk"
#             card_cls = "result-card-high" if is_high else "result-card-low"
#             prob_cls = "high" if is_high else "low"
#             pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
#             heading  = "⚠ High Attrition Risk" if is_high else "✓ Low Attrition Risk"
#             desc     = (
#                 "Multiple risk signals detected. Immediate HR intervention is recommended "
#                 "to retain this employee."
#             ) if is_high else (
#                 "This profile appears stable. Continue regular check-ins "
#                 "and career development planning."
#             )

#             # ── Result: 3 columns
#             c1, c2, c3 = st.columns([1, 1.6, 1.6])

#             # Col 1 — probability score
#             with c1:
#                 st.markdown(f"""
#                 <div class="{card_cls}" style="text-align:center">
#                     <div class="result-label">Risk Probability</div>
#                     <div class="result-prob {prob_cls}">{probability}</div>
#                     <br><span class="risk-pill {pill_cls}">{risk_level} Risk</span>
#                 </div>""", unsafe_allow_html=True)

#             # Col 2 — heading + description
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

#             # Col 3 — HR recommendations
#             with c3:
#                 recs = []
#                 if overtime == "Yes":
#                     recs.append(("Reduce Overtime",
#                                  "Excessive overtime is the #1 driver of attrition in this model."))
#                 if job_sat <= 2:
#                     recs.append(("Satisfaction Review",
#                                  "Schedule a 1:1 — low job satisfaction is a strong exit signal."))
#                 if income < 4000:
#                     recs.append(("Salary Benchmark",
#                                  "Pay is below market. A compensation review is recommended."))
#                 if years < 3:
#                     recs.append(("Onboarding Support",
#                                  "Early-tenure employees carry the highest flight risk."))
#                 if not recs:
#                     recs.append(("Maintain Engagement",
#                                  "Profile is healthy. Keep regular check-ins and recognition."))

#                 rec_html = "".join([
#                     f'<div class="rec-item"><strong>{t}</strong>{d}</div>'
#                     for t, d in recs
#                 ])
#                 st.markdown(f"""
#                 <div class="rec-panel">
#                     <div class="rec-panel-label">HR Recommendations</div>
#                     <div class="rec-grid">{rec_html}</div>
#                 </div>""", unsafe_allow_html=True)


# # ══════════════════════════════════════════════
# # PAGE: ANALYTICS DASHBOARD
# # ══════════════════════════════════════════════
# if page == "Analytics Dashboard":

#     # # ── Top bar ─────────────────────────────
#     # st.markdown("""
#     # <div class="topbar">
#     #     <div>
#     #         <h1>Workforce Analytics Dashboard</h1>
#     #         <p>Upload your HR dataset to generate predictions and insights</p>
#     #     </div>
#     #     <div class="badge-active"><span class="badge-dot"></span> Ready</div>
#     # </div>
#     # """, unsafe_allow_html=True)

#     # ── File upload ──────────────────────────
#     file = st.file_uploader("Upload HR Dataset", type=["csv"])

#     if file:
#         df = pd.read_csv(file)

#         # Validate required columns
#         required_cols = ['Age', 'MonthlyIncome', 'Department']
#         missing = [c for c in required_cols if c not in df.columns]
#         if missing:
#             st.markdown(
#                 f'<div class="alert-danger">⚠ <strong>Missing columns:</strong> {", ".join(missing)}</div>',
#                 unsafe_allow_html=True
#             )
#             st.stop()

#         st.subheader("Dataset Preview")
#         st.dataframe(df.head(), use_container_width=True, hide_index=True)

#         # ── Run model predictions ─────────────
#         if model:
#             with st.spinner("Analyzing workforce data..."):
#                 df_original = df.copy()
#                 df_enc = pd.get_dummies(df)
#                 df_enc = df_enc.reindex(columns=columns, fill_value=0)
#                 df_sc  = scaler.transform(df_enc)
#                 df_original['Prediction'] = model.predict(df_sc)
#                 df_original['Probability'] = model.predict_proba(df_sc)[:, 1]
#                 df_original['Prediction'] = df_original['Prediction'].map(
#                     {0: "No Attrition", 1: "Attrition"}
#                 )

#         # ── Summary stats ────────────────────
#         att_count = (df_original['Prediction'] == "Attrition").sum()
#         att_rate  = (df_original['Prediction'] == "Attrition").mean() * 100
#         avg_sal   = int(df_original['MonthlyIncome'].mean())
#         avg_risk  = df_original['Probability'].mean() * 100

#         # ── Alert banner ─────────────────────
#         if att_count > 50:
#             st.markdown(
#                 f'<div class="alert-danger">🔴 <strong>High Attrition Risk:</strong> '
#                 f'{att_count} employees ({att_rate:.1f}%) are predicted to leave. '
#                 f'Immediate action required.</div>',
#                 unsafe_allow_html=True
#             )
#         else:
#             st.markdown(
#                 f'<div class="alert-success">✅ <strong>Workforce Stable:</strong> '
#                 f'Attrition is within an acceptable range — '
#                 f'{att_count} employees ({att_rate:.1f}%).</div>',
#                 unsafe_allow_html=True
#             )

#         # ── KPI Cards ────────────────────────
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

#         # ── Dataset Health (standalone, compact) ──
#         st.markdown("""
#         <div class="section-hdr" style="margin-top:10px">
#             <span class="section-hdr-title">Dataset Health</span>
#         </div>
#         """, unsafe_allow_html=True)
#         h1, h2 = st.columns(2)
#         h1.metric("Missing Values", df_original.isnull().sum().sum())
#         h2.metric("Features", df_original.shape[1])

#         st.divider()

#         # ── Workforce Insights heading + inline Department filter ──
#         ins_col, filt_col = st.columns([2, 1])
#         with ins_col:
#             st.markdown("""
#             <div class="workforce-heading">
#                 <div class="workforce-heading-title">Workforce Insights</div>
#                 <div class="workforce-heading-sub">Charts filtered by department selection</div>
#             </div>
#             """, unsafe_allow_html=True)
#         with filt_col:
#             st.markdown("""
#             <div style="font-size:10px;font-weight:600;text-transform:uppercase;
#                         letter-spacing:1px;color:#3d4563;margin-bottom:4px;
#                         font-family:'JetBrains Mono',monospace;">
#                 Filter by Department
#             </div>
#             """, unsafe_allow_html=True)
#             dept_filter = st.multiselect(
#                 "Filter by Department",
#                 df_original['Department'].unique(),
#                 default=df_original['Department'].unique(),
#                 label_visibility="collapsed",
#                 placeholder="All departments"
#             )

#         filtered_df = df_original[df_original['Department'].isin(dept_filter)]

#         col1, col2 = st.columns(2)

#         fig = px.histogram(filtered_df, x="Prediction", color="Prediction",
#             title="Attrition Distribution",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig.update_layout(**DARK_PLOT, showlegend=False,
#                           title_font=dict(color="#f1f5f9", size=16, family="Inter"))
#         fig.update_traces(marker_line_width=0)
#         col1.plotly_chart(fig, use_container_width=True)

#         fig2 = px.box(filtered_df, x="Prediction", y="MonthlyIncome", color="Prediction",
#             title="Income Impact",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig2.update_layout(**DARK_PLOT, showlegend=False,
#                            title_font=dict(color="#f1f5f9", size=16, family="Inter"))
#         col2.plotly_chart(fig2, use_container_width=True)

#         col3, col4 = st.columns(2)

#         fig3 = px.histogram(filtered_df, x="Department", color="Prediction",
#             title="Department Impact",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#7c9ef5"})
#         fig3.update_layout(**DARK_PLOT,
#             title_font=dict(color="#f1f5f9", size=16, family="Inter"),
#             legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1,
#                         font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
#         fig3.update_traces(marker_line_width=0)
#         col3.plotly_chart(fig3, use_container_width=True)

#         fig4 = px.pie(filtered_df, names="Prediction", title="Risk Breakdown",
#             color_discrete_map={"Attrition": "#f87171", "No Attrition": "#34d399"})
#         fig4.update_layout(**DARK_PLOT,
#             title_font=dict(color="#f1f5f9", size=16, family="Inter"),
#             legend=dict(font=dict(color="#94a3b8", size=12), bgcolor="rgba(0,0,0,0)"))
#         fig4.update_traces(textfont_color="#f1f5f9", textfont_size=13)
#         col4.plotly_chart(fig4, use_container_width=True)

#         # ── High Risk Table ───────────────────
#         st.subheader("Top High Risk Employees")
#         high_risk = (
#             filtered_df[filtered_df['Prediction'] == "Attrition"]
#             .sort_values("Probability", ascending=False)
#             .head(10)
#         )
#         st.dataframe(high_risk, use_container_width=True, hide_index=True)

#         with st.expander("View Full Prediction Data"):
#             st.dataframe(df_original, use_container_width=True, hide_index=True)

#         # ── Key Insights ─────────────────────
#         insights = []

#         if 'OverTime' in df_original.columns:
#             ot_att  = df_original[df_original['OverTime'] == 'Yes']['Prediction'].eq('Attrition').mean() * 100
#             not_att = df_original[df_original['OverTime'] == 'No']['Prediction'].eq('Attrition').mean() * 100
#             lift    = ot_att - not_att
#             insights.append(("📊", "Overtime Impact",
#                 f"{ot_att:.1f}% attrition among overtime employees vs {not_att:.1f}% "
#                 f"for others — a <strong>{lift:.1f}pp lift</strong>."))

#         if 'MonthlyIncome' in df_original.columns:
#             low_sal = df_original[df_original['MonthlyIncome'] < 4000]['Prediction'].eq('Attrition').mean() * 100
#             hi_sal  = df_original[df_original['MonthlyIncome'] >= 4000]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("💰", "Salary Band Risk",
#                 f"Employees earning &lt;$4k/mo have <strong>{low_sal:.1f}%</strong> "
#                 f"attrition vs {hi_sal:.1f}% for higher earners."))

#         if 'JobSatisfaction' in df_original.columns:
#             low_js = df_original[df_original['JobSatisfaction'] <= 2]['Prediction'].eq('Attrition').mean() * 100
#             hi_js  = df_original[df_original['JobSatisfaction'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("😔", "Satisfaction vs Retention",
#                 f"Low satisfaction (≤2) employees show <strong>{low_js:.1f}%</strong> "
#                 f"attrition vs {hi_js:.1f}% for satisfied staff."))

#         if 'YearsAtCompany' in df_original.columns:
#             early  = df_original[df_original['YearsAtCompany'] < 3]['Prediction'].eq('Attrition').mean() * 100
#             senior = df_original[df_original['YearsAtCompany'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🕐", "Early Tenure Risk",
#                 f"Employees with &lt;3 years tenure have <strong>{early:.1f}%</strong> "
#                 f"predicted attrition vs {senior:.1f}% for veterans."))

#         if 'Department' in df_original.columns:
#             top_dept = (df_original[df_original['Prediction'] == 'Attrition']
#                         .groupby('Department').size().idxmax())
#             top_pct  = df_original[df_original['Department'] == top_dept]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("🏢", "Highest-Risk Department",
#                 f"<strong>{top_dept}</strong> has the most predicted attrition "
#                 f"at <strong>{top_pct:.1f}%</strong> of its headcount."))

#         if 'WorkLifeBalance' in df_original.columns:
#             poor_wlb = df_original[df_original['WorkLifeBalance'] == 1]['Prediction'].eq('Attrition').mean() * 100
#             good_wlb = df_original[df_original['WorkLifeBalance'] >= 3]['Prediction'].eq('Attrition').mean() * 100
#             insights.append(("⚖️", "Work-Life Balance",
#                 f"Poor WLB (score 1): <strong>{poor_wlb:.1f}%</strong> "
#                 f"attrition vs {good_wlb:.1f}% for good WLB."))

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

#         # ── HR Recommendations ────────────────
#         recommendations = []

#         if 'OverTime' in df_original.columns:
#             ot_att_n = df_original[
#                 (df_original['OverTime'] == 'Yes') &
#                 (df_original['Prediction'] == 'Attrition')
#             ].shape[0]
#             recommendations.append(("🔴", "High", "Reduce Overtime Load",
#                 f"<strong>{ot_att_n} at-risk employees</strong> are on overtime. "
#                 f"Redistribute workloads to bring OT headcount below 20%."))

#         if 'MonthlyIncome' in df_original.columns:
#             below_market = (df_original['MonthlyIncome'] < 4000).sum()
#             recommendations.append(("🟠", "Medium", "Compensation Review",
#                 f"<strong>{below_market} employees</strong> earn below $4k/mo. "
#                 f"Benchmark Level 1–2 roles against market rates immediately."))

#         if 'JobSatisfaction' in df_original.columns:
#             low_sat_n = (df_original['JobSatisfaction'] <= 2).sum()
#             recommendations.append(("🟠", "Medium", "Engagement Program",
#                 f"<strong>{low_sat_n} employees</strong> have satisfaction ≤ 2. "
#                 f"Launch pulse surveys and targeted 1:1 check-ins this quarter."))

#         if 'YearsAtCompany' in df_original.columns:
#             new_hires = (df_original['YearsAtCompany'] < 3).sum()
#             recommendations.append(("🟡", "Low", "Onboarding Reinforcement",
#                 f"<strong>{new_hires} employees</strong> have under 3 years tenure. "
#                 f"Assign mentors and strengthen the 90-day onboarding plan."))

#         if 'Department' in df_original.columns:
#             top_dept = (df_original[df_original['Prediction'] == 'Attrition']
#                         .groupby('Department').size().idxmax())
#             recommendations.append(("🔴", "High", f"{top_dept} — Urgent Review",
#                 f"This department has the highest predicted attrition. "
#                 f"Schedule an all-hands HR review and exit risk assessment."))

#         priority_color = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
#         priority_bg    = {"High": "#3f1515",  "Medium": "#3d2b08", "Low": "#0d3321"}

#         rec_html = "".join([
#             f"""<div class="hrec-item">
#                     <div class="hrec-item-top">
#                         <span class="hrec-item-icon">{icon}</span>
#                         <span class="hrec-item-title">{title}</span>
#                         <span class="hrec-priority-pill"
#                               style="background:{priority_bg[priority]};
#                                      color:{priority_color[priority]}">{priority}</span>
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

#         # ── Export ────────────────────────────
#         st.subheader("Export Results")
#         st.download_button(
#             "Download Predictions",
#             filtered_df.to_csv(index=False),
#             "attrition_results.csv"
#         )

# # ─────────────────────────────────────────────
# # FOOTER
# # ─────────────────────────────────────────────
# st.divider()
# st.caption(
# "PeopleIQ Workforce Intelligence Platform | ML Powered HR Decision Support | Built with FastAPI & Streamlit"
# )


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import joblib
import os
import sys

# Add project root to path so ai.py can be found from ui/app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ai import generate_hr_insights

st.set_page_config(
    page_title="PeopleIQ | AI Workforce Intelligence",
    page_icon="🧠",
    layout="wide"
)

# ── Load CSS ─────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")
with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Page header ──────────────────────────────────────────────────
st.title("PeopleIQ - AI Workforce Intelligence Platform")
st.caption("AI powered employee attrition prediction and HR decision intelligence system")
st.divider()

# ── Sidebar ──────────────────────────────────────────────────────
st.sidebar.title("Dashboard")
page = st.sidebar.radio("Navigation", ["Prediction", "Analytics Dashboard"])
st.sidebar.divider()
st.sidebar.success("Model Active")
st.sidebar.info("Algorithm: Logistic Regression")

# ── Load model ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model   = joblib.load(os.path.join(BASE_DIR, "backend", "models", "attrition_model.pkl"))
scaler  = joblib.load(os.path.join(BASE_DIR, "backend", "models", "scaler.pkl"))
columns = joblib.load(os.path.join(BASE_DIR, "backend", "models", "columns.pkl"))

# ── Plotly dark theme ────────────────────────────────────────────
DARK_PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=13),
    margin=dict(l=4, r=4, t=50, b=4),
    xaxis=dict(gridcolor="#2d3348", linecolor="#2d3348", showgrid=False, tickfont=dict(color="#64748b", size=12)),
    yaxis=dict(gridcolor="#2d3348", linecolor="#2d3348", tickfont=dict(color="#64748b", size=12)),
    hoverlabel=dict(bgcolor="#1e2130", font_size=13, bordercolor="#2d3348", font_color="#e2e8f0"),
)


# ════════════════════════════════════════════════════════════════
# PAGE: PREDICTION
# ════════════════════════════════════════════════════════════════
if page == "Prediction":

    st.subheader("Employee Risk Prediction")

    container = st.container(border=True)
    with container:
        col1, col2, col3, col4 = st.columns(4)
        age       = col1.slider("Age", 18, 60, 30)
        income    = col2.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
        job_level = col3.selectbox("Job Level", [1, 2, 3, 4, 5],
                        format_func=lambda x: {1:"Entry", 2:"Junior", 3:"Mid", 4:"Senior", 5:"Director"}[x])
        years     = col4.slider("Years at Company", 0, 40, 5)

        col1, col2, col3, col4 = st.columns(4)
        job_sat    = col1.selectbox("Job Satisfaction", [1, 2, 3, 4],
                        format_func=lambda x: {1:"Very Low", 2:"Low", 3:"Medium", 4:"High"}[x])
        worklife   = col2.selectbox("Work-Life Balance", [1, 2, 3, 4],
                        format_func=lambda x: {1:"Poor", 2:"Fair", 3:"Good", 4:"Excellent"}[x])
        overtime   = col3.selectbox("Overtime", ["No", "Yes"])
        department = col4.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([4, 2, 4])
    predict_clicked = btn_col.button("Run Risk Assessment", use_container_width=True)

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
                resp       = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
                result     = resp.json()
                prediction = result["Prediction"]
                probability= result["Probability"]
                risk_level = result["Risk Level"]
                api_ok     = True
            except Exception:
                api_ok = False

        if not api_ok:
            st.markdown(
                '<div class="alert-danger">API Unavailable - Cannot reach FastAPI server at localhost:8000. '
                'Make sure your backend is running.</div>',
                unsafe_allow_html=True
            )
        else:
            is_high  = prediction == "Attrition Risk"
            card_cls = "result-card-high" if is_high else "result-card-low"
            prob_cls = "high" if is_high else "low"
            pill_cls = "high" if risk_level == "High" else "med" if risk_level == "Medium" else "low"
            heading  = "High Attrition Risk" if is_high else "Low Attrition Risk"
            desc     = (
                "Multiple risk signals detected. Immediate HR intervention is recommended to retain this employee."
            ) if is_high else (
                "This profile appears stable. Continue regular check-ins and career development planning."
            )

            c1, c2 = st.columns([1, 1])

            with c1:
                st.markdown(f"""
                <div class="{card_cls}" style="text-align:center">
                    <div class="result-label">Risk Probability</div>
                    <div class="result-prob {prob_cls}">{probability}</div>
                    <br><span class="risk-pill {pill_cls}">{risk_level} Risk</span>
                </div>""", unsafe_allow_html=True)

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


            # ── AI recommendation for single employee ──────────
            st.markdown("<br>", unsafe_allow_html=True)
            with st.spinner("Getting AI recommendation..."):
                try:
                    from groq import Groq
                    from dotenv import load_dotenv
                    load_dotenv()
                    ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

                    emp_prompt = f"""You are a senior HR consultant. An employee has been assessed with the following profile:

                        Age: {age}
                        Monthly Income: ${income:,}
                        Job Level: {job_level}
                        Years at Company: {years}
                        Job Satisfaction: {job_sat}/4
                        Work-Life Balance: {worklife}/4
                        Overtime: {overtime}
                        Department: {department}

                        ML Model Result:
                        Prediction: {prediction}
                        Risk Probability: {probability}
                        Risk Level: {risk_level}

                        Write a concise, professional HR action plan in exactly this JSON format, no markdown:
                        {{
                        "summary": "One sentence summary of the risk assessment",
                        "actions": [
                            {{"priority": "High/Medium/Low", "action": "specific action title", "detail": "what to do and why"}},
                            {{"priority": "High/Medium/Low", "action": "specific action title", "detail": "what to do and why"}},
                            {{"priority": "High/Medium/Low", "action": "specific action title", "detail": "what to do and why"}}
                        ]
                        }}"""

                    ai_resp = ai_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": emp_prompt}],
                        temperature=0.4,
                        max_tokens=600,
                    )

                    raw = ai_resp.choices[0].message.content.strip()
                    if raw.startswith("```"):
                        raw = raw.split("```")[1]
                        if raw.startswith("json"):
                            raw = raw[4:]
                        raw = raw.strip()
                    start = raw.find("{")
                    end   = raw.rfind("}") + 1
                    if start != -1 and end > start:
                        raw = raw[start:end]

                    import json as _json
                    ai_emp = _json.loads(raw)
                    ai_ok  = True
                except Exception:
                    ai_ok = False

            if ai_ok:
                priority_color = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
                priority_bg    = {"High": "#3f1515",  "Medium": "#3d2b08", "Low": "#0d3321"}

                actions_html = "".join([
                    f"""<div style="background:#1e2130;border:1px solid #2d3348;border-radius:10px;
                                    padding:14px 16px;margin-bottom:10px;">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <span style="font-size:16px;font-weight:700;color:#e2e8f0;flex:1;">
                                    {a['action']}
                                </span>
                                <span style="background:{priority_bg.get(a['priority'],'#2d3348')};
                                             color:{priority_color.get(a['priority'],'#94a3b8')};
                                             font-size:14px;font-weight:700;padding:3px 10px;
                                             border-radius:20px;text-transform:uppercase;">
                                    {a['priority']}
                                </span>
                            </div>
                            <div style="font-size:16px;color:#94a3b8;line-height:1.6;">{a['detail']}</div>
                        </div>"""
                    for a in ai_emp.get("actions", [])
                ])

                st.markdown(f"""
                <div style="background:#13161e;border:1px solid #2d3348;border-radius:14px;padding:20px;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;
                                padding-bottom:12px;border-bottom:1px solid #2d3348;">
                        <div style="font-size:19px;font-weight:700;color:#f1f5f9;flex:1;">
                            AI Action Plan
                        </div>
                        <span style="background:#0d2818;color:#34d399;font-size:16px;font-weight:700;
                                     padding:3px 10px;border-radius:4px;letter-spacing:.5px;">Groq AI</span>
                    </div>
                    <div style="font-size:16px;color:#7c9ef5;margin-bottom:14px;
                                padding:10px 14px;background:#1a2240;border-radius:8px;">
                        {ai_emp.get('summary', '')}
                    </div>
                    {actions_html}
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS DASHBOARD
# ════════════════════════════════════════════════════════════════
if page == "Analytics Dashboard":

    file = st.file_uploader("Upload HR Dataset", type=["csv"])

    if file:
        df = pd.read_csv(file)

        # Validate columns
        required_cols = ['Age', 'MonthlyIncome', 'Department']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.markdown(
                f'<div class="alert-danger">Missing columns: {", ".join(missing)}</div>',
                unsafe_allow_html=True
            )
            st.stop()

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True, hide_index=True)

        # Run model predictions
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

        # Summary stats
        att_count = (df_original['Prediction'] == "Attrition").sum()
        att_rate  = (df_original['Prediction'] == "Attrition").mean() * 100
        avg_sal   = int(df_original['MonthlyIncome'].mean())
        avg_risk  = df_original['Probability'].mean() * 100

        # Alert banner
        if att_count > 50:
            st.markdown(
                f'<div class="alert-danger">High Attrition Risk: {att_count} employees ({att_rate:.1f}%) '
                f'are predicted to leave. Immediate action required.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="alert-success">Workforce Stable: Attrition is within an acceptable range - '
                f'{att_count} employees ({att_rate:.1f}%).</div>',
                unsafe_allow_html=True
            )

        # KPI Cards
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
                <span class="kpi-badge">Predicted</span>
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

        # Dataset Health
        st.markdown("""
        <div class="section-hdr" style="margin-top:10px">
            <span class="section-hdr-title">Dataset Health</span>
        </div>
        """, unsafe_allow_html=True)
        h1, h2 = st.columns(2)
        h1.metric("Missing Values", df_original.isnull().sum().sum())
        h2.metric("Features", df_original.shape[1])

        st.divider()

        # Workforce Insights heading + department filter
        ins_col, filt_col = st.columns([2, 1])
        with ins_col:
            st.markdown("""
            <div class="workforce-heading">
                <div class="workforce-heading-title">Workforce Insights</div>
                <div class="workforce-heading-sub">Charts filtered by department selection</div>
            </div>
            """, unsafe_allow_html=True)
        with filt_col:
            st.markdown(
                '<div style="font-size:10px;font-weight:600;text-transform:uppercase;'
                'letter-spacing:1px;color:#3d4563;margin-bottom:4px;font-family:monospace;">'
                'Filter by Department</div>',
                unsafe_allow_html=True
            )
            dept_filter = st.multiselect(
                "Filter by Department",
                df_original['Department'].unique(),
                default=df_original['Department'].unique(),
                label_visibility="collapsed",
                placeholder="All departments"
            )

        filtered_df = df_original[df_original['Department'].isin(dept_filter)]

        # Charts
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

        # High Risk Table
        st.subheader("Top High Risk Employees")
        high_risk = (
            filtered_df[filtered_df['Prediction'] == "Attrition"]
            .sort_values("Probability", ascending=False)
            .head(10)
        )
        st.dataframe(high_risk, use_container_width=True, hide_index=True)

        with st.expander("View Full Prediction Data"):
            st.dataframe(df_original, use_container_width=True, hide_index=True)

        # ────────────────────────────────────────────────────────
        # GROQ AI — INSIGHTS & RECOMMENDATIONS
        # generate_hr_insights() NEVER raises — always returns data
        # On API failure it silently falls back to computed stats
        # ────────────────────────────────────────────────────────

        cache_key = f"ai_{hash(str(df_original.shape) + str(int(att_count)))}"

        if cache_key not in st.session_state:
            with st.spinner("Generating AI insights with Groq..."):
                st.session_state[cache_key] = generate_hr_insights(df_original)

        ai = st.session_state[cache_key]

        # Badge color depends on source
        source      = ai.get("source", "computed")
        badge_color = "#34d399" if source == "groq" else "#7c9ef5"
        badge_bg    = "#0d2818" if source == "groq" else "#1e2a4a"
        badge_label = "Groq AI" if source == "groq" else "Computed"
        badge_sub   = "Llama 3.3 70B analysis" if source == "groq" else "Computed from dataset"

        # Key Insights section
        st.markdown(f"""
        <div class="section-hdr" style="margin-top:4px">
            <span class="section-hdr-title">Key Insights</span>
            <span class="section-hdr-sub">
                <span style="background:{badge_bg};color:{badge_color};font-size:10px;
                             font-weight:700;padding:2px 8px;border-radius:4px;
                             letter-spacing:.5px;margin-right:6px;">{badge_label}</span>
                {badge_sub}
            </span>
        </div>
        """, unsafe_allow_html=True)

        insight_html = "".join([
            f"""<div class="insight-item">
                    <div class="insight-item-icon">{item.get("icon", "📊")}</div>
                    <div>
                        <div class="insight-item-title">{item["title"]}</div>
                        <div class="insight-item-body">{item["body"]}</div>
                    </div>
                </div>"""
            for item in ai.get("insights", [])
        ])
        st.markdown(f'<div class="insight-grid">{insight_html}</div>', unsafe_allow_html=True)

        # Business Impact banner
        if ai.get("business_impact"):
            st.markdown(f"""
            <div style="margin-top:14px;padding:16px 20px;background:#1a1520;
                        border:1px solid #3d1a5f;border-left:4px solid #9f7aea;
                        border-radius:10px;font-size:15px;color:#c4b5fd;line-height:1.7;">
                <strong style="color:#a78bfa;display:block;margin-bottom:6px;
                               font-size:15px;text-transform:uppercase;letter-spacing:.8px;">
                    Business Impact
                </strong>
                {ai["business_impact"]}
            </div>
            """, unsafe_allow_html=True)

        # HR Recommendations section
        priority_color = {"High": "#f87171", "Medium": "#fbbf24", "Low": "#34d399"}
        priority_bg    = {"High": "#3f1515",  "Medium": "#3d2b08", "Low": "#0d3321"}

        rec_html = "".join([
            f"""<div class="hrec-item">
                    <div class="hrec-item-top">
                        <span class="hrec-item-icon">{item.get("icon", "✅")}</span>
                        <span class="hrec-item-title">{item["title"]}</span>
                        <span class="hrec-priority-pill"
                              style="background:{priority_bg.get(item['priority'], '#2d3348')};
                                     color:{priority_color.get(item['priority'], '#94a3b8')}">
                            {item["priority"]}
                        </span>
                    </div>
                    <div class="hrec-item-body">{item["body"]}</div>
                </div>"""
            for item in ai.get("recommendations", [])
        ])

        st.markdown(f"""
        <div class="section-hdr" style="margin-top:20px">
            <span class="section-hdr-title">HR Recommendations</span>
            <span class="section-hdr-sub">
                <span style="background:{badge_bg};color:{badge_color};font-size:10px;
                             font-weight:700;padding:2px 8px;border-radius:4px;
                             letter-spacing:.5px;margin-right:6px;">{badge_label}</span>
                {len(ai.get("recommendations", []))} action items
            </span>
        </div>
        <div class="hrec-grid">{rec_html}</div>
        """, unsafe_allow_html=True)

        # Regenerate button — clears cache and re-calls Groq
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Regenerate AI Analysis", key="regen_ai"):
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            st.rerun()

        # Export
        st.subheader("Export Results")
        st.download_button(
            "Download Predictions",
            filtered_df.to_csv(index=False),
            "attrition_results.csv"
        )

# ── Footer ───────────────────────────────────────────────────────
st.divider()
st.caption(
    "PeopleIQ | AI Workforce Intelligence Platform | AI Powered HR Decision Support"
)