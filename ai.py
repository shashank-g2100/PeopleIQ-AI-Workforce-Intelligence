from groq import Groq
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ── Groq client ─────────────────────────────────────────────────
# Add GROQ_API_KEY=your_key to your .env file
# Get free key at: https://console.groq.com
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Model to use — llama-3.3-70b-versatile is free and very capable
GROQ_MODEL = "llama-3.3-70b-versatile"


def _compute_fallback(df: pd.DataFrame) -> dict:
    """
    Compute insights and recommendations directly from the dataframe.
    Used when Groq API is unavailable or fails for any reason.
    Always returns a valid dict — never raises.
    """
    insights = []
    recommendations = []

    if 'OverTime' in df.columns:
        ot  = df[df['OverTime'] == 'Yes']['Prediction'].eq('Attrition').mean() * 100
        nOt = df[df['OverTime'] == 'No']['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "📊", "title": "Overtime Impact",
            "body": f"{ot:.1f}% attrition among overtime employees vs {nOt:.1f}% for others — a <strong>{ot - nOt:.1f}pp lift</strong>."
        })

    if 'MonthlyIncome' in df.columns:
        lo = df[df['MonthlyIncome'] < 4000]['Prediction'].eq('Attrition').mean() * 100
        hi = df[df['MonthlyIncome'] >= 4000]['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "💰", "title": "Salary Band Risk",
            "body": f"Employees earning &lt;$4k/mo have <strong>{lo:.1f}%</strong> attrition vs {hi:.1f}% for higher earners."
        })

    if 'JobSatisfaction' in df.columns:
        lo = df[df['JobSatisfaction'] <= 2]['Prediction'].eq('Attrition').mean() * 100
        hi = df[df['JobSatisfaction'] >= 3]['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "😔", "title": "Satisfaction vs Retention",
            "body": f"Low satisfaction (<=2) employees show <strong>{lo:.1f}%</strong> attrition vs {hi:.1f}% for satisfied staff."
        })

    if 'YearsAtCompany' in df.columns:
        early  = df[df['YearsAtCompany'] < 3]['Prediction'].eq('Attrition').mean() * 100
        senior = df[df['YearsAtCompany'] >= 3]['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "🕐", "title": "Early Tenure Risk",
            "body": f"Employees with &lt;3 years tenure have <strong>{early:.1f}%</strong> predicted attrition vs {senior:.1f}% for veterans."
        })

    if 'Department' in df.columns:
        top = df[df['Prediction'] == 'Attrition'].groupby('Department').size().idxmax()
        pct = df[df['Department'] == top]['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "🏢", "title": "Highest-Risk Department",
            "body": f"<strong>{top}</strong> has the most predicted attrition at <strong>{pct:.1f}%</strong> of its headcount."
        })

    if 'WorkLifeBalance' in df.columns:
        poor = df[df['WorkLifeBalance'] == 1]['Prediction'].eq('Attrition').mean() * 100
        good = df[df['WorkLifeBalance'] >= 3]['Prediction'].eq('Attrition').mean() * 100
        insights.append({
            "icon": "⚖️", "title": "Work-Life Balance",
            "body": f"Poor WLB (score 1): <strong>{poor:.1f}%</strong> attrition vs {good:.1f}% for good WLB."
        })

    if 'OverTime' in df.columns:
        n = df[(df['OverTime'] == 'Yes') & (df['Prediction'] == 'Attrition')].shape[0]
        recommendations.append({
            "icon": "🔴", "priority": "High", "title": "Reduce Overtime Load",
            "body": f"<strong>{n} at-risk employees</strong> are on overtime. Redistribute workloads to bring OT headcount below 20%."
        })

    if 'MonthlyIncome' in df.columns:
        n = (df['MonthlyIncome'] < 4000).sum()
        recommendations.append({
            "icon": "🟠", "priority": "Medium", "title": "Compensation Review",
            "body": f"<strong>{n} employees</strong> earn below $4k/mo. Benchmark Level 1-2 roles against market rates immediately."
        })

    if 'JobSatisfaction' in df.columns:
        n = (df['JobSatisfaction'] <= 2).sum()
        recommendations.append({
            "icon": "🟠", "priority": "Medium", "title": "Engagement Program",
            "body": f"<strong>{n} employees</strong> have satisfaction <= 2. Launch pulse surveys and targeted 1:1 check-ins this quarter."
        })

    if 'YearsAtCompany' in df.columns:
        n = (df['YearsAtCompany'] < 3).sum()
        recommendations.append({
            "icon": "🟡", "priority": "Low", "title": "Onboarding Reinforcement",
            "body": f"<strong>{n} employees</strong> have under 3 years tenure. Assign mentors and strengthen the 90-day onboarding plan."
        })

    if 'Department' in df.columns:
        top = df[df['Prediction'] == 'Attrition'].groupby('Department').size().idxmax()
        recommendations.append({
            "icon": "🔴", "priority": "High", "title": f"{top} - Urgent Review",
            "body": "This department has the highest predicted attrition. Schedule an all-hands HR review and exit risk assessment."
        })

    rate   = (df['Prediction'] == 'Attrition').mean() * 100
    income = df['MonthlyIncome'].mean()

    return {
        "insights": insights,
        "recommendations": recommendations,
        "business_impact": (
            f"With a predicted attrition rate of {rate:.1f}%, the organisation faces significant replacement costs "
            f"estimated at 50-200% of annual salary per departing employee. At an average income of ${income:,.0f}/mo, "
            f"proactive retention investment is substantially more cost-effective than reactive hiring."
        ),
        "source": "computed"
    }


def generate_hr_insights(df: pd.DataFrame) -> dict:
    """
    Calls Groq (llama-3.3-70b-versatile) for AI-generated HR insights.
    Falls back to _compute_fallback() silently on ANY error.
    NEVER raises — always returns a valid dict.

    Returns dict with keys:
        insights        -> list of {icon, title, body}
        recommendations -> list of {icon, priority, title, body}
        business_impact -> str
        source          -> "groq" | "computed"
    """
    try:
        rate     = (df['Prediction'] == "Attrition").mean() * 100
        count    = (df['Prediction'] == "Attrition").sum()
        total    = len(df)
        income   = df['MonthlyIncome'].mean()
        ot_att   = df[df['OverTime'] == 'Yes']['Prediction'].eq("Attrition").mean() * 100 if 'OverTime' in df.columns else None
        sat_att  = df[df['JobSatisfaction'] <= 2]['Prediction'].eq("Attrition").mean() * 100 if 'JobSatisfaction' in df.columns else None
        ten_att  = df[df['YearsAtCompany'] < 3]['Prediction'].eq("Attrition").mean() * 100 if 'YearsAtCompany' in df.columns else None
        sal_att  = df[df['MonthlyIncome'] < 4000]['Prediction'].eq("Attrition").mean() * 100 if 'MonthlyIncome' in df.columns else None
        top_dept = df[df['Prediction'] == 'Attrition'].groupby('Department').size().idxmax() if 'Department' in df.columns else "Unknown"

        stats = f"""
Total employees        : {total}
Predicted attrition    : {count} employees ({rate:.1f}%)
Average monthly income : ${income:,.0f}
Overtime attrition     : {f"{ot_att:.1f}%" if ot_att is not None else "N/A"}
Low satisfaction att.  : {f"{sat_att:.1f}%" if sat_att is not None else "N/A"}
Early tenure (<3yr)    : {f"{ten_att:.1f}%" if ten_att is not None else "N/A"}
Low salary (<$4k) att. : {f"{sal_att:.1f}%" if sal_att is not None else "N/A"}
Highest risk dept.     : {top_dept}
"""

        prompt = f"""You are a senior HR data scientist analysing workforce attrition data.

Dataset statistics:
{stats}

Return ONLY a valid JSON object. No markdown fences, no explanation, no text before or after the JSON.

{{
  "insights": [
    {{"icon": "emoji", "title": "short title", "body": "1-2 sentence insight referencing actual numbers"}},
    {{"icon": "emoji", "title": "short title", "body": "1-2 sentence insight referencing actual numbers"}},
    {{"icon": "emoji", "title": "short title", "body": "1-2 sentence insight referencing actual numbers"}},
    {{"icon": "emoji", "title": "short title", "body": "1-2 sentence insight referencing actual numbers"}}
  ],
  "recommendations": [
    {{"icon": "emoji", "priority": "High",   "title": "action title", "body": "specific actionable recommendation"}},
    {{"icon": "emoji", "priority": "High",   "title": "action title", "body": "specific actionable recommendation"}},
    {{"icon": "emoji", "priority": "Medium", "title": "action title", "body": "specific actionable recommendation"}},
    {{"icon": "emoji", "priority": "Low",    "title": "action title", "body": "specific actionable recommendation"}}
  ],
  "business_impact": "Exactly two sentences on the financial cost and strategic risk of this attrition level."
}}

Strict rules:
- Use professional HR language
- Reference actual numbers from the dataset stats
- Each icon must be a single emoji character
- priority must be exactly one of: High, Medium, Low
- Return ONLY the JSON object, nothing else"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1200,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if the model wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        # Strip any leading/trailing text before the first { and after the last }
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        result = json.loads(raw)
        result["source"] = "groq"
        return result

    except Exception:
        # API error, quota, network issue, JSON parse error — all fall back silently
        return _compute_fallback(df)