from groq import Groq
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"


def generate_hr_insights(df: pd.DataFrame) -> dict:
    """
    Calls Groq (llama-3.3-70b-versatile) for AI-generated HR insights.
    Falls back to computed stats silently on ANY error.
    NEVER raises — always returns a valid dict.

    Returns dict with keys:
        insights        -> list of {icon, title, body}
        recommendations -> list of {icon, priority, title, body}
        business_impact -> str
        source          -> "groq" | "computed"
    """
    try:
        # Client created INSIDE try — if key missing it falls back, never crashes
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # ── Build stats from dataframe ──────────────────────────
        rate     = (df['Prediction'] == "Attrition").mean() * 100
        count    = (df['Prediction'] == "Attrition").sum()
        total    = len(df)
        income   = df['MonthlyIncome'].mean()

        ot_att   = df[df['OverTime'] == 'Yes']['Prediction'].eq("Attrition").mean() * 100 if 'OverTime' in df.columns else None
        no_ot    = df[df['OverTime'] == 'No']['Prediction'].eq("Attrition").mean() * 100 if 'OverTime' in df.columns else None
        sat_att  = df[df['JobSatisfaction'] <= 2]['Prediction'].eq("Attrition").mean() * 100 if 'JobSatisfaction' in df.columns else None
        sat_ok   = df[df['JobSatisfaction'] >= 3]['Prediction'].eq("Attrition").mean() * 100 if 'JobSatisfaction' in df.columns else None
        ten_att  = df[df['YearsAtCompany'] < 3]['Prediction'].eq("Attrition").mean() * 100 if 'YearsAtCompany' in df.columns else None
        ten_ok   = df[df['YearsAtCompany'] >= 3]['Prediction'].eq("Attrition").mean() * 100 if 'YearsAtCompany' in df.columns else None
        sal_att  = df[df['MonthlyIncome'] < 4000]['Prediction'].eq("Attrition").mean() * 100 if 'MonthlyIncome' in df.columns else None
        sal_ok   = df[df['MonthlyIncome'] >= 4000]['Prediction'].eq("Attrition").mean() * 100 if 'MonthlyIncome' in df.columns else None
        wlb_poor = df[df['WorkLifeBalance'] == 1]['Prediction'].eq("Attrition").mean() * 100 if 'WorkLifeBalance' in df.columns else None
        wlb_good = df[df['WorkLifeBalance'] >= 3]['Prediction'].eq("Attrition").mean() * 100 if 'WorkLifeBalance' in df.columns else None
        top_dept = df[df['Prediction'] == 'Attrition'].groupby('Department').size().idxmax() if 'Department' in df.columns else "Unknown"
        top_pct  = df[df['Department'] == top_dept]['Prediction'].eq('Attrition').mean() * 100 if 'Department' in df.columns else None
        ot_risk_n= df[(df['OverTime'] == 'Yes') & (df['Prediction'] == 'Attrition')].shape[0] if 'OverTime' in df.columns else 0
        low_sal_n= (df['MonthlyIncome'] < 4000).sum() if 'MonthlyIncome' in df.columns else 0
        low_sat_n= (df['JobSatisfaction'] <= 2).sum() if 'JobSatisfaction' in df.columns else 0
        new_hire = (df['YearsAtCompany'] < 3).sum() if 'YearsAtCompany' in df.columns else 0

        stats = f"""
Total employees              : {total}
Predicted attrition          : {count} employees ({rate:.1f}%)
Average monthly income       : ${income:,.0f}
Overtime attrition rate      : {f"{ot_att:.1f}%" if ot_att is not None else "N/A"} vs {f"{no_ot:.1f}%" if no_ot is not None else "N/A"} non-overtime
Low job satisfaction att.    : {f"{sat_att:.1f}%" if sat_att is not None else "N/A"} vs {f"{sat_ok:.1f}%" if sat_ok is not None else "N/A"} satisfied
Early tenure (<3yr) att.     : {f"{ten_att:.1f}%" if ten_att is not None else "N/A"} vs {f"{ten_ok:.1f}%" if ten_ok is not None else "N/A"} veterans
Low salary (<$4k) att.       : {f"{sal_att:.1f}%" if sal_att is not None else "N/A"} vs {f"{sal_ok:.1f}%" if sal_ok is not None else "N/A"} higher earners
Poor work-life balance att.  : {f"{wlb_poor:.1f}%" if wlb_poor is not None else "N/A"} vs {f"{wlb_good:.1f}%" if wlb_good is not None else "N/A"} good WLB
Highest risk department      : {top_dept} ({f"{top_pct:.1f}%" if top_pct is not None else "N/A"} attrition)
At-risk overtime employees   : {ot_risk_n}
Employees below $4k/mo       : {low_sal_n}
Low satisfaction employees   : {low_sat_n}
Early tenure employees       : {new_hire}
"""

        prompt = f"""You are a senior HR data scientist analysing workforce attrition predictions.

Here are the exact computed statistics from the dataset:
{stats}

Generate professional HR insights using THESE EXACT NUMBERS from the stats above.
Return ONLY a valid JSON object — no markdown, no explanation, nothing before or after the JSON.

{{
  "insights": [
    {{
      "icon": "📊",
      "title": "Overtime Impact",
      "body": "Write 1-2 sentences using the exact overtime attrition numbers from stats above."
    }},
    {{
      "icon": "💰",
      "title": "Salary Band Risk",
      "body": "Write 1-2 sentences using the exact low salary attrition numbers from stats above."
    }},
    {{
      "icon": "😔",
      "title": "Satisfaction vs Retention",
      "body": "Write 1-2 sentences using the exact low satisfaction attrition numbers from stats above."
    }},
    {{
      "icon": "🕐",
      "title": "Early Tenure Risk",
      "body": "Write 1-2 sentences using the exact early tenure attrition numbers from stats above."
    }},
    {{
      "icon": "🏢",
      "title": "Highest-Risk Department",
      "body": "Write 1-2 sentences using the exact department name and attrition % from stats above."
    }},
    {{
      "icon": "⚖️",
      "title": "Work-Life Balance",
      "body": "Write 1-2 sentences using the exact WLB attrition numbers from stats above."
    }}
  ],
  "recommendations": [
    {{
      "icon": "🔴",
      "priority": "High",
      "title": "Reduce Overtime Load",
      "body": "Specific recommendation referencing the {ot_risk_n} at-risk overtime employees."
    }},
    {{
      "icon": "🟠",
      "priority": "High",
      "title": "Compensation Review",
      "body": "Specific recommendation referencing the {low_sal_n} employees below $4k/mo."
    }},
    {{
      "icon": "🟡",
      "priority": "Medium",
      "title": "Engagement Program",
      "body": "Specific recommendation referencing the {low_sat_n} low-satisfaction employees."
    }},
    {{
      "icon": "🟢",
      "priority": "Low",
      "title": "Onboarding Reinforcement",
      "body": "Specific recommendation referencing the {new_hire} early-tenure employees."
    }}
  ],
  "business_impact": "Two sentences on financial cost and strategic risk using the {rate:.1f}% attrition rate and ${income:,.0f} average income."
}}

STRICT RULES:
- Use the EXACT numbers from the stats — do not invent or round differently
- Each icon must be a single emoji
- priority must be exactly: High, Medium, or Low
- Return ONLY the JSON object, nothing before or after it
- Use professional HR language throughout"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if model wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        # Extract just the JSON object
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        result = json.loads(raw)
        result["source"] = "groq"
        return result

    except Exception as e:
        return {
            "insights": [],
            "recommendations": [],
            "business_impact": "AI insights unavailable. Groq API error.",
            "source": "error"
        }