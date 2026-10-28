"""FastAPI Web Application & REST API for Bank Transaction Fraud Screening.

Provides an interactive, responsive web interface and backend API for real-time
fraud analytics, dynamic threshold tuning, priority review queues, and live reporting.
"""

import os
import io
from typing import Dict, Any, Optional, List
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.data_generator import generate_synthetic_transactions
from src.cleaning import clean_transaction_data, inspect_data_summary
from src.rules import apply_all_rules_and_score, apply_high_amount_rule, apply_late_night_rule, apply_high_frequency_rule
from src.analytics import (
    get_suspicious_queue,
    get_type_analysis,
    get_channel_analysis,
    get_hour_analysis,
    get_account_risk_analysis,
    get_pattern_summary,
    get_rule_combination_analysis,
    evaluate_against_ground_truth,
    answer_business_questions,
)


class ScreenConfigRequest(BaseModel):
    amount_method: str = "p99"
    custom_amount_threshold: Optional[float] = None
    late_night_start: int = 23
    late_night_end: int = 5
    freq_threshold: int = 5
    suspicion_threshold: int = 2


class AppState:
    """In-memory state holding current dataset and evaluated rules."""

    def __init__(self):
        self.raw_df: pd.DataFrame = pd.DataFrame()
        self.cleaned_df: pd.DataFrame = pd.DataFrame()
        self.scored_df: pd.DataFrame = pd.DataFrame()
        self.cleaning_log: Dict[str, Any] = {}
        self.config: ScreenConfigRequest = ScreenConfigRequest()
        self.load_default_data()

    def load_default_data(self):
        default_csv = "data/bank_transactions.csv"
        if os.path.exists(default_csv):
            try:
                self.raw_df = pd.read_csv(default_csv)
            except Exception:
                self.raw_df = generate_synthetic_transactions(n=5000, seed=42)
        else:
            self.raw_df = generate_synthetic_transactions(n=5000, seed=42)
        self.process_and_score()

    def process_and_score(self):
        self.cleaned_df, self.cleaning_log = clean_transaction_data(self.raw_df)
        df, _ = apply_high_amount_rule(
            self.cleaned_df,
            method=self.config.amount_method,
            threshold_val=self.config.custom_amount_threshold,
        )
        df = apply_late_night_rule(
            df,
            start_hour=self.config.late_night_start,
            end_hour=self.config.late_night_end,
        )
        df = apply_high_frequency_rule(
            df,
            threshold=self.config.freq_threshold,
        )
        df["Suspicion_Score"] = (
            df["Rule_High_Amount"] + df["Rule_Late_Night"] + df["Rule_High_Frequency"]
        ).astype(int)
        df["Suspicious"] = (df["Suspicion_Score"] >= self.config.suspicion_threshold).astype(int)
        df["Rule_Combination"] = (
            df["Rule_High_Amount"].astype(str) + "_" +
            df["Rule_Late_Night"].astype(str) + "_" +
            df["Rule_High_Frequency"].astype(str)
        )
        self.scored_df = df


state = AppState()

app = FastAPI(
    title="Rule-Based Bank Fraud Detection & Screening",
    description="Interactive Web Application and Fraud Risk Analytics Engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_index():
    """Serve the primary single-page responsive dashboard."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Fraud Analytics Dashboard</h1><p>Frontend template initializing...</p>"


@app.get("/api/kpis")
def get_kpis():
    """Retrieve high-level overview metrics and KPI cards."""
    df = state.scored_df
    total = len(df)
    susp = int(df["Suspicious"].sum())
    susp_pct = round((susp / total * 100.0), 2) if total > 0 else 0.0
    total_val = float(df["Amount"].sum()) if "Amount" in df.columns else 0.0
    avg_amt = float(df["Amount"].mean()) if "Amount" in df.columns else 0.0
    p99 = float(df["Amount"].quantile(0.99)) if "Amount" in df.columns else 0.0
    
    score_counts = {
        "score_0": int((df["Suspicion_Score"] == 0).sum()),
        "score_1": int((df["Suspicion_Score"] == 1).sum()),
        "score_2": int((df["Suspicion_Score"] == 2).sum()),
        "score_3": int((df["Suspicion_Score"] == 3).sum()),
    }

    rule_alerts = {
        "high_amount": int(df["Rule_High_Amount"].sum()),
        "late_night": int(df["Rule_Late_Night"].sum()),
        "high_frequency": int(df["Rule_High_Frequency"].sum()),
    }

    eval_metrics = evaluate_against_ground_truth(df)

    return {
        "total_transactions": total,
        "suspicious_transactions": susp,
        "suspicious_percentage": susp_pct,
        "total_monetary_volume": round(total_val, 2),
        "average_transaction_amount": round(avg_amt, 2),
        "amount_p99": round(p99, 2),
        "score_counts": score_counts,
        "rule_alerts": rule_alerts,
        "evaluation": eval_metrics,
        "active_config": state.config.model_dump(),
    }


@app.get("/api/charts")
def get_chart_data():
    """Retrieve structured data series formatted for Chart.js rendering."""
    df = state.scored_df

    # 1. Hourly Trend
    hour_df = get_hour_analysis(df)
    hours_labels = [f"{int(h):02d}:00" for h in hour_df["Hour"]]
    hours_total = [int(v) for v in hour_df["Transactions"]]
    hours_susp = [int(v) for v in hour_df["Suspicious"]]
    hours_rate = [float(v) for v in hour_df["Suspicious_Rate"]]

    # 2. Type Analysis
    type_df = get_type_analysis(df)
    type_labels = list(type_df["Transaction_Type"]) if not type_df.empty else []
    type_counts = [int(v) for v in type_df["Transactions"]] if not type_df.empty else []
    type_rates = [float(v) for v in type_df["Suspicious_Rate"]] if not type_df.empty else []

    # 3. Channel Analysis
    ch_df = get_channel_analysis(df)
    ch_labels = list(ch_df["Channel"]) if not ch_df.empty else []
    ch_rates = [float(v) for v in ch_df["Suspicious_Rate"]] if not ch_df.empty else []
    ch_counts = [int(v) for v in ch_df["Transactions"]] if not ch_df.empty else []

    # 4. Rule Combination Analysis
    comb_df = get_rule_combination_analysis(df)
    comb_labels = [f"{r['Rule_Combination']} ({r['Description'][:15]})" for _, r in comb_df.iterrows()]
    comb_counts = [int(v) for v in comb_df["Transactions"]]

    return {
        "hourly": {
            "labels": hours_labels,
            "total": hours_total,
            "suspicious": hours_susp,
            "rates": hours_rate,
        },
        "types": {
            "labels": type_labels,
            "counts": type_counts,
            "rates": type_rates,
        },
        "channels": {
            "labels": ch_labels,
            "counts": ch_counts,
            "rates": ch_rates,
        },
        "combinations": {
            "labels": comb_labels,
            "counts": comb_counts,
        },
    }


@app.get("/api/transactions/suspicious")
def get_suspicious_transactions(
    score_filter: Optional[int] = Query(None, description="Filter by minimum Suspicion_Score"),
    channel_filter: Optional[str] = Query(None),
    type_filter: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = 100,
    offset: int = 0,
):
    """Retrieve paginated, filterable priority investigation queue."""
    queue = get_suspicious_queue(state.scored_df)

    if score_filter is not None:
        queue = queue[queue["Suspicion_Score"] >= score_filter]
    if channel_filter:
        queue = queue[queue["Channel"].str.lower() == channel_filter.lower()]
    if type_filter:
        queue = queue[queue["Transaction_Type"].str.lower() == type_filter.lower()]
    if search:
        s = search.lower()
        queue = queue[
            queue["Transaction_ID"].str.lower().str.contains(s) |
            queue["Account_ID"].str.lower().str.contains(s)
        ]

    total_matched = len(queue)
    paginated = queue.iloc[offset : offset + limit]

    # Convert timestamps/dates to string for JSON serialization
    records = paginated.copy()
    for col in records.select_dtypes(include=["datetime64[ns]", "datetime64"]).columns:
        records[col] = records[col].astype(str)

    return {
        "total": total_matched,
        "offset": offset,
        "limit": limit,
        "records": records.to_dict(orient="records"),
    }


@app.get("/api/accounts/risk")
def get_account_risk(limit: int = 20):
    """Retrieve top customer accounts with repeat suspicious activity."""
    acc_df = get_account_risk_analysis(state.scored_df)
    top_accounts = acc_df.head(limit)
    return {
        "total_accounts": len(acc_df),
        "repeat_offenders_count": int((acc_df["Suspicious_Transactions"] > 1).sum()),
        "top_accounts": top_accounts.to_dict(orient="records"),
    }


@app.get("/api/questions")
def get_business_questions():
    """Retrieve the answers to all 10 core business questions."""
    return answer_business_questions(state.scored_df)


@app.post("/api/screen")
def update_screening_config(config: ScreenConfigRequest):
    """Dynamically re-screen the dataset with modified rule thresholds."""
    state.config = config
    state.process_and_score()
    return {
        "status": "success",
        "message": "Screening parameters updated and transactions re-scored.",
        "kpis": get_kpis(),
    }


@app.post("/api/generate")
def generate_fresh_data(n: int = 5000, seed: int = 42):
    """Generate and screen a new synthetic transaction dataset."""
    if n < 100 or n > 50000:
        raise HTTPException(status_code=400, detail="Count must be between 100 and 50,000")
    state.raw_df = generate_synthetic_transactions(n=n, seed=seed)
    state.process_and_score()
    return {
        "status": "success",
        "message": f"Generated and screened {n:,} fresh transactions.",
        "kpis": get_kpis(),
    }


@app.post("/api/upload")
async def upload_csv_dataset(file: UploadFile = File(...)):
    """Upload and screen a custom CSV dataset."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a CSV.")
    
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    required_check = ["Transaction_ID", "Account_ID", "Amount", "Transaction_Time"]
    missing = [c for c in required_check if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing essential columns: {missing}")

    state.raw_df = df
    state.process_and_score()
    return {
        "status": "success",
        "message": f"Successfully ingested and screened {len(df):,} transactions from {file.filename}.",
        "kpis": get_kpis(),
    }


@app.get("/api/export/suspicious")
def export_suspicious_csv():
    """Download the current prioritized suspicious queue as CSV."""
    queue = get_suspicious_queue(state.scored_df)
    stream = io.StringIO()
    queue.to_csv(stream, index=False)
    return Response(
        content=stream.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=suspicious_transactions.csv"}
    )
