import streamlit as st
THEMES={
"Blush Pink":{"background":"#FFF8F5","sidebar":"#F1DDDE","card":"#FFFFFF","accent":"#B77B84","accent_dark":"#8F5963","text":"#403438","muted":"#796B6F","border":"#EBD9D9","soft":"#F8E9E9","swatches":["#FFF8F5","#F1DDDE","#B77B84","#8F5963"]},
"Ocean Blue":{"background":"#F6FAFC","sidebar":"#DCE8EE","card":"#FFFFFF","accent":"#648DA3","accent_dark":"#456B80","text":"#303D46","muted":"#667984","border":"#D8E4EA","soft":"#E8F1F5","swatches":["#F6FAFC","#DCE8EE","#648DA3","#456B80"]},
"Midnight Purple":{"background":"#272735","sidebar":"#222230","card":"#353448","accent":"#A9A2D1","accent_dark":"#C2BCE7","text":"#F3F1FA","muted":"#C0BDD0","border":"#4B4962","soft":"#403E57","swatches":["#272735","#353448","#77739E","#B9B3DA"]}}
def apply_theme(t):
    st.markdown(f"""
    <style>
    :root{{--bg:{t['background']};--side:{t['sidebar']};--card:{t['card']};--accent:{t['accent']};--accentdark:{t['accent_dark']};--text:{t['text']};--muted:{t['muted']};--border:{t['border']};--soft:{t['soft']};}}
    .stApp{{background:var(--bg);color:var(--text)}} [data-testid="stSidebar"]{{background:var(--side);border-right:1px solid var(--border)}} [data-testid="stSidebar"] *{{color:var(--text)}}
    .block-container{{padding-top:2rem;padding-bottom:3rem;max-width:1500px}} h1,h2,h3,h4,p,label{{color:var(--text)}}
    .page-heading h1{{margin:0 0 .25rem;font-size:2.15rem;letter-spacing:-.04em}} .page-heading p{{margin-top:0;color:var(--muted)}}
    .brand{{display:flex;align-items:center;gap:.7rem;padding:.5rem 0 1rem}} .brand-mark{{display:flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:14px;background:var(--card);font-size:1.5rem}}
    .brand-name{{font-size:1.25rem;font-weight:750;letter-spacing:-.03em}} .brand-tag{{font-size:.58rem;letter-spacing:.12em;color:var(--muted)}}
    .welcome-note{{background:var(--soft);border:1px solid var(--border);padding:1rem 1.2rem;border-radius:16px;margin:.6rem 0 1.3rem}}
    .metric-card,.chart-card,.benchmark-card,.coaching-card,.theme-card,.insight-card{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1rem;margin-bottom:1rem;box-shadow:0 3px 12px #28202808}}
    .metric-card{{min-height:140px}} .metric-icon{{font-size:1.35rem;margin-bottom:.35rem}} .metric-label{{color:var(--muted);font-size:.86rem}} .metric-value{{font-size:1.75rem;font-weight:750;letter-spacing:-.04em;margin:.25rem 0}} .metric-note{{font-size:.75rem;color:var(--muted)}}
    .insight-card{{min-height:160px}} .insight-card p{{color:var(--muted);font-size:.9rem}} .motivation-card{{background:var(--soft);border:1px solid var(--border);border-radius:22px;padding:1.5rem;margin-top:1rem}}
    .motivation-kicker{{color:var(--accentdark);letter-spacing:.13em;font-size:.7rem;font-weight:800}} .motivation-card h3{{font-size:1.45rem;margin:.5rem 0}} .motivation-card p{{color:var(--muted);margin-bottom:0}}
    div[data-testid="stMetric"]{{background:var(--card);border:1px solid var(--border);padding:1rem;border-radius:16px}} div.stButton>button{{border-radius:12px;border:1px solid var(--border);font-weight:600}} div.stButton>button[kind="primary"]{{background:var(--accent);color:white;border:1px solid var(--accent)}} [data-testid="stProgressBar"]>div>div{{background:var(--accent)}}
    @media(max-width:700px){{.block-container{{padding:1rem}}.page-heading h1{{font-size:1.7rem}}.metric-value{{font-size:1.4rem}}}}
    </style>""",unsafe_allow_html=True)
