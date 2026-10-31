from pathlib import Path
import pandas as pd

CSV_FILENAME = "PJ2_Emily_Park_wellness_2025.csv"
ALIASES = {
    "date":["date","day","timestamp"],
    "steps":["steps","step_count","daily_steps"],
    "sleep_hours":["sleep_hours","sleep_duration","sleep"],
    "exercise_minutes":["exercise_minutes","active_minutes"],
    "stress_score":["stress_score","stress"],
    "water_liters":["water_liters","water_litres","water_intake_liters","water_intake"],
    "mood_1to5":["mood_1to5","mood","mood_score"],
    "calories_burned":["calories_burned","calories"],
    "distance_km":["distance_km","distance"],
    "sleep_score":["sleep_score"],
    "exercise_type":["exercise_type"],
    "resting_heart_rate":["resting_heart_rate","resting_hr"],
    "average_heart_rate":["average_heart_rate","avg_heart_rate"],
    "hrv":["hrv","heart_rate_variability"],
    "deep_sleep_pct":["deep_sleep_pct"],
    "weight_kg":["weight_kg"],
}
def norm(x): return str(x).strip().lower().replace("-","_").replace(" ","_")
def load_wellness_data(base_dir):
    base_dir=Path(base_dir)
    candidates=[base_dir/"data"/CSV_FILENAME,base_dir/CSV_FILENAME]
    path=next((p for p in candidates if p.exists()),None)
    if path is None: return pd.DataFrame(),"CSV not found. Put PJ2_Emily_Park_wellness_2025.csv inside the data folder."
    try: df=pd.read_csv(path)
    except Exception as exc: return pd.DataFrame(),f"Could not read CSV: {exc}"
    lookup={norm(c):c for c in df.columns}; rename={}
    for standard,aliases in ALIASES.items():
        for alias in aliases:
            if norm(alias) in lookup:
                rename[lookup[norm(alias)]]=standard; break
    df=df.rename(columns=rename)
    if "date" not in df.columns: return pd.DataFrame(),"CSV loaded, but a date column could not be identified."
    dates=pd.to_datetime(df["date"],dayfirst=True,errors="coerce")
    missing=dates.isna()
    if missing.any(): dates.loc[missing]=pd.to_datetime(df.loc[missing,"date"],errors="coerce")
    df["date"]=dates
    df=df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    for c in ["steps","distance_km","calories_burned","exercise_minutes","average_heart_rate","resting_heart_rate","hrv","sleep_hours","deep_sleep_pct","sleep_score","stress_score","water_liters","weight_kg","mood_1to5"]:
        if c in df: df[c]=pd.to_numeric(df[c],errors="coerce")
    return df,(None if not df.empty else "CSV contains no usable date records.")
def filter_by_dates(df,start,end):
    if df.empty:return df.copy()
    start=pd.Timestamp(start); end=pd.Timestamp(end)+pd.Timedelta(days=1)-pd.Timedelta(microseconds=1)
    return df[(df.date>=start)&(df.date<=end)].copy()
def metric_average(df,column):
    if column not in df:return None
    s=pd.to_numeric(df[column],errors="coerce").dropna()
    return None if s.empty else float(s.mean())
def format_value(value,decimals=1):
    if value is None or pd.isna(value):return "—"
    return f"{value:,.0f}" if decimals==0 else f"{value:,.{decimals}f}"
