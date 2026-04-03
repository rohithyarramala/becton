import streamlit as st
import google.generativeai as genai
from streamlit_pdf_viewer import pdf_viewer
from supabase import create_client, Client
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(
    # Keywords: Bectagon 2k26, Schedule, BEC, AI Assistant
    page_title="BECTON | Bectagon 2k26 Schedule & AI Assistant", 
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://becbapatla.ac.in',
        'Report a bug': "mailto:rohithyarramala@gmail.com",
        'About': "# BECTON\nOfficial AI Guide for Bectagon 2k26. Created by Rohith Yarramala."
    }
)
# --- INITIALIZE SUPABASE & AI ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# --- FUTURISTIC CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

/* ═══ ROOT THEME ═══ */
:root {
    --neon-cyan: #00f5ff;
    --neon-green: #39ff14;
    --neon-purple: #bf00ff;
    --neon-orange: #ff6b00;
    --dark-bg: #050810;
    --card-bg: rgba(0, 245, 255, 0.03);
    --card-border: rgba(0, 245, 255, 0.15);
    --grid-color: rgba(0, 245, 255, 0.04);
    --glow-sm: 0 0 10px rgba(0, 245, 255, 0.3);
    --glow-md: 0 0 20px rgba(0, 245, 255, 0.4), 0 0 40px rgba(0, 245, 255, 0.1);
    --glow-lg: 0 0 30px rgba(0, 245, 255, 0.5), 0 0 60px rgba(0, 245, 255, 0.2), 0 0 100px rgba(0, 245, 255, 0.05);
    --font-display: 'Orbitron', monospace;
    --font-body: 'Rajdhani', sans-serif;
    --font-mono: 'Share Tech Mono', monospace;
}

/* ═══ GLOBAL RESET ═══ */
.stApp {
    background-color: var(--dark-bg) !important;
    background-image:
        linear-gradient(var(--grid-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-color) 1px, transparent 1px),
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0, 245, 255, 0.08) 0%, transparent 70%);
    background-size: 40px 40px, 40px 40px, 100% 100%;
    font-family: var(--font-body) !important;
    color: #c8e6f0 !important;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060c18 0%, #050810 60%, #08040e 100%) !important;
    border-right: 1px solid var(--card-border) !important;
    box-shadow: 4px 0 30px rgba(0, 245, 255, 0.05) !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-purple), var(--neon-cyan), transparent);
    animation: borderFlow 3s linear infinite;
}

@keyframes borderFlow {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

/* ═══ SIDEBAR LOGO AREA ═══ */
.sidebar-logo {
    text-align: center;
    padding: 20px 10px 30px;
    border-bottom: 1px solid var(--card-border);
    margin-bottom: 20px;
}

.sidebar-logo .logo-hex {
    width: 70px; height: 70px;
    margin: 0 auto 12px;
    background: conic-gradient(from 0deg, var(--neon-cyan), var(--neon-purple), var(--neon-cyan));
    clip-path: polygon(50% 0%, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%);
    display: flex; align-items: center; justify-content: center;
    animation: hexSpin 8s linear infinite;
    position: relative;
}

@keyframes hexSpin {
    0% { filter: hue-rotate(0deg) brightness(1); }
    50% { filter: hue-rotate(60deg) brightness(1.3); }
    100% { filter: hue-rotate(0deg) brightness(1); }
}

.sidebar-logo .logo-inner {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 900;
    color: var(--dark-bg);
    position: absolute;
}

.sidebar-logo h1 {
    font-family: var(--font-display) !important;
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    letter-spacing: 4px !important;
    background: linear-gradient(135deg, var(--neon-cyan), #fff, var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 4px !important;
    text-shadow: none;
}

.sidebar-logo p {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    color: rgba(0, 245, 255, 0.5) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase;
    margin: 0 !important;
}

/* ═══ SIDEBAR NAV ITEMS ═══ */
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stSelectbox > label {
    font-family: var(--font-body) !important;
    color: rgba(0, 245, 255, 0.7) !important;
    font-size: 0.7rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    color: var(--neon-cyan) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    border-radius: 4px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div:hover {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-sm) !important;
}

/* Sidebar stat mini cards */
.sidebar-stat {
    background: rgba(0, 245, 255, 0.04);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-left: 3px solid var(--neon-cyan);
    border-radius: 4px;
    padding: 10px 14px;
    margin: 8px 0;
    font-family: var(--font-mono);
}

.sidebar-stat .stat-label {
    font-size: 0.6rem;
    color: rgba(0, 245, 255, 0.5);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.sidebar-stat .stat-value {
    font-size: 1.1rem;
    color: var(--neon-cyan);
    font-weight: 700;
}

/* Sidebar online indicator */
.online-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(57, 255, 20, 0.1);
    border: 1px solid rgba(57, 255, 20, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--neon-green);
    letter-spacing: 1px;
    margin-top: 12px;
}

.pulse-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--neon-green);
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

/* ═══ TICKER ═══ */
.ticker-wrap {
    background: linear-gradient(90deg, #060c18, #0a1428, #060c18);
    border-top: 1px solid rgba(0, 245, 255, 0.2);
    border-bottom: 1px solid rgba(0, 245, 255, 0.2);
    padding: 10px 0;
    overflow: hidden;
    position: relative;
    margin-bottom: 28px;
}

.ticker-wrap::before,
.ticker-wrap::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 60px;
    z-index: 2;
}

.ticker-wrap::before { left: 0; background: linear-gradient(90deg, #060c18, transparent); }
.ticker-wrap::after { right: 0; background: linear-gradient(-90deg, #060c18, transparent); }

.ticker-label {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    background: var(--neon-cyan);
    color: var(--dark-bg);
    font-family: var(--font-display);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    z-index: 3;
}

.ticker-content {
    white-space: nowrap;
    animation: ticker 35s linear infinite;
    font-family: var(--font-mono);
    color: var(--neon-cyan);
    font-size: 0.85rem;
    letter-spacing: 1px;
    padding-left: 80px;
    display: inline-block;
}

@keyframes ticker {
    0% { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

.ticker-sep { color: rgba(0, 245, 255, 0.3); margin: 0 16px; }

/* ═══ PAGE HEADERS ═══ */
.page-header {
    margin-bottom: 32px;
    position: relative;
    padding-bottom: 16px;
}

.page-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 60px; height: 2px;
    background: linear-gradient(90deg, var(--neon-cyan), transparent);
}

.page-header h1 {
    font-family: var(--font-display) !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    letter-spacing: 6px !important;
    color: #fff !important;
    margin: 0 0 6px !important;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.4);
}

.page-header .sub {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: rgba(0, 245, 255, 0.5);
    letter-spacing: 4px;
    text-transform: uppercase;
}

/* ═══ GLASS CARDS ═══ */
.glass-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 24px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    opacity: 0.6;
}

.glass-card:hover {
    border-color: rgba(0, 245, 255, 0.35);
    box-shadow: var(--glow-sm);
}

.glass-card-title {
    font-family: var(--font-display);
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: var(--neon-cyan);
    text-transform: uppercase;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.glass-card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--card-border), transparent);
}

/* ═══ CHAT INTERFACE ═══ */
[data-testid="stChatInput"] textarea {
    background: rgba(0, 245, 255, 0.03) !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
    border-radius: 6px !important;
    color: #c8e6f0 !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-sm) !important;
    outline: none !important;
}

[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(191,0,255,0.15)) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stChatInput"] button:hover {
    box-shadow: var(--glow-sm) !important;
    border-color: var(--neon-cyan) !important;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(0, 245, 255, 0.02) !important;
    border: 1px solid rgba(0, 245, 255, 0.07) !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    border-left: 3px solid rgba(191, 0, 255, 0.5) !important;
}

[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-left: 3px solid rgba(0, 245, 255, 0.5) !important;
}

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(0, 245, 255, 0.3) !important;
    color: var(--neon-cyan) !important;
    font-family: var(--font-display) !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.1), transparent);
    transition: left 0.4s ease;
}

.stButton > button:hover {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-sm), inset 0 0 20px rgba(0,245,255,0.05) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:hover::before { left: 100%; }
/* ═══ REFINED INPUTS ═══ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
[data-testid="stChatInput"] textarea {
    background: rgba(0, 245, 255, 0.02) !important;
    border: 1px solid rgba(0, 245, 255, 0.1) !important;
    border-radius: 8px !important;
            padding: 10px 14px !important;
    color: #c8e6f0 !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    outline: none !important; /* Removes the awkward default browser ring */
    box-shadow: none !important;
}

/* Smooth Hover State */
.stTextInput > div > div > input:hover,
.stTextArea > div > div > textarea:hover {
    border-color: rgba(0, 245, 255, 0.3) !important;
    background: rgba(0, 245, 255, 0.04) !important;
}

/* Focused State (Active) */
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--neon-cyan) !important;
    background: rgba(0, 245, 255, 0.06) !important;
    box-shadow: 0 0 15px rgba(0, 245, 255, 0.15) !important;
    outline: none !important;
}

/* Labels */
.stTextInput > label,
.stTextArea > label,
.stFileUploader > label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    color: rgba(0, 245, 255, 0.5) !important;
    text-transform: uppercase !important;
    margin-bottom: 5px !important;
}
/* ═══ METRICS ═══ */
[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 8px !important;
    padding: 16px !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    color: rgba(0, 245, 255, 0.5) !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 1.4rem !important;
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 20px rgba(0, 245, 255, 0.5) !important;
}

/* ═══ ALERTS ═══ */
.stAlert {
    background: rgba(255, 107, 0, 0.06) !important;
    border: 1px solid rgba(255, 107, 0, 0.3) !important;
    border-radius: 4px !important;
    font-family: var(--font-body) !important;
}

.stSuccess {
    background: rgba(57, 255, 20, 0.06) !important;
    border: 1px solid rgba(57, 255, 20, 0.3) !important;
    border-radius: 4px !important;
    font-family: var(--font-body) !important;
}

/* ═══ FILE UPLOADER ═══ */
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(0, 245, 255, 0.2) !important;
    border-radius: 6px !important;
    background: rgba(0, 245, 255, 0.02) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(0, 245, 255, 0.4) !important;
    box-shadow: var(--glow-sm) !important;
}

/* ═══ SUBHEADERS ═══ */
.stMarkdown h3 {
    font-family: var(--font-display) !important;
    font-size: 0.8rem !important;
    letter-spacing: 4px !important;
    color: var(--neon-cyan) !important;
    text-transform: uppercase !important;
    margin-top: 28px !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid var(--card-border) !important;
}

/* ═══ SCROLLBAR ═══ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--dark-bg); }
::-webkit-scrollbar-thumb { background: rgba(0, 245, 255, 0.3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

/* ═══ DIVIDER ═══ */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--card-border), transparent) !important;
    margin: 20px 0 !important;
}

/* ═══ SPINNER ═══ */
.stSpinner > div {
    border-color: var(--neon-cyan) transparent transparent !important;
}

/* ═══ SCAN LINE EFFECT ═══ */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.03) 2px,
        rgba(0, 0, 0, 0.03) 4px
    );
    z-index: 9999;
}

/* ═══ STATUS BADGE ═══ */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.status-online {
    background: rgba(57, 255, 20, 0.08);
    border: 1px solid rgba(57, 255, 20, 0.3);
    color: var(--neon-green);
}

.status-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 1.5s ease infinite;
}

/* ═══ CORNER DECORATIONS ═══ */
.corner-deco {
    position: relative;
    padding: 2px;
}
.corner-deco::before, .corner-deco::after {
    content: '';
    position: absolute;
    width: 10px; height: 10px;
}
.corner-deco::before {
    top: 0; left: 0;
    border-top: 2px solid var(--neon-cyan);
    border-left: 2px solid var(--neon-cyan);
}
.corner-deco::after {
    bottom: 0; right: 0;
    border-bottom: 2px solid var(--neon-purple);
    border-right: 2px solid var(--neon-purple);
}

/* ═══ ABOUT PAGE TECH PILLS ═══ */
.tech-pill {
    display: inline-block;
    background: rgba(0, 245, 255, 0.06);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 4px;
    padding: 6px 16px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--neon-cyan);
    letter-spacing: 1px;
    margin: 4px;
}

.tech-pill.purple {
    background: rgba(191, 0, 255, 0.06);
    border-color: rgba(191, 0, 255, 0.25);
    color: #d470ff;
}

.tech-pill.green {
    background: rgba(57, 255, 20, 0.05);
    border-color: rgba(57, 255, 20, 0.2);
    color: var(--neon-green);
}

/* ═══ STAT ROW ═══ */
.stat-row {
    display: flex;
    gap: 12px;
    margin: 16px 0;
    flex-wrap: wrap;
}

.stat-box {
    flex: 1;
    min-width: 100px;
    background: rgba(0, 245, 255, 0.03);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-top: 2px solid var(--neon-cyan);
    border-radius: 4px;
    padding: 14px 16px;
    text-align: center;
}

.stat-box .num {
    font-family: var(--font-display);
    font-size: 1.6rem;
    font-weight: 900;
    color: var(--neon-cyan);
    text-shadow: 0 0 20px rgba(0,245,255,0.4);
    line-height: 1;
}

.stat-box .lbl {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 2px;
    color: rgba(0, 245, 255, 0.5);
    text-transform: uppercase;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)


# --- HELPER: LIVE TICKER ---
def get_updates():
    res = supabase.table("updates").select("content").order("created_at", desc=True).limit(5).execute()
    return [row['content'] for row in res.data] if res.data else ["BECTAGON 2K26 IS LIVE — GET READY TO WITNESS THE FUTURE"]

# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-hex">
            <span class="logo-inner">B</span>
        </div>
        <h1>BECTON</h1>
        <p>AI Event Intelligence</p>
        <div class="online-badge">
            <div class="pulse-dot"></div>
            SYSTEMS ONLINE
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "◈  NAVIGATION",
        ["⚡ Becton Chat", "📡 Organizer Portal", "🛠️ Admin Console", "🌐 About Becton"],
        key="page_select"
    )

    st.markdown("---")

    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:rgba(0,245,255,0.4);
         letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">◈ System Status</div>

    <div class="sidebar-stat">
        <div class="stat-label">Active Model</div>
        <div class="stat-value" style="font-size:0.85rem;">Gemini 2.0 Flash</div>
    </div>
    <div class="sidebar-stat" style="border-left-color:#bf00ff;">
        <div class="stat-label">Event</div>
        <div class="stat-value" style="font-size:0.85rem; color:#d470ff;">Bectagon 2k26</div>
    </div>
    <div class="sidebar-stat" style="border-left-color:#39ff14;">
        <div class="stat-label">Status</div>
        <div class="stat-value" style="font-size:0.85rem; color:#39ff14;">● LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.55rem;
         color:rgba(0,245,255,0.25); letter-spacing:1px; text-align:center; margin-top:auto; padding-top:20px;">
        BAPATLA ENGINEERING COLLEGE<br>
        © 2026 — BECTAGON EDITION
    </div>
    """, unsafe_allow_html=True)

# ─── LIVE TICKER ───────────────────────────────────────────
updates = get_updates()
items = " <span class='ticker-sep'>///</span> ".join([f"⚡ {u}" for u in updates])
st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker-label">LIVE</div>
    <div class="ticker-content">{items} <span class="ticker-sep">///</span> {items}</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: CHAT
# ═══════════════════════════════════════════════════════════
if page == "⚡ Becton Chat":
    st.markdown("""
    <div class="page-header">
        <h1>BECTON CHAT</h1>
        <div class="sub">◈ AI-POWERED EVENT INTELLIGENCE INTERFACE</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="glass-card-title">◈ Neural Query Interface</div>
        """, unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat messages
        chat_container = st.container(height=500)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align:center; padding: 60px 20px; font-family:'Share Tech Mono',monospace;">
                    <div style="font-size:2rem; margin-bottom:16px; opacity:0.3;">⚡</div>
                    <div style="color:rgba(0,245,255,0.3); font-size:0.75rem; letter-spacing:3px; text-transform:uppercase;">
                        BECTON IS READY<br>ASK ME ANYTHING ABOUT BECTAGON 2K26
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for role, text in st.session_state.chat_history:
                    with st.chat_message("user" if role == "You" else "assistant"):
                        st.write(text)

        user_input = st.chat_input("⚡  Ask Becton about Bectagon 2k26...")
        if user_input:
            with st.spinner("🔮 Processing query..."):
                resp = model.generate_content(
                    f"You are BECTON, the AI assistant for Bectagon 2k26 at Bapatla Engineering College. "
                    f"Answer in 2-3 sentences, be energetic and futuristic in tone. "
                    f"User question: {user_input}"
                )
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Becton", resp.text))
            st.rerun()

    with col2:
        st.markdown("""
        <div class="glass-card-title">◈ Schedule Reference Matrix</div>
        """, unsafe_allow_html=True)

        pdf_path = "bectagon_schedule.pdf"
        if os.path.exists(pdf_path):
            pdf_viewer(pdf_path, height=520)
        else:
            st.markdown("""
            <div style="
                border: 1px dashed rgba(0,245,255,0.15);
                border-radius: 6px;
                padding: 60px 20px;
                text-align: center;
                font-family: 'Share Tech Mono', monospace;
                height: 520px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <div style="font-size:3rem; opacity:0.15; margin-bottom:16px;">📄</div>
                <div style="color:rgba(255,107,0,0.7); font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">
                    SCHEDULE PDF NOT UPLOADED
                </div>
                <div style="color:rgba(0,245,255,0.3); font-size:0.6rem; letter-spacing:1px; margin-top:8px;">
                    Upload via Admin Console
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quick stats row
    st.markdown("""
    <div class="stat-row" style="margin-top: 24px;">
        <div class="stat-box"><div class="num">24H</div><div class="lbl">Uptime</div></div>
        <div class="stat-box" style="border-top-color:#bf00ff;"><div class="num" style="color:#d470ff;">∞</div><div class="lbl">Queries</div></div>
        <div class="stat-box" style="border-top-color:#39ff14;"><div class="num" style="color:#39ff14; font-size:1rem;">LIVE</div><div class="lbl">Status</div></div>
        <div class="stat-box" style="border-top-color:#ff6b00;"><div class="num" style="color:#ff9f40;">2K26</div><div class="lbl">Edition</div></div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: ORGANIZER PORTAL
# ═══════════════════════════════════════════════════════════
elif page == "📡 Organizer Portal":
    st.markdown("""
    <div class="page-header">
        <h1>ORGANIZER PORTAL</h1>
        <div class="sub">◈ AUTHORIZED BROADCAST CONTROL SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown("""
        <div class="glass-card-title">◈ Authentication Matrix</div>
        """, unsafe_allow_html=True)

        user = st.text_input("OPERATOR ID", placeholder="Enter username...")
        pw = st.text_input("ACCESS KEY", type="password", placeholder="Enter password...")

    with col2:
        if user == st.secrets.get("ADMIN_USER") and pw == st.secrets.get("ADMIN_PASS"):
            st.markdown("""
            <div class="glass-card-title">◈ Broadcast Transmission</div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="
                background: rgba(57,255,20,0.06);
                border: 1px solid rgba(57,255,20,0.25);
                border-left: 3px solid #39ff14;
                border-radius: 4px;
                padding: 10px 16px;
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.7rem;
                color: #39ff14;
                letter-spacing: 2px;
                margin-bottom: 20px;
            ">◈ AUTHENTICATION VERIFIED — ACCESS GRANTED</div>
            """, unsafe_allow_html=True)

            new_msg = st.text_area(
                "BROADCAST MESSAGE",
                placeholder="Enter live ticker message (max 100 chars)...",
                max_chars=100,
                height=100
            )
            char_count = len(new_msg) if new_msg else 0
            st.markdown(f"""
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem;
                 color:{'rgba(255,107,0,0.7)' if char_count > 80 else 'rgba(0,245,255,0.4)'};
                 letter-spacing:1px; margin-bottom:12px;">
                CHARS: {char_count}/100
            </div>
            """, unsafe_allow_html=True)

            if st.button("⚡  BROADCAST TO TICKER"):
                bad_words = ["bad", "fail", "delay", "worst", "cancel", "postpone"]
                if any(w in new_msg.lower() for w in bad_words):
                    st.error("⚠ Transmission rejected — maintain positive signal integrity.")
                elif len(new_msg.strip()) < 5:
                    st.warning("⚠ Message too short. Minimum 5 characters.")
                else:
                    supabase.table("updates").insert({"content": new_msg}).execute()
                    st.success("✓ Message broadcasted to live ticker successfully.")
                    st.rerun()

            st.markdown("---")
            st.markdown("""
            <div class="glass-card-title">◈ Recent Transmissions</div>
            """, unsafe_allow_html=True)

            updates_data = supabase.table("updates").select("content, created_at").order("created_at", desc=True).limit(5).execute()
            if updates_data.data:
                for row in updates_data.data:
                    ts = row.get("created_at", "")[:16].replace("T", " ")
                    st.markdown(f"""
                    <div style="
                        background: rgba(0,245,255,0.02);
                        border-left: 2px solid rgba(0,245,255,0.2);
                        padding: 8px 14px;
                        margin: 6px 0;
                        border-radius: 0 4px 4px 0;
                        font-family:'Share Tech Mono',monospace;
                    ">
                        <div style="font-size:0.75rem; color:#c8e6f0;">{row['content']}</div>
                        <div style="font-size:0.58rem; color:rgba(0,245,255,0.3); margin-top:4px; letter-spacing:1px;">{ts}</div>
                    </div>
                    """, unsafe_allow_html=True)
        elif user or pw:
            st.markdown("""
            <div style="
                background: rgba(255,107,0,0.06);
                border: 1px solid rgba(255,107,0,0.3);
                border-left: 3px solid #ff6b00;
                border-radius: 4px;
                padding: 10px 16px;
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.7rem;
                color: #ff9f40;
                letter-spacing: 2px;
                margin-top: 20px;
            ">◈ ACCESS DENIED — INVALID CREDENTIALS</div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: ADMIN CONSOLE
# ═══════════════════════════════════════════════════════════
elif page == "🛠️ Admin Console":
    st.markdown("""
    <div class="page-header">
        <h1>ADMIN CONSOLE</h1>
        <div class="sub">◈ SYSTEM CONTROL & CONTENT MANAGEMENT</div>
    </div>
    """, unsafe_allow_html=True)

    pw = st.text_input("ADMIN AUTHORIZATION KEY", type="password", placeholder="Enter admin key...")

    if pw == "Becton123":
        st.markdown("""
        <div style="
            background: rgba(57,255,20,0.06);
            border: 1px solid rgba(57,255,20,0.25);
            border-left: 3px solid #39ff14;
            border-radius: 4px;
            padding: 10px 16px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.7rem;
            color: #39ff14;
            letter-spacing: 2px;
            margin: 16px 0 28px;
        ">◈ ADMIN ACCESS GRANTED — ALL SYSTEMS ACCESSIBLE</div>
        """, unsafe_allow_html=True)

        # Metrics
        st.markdown('<div class="glass-card-title">◈ System Diagnostics</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("AI Model", "Gemini 2.0")
        with c2: st.metric("Cost / 1k Users", "$0.08")
        with c3: st.metric("DB Provider", "Supabase")
        with c4: st.metric("UI Framework", "Streamlit")

        st.markdown("---")

        # Upload
        st.markdown('<div class="glass-card-title">◈ Content Matrix Upload</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "UPLOAD SCHEDULE PDF",
            type="pdf",
            help="This will replace the currently displayed schedule for all users."
        )
        if uploaded_file:
            with open("bectagon_schedule.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✓ Schedule PDF updated — '{uploaded_file.name}' is now live for all users.")

        st.markdown("---")

        # Danger zone
        st.markdown('<div class="glass-card-title" style="color:rgba(255,107,0,0.8);">◈ Ticker Management</div>', unsafe_allow_html=True)

        count_res = supabase.table("updates").select("id", count="exact").execute()
        count = count_res.count if count_res.count else 0
        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:rgba(0,245,255,0.5); margin-bottom:12px;">
            TOTAL BROADCASTS IN DB: <span style="color:var(--neon-cyan);">{count}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚠ FLUSH ALL TICKER MESSAGES"):
            supabase.table("updates").delete().neq("id", 0).execute()
            st.success("✓ Ticker cleared. Default message will display.")
            st.rerun()

    elif pw:
        st.markdown("""
        <div style="
            background: rgba(255,107,0,0.06);
            border: 1px solid rgba(255,107,0,0.3);
            border-left: 3px solid #ff6b00;
            border-radius: 4px;
            padding: 10px 16px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.7rem;
            color: #ff9f40;
            letter-spacing: 2px;
            margin-top: 12px;
        ">◈ UNAUTHORIZED — INVALID ADMIN KEY</div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════════
elif page == "🌐 About Becton":
    st.markdown("""
    <div class="page-header">
        <h1>ABOUT BECTON</h1>
        <div class="sub">◈ AI INTELLIGENCE ARCHITECTURE & ORIGIN PROTOCOL</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="glass-card-title">◈ Mission Protocol</div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.05rem; color:#c8e6f0; line-height:1.8; margin-bottom:28px;">
            <strong style="color:#00f5ff;">BECTON</strong> is Bapatla Engineering College's first
            AI-powered Event Intelligence System — built to handle real-time student queries,
            broadcast live updates, and manage all information streams for
            <strong style="color:#bf00ff;">Bectagon 2k26</strong>.
        </div>

        <div class="glass-card-title">◈ Creator Node</div>
        <div style="
            background: rgba(0,245,255,0.03);
            border: 1px solid rgba(0,245,255,0.12);
            border-radius: 6px;
            padding: 20px 24px;
            font-family:'Rajdhani',sans-serif;
            margin-bottom:24px;
        ">
            <div style="font-family:'Orbitron',monospace; font-size:1.1rem; font-weight:900;
                 color:#fff; letter-spacing:2px; margin-bottom:4px;">
                ROHITH YARRAMALA
            </div>
            <div style="color:rgba(0,245,255,0.5); font-size:0.75rem; font-family:'Share Tech Mono',monospace;
                 letter-spacing:2px; margin-bottom:12px;">
                FINAL YEAR · CSE · REG: L23ACS615
            </div>
            <div style="color:#c8e6f0; font-size:0.9rem;">
                AI Research & Development · Bectagon 2k26 Technical Lead
            </div>
        </div>

        <div class="glass-card-title">◈ Tech Stack</div>
        <div>
            <span class="tech-pill">Gemini 2.0 Flash-Lite</span>
            <span class="tech-pill purple">Supabase DB</span>
            <span class="tech-pill">Streamlit</span>
            <span class="tech-pill green">Python 3.11</span>
            <span class="tech-pill purple">Real-time Broadcast</span>
            <span class="tech-pill">PDF Viewer</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card-title">◈ Capability Matrix</div>
        """, unsafe_allow_html=True)

        features = [
            ("⚡", "Real-time Q&A", "AI-powered instant responses to event queries"),
            ("📡", "Live Broadcasting", "Organizer-controlled live ticker feed"),
            ("🔐", "Secure Portals", "Role-based access for organizers & admins"),
            ("📄", "Schedule Matrix", "Integrated PDF schedule viewer"),
            ("🛠️", "Admin Console", "Full content & system management"),
        ]

        for icon, title, desc in features:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 14px;
                padding: 14px 0;
                border-bottom: 1px solid rgba(0,245,255,0.06);
            ">
                <div style="
                    width: 36px; height: 36px;
                    background: rgba(0,245,255,0.06);
                    border: 1px solid rgba(0,245,255,0.15);
                    border-radius: 4px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1rem; flex-shrink: 0;
                ">{icon}</div>
                <div>
                    <div style="font-family:'Orbitron',monospace; font-size:0.65rem;
                         font-weight:700; letter-spacing:2px; color:#00f5ff;
                         text-transform:uppercase; margin-bottom:4px;">{title}</div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:0.85rem;
                         color:rgba(200,230,240,0.6); line-height:1.4;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if os.path.exists("bec_logo.png"):
            st.image("bec_logo.png", width=120)