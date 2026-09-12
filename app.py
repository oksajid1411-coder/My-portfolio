# ==========================================
# IMPORTS
# ==========================================
import re
import streamlit as st
from supabase import create_client, Client
import html
import urllib.parse
# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="MD. Omar Kamran Chy | Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SUPABASE CONNECTION
# ==========================================
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"⚠️ Supabase Configuration Error: Missing or invalid credentials in Streamlit Secrets. Details: {e}")
        st.stop()

supabase = init_supabase()

@st.cache_resource
def get_supabase_client() -> Client:

    try:
        # Streamlit Cloud Advanced Settings / secrets.toml থেকে ডাটা নেওয়া হচ্ছে
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except KeyError as e:
        st.error(f"⚠️ Secrets missing: {e}. Please add SUPABASE_URL and SUPABASE_KEY in Secrets.")
        return None
    except Exception as e:
        st.error(f"❌ Failed to connect to Supabase: {e}")
        return None


# ==========================================
# AUTHENTICATION
# ==========================================
def check_admin_auth():
    return st.session_state.get("admin_authenticated", False)

def login_admin(code_input):
    try:
        correct_code = st.secrets["ADMIN_CODE"]
        if code_input == correct_code:
            st.session_state["admin_authenticated"] = True
            st.session_state["auth_error"] = False
        else:
            st.session_state["auth_error"] = True
    except Exception:
        st.error("ADMIN_CODE missing in Streamlit Secrets.")

def logout_admin():
    st.session_state["admin_authenticated"] = False

# ==========================================
# VALIDATION
# ==========================================
def is_valid_url(url: str) -> bool:
    if not url:
        return True
    pattern = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# ==========================================
# DATABASE FUNCTIONS
# ==========================================

# Profiles
def get_profile():
    res = supabase.table("profiles").select("*").limit(1).execute()
    return res.data[0] if res.data else {}

def update_profile(profile_id, data):
    return supabase.table("profiles").update(data).eq("id", profile_id).execute()

# Skills
def get_skills():
    res = supabase.table("skills").select("*").order("display_order").execute()
    return res.data or []

def add_skill(data):
    return supabase.table("skills").insert(data).execute()

def update_skill(skill_id, data):
    return supabase.table("skills").update(data).eq("id", skill_id).execute()

def delete_skill(skill_id):
    return supabase.table("skills").delete().eq("id", skill_id).execute()

# Projects
def get_projects():
    res = supabase.table("projects").select("*").order("display_order").execute()
    return res.data or []

def add_project(data):
    return supabase.table("projects").insert(data).execute()

def update_project(project_id, data):
    return supabase.table("projects").update(data).eq("id", project_id).execute()

def delete_project(project_id):
    return supabase.table("projects").delete().eq("id", project_id).execute()

# Services
def get_services():
    res = supabase.table("services").select("*").order("display_order").execute()
    return res.data or []

def add_service(data):
    return supabase.table("services").insert(data).execute()

def update_service(service_id, data):
    return supabase.table("services").update(data).eq("id", service_id).execute()

def delete_service(service_id):
    return supabase.table("services").delete().eq("id", service_id).execute()

# Experience
def get_experience():
    res = supabase.table("experience").select("*").order("display_order").execute()
    return res.data or []

def add_experience(data):
    return supabase.table("experience").insert(data).execute()

def update_experience(exp_id, data):
    return supabase.table("experience").update(data).eq("id", exp_id).execute()

def delete_experience(exp_id):
    return supabase.table("experience").delete().eq("id", exp_id).execute()

# Learning Journey
def get_learning_journey():
    res = supabase.table("learning_journey").select("*").order("display_order").execute()
    return res.data or []

def add_learning_item(data):
    return supabase.table("learning_journey").insert(data).execute()

def update_learning_item(item_id, data):
    return supabase.table("learning_journey").update(data).eq("id", item_id).execute()

def delete_learning_item(item_id):
    return supabase.table("learning_journey").delete().eq("id", item_id).execute()

# Social Links
def get_social_links():
    res = supabase.table("social_links").select("*").order("display_order").execute()
    return res.data or []

def add_social_link(data):
    return supabase.table("social_links").insert(data).execute()

def update_social_link(link_id, data):
    return supabase.table("social_links").update(data).eq("id", link_id).execute()

def delete_social_link(link_id):
    return supabase.table("social_links").delete().eq("id", link_id).execute()

# ==========================================
# CSS (DARK THEME)
# ==========================================
st.markdown("""
<style>
    /* Dark Theme Global Styling */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Card Component */
    .custom-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Badges */
    .badge {
        background-color: #3b82f6;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-secondary {
        background-color: #475569;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700;
    }
    
    /* Timeline */
    .timeline-item {
        border-left: 2px solid #3b82f6;
        padding-left: 20px;
        margin-left: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# HOME PAGE (ULTRA-PROFESSIONAL EDITION)
# ==========================================
def render_home():
    profile = get_profile() or {}

    # --------------------------------------
    # EXECUTIVE CSS STYLING
    # --------------------------------------
    st.markdown("""
    <style>
        /* Modern Keyframe Animations */
        @keyframes pulse-dot {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        @keyframes text-gradient-flow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphic Container Cards */
        .pro-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .pro-card:hover {
            transform: translateY(-6px);
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4), 0 0 25px rgba(59, 130, 246, 0.15);
        }

        .pro-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.6), transparent);
        }

        /* Animated Typography */
        .hero-title {
            background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #3b82f6 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            animation: text-gradient-flow 6s ease infinite;
        }

        /* Status & Badges */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #4ade80;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .status-dot-active {
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            animation: pulse-dot 2s infinite;
        }

        .skill-badge {
            background: rgba(30, 58, 138, 0.35);
            color: #93c5fd;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin: 4px 4px 4px 0;
            border: 1px solid rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
        }

        .skill-badge:hover {
            background: #2563eb;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        /* Executive Metric Tiles */
        .metric-tile {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .metric-tile:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(59, 130, 246, 0.4);
            transform: translateY(-4px);
        }

        .metric-label {
            font-size: 0.75rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .metric-val {
            font-size: 1.35rem;
            color: #f8fafc;
            font-weight: 700;
        }

        /* Workflow Step Flow */
        .workflow-box {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .workflow-node {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e2e8f0;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.88rem;
            font-weight: 600;
            text-align: center;
            flex: 1;
            min-width: 120px;
            transition: all 0.3s ease;
        }

        .workflow-node:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
        }

        .workflow-arrow {
            color: #60a5fa;
            font-weight: 700;
            font-size: 1.1rem;
        }

        /* Image Masking */
        .avatar-frame img {
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 12px 32px rgba(0,0,0,0.4);
            transition: all 0.4s ease;
        }

        .avatar-frame img:hover {
            transform: scale(1.02);
            border-color: #3b82f6;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # HERO SECTION
    # --------------------------------------
    hero_col1, hero_col2 = st.columns([1, 2.2], gap="large")

    with hero_col1:
        st.markdown('<div class="avatar-frame">', unsafe_allow_html=True)
        img_url = "https://raw.githubusercontent.com/oksajid1411-coder/My-portfolio/master/sajid_imag.jpg"
        if img_url:
            st.image(img_url, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with hero_col2:
        name = profile.get("name", "MD. Omar Kamran Chy")
        title = profile.get("title", "Data Scientist & ML Engineer")
        location = profile.get("location", "Chattogram, Bangladesh")
        email = profile.get("email", "")
        bio = profile.get("bio", "Passionate about transforming complex datasets into actionable business intelligence and high-performing machine learning architectures.")

        st.markdown(f"<div class='hero-title'>{name}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #60a5fa; font-size: 1.2rem; font-weight: 600; margin-top: -5px;'>{title}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #94a3b8; font-size: 0.95rem;'>📍 {location} &nbsp;•&nbsp; ✉️ <a href='mailto:{email}' style='color:#94a3b8; text-decoration:none;'>{email}</a></p>", unsafe_allow_html=True)

        st.markdown(f"<p style='color:#cbd5e1; font-size: 1.02rem; line-height:1.6; margin-top:15px;'>{bio}</p>", unsafe_allow_html=True)

        # Action Buttons Layout
        btn_c1, btn_c2, btn_c3 = st.columns([1.1, 1.1, 1])
        with btn_c1:
            if st.button("📁 Explore Projects", use_container_width=True):
                st.session_state["nav"] = "Projects"
                st.rerun()
        with btn_c2:
            if st.button("✉️ Get In Touch", use_container_width=True):
                st.session_state["nav"] = "Contact"
                st.rerun()
        with btn_c3:
            st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)]({email})")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # METRICS & OVERVIEW
    # --------------------------------------
    sc1, sc2, sc3, sc4 = st.columns(4)
    exp_years = profile.get('experience_years', 1)

    with sc1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-label">Experience</div>
            <div class="metric-val">{exp_years}+ Year</div>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-label">Core Focus</div>
            <div class="metric-val">Data Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with sc3:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-label">Expertise</div>
            <div class="metric-val">ML & DL</div>
        </div>
        """, unsafe_allow_html=True)

    with sc4:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-label">Availability</div>
            <div class="status-pill" style="margin-top: 4px;">
                <span class="status-dot-active"></span> Open to Work
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)

    # --------------------------------------
    # CORE EXPERTISE CARDS
    # --------------------------------------
    st.markdown("<h2 style='font-size: 1.6rem; font-weight: 700; margin-bottom: 20px;'>⚡ Technical Domains</h2>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3, gap="medium")

    with col_a:
        st.markdown("""
        <div class="pro-card">
            <h3 style="margin-top:0; font-size:1.2rem; color:#f8fafc;">📊 Data Analysis</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.5; min-height:48px;">Transforming complex, unstructured datasets into intuitive and actionable visual intelligence.</p>
            <div>
                <span class="skill-badge">Data Cleaning</span>
                <span class="skill-badge">EDA</span>
                <span class="skill-badge">Visualization</span>
                <span class="skill-badge">Statistics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="pro-card">
            <h3 style="margin-top:0; font-size:1.2rem; color:#f8fafc;">🤖 Machine Learning</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.5; min-height:48px;">Engineering end-to-end predictive models, automated features, and robust algorithms.</p>
            <div>
                <span class="skill-badge">Regression</span>
                <span class="skill-badge">Classification</span>
                <span class="skill-badge">Feature Eng.</span>
                <span class="skill-badge">Evaluation</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="pro-card">
            <h3 style="margin-top:0; font-size:1.2rem; color:#f8fafc;">🧠 Deep Learning</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.5; min-height:48px;">Building neural networks, computer vision frameworks, and scalable deep architectures.</p>
            <div>
                <span class="skill-badge">Neural Networks</span>
                <span class="skill-badge">CNN</span>
                <span class="skill-badge">Computer Vision</span>
                <span class="skill-badge">PyTorch/TF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # WORKFLOW PIPELINE
    # --------------------------------------
    st.markdown("<h2 style='font-size: 1.6rem; font-weight: 700; margin-bottom: 20px;'>🔄 Analytical Workflow</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="workflow-box">
        <div class="workflow-node">📥 1. Collection</div>
        <div class="workflow-arrow">➔</div>
        <div class="workflow-node">🧹 2. Cleaning</div>
        <div class="workflow-arrow">➔</div>
        <div class="workflow-node">🔍 3. EDA</div>
        <div class="workflow-arrow">➔</div>
        <div class="workflow-node">⚙️ 4. Feature Eng.</div>
        <div class="workflow-arrow">➔</div>
        <div class="workflow-node">🤖 5. ML/DL Model</div>
        <div class="workflow-arrow">➔</div>
        <div class="workflow-node">🎯 6. Insights</div>
    </div>
    """, unsafe_allow_html=True)

import html

# ==========================================
# SKILLS PAGE (ANIMATED & GORGEOUS)
# ==========================================
def render_skills():
    # Safely fetch skills
    skills = get_skills() if 'get_skills' in globals() and callable(get_skills) else []
    
    if not skills:
        st.info("No skills currently listed.")
        return

    # --------------------------------------
    # HIGH-END STYLES & ANIMATIONS
    # --------------------------------------
    st.markdown("""
    <style>
        @keyframes pulseGlow {
            0% { box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); }
            50% { box-shadow: 0 8px 32px 0 rgba(59, 130, 246, 0.25); }
            100% { box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); }
        }

        /* Glassmorphic Skill Card */
        .pro-skill-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 18px 16px;
            text-align: left;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }

        /* Top Glowing Edge */
        .pro-skill-card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, #60a5fa, transparent);
            transition: all 0.6s ease;
        }

        .pro-skill-card:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: rgba(96, 165, 250, 0.5);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 25px rgba(59, 130, 246, 0.3);
        }

        .pro-skill-card:hover::before {
            left: 100%;
        }

        .skill-header-flex {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }

        .skill-name {
            color: #f8fafc;
            font-size: 1.02rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        /* Dynamic Skill Level Badges */
        .level-badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.70rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            transition: transform 0.3s ease;
        }

        .pro-skill-card:hover .level-badge {
            transform: scale(1.08);
        }

        .level-advanced {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.15);
        }

        .level-intermediate {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.35);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.15);
        }

        .level-beginner {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.35);
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.15);
        }

        /* Category Header Section */
        .category-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 30px 0 20px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
        }

        .category-title {
            color: #f8fafc;
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0;
        }

        .category-count {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # PAGE HEADER
    # --------------------------------------
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>⚡ Technical Expertise</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 25px;'>Comprehensive breakdown of my technical stack and proficiency levels.</p>", unsafe_allow_html=True)

    # --------------------------------------
    # CATEGORY FILTER
    # --------------------------------------
    categories = sorted(list(set([s.get("category", "Uncategorized") for s in skills])))
    
    col_filter, _ = st.columns([1.2, 2])
    with col_filter:
        selected_cat = st.selectbox("🎯 Filter Expertise", ["All Categories"] + categories)
    
    filtered_skills = skills if selected_cat == "All Categories" else [s for s in skills if s.get("category", "Uncategorized") == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # RENDER SKILLS BY CATEGORY
    # --------------------------------------
    display_cats = sorted(list(set([s.get("category", "Uncategorized") for s in filtered_skills])))

    for cat in display_cats:
        cat_skills = [s for s in filtered_skills if s.get("category", "Uncategorized") == cat]
        
        st.markdown(f'''
        <div class="category-container">
            <h3 class="category-title">🔹 {html.escape(str(cat))}</h3>
            <span class="category-count">{len(cat_skills)} Skills</span>
        </div>
        ''', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for idx, skill in enumerate(cat_skills):
            skill_name = html.escape(str(skill.get('name', 'Unnamed Skill')))
            raw_level = str(skill.get('level', 'Intermediate')).strip()
            level_lower = raw_level.lower()
            
            if 'adv' in level_lower or 'expert' in level_lower:
                badge_class = "level-advanced"
                display_level = "Advanced"
            elif 'beg' in level_lower or 'basic' in level_lower:
                badge_class = "level-beginner"
                display_level = "Beginner"
            else:
                badge_class = "level-intermediate"
                display_level = "Intermediate"

            with cols[idx % 4]:
                st.markdown(f'''
                <div class="pro-skill-card">
                    <div class="skill-header-flex">
                        <span class="skill-name">{skill_name}</span>
                        <span class="level-badge {badge_class}">{display_level}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)


# ==========================================
# PROJECTS PAGE (ULTRA-PROFESSIONAL & ANIMATED)
# ==========================================
def render_projects():
    projects = get_projects() if 'get_projects' in globals() and callable(get_projects) else []
    
    if not projects:
        st.info("No projects available.")
        return

    # --------------------------------------
    # HIGH-END STYLES & ANIMATIONS
    # --------------------------------------
    st.markdown("""
    <style>
        /* Glassmorphic Project Card */
        .pro-project-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.88) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        /* Shimmer Animation Effect */
        .pro-project-card::before {
            content: '';
            position: absolute;
            top: 0; left: -150%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
            transform: skewX(-25deg);
            transition: all 0.75s ease;
        }

        .pro-project-card:hover {
            transform: translateY(-8px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45), 0 0 30px rgba(59, 130, 246, 0.25);
        }

        .pro-project-card:hover::before {
            left: 150%;
        }

        /* Typography & Badges */
        .project-header-title {
            color: #f8fafc;
            font-size: 1.45rem;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .category-badge {
            background: rgba(59, 130, 246, 0.12);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .star-featured-badge {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #ffffff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
            animation: pulseStar 2s infinite ease-in-out;
        }

        @keyframes pulseStar {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .tech-pill {
            background: rgba(30, 58, 138, 0.35);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.25);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-block;
            margin: 4px 4px 4px 0;
            transition: all 0.3s ease;
        }

        .tech-pill:hover {
            background: #2563eb;
            color: #ffffff;
            border-color: #3b82f6;
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4);
        }

        /* Custom Action Buttons */
        .btn-action-primary {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff !important;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
            width: 100%;
            text-align: center;
        }

        .btn-action-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 22px rgba(37, 99, 235, 0.5);
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }

        .btn-action-secondary {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 10px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #f8fafc !important;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
        }

        .btn-action-secondary:hover {
            background: rgba(51, 65, 85, 0.95);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-3px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # PAGE HEADER
    # --------------------------------------
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>🚀 Featured Projects</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 25px;'>A showcase of data analytics, machine learning, and software engineering solutions.</p>", unsafe_allow_html=True)

    # --------------------------------------
    # SEARCH & CATEGORY FILTER CONTROL PANEL
    # --------------------------------------
    col_search, col_cat = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("🔍 Search Projects", "", placeholder="Type keywords, techniques, or title...")
        
    with col_cat:
        categories = ["All Categories"] + sorted(list(set([p.get("category", "General") for p in projects])))
        selected_cat = st.selectbox("🎯 Category Filter", categories)
    
    filtered = projects
    if selected_cat != "All Categories":
        filtered = [p for p in filtered if p.get("category") == selected_cat]
    if search:
        filtered = [p for p in filtered if search.lower() in p.get("title", "").lower() or search.lower() in p.get("description", "").lower()]

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.warning("No projects match your search criteria.")
        return

    # --------------------------------------
    # RENDER PROJECT CARDS
    # --------------------------------------
    for proj in filtered:
        title = html.escape(str(proj.get('title', 'Project Title')))
        category = html.escape(str(proj.get('category', 'General')))
        description = html.escape(str(proj.get('description', '')))
        featured_html = '<span class="star-featured-badge">⭐ Featured</span>' if proj.get('featured') else ''
        
        tech_list = proj.get('technologies', '').split(',') if isinstance(proj.get('technologies'), str) else []
        tech_badges = "".join([f'<span class="tech-pill">{html.escape(t.strip())}</span>' for t in tech_list if t.strip()])
        
        st.markdown(f'''
        <div class="pro-project-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <div class="project-header-title">{title}</div>
                <div>{featured_html}</div>
            </div>
            <div style="margin-bottom: 14px;">
                <span class="category-badge">{category}</span>
            </div>
            <p style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.6; margin-bottom: 18px;">{description}</p>
            <div>
                <span style="color: #64748b; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; display: block; margin-bottom: 6px;">Technologies Used:</span>
                {tech_badges if tech_badges else '<span style="color:#64748b;">N/A</span>'}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Details Breakdown & Action Buttons
        with st.expander("📄 Detailed Breakdown & Repository Links"):
            st.markdown("<br>", unsafe_allow_html=True)
            if proj.get("overview"):
                st.markdown(f"**📌 Overview:**\n{proj['overview']}")
            if proj.get("problem"):
                st.markdown(f"**🎯 Problem Statement:**\n{proj['problem']}")
            if proj.get("dataset"):
                st.markdown(f"**📊 Dataset:**\n{proj['dataset']}")
            if proj.get("approach"):
                st.markdown(f"**⚙️ Methodology & Approach:**\n{proj['approach']}")
            if proj.get("results"):
                st.markdown(f"**📈 Key Results:**\n{proj['results']}")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            btn_col1, btn_col2, _ = st.columns([1, 1, 1.5])
            with btn_col1:
                if proj.get("github_url"):
                    st.markdown(f'<a href="{proj["github_url"]}" target="_blank" class="btn-action-secondary">💻 Source Code</a>', unsafe_allow_html=True)
            with btn_col2:
                if proj.get("demo_url"):
                    st.markdown(f'<a href="{proj["demo_url"]}" target="_blank" class="btn-action-primary">🚀 Live Demo</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SERVICES PAGE (ULTRA-PROFESSIONAL & ANIMATED)
# ==========================================
def render_services():
    services = get_services()
    
    active_services = [s for s in services if s.get("active", True)]
    
    if not active_services:
        st.info("No active services available at the moment.")
        return

    # --------------------------------------
    # EXECUTIVE CSS STYLING & ANIMATIONS
    # --------------------------------------
    st.markdown("""
    <style>
        /* Glassmorphic Service Card */
        .pro-service-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }

        .pro-service-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, #3b82f6, #60a5fa, transparent);
            opacity: 0.3;
            transition: opacity 0.4s ease;
        }

        .pro-service-card:hover {
            transform: translateY(-8px);
            border-color: rgba(59, 130, 246, 0.45);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 25px rgba(59, 130, 246, 0.2);
        }

        .pro-service-card:hover::before {
            opacity: 1;
        }

        /* Typography */
        .service-card-title {
            color: #f8fafc;
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.3px;
        }

        .service-card-desc {
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        /* Custom Visual List Items */
        .service-bullet-list {
            list-style: none;
            padding-left: 0;
            margin: 0 0 20px 0;
        }

        .service-bullet-list li {
            color: #cbd5e1;
            font-size: 0.9rem;
            padding: 8px 0;
            position: relative;
            padding-left: 26px;
            line-height: 1.4;
        }

        .service-bullet-list li::before {
            content: "⚡";
            position: absolute;
            left: 0;
            top: 7px;
            color: #60a5fa;
            font-size: 0.85rem;
        }

        /* Divider Line */
        .card-divider {
            border: 0;
            height: 1px;
            background: rgba(255, 255, 255, 0.06);
            margin: 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # PAGE HEADER
    # --------------------------------------
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>💼 Services & Solutions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 30px;'>Tailored technical services to transform raw data into intelligent, scalable business solutions.</p>", unsafe_allow_html=True)

    # --------------------------------------
    # RENDER SERVICES GRID (2-COLUMN)
    # --------------------------------------
    cols = st.columns(2, gap="large")
    
    for idx, srv in enumerate(active_services):
        items_html = "".join([f'<li>{item}</li>' for item in srv.get('items', [])])
        
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="pro-service-card">
                <div>
                    <div class="service-card-title">
                        <span>🛠️</span> {srv['title']}
                    </div>
                    <div class="service-card-desc">{srv['description']}</div>
                    <hr class="card-divider">
                    <ul class="service-bullet-list">
                        {items_html}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Inquiry Button
            if st.button(f"📩 Inquire About {srv['title']}", key=f"srv_btn_{idx}", use_container_width=True):
                st.session_state["selected_service"] = srv['title']
                st.session_state["nav"] = "Contact"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

#=====================================
#Experience
#====================================


def render_experience():
    # --------------------------------------
    # HIGH-END STYLES & ANIMATIONS
    # --------------------------------------
    st.markdown("""
    <style>
        /* Timeline Container */
        .timeline-wrapper {
            position: relative;
            padding-left: 32px;
            margin-bottom: 35px;
        }
        
        /* Vertical Glowing Line */
        .timeline-wrapper::before {
            content: '';
            position: absolute;
            left: 10px;
            top: 5px;
            bottom: 5px;
            width: 3px;
            background: linear-gradient(180deg, #3b82f6 0%, #60a5fa 50%, rgba(59, 130, 246, 0.1) 100%);
            border-radius: 4px;
        }

        /* Glassmorphic Timeline Card */
        .timeline-card {
            position: relative;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .timeline-card:hover {
            transform: translateX(8px);
            border-color: rgba(59, 130, 246, 0.45);
            box-shadow: 0 12px 35px rgba(59, 130, 246, 0.2);
        }

        /* Glowing Node Dot */
        .timeline-card::before {
            content: '';
            position: absolute;
            left: -30px;
            top: 28px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #2563eb;
            border: 3px solid #0f172a;
            box-shadow: 0 0 12px #3b82f6;
            transition: all 0.3s ease;
        }

        .timeline-card:hover::before {
            background: #60a5fa;
            box-shadow: 0 0 18px #60a5fa;
            transform: scale(1.25);
        }

        /* Typography & Badges */
        .exp-role-title {
            color: #f8fafc;
            font-size: 1.3rem;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .exp-org-name {
            color: #60a5fa;
            font-weight: 600;
        }

        .exp-badge-date {
            color: #94a3b8;
            font-size: 0.82rem;
            font-weight: 600;
            display: inline-block;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 3px 12px;
            border-radius: 20px;
            margin-top: 6px;
            margin-bottom: 14px;
        }

        .exp-description {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 12px;
            white-space: pre-line;
        }

        .skill-chip {
            background: rgba(30, 58, 138, 0.3);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.76rem;
            font-weight: 600;
            display: inline-block;
            margin-right: 6px;
            margin-top: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Clean text helper without breaking standard text
    def clean_text(val, default=''):
        if not val:
            return default
        return str(val).strip()

    # --------------------------------------
    # PAGE HEADER
    # --------------------------------------
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>💼 Experience & Career Path</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 30px;'>A summary of my professional background, key roles, and continuous learning achievements.</p>", unsafe_allow_html=True)

    # --------------------------------------
    # PROFESSIONAL EXPERIENCE SECTION
    # --------------------------------------
    st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 20px;'>🏢 Professional Experience</h3>", unsafe_allow_html=True)
    
    exps = get_experience() if 'get_experience' in globals() and callable(get_experience) else []
    
    if isinstance(exps, list) and len(exps) > 0:
        cards_html = ""
        for exp in exps:
            if not isinstance(exp, dict):
                continue

            raw_skills = exp.get('skills', '')
            skills_html = ""
            if raw_skills:
                if isinstance(raw_skills, str):
                    skills_list = [s.strip() for s in raw_skills.split(',') if s.strip()]
                elif isinstance(raw_skills, (list, tuple)):
                    skills_list = [str(s).strip() for s in raw_skills if str(s).strip()]
                else:
                    skills_list = []
                
                skills_html = "".join([f'<span class="skill-chip">{html.escape(s)}</span>' for s in skills_list])
            
            position = html.escape(clean_text(exp.get('position'), 'N/A'))
            organization = html.escape(clean_text(exp.get('organization'), 'N/A'))
            start_date = html.escape(clean_text(exp.get('start_date'), 'N/A'))
            end_date = html.escape(clean_text(exp.get('end_date'), 'Present'))
            description = html.escape(clean_text(exp.get('description'), ''))

            skills_div = f'<div style="margin-top: 10px;">{skills_html}</div>' if skills_html else ''

            cards_html += f'''<div class="timeline-card"><div class="exp-role-title">{position} &nbsp;•&nbsp; <span class="exp-org-name">{organization}</span></div><div class="exp-badge-date">🗓️ {2025} — {end_date}</div><p class="exp-description">{description}</p>{skills_div}</div>'''
        
        st.markdown(f'<div class="timeline-wrapper">{cards_html}</div>', unsafe_allow_html=True)
    else:
        st.info("No professional experience listed.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # LEARNING JOURNEY TIMELINE
    # --------------------------------------
    st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 20px;'>🎓 Learning Journey & Milestones</h3>", unsafe_allow_html=True)
    
    journey = get_learning_journey() if 'get_learning_journey' in globals() and callable(get_learning_journey) else []
    
    if isinstance(journey, list) and len(journey) > 0:
        journey_cards_html = ""
        for item in journey:
            if not isinstance(item, dict):
                continue

            title = html.escape(clean_text(item.get('title'), 'Milestone'))
            date_val = html.escape(clean_text(item.get('date'), ''))
            description = html.escape(clean_text(item.get('description'), ''))
            
            date_info = f"<div class='exp-badge-date'>📅 {date_val}</div>" if date_val else ""

            journey_cards_html += f'''<div class="timeline-card"><div class="exp-role-title">{title}</div>{date_info}<p class="exp-description">{description}</p></div>'''
        
        st.markdown(f'<div class="timeline-wrapper">{journey_cards_html}</div>', unsafe_allow_html=True)
    else:
        st.info("No learning journey timeline listed.")
        
# ==========================================
# CONTACT PAGE (ULTRA-PROFESSIONAL & INTERACTIVE)
# ==========================================

def render_contact():
    profile = get_profile()
    
    # Check if user arrived via Service Inquiry
    selected_service = st.session_state.get("selected_service", None)
    
    # --------------------------------------
    # EXECUTIVE CSS STYLING
    # --------------------------------------
    st.markdown("""
    <style>
        /* Glassmorphic Contact Card */
        .pro-contact-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .pro-contact-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, #3b82f6, #60a5fa, transparent);
            opacity: 0.3;
        }

        .pro-contact-card:hover {
            border-color: rgba(59, 130, 246, 0.45);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 0 0 20px rgba(59, 130, 246, 0.2);
        }

        .contact-card-title {
            color: #f8fafc;
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.3px;
        }

        /* Modern Action Buttons */
        .social-link-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.25);
            color: #60a5fa !important;
            padding: 12px 18px;
            border-radius: 12px;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 12px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .social-link-btn:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff !important;
            border-color: #3b82f6;
            transform: translateX(6px);
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }

        .info-row {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #cbd5e1;
            font-size: 0.95rem;
            margin-bottom: 14px;
        }

        .info-icon {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # PAGE HEADER
    # --------------------------------------
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>📬 Let's Connect</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 30px;'>Have a project in mind, a service inquiry, or just want to say hi? Feel free to reach out!</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    # --------------------------------------
    # LEFT COLUMN: DIRECT INFO & SOCIALS
    # --------------------------------------
    with col1:
        user_email = profile.get('email', '')
        
        st.markdown(f"""
        <div class="pro-contact-card">
            <div class="contact-card-title">📍 Contact Information</div>
            <div class="info-row">
                <div class="info-icon">🏢</div>
                <div>
                    <div style="color:#64748b; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Location</div>
                    <div style="color:#f8fafc; font-weight:600;">{profile.get('location', 'Chattogram, Bangladesh')}</div>
                </div>
            </div>
            <div class="info-row">
                <div class="info-icon">📧</div>
                <div>
                    <div style="color:#64748b; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Email Address</div>
                    <div style="color:#f8fafc; font-weight:600;">{user_email}</div>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <a href="mailto:{user_email}" class="social-link-btn" style="justify-content: center;">
                    ✉️ Launch Default Mail Client
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="pro-contact-card">', unsafe_allow_html=True)
        st.markdown('<div class="contact-card-title">🌐 Digital Presence</div>', unsafe_allow_html=True)
        
        socials = get_social_links()
        active_socials = [soc for soc in socials if soc.get("active", True)]
        
        if active_socials:
            for soc in active_socials:
                st.markdown(f"""
                <a href='{soc['url']}' target='_blank' class='social-link-btn'>
                    🔗 <span>{soc['label']}</span>
                </a>
                """, unsafe_allow_html=True)
        else:
            st.info("No social profiles currently linked.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------
    # RIGHT COLUMN: INTERACTIVE MESSAGE FORM
    # --------------------------------------
    with col2:
        st.markdown('<div class="pro-contact-card">', unsafe_allow_html=True)
        st.markdown('<div class="contact-card-title">💬 Send a Direct Message</div>', unsafe_allow_html=True)
        
        # Service options for selection dropdown
        services_list = ["General Inquiry"]
        try:
            available_services = [s['title'] for s in get_services() if s.get("active", True)]
            services_list.extend(available_services)
        except NameError:
            pass
            
        # Streamlit Contact Form
        with st.form("pro_contact_form", clear_on_submit=False):
            sender_name = st.text_input("Full Name *", placeholder="John Doe")
            sender_email = st.text_input("Email Address *", placeholder="john@example.com")
            
            # Auto-select service if coming from Services page
            default_idx = services_list.index(selected_service) if selected_service in services_list else 0
            subject_type = st.selectbox("Topic / Service Required", services_list, index=default_idx)
            
            message_body = st.text_area("Your Message *", placeholder="Describe your project, question, or proposal...", height=150)
            
            submit_btn = st.form_submit_button("📩 Send Message", use_container_width=True)
            
            if submit_btn:
                if not sender_name or not sender_email or not message_body:
                    st.error("⚠️ Please fill in all required fields before sending.")
                elif "@" not in sender_email or "." not in sender_email:
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    encoded_subject = urllib.parse.quote(f"Portfolio [{subject_type}]: Message from {sender_name}")
                    encoded_body = urllib.parse.quote(f"Name: {sender_name}\nEmail: {sender_email}\nService Topic: {subject_type}\n\nMessage:\n{message_body}")
                    
                    st.success("✅ Your message draft is ready to send!")
                    st.markdown(f"""
                    <div style="margin-top: 15px;">
                        <a href="mailto:{user_email}?subject={encoded_subject}&body={encoded_body}" target="_blank" class="social-link-btn" style="text-align:center; justify-content:center; background:linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color:white !important; border:none;">
                            🚀 Confirm & Send Email Now
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Clear selected service from state after use
                    if "selected_service" in st.session_state:
                        del st.session_state["selected_service"]
                    
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# REVIEWS / TESTIMONIALS SYSTEM (ENHANCED)
# ==========================================
def render_reviews():
    # ১. Supabase Client কল করা
    supabase = get_supabase_client()
    if not supabase:
        st.warning("⚠️ Database connection unavailable.")
        return

    # --------------------------------------
    # HIGH-END STYLES & GLASSMORPHISM CSS
    # --------------------------------------
    st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .review-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            animation: fadeInUp 0.4s ease-out;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .review-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, #3b82f6, #60a5fa, transparent);
            opacity: 0.3;
        }

        .review-card:hover {
            border-color: rgba(59, 130, 246, 0.45);
            transform: translateY(-4px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35), 0 0 20px rgba(59, 130, 246, 0.15);
        }

        .reviewer-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 14px;
        }

        .reviewer-avatar {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        }

        .reviewer-name {
            color: #f8fafc;
            font-weight: 700;
            font-size: 1.05rem;
            line-height: 1.2;
        }

        .reviewer-role {
            color: #60a5fa;
            font-size: 0.82rem;
            font-weight: 500;
        }

        .review-stars {
            color: #fbbf24;
            font-size: 1rem;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .review-comment {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
            font-style: italic;
        }

        .review-summary-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 14px 20px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
    </style>
    """, unsafe_allow_html=True)

    # PAGE TITLE
    st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;'>💬 Client Reviews & Testimonials</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1rem; margin-bottom: 30px;'>Feedback and recommendations from people I have collaborated with.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    # --------------------------------------
    # LEFT COLUMN: DISPLAY REVIEWS
    # --------------------------------------
    with col1:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 20px;'>⭐ What People Say</h3>", unsafe_allow_html=True)
        
        try:
            response = supabase.table("reviews").select("*").eq("is_approved", True).order("created_at", desc=True).execute()
            approved_reviews = response.data
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            approved_reviews = []

        if approved_reviews:
            # Summary Calculation
            total_reviews = len(approved_reviews)
            avg_rating = sum(r.get("rating", 5) for r in approved_reviews) / total_reviews
            
            st.markdown(f"""
            <div class="review-summary-box">
                <div>
                    <span style="color: #cbd5e1; font-size: 0.9rem;">Overall Rating:</span>
                    <span style="color: #fbbf24; font-weight: 700; font-size: 1.1rem; margin-left: 6px;">{avg_rating:.1f} / 5.0</span>
                </div>
                <div style="color: #94a3b8; font-size: 0.88rem;">
                    Total Testimonials: <strong style="color: #f8fafc;">{total_reviews}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for rev in approved_reviews:
                stars = "★" * rev.get("rating", 5) + "☆" * (5 - rev.get("rating", 5))
                initial = rev.get("name", "A")[0].upper() if rev.get("name") else "A"
                
                card_html = f"""
                <div class='review-card'>
                    <div class='review-stars'>{stars}</div>
                    <div class='review-comment'>'{rev.get('comment', '')}'</div>
                    <div class="reviewer-header">
                        <div class="reviewer-avatar">{initial}</div>
                        <div>
                            <div class="reviewer-name">{rev.get('name', 'Anonymous')}</div>
                            <div class="reviewer-role">{rev.get('role', 'Client')}</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("No approved reviews available yet. Be the first to share your feedback!")

    # --------------------------------------
    # RIGHT COLUMN: INPUT FORM
    # --------------------------------------
    with col2:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 20px;'>✍️ Share Your Feedback</h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="review-card" style="animation: none;">', unsafe_allow_html=True)
        with st.form("submit_review_form", clear_on_submit=True):
            name = st.text_input("Your Name *", placeholder="e.g. Abdullah")
            role = st.text_input("Designation / Company", placeholder="e.g. Software Engineer at TechCorp")
            rating = st.slider("Rating (Stars)", min_value=1, max_value=5, value=5)
            comment = st.text_area("Your Review / Feedback *", placeholder="Share your experience working together...", height=130)
            
            submit_btn = st.form_submit_button("🚀 Submit Review", use_container_width=True)
            
            if submit_btn:
                if not name.strip() or not comment.strip():
                    st.error("⚠️ Please fill in all required fields (Name and Review).")
                else:
                    try:
                        new_review = {
                            "name": name.strip(),
                            "role": role.strip() if role.strip() else "Client",
                            "rating": rating,
                            "comment": comment.strip(),
                            "is_approved": False
                        }
                        supabase.table("reviews").insert(new_review).execute()
                        st.success("✅ Thank you! Your review has been submitted for approval.")
                    except Exception as e:
                        st.error(f"Failed to submit review: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
# ==========================================
# ADMIN PAGE (ENHANCED & DYNAMIC CATEGORIES)
# ==========================================
def render_admin():
    st.title('🔒 Admin Control Panel')
    
    # --------------------------------------
    # CUSTOM CSS FOR GLASSMORPHISM ADMIN UI
    # --------------------------------------
    st.markdown("""
    <style>
        .admin-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }
        .admin-section-title {
            color: #60a5fa;
            font-size: 1.1em;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .cat-badge {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.85em;
            display: inline-block;
            margin-right: 6px;
            margin-bottom: 6px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if not check_admin_auth():
        with st.form("admin_login"):
            code = st.text_input("Enter Admin Passcode", type="password")
            submit = st.form_submit_button("🔑 Unlock Panel", use_container_width=True)
            if submit:
                login_admin(code)
                if check_admin_auth():
                    st.success("Authenticated successfully.")
                    st.rerun()
                else:
                    st.error("Invalid Admin Code. Access Denied.")
        return

    st.sidebar.button("🚪 Logout Admin", on_click=logout_admin)
    
    tabs = st.tabs(["👤 Profile", "🛠️ Skills & Categories", "🚀 Projects", "💼 Services", "🏢 Experience", "🎓 Learning", "🔗 Socials"])
    
    # --- Profile Tab ---
    with tabs[0]:
        st.subheader("Edit Profile Information")
        profile = get_profile()
        if profile:
            with st.form("edit_profile_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Name", profile.get("name", ""))
                    title = st.text_input("Title", profile.get("title", ""))
                    location = st.text_input("Location", profile.get("location", ""))
                with col2:
                    email = st.text_input("Email", profile.get("email", ""))
                    image_url = st.text_input("Profile Image URL", profile.get("profile_image", ""))
                    exp_years = st.number_input("Years of Experience", value=int(profile.get("experience_years", 1)))
                
                bio = st.text_area("Bio Description", profile.get("bio", ""), height=120)
                
                if st.form_submit_button("💾 Save Profile Changes", use_container_width=True):
                    if not is_valid_email(email):
                        st.error("Invalid email address format.")
                    elif not is_valid_url(image_url):
                        st.error("Invalid image URL format.")
                    else:
                        update_profile(profile["id"], {
                            "name": name, "title": title, "location": location,
                            "email": email, "profile_image": image_url,
                            "experience_years": exp_years, "bio": bio
                        })
                        st.success("Profile updated successfully!")
                        st.rerun()

    # --- Skills Tab (Dynamic Category System) ---
    with tabs[1]:
        skills = get_skills()
        
        # 1. Dynamically extract current existing categories from skills database
        existing_categories = sorted(list(set([s["category"] for s in skills if s.get("category")])))
        if "General" not in existing_categories:
            existing_categories.insert(0, "General")

        col_left, col_right = st.columns([3, 2], gap="large")
        
        # Left Side: Existing Skills List
        with col_left:
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">📊 Existing Skills</div>', unsafe_allow_html=True)
            if skills:
                for s in skills:
                    cols = st.columns([3, 2, 2, 1])
                    cols[0].write(f"**{s['name']}**")
                    cols[1].write(f"<span class='cat-badge'>{s['category']}</span>", unsafe_allow_html=True)
                    cols[2].write(f"_{s['level']}_")
                    if cols[3].button("🗑️", key=f"del_sk_{s['id']}"):
                        delete_skill(s["id"])
                        st.rerun()
            else:
                st.info("No skills added yet.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Right Side: Category Manager & Add Skill Form
        with col_right:
            # Manage Categories Box
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">🏷️ Manage Categories</div>', unsafe_allow_html=True)
            
            # Show existing categories with delete option
            st.write("**Current Categories:**")
            for cat in existing_categories:
                c_col1, c_col2 = st.columns([4, 1])
                c_col1.write(f"• {cat}")
                # Prevent deleting 'General' or categories currently assigned to active skills
                if cat != "General":
                    skills_in_cat = [s for s in skills if s.get("category") == cat]
                    if c_col2.button("❌", key=f"del_cat_{cat}"):
                        if skills_in_cat:
                            st.warning(f"Cannot delete '{cat}'. First delete or reassign skills under this category.")
                        else:
                            st.success(f"Category '{cat}' removed.")
                            st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Quick Add New Category Form
            with st.form("add_category_quick_form"):
                new_cat_input = st.text_input("➕ Add New Category Name", placeholder="e.g. Cloud & DevOps")
                if st.form_submit_button("Create Category"):
                    if new_cat_input.strip():
                        formatted_cat = new_cat_input.strip()
                        if formatted_cat not in existing_categories:
                            # Add a placeholder skill or simply refresh dropdown
                            add_skill({"name": "Sample Skill", "category": formatted_cat, "level": "Intermediate", "display_order": 99})
                            st.success(f"Category '{formatted_cat}' added successfully!")
                            st.rerun()
                        else:
                            st.error("Category already exists.")
                    else:
                        st.error("Category name cannot be empty.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Add New Skill Form with Dynamic Category Dropdown
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">✨ Add New Skill</div>', unsafe_allow_html=True)
            with st.form("add_skill_form"):
                sk_name = st.text_input("Skill Name", placeholder="e.g. Python, Docker")
                
                # Dynamic Category Selectbox
                sk_cat = st.selectbox("Choose Category", existing_categories)
                
                sk_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced"], index=1)
                sk_order = st.number_input("Display Order", value=1, min_value=1)
                
                if st.form_submit_button("⚡ Add Skill Now", use_container_width=True):
                    if sk_name.strip():
                        add_skill({"name": sk_name.strip(), "category": sk_cat, "level": sk_level, "display_order": sk_order})
                        st.success(f"Skill '{sk_name}' added to category '{sk_cat}'.")
                        st.rerun()
                    else:
                        st.error("Please enter a skill name.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Projects Tab ---
    with tabs[2]:
        st.subheader("Manage Projects")
        projects = get_projects()
        if projects:
            for p in projects:
                cols = st.columns([4, 2, 1])
                cols[0].write(f"**{p['title']}** ({p['category']})")
                cols[1].write(f"Order: {p.get('display_order', 1)}")
                if cols[2].button("🗑️", key=f"del_proj_{p['id']}"):
                    delete_project(p["id"])
                    st.rerun()
        else:
            st.info("No projects added yet.")
                
        st.markdown("---")
        st.markdown("### ➕ Add New Project")
        with st.form("add_proj_form"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_title = st.text_input("Project Title")
                p_cat = st.selectbox("Category", ["Data Analysis", "Machine Learning", "Deep Learning", "Web Scraping", "Full-Stack"])
                p_desc = st.text_area("Short Description")
                p_tech = st.text_input("Technologies (comma separated)")
                p_gh = st.text_input("GitHub URL")
                p_demo = st.text_input("Demo URL")
            
            with col_p2:
                p_feat = st.checkbox("Featured Project", value=False)
                p_order = st.number_input("Display Order", value=1)
                p_overview = st.text_area("Overview")
                p_problem = st.text_area("Problem Statement")
                p_dataset = st.text_area("Dataset Details")
                p_approach = st.text_area("Approach & Methodology")
                p_results = st.text_area("Results")
            
            if st.form_submit_button("🚀 Add Project", use_container_width=True):
                if p_gh and not is_valid_url(p_gh):
                    st.error("Invalid GitHub URL.")
                elif p_demo and not is_valid_url(p_demo):
                    st.error("Invalid Demo URL.")
                elif p_title and p_desc:
                    add_project({
                        "title": p_title, "category": p_cat, "description": p_desc,
                        "technologies": p_tech, "github_url": p_gh, "demo_url": p_demo,
                        "featured": p_feat, "display_order": p_order, "overview": p_overview,
                        "problem": p_problem, "dataset": p_dataset, "approach": p_approach,
                        "results": p_results
                    })
                    st.success("Project added successfully.")
                    st.rerun()

    # --- Services Tab ---
    with tabs[3]:
        st.subheader("Manage Services")
        services = get_services()
        for srv in services:
            cols = st.columns([4, 1])
            cols[0].write(f"**{srv['title']}**")
            if cols[1].button("🗑️", key=f"del_srv_{srv['id']}"):
                delete_service(srv["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_srv_form"):
            s_title = st.text_input("Service Title")
            s_desc = st.text_area("Service Description")
            s_items = st.text_area("Service Items (one per line)")
            s_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Service"):
                items_list = [i.strip() for i in s_items.split("\n") if i.strip()]
                add_service({"title": s_title, "description": s_desc, "items": items_list, "display_order": s_order, "active": True})
                st.success("Service added.")
                st.rerun()

    # --- Experience Tab ---
    with tabs[4]:
        st.subheader("Manage Experience")
        exps = get_experience()
        for e in exps:
            cols = st.columns([4, 1])
            cols[0].write(f"**{e['position']}** at {e['organization']}")
            if cols[1].button("🗑️", key=f"del_exp_{e['id']}"):
                delete_experience(e["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_exp_form"):
            e_pos = st.text_input("Position")
            e_org = st.text_input("Organization")
            e_start = st.text_input("Start Date")
            e_end = st.text_input("End Date")
            e_desc = st.text_area("Description")
            e_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Experience"):
                add_experience({"position": e_pos, "organization": e_org, "start_date": e_start, "end_date": e_end, "description": e_desc, "display_order": e_order})
                st.success("Experience added.")
                st.rerun()

    # --- Learning Journey Tab ---
    with tabs[5]:
        st.subheader("Manage Learning Journey")
        items = get_learning_journey()
        for item in items:
            cols = st.columns([4, 1])
            cols[0].write(f"**{item['title']}**")
            if cols[1].button("🗑️", key=f"del_learn_{item['id']}"):
                delete_learning_item(item["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_learn_form"):
            l_title = st.text_input("Title")
            l_desc = st.text_area("Description")
            l_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Learning Item"):
                add_learning_item({"title": l_title, "description": l_desc, "display_order": l_order})
                st.success("Learning item added.")
                st.rerun()

    # --- Social Links Tab ---
    with tabs[6]:
        st.subheader("Manage Social Links")
        socials = get_social_links()
        for soc in socials:
            cols = st.columns([3, 3, 1])
            cols[0].write(soc["platform"])
            cols[1].write(soc["url"])
            if cols[2].button("🗑️", key=f"del_soc_{soc['id']}"):
                delete_social_link(soc["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_soc_form"):
            sc_plat = st.text_input("Platform")
            sc_lbl = st.text_input("Label")
            sc_url = st.text_input("URL")
            sc_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Social Link"):
                add_social_link({"platform": sc_plat, "label": sc_lbl, "url": sc_url, "display_order": sc_order, "active": True})
                st.success("Social link added.")
                st.rerun()
                
# ==========================================
# MAIN APP (UPDATED & COMPLETE NAVIGATION)
# ==========================================

def main():
    pages = {
        "Home": render_home,
        "Skills": render_skills,
        "Projects": render_projects,
        "Services": render_services,
        "Experience": render_experience,
        "Contact": render_contact,
        "Reviews":render_reviews,
        "Admin": render_admin
    }

    # 2. Navigation State Initialization & Validation
    if "nav" not in st.session_state or st.session_state["nav"] not in pages:
        st.session_state["nav"] = "Home"

    # 3. Safe Index Calculation
    page_keys = list(pages.keys())
    current_index = page_keys.index(st.session_state["nav"])

    # 4. Sidebar Radio
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to", 
        page_keys, 
        index=current_index
    )
