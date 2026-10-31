from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import load_wellness_data, filter_by_dates, metric_average, format_value
from theme_config import THEMES, apply_theme

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title="WellnessWise", page_icon="🌷", layout="wide")
df, data_message = load_wellness_data(BASE)
if "page" not in st.session_state: st.session_state.page = "Overview"
if "theme_name" not in st.session_state: st.session_state.theme_name = "Blush Pink"
theme = THEMES[st.session_state.theme_name]
apply_theme(theme)

def header(title, subtitle):
    st.markdown(f"<div class='page-heading'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)

def plot_line(data, field, title, height=300):
    chart = data[["date", field]].dropna().sort_values("date")
    fig = px.line(chart, x="date", y=field, markers=True, title=title)
    fig.update_layout(height=height, margin=dict(l=10,r=10,t=45,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color=theme["text"], xaxis_title="", yaxis_title=title,
        hovermode="x unified")
    fig.update_traces(line_color=theme["accent"], marker_color=theme["accent"], line_width=2.5)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def get_period():
    if df.empty or "date" not in df or df["date"].dropna().empty: return df.copy()
    lo, hi = df.date.min().date(), df.date.max().date()
    default_start = max(lo, (pd.Timestamp(hi)-pd.Timedelta(days=6)).date())
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📅 Date range")
        chosen = st.date_input("Choose dates", value=(default_start, hi), min_value=lo, max_value=hi)
    if isinstance(chosen, (tuple,list)) and len(chosen)==2: start,end=chosen
    elif isinstance(chosen, (tuple,list)) and len(chosen)==1: start=end=chosen[0]
    else: start=end=chosen
    return filter_by_dates(df,start,end)

def card(label, value, unit, icon):
    st.markdown(f"<div class='metric-card'><div class='metric-icon'>{icon}</div><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-note'>{unit}</div></div>", unsafe_allow_html=True)

def overview(data):
    header("Welcome, Emily! 🌷", "Your wellness journey matters. Let's celebrate your little wins.")
    st.markdown("<div class='welcome-note'>Small steps, repeated with care, can make a meaningful difference. Your dashboard helps you notice patterns—not chase perfection.</div>", unsafe_allow_html=True)
    if data.empty: st.info("No records for this date range."); return
    for col,(label,field,unit,icon,dec) in zip(st.columns(4),[
        ("Average Daily Steps","steps","steps/day","👟",0),
        ("Average Sleep","sleep_hours","hours/night","🌙",1),
        ("Daily Exercise","exercise_minutes","minutes/day","🏃",0),
        ("Water Intake","water_liters","litres/day","💧",1)]):
        with col: card(label,format_value(metric_average(data,field),dec),unit if field in data else "No data",icon)
    st.markdown("### Your wellness at a glance")
    cols=st.columns(3)
    for col,(label,field) in zip(cols,[("Steps Trend","steps"),("Sleep Duration","sleep_hours"),("Stress Score","stress_score")]):
        with col:
            if field in data and data[field].notna().any(): plot_line(data,field,label,270)
            else: st.info(f"{label}: data unavailable")
    st.markdown("### Personal insights")
    cols=st.columns(3)
    for col,(label,field,unit) in zip(cols,[("👟 Steps","steps","steps"),("🌙 Sleep","sleep_hours","hours"),("😊 Mood","mood_1to5","/5")]):
        with col:
            if field in data and data[field].notna().any():
                x=data.dropna(subset=[field]).sort_values(field); avg=data[field].mean()
                st.markdown(f"<div class='insight-card'><h4>{label}</h4><p>Average: <b>{format_value(avg,1)} {unit}</b></p><p>Highest: {format_value(x.iloc[-1][field],1)} on {x.iloc[-1]['date']:%d %b}</p><p>Lowest: {format_value(x.iloc[0][field],1)} on {x.iloc[0]['date']:%d %b}</p></div>",unsafe_allow_html=True)
            else: st.info(f"{label}: data unavailable")
    st.markdown("<div class='motivation-card'><div class='motivation-kicker'>☀️ YOUR DAILY MOTIVATION</div><h3>Discipline today builds the healthy, happy you tomorrow.</h3><p>You've got this, Emily! 🌷</p></div>",unsafe_allow_html=True)

def weekly(data):
    header("Weekly Summary","A simple look at Emily's recent wellness patterns.")
    if data.empty: st.info("No records for this date range."); return
    cols=st.columns(4)
    for col,(label,field,unit,dec) in zip(cols,[("Average steps","steps","steps/day",0),("Average sleep","sleep_hours","hours/night",1),("Exercise","exercise_minutes","minutes/day",0),("Water intake","water_liters","litres/day",1)]):
        with col: st.metric(label,format_value(metric_average(data,field),dec),unit)
    if "steps" in data and data.steps.notna().any():
        x=data.dropna(subset=["steps"]); a=x.loc[x.steps.idxmax()]; b=x.loc[x.steps.idxmin()]
        c1,c2=st.columns(2); c1.success(f"Highest steps: {a.steps:,.0f} on {a.date:%d %b %Y}"); c2.info(f"Lowest steps: {b.steps:,.0f} on {b.date:%d %b %Y}")
    c1,c2=st.columns(2)
    for col,(label,field) in zip([c1,c2],[("Daily steps","steps"),("Sleep duration","sleep_hours")]):
        with col:
            if field in data and data[field].notna().any(): plot_line(data,field,label,300)
    if "mood_1to5" in data and data.mood_1to5.notna().any(): plot_line(data,"mood_1to5","Mood across selected period",280)
    st.info("Use these summaries as gentle feedback. A single day does not define your wellness.")

def charts(data):
    header("Charts & Trends","Explore Emily's recorded wellness metrics over time.")
    if data.empty: st.info("No records for this date range."); return
    metrics={"Daily Steps":"steps","Sleep Duration":"sleep_hours","Exercise Minutes":"exercise_minutes","Stress Score":"stress_score","Water Intake":"water_liters","Mood":"mood_1to5","Calories Burned":"calories_burned","Distance Travelled":"distance_km","Sleep Score":"sleep_score","Resting Heart Rate":"resting_heart_rate","Average Heart Rate":"average_heart_rate","HRV":"hrv"}
    available={label:field for label,field in metrics.items() if field in data and data[field].notna().any()}
    if not available: st.warning("No chartable numeric metrics found."); return
    defaults=[x for x in ["Daily Steps","Sleep Duration","Exercise Minutes","Stress Score","Water Intake","Mood"] if x in available]
    selected=st.multiselect("Choose metrics to explore",list(available),default=defaults)
    for i in range(0,len(selected),2):
        cols=st.columns(2)
        for col,label in zip(cols,selected[i:i+2]):
            with col:
                field=available[label]; plot_line(data,field,label,320)
                st.caption(f"Selected-period average: {format_value(metric_average(data,field),2)}")
    if "exercise_type" in data and data.exercise_type.notna().any():
        st.markdown("### Exercise type distribution")
        counts=data.exercise_type.dropna().value_counts().rename_axis("Exercise type").reset_index(name="Days")
        fig=px.pie(counts,names="Exercise type",values="Days",hole=.48)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color=theme["text"])
        st.plotly_chart(fig,use_container_width=True)

def benchmarks(data):
    header("Wellness Benchmarks","General references to help you track progress—not pass-or-fail scores.")
    if data.empty: st.info("No records for this date range."); return
    items=[("👟","Daily steps","steps",8000,"steps/day","8,000 is an illustrative personal goal, not a universal requirement."),
           ("🌙","Sleep","sleep_hours",7,"hours/night","Adults generally need at least 7 hours of sleep."),
           ("🏃","Exercise","exercise_minutes",150/7,"minutes/day average","WHO guidance is 150–300 minutes of moderate activity weekly."),
           ("💧","Water intake","water_liters",2,"litres/day","2 litres is an illustrative comparison; needs vary.")]
    cols=st.columns(2)
    for i,(icon,label,field,target,unit,note) in enumerate(items):
        with cols[i%2]:
            st.markdown("<div class='benchmark-card'>",unsafe_allow_html=True); st.markdown(f"### {icon} {label}"); st.caption(note)
            value=metric_average(data,field)
            if value is None: st.info("No data available.")
            else:
                st.metric("Selected-period average",f"{format_value(value,1)} {unit}")
                ratio=max(0,min(float(value)/target,1)); st.progress(ratio,text=f"{ratio*100:.0f}% of comparison target")
                st.success("Meeting this reference goal.") if value>=target else st.info("A possible goal to work toward at your own pace.")
            st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("### Reference sources")
    st.markdown("- [CDC: About Sleep](https://www.cdc.gov/sleep/about/index.html)\n- [WHO: Physical Activity](https://www.who.int/news-room/fact-sheets/detail/physical-activity)")
    st.caption("This educational dashboard does not provide medical advice.")

def coaching(data):
    header("Personal Coaching","Gentle, practical ideas based on the selected records.")
    if data.empty: st.info("No records for this date range."); return
    items=[("👟","Movement","steps",8000,0,"steps/day","Try adding a short walk to your usual routine if manageable."),
           ("🌙","Sleep routine","sleep_hours",7,1,"hours/night","A consistent bedtime and calming wind-down may help."),
           ("🏃","Exercise","exercise_minutes",150/7,0,"minutes/day","Choose activities you enjoy and increase gradually."),
           ("💧","Hydration","water_liters",2,1,"litres/day","Keep water accessible and drink regularly according to your needs.")]
    cols=st.columns(2)
    for i,(icon,label,field,target,dec,unit,tip) in enumerate(items):
        with cols[i%2]:
            st.markdown("<div class='coaching-card'>",unsafe_allow_html=True); st.markdown(f"### {icon} {label}")
            val=metric_average(data,field)
            if val is None: st.write("This metric is not available in the selected records.")
            else:
                st.write(f"Your average: **{format_value(val,dec)} {unit}**.")
                st.write(tip)
                st.caption("You're meeting the comparison target." if val>=target else "Try one small step at a time.")
            st.markdown("</div>",unsafe_allow_html=True)
    mood=metric_average(data,"mood_1to5"); stress=metric_average(data,"stress_score")
    st.markdown("### Mood & stress check-in")
    if mood is not None and stress is not None: st.write(f"Average mood: **{mood:.1f}/5** · Average stress score: **{stress:.1f}**. Notice which routines support how you feel.")
    else: st.write("Mood or stress data is incomplete. Take a moment to check in with how you feel beyond the numbers.")
    st.markdown("<div class='motivation-card'><h3>You're stronger than you think, Emily.</h3><p>Small steps count. Be kind to yourself as you build routines. 🌷</p></div>",unsafe_allow_html=True)
    st.caption("Suggestions are informational and are not medical advice.")

def settings():
    header("Settings","Make WellnessWise feel like your space.")
    st.markdown("### Choose your colour theme")
    st.write("The layout stays the same; only the colours change.")
    cols=st.columns(3)
    desc={"Blush Pink":"Dusty rose, warm ivory, and soft cream.","Ocean Blue":"Muted blue, cool white, and blue-grey.","Midnight Purple":"Dark charcoal-purple with lavender accents."}
    for col,name in zip(cols,THEMES):
        with col:
            st.markdown("<div class='theme-card'>",unsafe_allow_html=True); st.markdown(f"### {name}"); st.write(desc[name])
            st.markdown("".join(f"<span style='display:inline-block;width:24px;height:24px;border-radius:6px;margin-right:5px;background:{c};border:1px solid #9995'></span>" for c in THEMES[name]["swatches"]),unsafe_allow_html=True)
            if st.session_state.theme_name==name: st.success("Currently selected")
            if st.button("Use this theme",key=f"theme_{name}",use_container_width=True):
                st.session_state.theme_name=name; st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("### About WellnessWise")
    st.write("An educational student project using synthetic wellness records for Emily Park. It is not a medical tool.")

with st.sidebar:
    st.markdown("<div class='brand'><div class='brand-mark'>🌷</div><div><div class='brand-name'>WellnessWise</div><div class='brand-tag'>YOUR DAILY WELLNESS COMPANION</div></div></div>",unsafe_allow_html=True)
    st.markdown("#### YOUR SPACE")
    for name,icon in [("Overview","⌂"),("Weekly Summary","▦"),("Charts","▥"),("Benchmarks","◎"),("Coaching","♡"),("Settings","⚙")]:
        if st.button(f"{icon}   {name}",key=f"nav_{name}",use_container_width=True,type="primary" if st.session_state.page==name else "secondary"):
            st.session_state.page=name; st.rerun()
    if not df.empty:
        lo,hi=df.date.min().date(),df.date.max().date()
        default_start=max(lo,(pd.Timestamp(hi)-pd.Timedelta(days=6)).date())
        st.markdown("---"); st.markdown("### 📅 Date range")
        chosen=st.date_input("Choose dates",value=(default_start,hi),min_value=lo,max_value=hi)
    else: chosen=None

if data_message:
    with st.sidebar: st.warning(data_message)
if df.empty:
    if st.session_state.page=="Settings": settings()
    else:
        header("Welcome, Emily! 🌷","Your wellness journey matters. Let's celebrate your little wins.")
        st.warning(data_message or "Add Emily's CSV to the data folder.")
else:
    if isinstance(chosen,(tuple,list)) and len(chosen)==2: start,end=chosen
    elif isinstance(chosen,(tuple,list)) and len(chosen)==1: start=end=chosen[0]
    else: start=end=chosen
    period=filter_by_dates(df,start,end)
    {"Overview":overview,"Weekly Summary":weekly,"Charts":charts,"Benchmarks":benchmarks,"Coaching":coaching,"Settings":settings}[st.session_state.page](period) if st.session_state.page!="Settings" else settings()
