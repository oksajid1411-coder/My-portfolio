# ==========================================
# IMPORTS
# ==========================================
import re
import streamlit as st
from supabase import create_client, Client

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="MD. Omar Kamran Chy | Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    '<meta name="google-site-verification" content="pGuh741_Y7EMkFFGYXcLStLdjI02nsOlbVrxw6eWcYU" />',
    unsafe_allow_html=True
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
    try:
        res = supabase.table("profiles").select("*").limit(1).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return None
    except Exception as e:
        st.error(f"Error fetching profile: {e}")
        return None

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
# HOME PAGE
# ==========================================
def render_home():
    profile = get_profile()
    
    # Ultra-Modern Dark Theme CSS with Advanced Animations & Visual Effects
    st.markdown("""
        <style>
        /* Modern CSS Keyframes */
        @keyframes subtleGlow {
            0% { box-shadow: 0 0 15px rgba(255, 75, 75, 0.15); }
            50% { box-shadow: 0 0 30px rgba(108, 92, 231, 0.3); }
            100% { box-shadow: 0 0 15px rgba(255, 75, 75, 0.15); }
        }

        @keyframes flowPulse {
            0% { transform: scale(1); filter: drop-shadow(0 0 2px #3B82F6); }
            50% { transform: scale(1.15) translateX(3px); filter: drop-shadow(0 0 8px #60A5FA); }
            100% { transform: scale(1); filter: drop-shadow(0 0 2px #3B82F6); }
        }

        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Hero Glass Container */
        .glass-hero-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 24px;
            padding: 35px;
            margin-bottom: 30px;
            animation: subtleGlow 8s infinite alternate ease-in-out;
        }

        /* Animated Title Gradient */
        .pro-hero-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        /* Premium Workflow Box */
        .workflow-wrapper {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px 20px;
            margin: 30px 0;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
        }

        .workflow-title {
            text-align: center;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #94A3B8;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .flow-flex {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        /* Glassmorphism Process Step Chips */
        .flow-chip {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 10px 18px;
            color: #F8FAFC;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
        }

        .flow-chip:hover {
            transform: translateY(-6px) scale(1.05);
            border-color: #3B82F6;
            background: linear-gradient(145deg, rgba(59, 130, 246, 0.2), rgba(30, 41, 59, 0.9));
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.35);
            color: #FFFFFF;
        }

        .flow-chip-final {
            border-color: rgba(46, 204, 113, 0.5) !important;
        }
        .flow-chip-final:hover {
            border-color: #2ECC71 !important;
            background: linear-gradient(145deg, rgba(46, 204, 113, 0.25), rgba(30, 41, 59, 0.9)) !important;
            box-shadow: 0 10px 25px rgba(46, 204, 113, 0.35) !important;
        }

        .flow-arrow-icon {
            color: #3B82F6;
            font-size: 1.2rem;
            animation: flowPulse 2s infinite ease-in-out;
        }

        /* Metric Interactive Cards */
        .pro-stat-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 22px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .pro-stat-card:hover {
            transform: translateY(-8px);
            border-color: rgba(255, 75, 75, 0.6);
            box-shadow: 0 12px 30px rgba(255, 75, 75, 0.2);
        }

        .pro-stat-title {
            font-size: 0.8rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 600;
        }

        .pro-stat-val {
            font-size: 2rem;
            font-weight: 800;
            color: #FFFFFF;
            margin: 8px 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }

        .pro-stat-badge {
            display: inline-block;
            background: rgba(46, 204, 113, 0.12);
            border: 1px solid rgba(46, 204, 113, 0.3);
            color: #2ECC71;
            padding: 4px 14px;
            border-radius: 30px;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        </style>
    """, unsafe_allow_html=True)

    if not profile:
        st.warning("No profile data found. Please add profile info from the Admin panel.")
        return

    # 1. HERO SECTION
    st.markdown('<div class="glass-hero-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 2], gap="large")
    
    with col1:
        img_url = profile.get("profile_image", "")
        if img_url:
            st.image(img_url, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300", caption="No Image Available", use_container_width=True)
            
    with col2:
        name = profile.get("name", "MD. Omar Kamran Chy")
        title = profile.get("title", "Data Scientist & Developer")
        
        st.markdown(f'<h1 class="pro-hero-title">{name}</h1>', unsafe_allow_html=True)
        st.subheader(title)
        
        location = profile.get("location", "")
        if location:
            st.markdown(f"📍 **{location}**")
            
        bio = profile.get("bio", "")
        if bio:
            st.write(bio)
            
        st.write("") 

        # Interactive Call To Action Buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("🚀 View Projects", use_container_width=True):
                st.session_state["nav_selection"] = "Projects"
                st.rerun()
        with btn_col2:
            if st.button("📩 Contact Me", use_container_width=True):
                st.session_state["nav_selection"] = "Contact"
                st.rerun()
        with btn_col3:
            resume_url = profile.get("resume_url", "")
            if resume_url:
                st.link_button("📄 Resume", resume_url, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 2. ULTRA-ANIMATED WORKFLOW FLOWCHART
    st.markdown("""
        <div class="workflow-wrapper">
            <div class="workflow-title">⚡ End-to-End Analytical Workflow</div>
            <div class="flow-flex">
                <div class="flow-chip">📊 Data Collection</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip">🧹 Data Cleaning</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip">🔍 Exploratory EDA</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip">⚙️ Feature Engineering</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip">🤖 ML/DL Modeling</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip">📈 Model Evaluation</div>
                <div class="flow-arrow-icon">➔</div>
                <div class="flow-chip flow-chip-final">💡 Insights & Solution</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # 3. INTERACTIVE METRIC STATS SECTION
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="pro-stat-card">
                <div class="pro-stat-title">Experience</div>
                <div class="pro-stat-val">1+ Years</div>
                <div class="pro-stat-badge">↑ Active Learner</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="pro-stat-card">
                <div class="pro-stat-title">Completed Projects</div>
                <div class="pro-stat-val">10+</div>
                <div class="pro-stat-badge">↑ Data & ML</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="pro-stat-card">
                <div class="pro-stat-title">Core Expertise</div>
                <div class="pro-stat-val">Data Analysis</div>
                <div class="pro-stat-badge">↑ Python | Pandas | Power BI</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Center-aligned 4th Metric Card
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown("""
            <div class="pro-stat-card">
                <div class="pro-stat-title">Other Expertise</div>
                <div class="pro-stat-val">ML & DL</div>
                <div class="pro-stat-badge">↑ Tensorflow | PyTorch | SKLearn</div>
            </div>
        """, unsafe_allow_html=True)
        
#===========================================
# ABOUT PAGE
# ==========================================
# def render_about():
#     profile = get_profile()
    
#     # Custom CSS for About Page Styling & Flowchart
#     st.markdown("""
#         <style>
#         .about-glass-card {
#             background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
#             backdrop-filter: blur(10px);
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             border-radius: 18px;
#             padding: 28px;
#             margin-bottom: 25px;
#         }
#         .animated-hero-title {
#             font-size: 2.6rem;
#             font-weight: 800;
#             background: linear-gradient(-45deg, #FF4B4B, #FF8F8F, #6C5CE7, #00CEC9);
#             background-size: 300% 300%;
#             animation: gradientBG 6s ease infinite;
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#         }
#         @keyframes gradientBG {
#             0% { background-position: 0% 50%; }
#             50% { background-position: 100% 50%; }
#             100% { background-position: 0% 50%; }
#         }
#         .flow-container {
#             display: flex;
#             flex-wrap: wrap;
#             align-items: center;
#             justify-content: center;
#             gap: 10px;
#             padding-top: 15px;
#         }
#         .flow-card {
#             background: rgba(30, 41, 59, 0.7);
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             border-radius: 10px;
#             padding: 8px 14px;
#             color: #F8FAFC;
#             font-weight: 600;
#             font-size: 0.82rem;
#             transition: all 0.3s ease;
#         }
#         .flow-card:hover {
#             transform: translateY(-3px);
#             border-color: #3B82F6;
#             background: rgba(59, 130, 246, 0.15);
#             box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
#         }
#         .flow-arrow {
#             color: #3B82F6;
#             font-size: 1.1rem;
#             font-weight: bold;
#             animation: pulse 1.8s infinite ease-in-out;
#         }
#         @keyframes pulse {
#             0% { transform: translateX(0); opacity: 0.5; }
#             50% { transform: translateX(3px); opacity: 1; }
#             100% { transform: translateX(0); opacity: 0.5; }
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     if not profile:
#         st.warning("No profile data found.")
#         return

#     # MAIN ABOUT CARD CONTAINER
#     st.markdown('<div class="about-glass-card">', unsafe_allow_html=True)
    
#     # 1. Profile Info & Image Grid
#     col1, col2 = st.columns([1.2, 2], gap="large")
    
#     with col1:
#         img_url = profile.get("profile_image", "")
#         if img_url:
#             st.image(img_url, use_container_width=True)
#         else:
#             st.image("https://via.placeholder.com/300", caption="No Image Available", use_container_width=True)
            
#     with col2:
#         name = profile.get("name", "MD. Omar Kamran Chy")
#         title = profile.get("title", "Data Scientist & Developer")
        
#         st.markdown(f'<h1 class="animated-hero-title">{name}</h1>', unsafe_allow_html=True)
#         st.subheader(title)
        
#         location = profile.get("location", "")
#         if location:
#             st.markdown(f"📍 **{location}**")
            
#         bio = profile.get("bio", "")
#         if bio:
#             st.write(bio)
            
#         st.write("") 

#         # Action Buttons
#         btn_col1, btn_col2, btn_col3 = st.columns(3)
#         with btn_col1:
#             if st.button("🚀 View Projects", use_container_width=True):
#                 st.session_state["nav_selection"] = "Projects"
#                 st.rerun()
#         with btn_col2:
#             if st.button("📩 Contact Me", use_container_width=True):
#                 st.session_state["nav_selection"] = "Contact"
#                 st.rerun()
#         with btn_col3:
#             resume_url = profile.get("resume_url", "")
#             if resume_url:
#                 st.link_button("📄 Resume", resume_url, use_container_width=True)

#     # 2. Analytical & Modeling Approach (About-এর নিচের অংশ)
#     st.write("---")
#     st.markdown("#### 🧠 My Analytical & Modeling Approach")

#     st.markdown("""
#         <div class="flow-container">
#             <div class="flow-card">📊 Data Collection</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card">🧹 Data Cleaning</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card">🔍 Exploratory EDA</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card">⚙️ Feature Engineering</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card">🤖 ML/DL Modeling</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card">📈 Model Evaluation</div>
#             <div class="flow-arrow">➔</div>
#             <div class="flow-card" style="border-color: #2ECC71;">💡 Insights & Solution</div>
#         </div>
#     """, unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)
# ==========================================
# SKILLS PAGE
# ==========================================
def render_skills():
    skills = get_skills()
    
    # Ultra-Modern CSS for Skills Grid & Glowing Badges
    st.markdown("""
        <style>
        /* Animated Title Shimmer */
        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .skills-header-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .skills-sub-title {
            text-align: center;
            color: #94A3B8;
            font-size: 1rem;
            margin-bottom: 30px;
        }

        /* Category Section Headers */
        .cat-heading {
            color: #F8FAFC;
            font-size: 1.3rem;
            font-weight: 700;
            margin: 25px 0 15px 0;
            padding-bottom: 6px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Glassmorphism Skill Card */
        .skill-glass-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 18px 12px;
            text-align: center;
            margin-bottom: 15px;
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .skill-glass-card:hover {
            transform: translateY(-6px) scale(1.02);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        }

        .skill-name {
            color: #F8FAFC;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 8px;
        }

        /* Proficiency Pills */
        .level-pill {
            display: inline-block;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .level-advanced {
            background: rgba(46, 204, 113, 0.15);
            border: 1px solid rgba(46, 204, 113, 0.4);
            color: #2ECC71;
        }

        .level-intermediate {
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #60A5FA;
        }

        .level-beginner {
            background: rgba(241, 196, 15, 0.15);
            border: 1px solid rgba(241, 196, 15, 0.4);
            color: #F1C40F;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown('<h1 class="skills-header-title">Technical Expertise</h1>', unsafe_allow_html=True)
    st.markdown('<p class="skills-sub-title">Core competencies, tools, and technologies I work with.</p>', unsafe_allow_html=True)

    if not skills:
        st.info("No skills currently listed.")
        return

    # Filter System
    categories = sorted(list(set([s.get("category", "General") for s in skills if s.get("category")])))
    selected_cat = st.selectbox("🎯 Category Filter", ["All"] + categories)
    
    filtered_skills = skills if selected_cat == "All" else [s for s in skills if s.get("category") == selected_cat]

    if not filtered_skills:
        st.warning("No skills found under this category.")
        return

    # Unique Categories among Filtered Skills
    active_cats = sorted(list(set([s.get("category", "General") for s in filtered_skills])))

    for cat in active_cats:
        st.markdown(f'<div class="cat-heading">📌 {cat}</div>', unsafe_allow_html=True)
        
        # Display skills in a 4-column layout
        cat_skills = sorted(
            [s for s in filtered_skills if s.get("category") == cat],
            key=lambda x: x.get("display_order", 1)
        )
        
        cols = st.columns(4, gap="medium")
        for idx, skill in enumerate(cat_skills):
            col = cols[idx % 4]
            
            # Dynamic Class for Proficiency Levels
            lvl = skill.get('level', 'Intermediate')
            lvl_class = "level-intermediate"
            if lvl.lower() == "advanced":
                lvl_class = "level-advanced"
            elif lvl.lower() == "beginner":
                lvl_class = "level-beginner"

            with col:
                st.markdown(f"""
                    <div class="skill-glass-card">
                        <div class="skill-name">{skill['name']}</div>
                        <span class="level-pill {lvl_class}">⭐ {lvl}</span>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# PROJECTS PAGE
# ==========================================
def render_projects():
    # Ultra-Modern CSS for Projects Page UI
    st.markdown("""
        <style>
        /* Shimmer Title Animation */
        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .proj-header-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .proj-sub-title {
            text-align: center;
            color: #94A3B8;
            font-size: 1rem;
            margin-bottom: 30px;
        }

        /* Project Glass Card */
        .proj-glass-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }

        .proj-glass-card:hover {
            transform: translateY(-6px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 12px 30px rgba(59, 130, 246, 0.25);
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        }

        .proj-title {
            color: #F8FAFC;
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .proj-category-badge {
            display: inline-block;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #60A5FA;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .proj-desc {
            color: #CBD5E1;
            font-size: 0.92rem;
            line-height: 1.6;
            margin-bottom: 16px;
        }

        /* Tech Badges Container */
        .tech-pill-wrapper {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 15px;
        }

        .tech-pill {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94A3B8;
            font-size: 0.78rem;
            padding: 2px 10px;
            border-radius: 12px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Title
    st.markdown('<h1 class="proj-header-title">Featured Projects</h1>', unsafe_allow_html=True)
    st.markdown('<p class="proj-sub-title">Explore my latest work across Data Science, Machine Learning, and Web Development.</p>', unsafe_allow_html=True)

    projects = get_projects()
    if not projects:
        st.info("No projects available right now.")
        return

    # Filter Controls UI Section
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search = st.text_input("🔍 Search Projects", "", placeholder="Search by title or keyword...")
    with f_col2:
        categories = ["All"] + sorted(list(set([p.get("category", "General") for p in projects])))
        selected_cat = st.selectbox("Category Filter", categories)

    # Filtering Logic
    filtered = projects
    if selected_cat != "All":
        filtered = [p for p in filtered if p.get("category") == selected_cat]
    if search:
        search_lower = search.lower()
        filtered = [
            p for p in filtered 
            if search_lower in p.get("title", "").lower() 
            or search_lower in p.get("description", "").lower()
            or search_lower in str(p.get("technologies", "")).lower()
        ]

    st.write("")

    if not filtered:
        st.warning("No projects matched your search criteria.")
        return

    # Grid Display Layout (2 Columns)
    cols = st.columns(2, gap="large")

    for idx, proj in enumerate(filtered):
        col = cols[idx % 2]
        
        # Prepare Tech Badges HTML
        raw_techs = proj.get('technologies', '')
        if isinstance(raw_techs, str):
            tech_list = [t.strip() for t in raw_techs.split(',') if t.strip()]
        else:
            tech_list = raw_techs
            
        tech_html = "".join([f'<span class="tech-pill">{t}</span>' for t in tech_list])

        featured_star = '⭐' if proj.get('featured') else ''
        category_name = proj.get('category', 'Project')

        with col:
            st.markdown(f"""
                <div class="proj-glass-card">
                    <div>
                        <div class="proj-title">
                            <span>{proj['title']}</span>
                            <span>{featured_star}</span>
                        </div>
                        <span class="proj-category-badge">{category_name}</span>
                        <div class="proj-desc">{proj.get('description', '')}</div>
                    </div>
                    <div>
                        <div class="tech-pill-wrapper">
                            {tech_html}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Details & Links Accordion
            with st.expander("📄 View Details & Links"):
                if proj.get("overview"):
                    st.write(f"**Overview:** {proj['overview']}")
                if proj.get("problem"):
                    st.write(f"**Problem:** {proj['problem']}")
                if proj.get("dataset"):
                    st.write(f"**Dataset:** {proj['dataset']}")
                if proj.get("approach"):
                    st.write(f"**Approach:** {proj['approach']}")
                if proj.get("results"):
                    st.write(f"**Results:** {proj['results']}")
                
                st.write("")
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if proj.get("github_url"):
                        st.link_button("🔗 GitHub Repo", proj['github_url'], use_container_width=True)
                with btn_c2:
                    if proj.get("demo_url"):
                        st.link_button("🚀 Live Demo", proj['demo_url'], use_container_width=True)

            st.write("") # Margin spacing between rows
# ==========================================
# SERVICES PAGE
# ==========================================
def render_services():
    services = get_services()
    active_services = [s for s in services if s.get("active", True)]

    # Ultra-Modern CSS for Services Cards & Grid
    st.markdown("""
        <style>
        /* Shimmer Title Animation */
        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .services-header-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .services-sub-title {
            text-align: center;
            color: #94A3B8;
            font-size: 1rem;
            margin-bottom: 35px;
        }

        /* Glassmorphism Card Container */
        .service-glass-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 25px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }

        .service-glass-card:hover {
            transform: translateY(-8px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 15px 35px rgba(59, 130, 246, 0.25);
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        }

        .service-title {
            color: #F8FAFC;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .service-desc {
            color: #CBD5E1;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 18px;
        }

        /* List Items Styling */
        .service-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .service-list-item {
            color: #94A3B8;
            font-size: 0.9rem;
            padding: 6px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            transition: color 0.3s ease;
        }

        .service-glass-card:hover .service-list-item {
            color: #E2E8F0;
        }

        .service-badge {
            color: #3B82F6;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Title
    st.markdown('<h1 class="services-header-title">My Services</h1>', unsafe_allow_html=True)
    st.markdown('<p class="services-sub-title">High-impact solutions tailored to solve complex data and software challenges.</p>', unsafe_allow_html=True)

    if not active_services:
        st.info("No active services available right now.")
        return

    # Responsive 2-Column Grid System
    cols = st.columns(2, gap="large")

    for idx, srv in enumerate(active_services):
        col = cols[idx % 2]
        
        items_html = ""
        for item in srv.get('items', []):
            items_html += f'<li class="service-list-item"><span class="service-badge">✓</span> {item}</li>'

        icon = srv.get('icon', '⚡') # Optional icon support

        with col:
            st.markdown(f"""
                <div class="service-glass-card">
                    <div>
                        <div class="service-title"><span>{icon}</span> {srv['title']}</div>
                        <div class="service-desc">{srv['description']}</div>
                    </div>
                    <div>
                        <ul class="service-list">
                            {items_html}
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# EXPERIENCE PAGE
# ==========================================
def render_experience():
    # Ultra-Modern CSS for Vertical Timeline & Dynamic Hover Effects
    st.markdown("""
        <style>
        /* Shimmer Title Animation */
        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .exp-header-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .exp-sub-title {
            text-align: center;
            color: #94A3B8;
            font-size: 1rem;
            margin-bottom: 35px;
        }

        /* Timeline Main Wrapper */
        .timeline-container {
            position: relative;
            padding-left: 30px;
            margin: 20px 0 40px 10px;
            border-left: 2px solid rgba(59, 130, 246, 0.3);
        }

        /* Timeline Card Item */
        .timeline-card {
            position: relative;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 25px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        .timeline-card:hover {
            transform: translateX(8px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.25);
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        }

        /* Glowing Timeline Dot Node */
        .timeline-card::before {
            content: '';
            position: absolute;
            left: -39px;
            top: 24px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #3B82F6;
            border: 3px solid #0F172A;
            box-shadow: 0 0 10px #3B82F6;
            transition: all 0.3s ease;
        }

        .timeline-card:hover::before {
            background: #FF4B4B;
            box-shadow: 0 0 15px #FF4B4B;
            transform: scale(1.3);
        }

        .exp-role {
            color: #F8FAFC;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .exp-org {
            color: #3B82F6;
            font-weight: 600;
        }

        .exp-date-badge {
            display: inline-block;
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #60A5FA;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 12px;
            border-radius: 20px;
            margin: 8px 0 14px 0;
        }

        .exp-desc {
            color: #CBD5E1;
            font-size: 0.92rem;
            line-height: 1.6;
            margin: 0;
        }

        .section-tag {
            color: #F8FAFC;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 30px 0 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header Title
    st.markdown('<h1 class="exp-header-title">Experience & Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="exp-sub-title">A timeline of my professional roles, milestones, and continuous learning path.</p>', unsafe_allow_html=True)

    # 1. PROFESSIONAL EXPERIENCE SECTION
    st.markdown('<div class="section-tag">💼 Professional Experience</div>', unsafe_allow_html=True)
    exps = get_experience()
    
    if exps:
        exp_html = '<div class="timeline-container">'
        for exp in exps:
            position = exp.get('position', 'Role')
            organization = exp.get('organization', 'Company')
            start_date = exp.get('start_date', '')
            end_date = exp.get('end_date', 'Present')
            description = exp.get('description', '')

            exp_html += f"""
                <div class="timeline-card">
                    <div class="exp-role">{position} <span class="exp-org">@ {organization}</span></div>
                    <div class="exp-date-badge">🗓️ {start_date} - {end_date}</div>
                    <p class="exp-desc">{description}</p>
                </div>
            """
        exp_html += '</div>'
        st.markdown(exp_html, unsafe_allow_html=True)
    else:
        st.info("No professional experience listed yet.")

    st.write("---")

    # 2. LEARNING JOURNEY TIMELINE SECTION
    st.markdown('<div class="section-tag">🚀 Learning Journey Timeline</div>', unsafe_allow_html=True)
    journey = get_learning_journey()
    
    if journey:
        journey_html = '<div class="timeline-container">'
        for item in journey:
            title = item.get('title', 'Milestone')
            description = item.get('description', '')

            journey_html += f"""
                <div class="timeline-card">
                    <div class="exp-role">🎓 {title}</div>
                    <p class="exp-desc" style="margin-top: 10px;">{description}</p>
                </div>
            """
        journey_html += '</div>'
        st.markdown(journey_html, unsafe_allow_html=True)
    else:
        st.info("No learning journey milestones listed yet.")
# ==========================================
# CONTACT PAGE
# ==========================================
def render_contact():
    profile = get_profile()
    
    # Ultra-Modern Dark Glass & Hover Animations CSS
    st.markdown("""
        <style>
        /* Card Animations & Shimmer */
        @keyframes subtleGlow {
            0% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.15); }
            50% { box-shadow: 0 0 30px rgba(108, 92, 231, 0.3); }
            100% { box-shadow: 0 0 15px rgba(59, 130, 246, 0.15); }
        }

        @keyframes titleShimmer {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphism Cards */
        .contact-glass-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            height: 100%;
            transition: all 0.4s ease-in-out;
        }

        .contact-glass-card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
            transform: translateY(-4px);
        }

        /* Animated Section Header */
        .contact-header-title {
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #FF4B4B, #FF8E53, #6C5CE7, #00CEC9);
            background-size: 300% 300%;
            animation: titleShimmer 6s infinite linear;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .contact-sub-title {
            text-align: center;
            color: #94A3B8;
            font-size: 1rem;
            margin-bottom: 35px;
        }

        .card-header-text {
            color: #F8FAFC;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 20px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
        }

        /* Contact Items */
        .info-item {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            transition: all 0.3s ease;
        }

        .info-item:hover {
            background: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.3);
            transform: translateX(6px);
        }

        .info-icon {
            font-size: 1.5rem;
        }

        .info-label {
            font-size: 0.8rem;
            color: #94A3B8;
            text-transform: uppercase;
            font-weight: 600;
        }

        .info-val {
            font-size: 1rem;
            color: #F8FAFC;
            font-weight: 600;
        }

        /* Social Link Buttons */
        .social-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 12px;
            margin-top: 15px;
        }

        .social-chip {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            color: #F8FAFC !important;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none !important;
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .social-chip:hover {
            transform: translateY(-5px) scale(1.03);
            background: linear-gradient(135deg, rgba(255, 75, 75, 0.2), rgba(108, 92, 231, 0.3));
            border-color: #FF4B4B;
            box-shadow: 0 8px 20px rgba(255, 75, 75, 0.25);
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Title
    st.markdown('<h1 class="contact-header-title">Get In Touch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="contact-sub-title">Have a project in mind or want to collaborate? Feel free to reach out!</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # LEFT COLUMN: Contact Details & Mail Link
    with col1:
        st.markdown("""
            <div class="contact-glass-card">
                <div class="card-header-text">📍 Contact Information</div>
        """, unsafe_allow_html=True)
        
        email_val = profile.get('email', 'N/A')
        loc_val = profile.get('location', 'N/A')

        st.markdown(f"""
            <div class="info-item">
                <div class="info-icon">📍</div>
                <div>
                    <div class="info-label">Location</div>
                    <div class="info-val">{loc_val}</div>
                </div>
            </div>
            
            <div class="info-item">
                <div class="info-icon">📧</div>
                <div>
                    <div class="info-label">Email Address</div>
                    <div class="info-val">{email_val}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        if email_val != 'N/A':
            st.link_button("📩 Send Direct Email", f"mailto:{email_val}", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT COLUMN: Interactive Social Profiles
    with col2:
        st.markdown("""
            <div class="contact-glass-card">
                <div class="card-header-text">🌐 Connect With Me</div>
        """, unsafe_allow_html=True)
        
        socials = get_social_links()
        active_socials = [s for s in socials if s.get("active", True)]

        if active_socials:
            social_html = '<div class="social-grid">'
            for soc in active_socials:
                label = soc.get('label', 'Link')
                url = soc.get('url', '#')
                social_html += f'<a href="{url}" target="_blank" class="social-chip">🔗 {label}</a>'
            social_html += '</div>'
            st.markdown(social_html, unsafe_allow_html=True)
        else:
            st.info("No social links available right now.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # OPTIONAL SECTION: Interactive Quick Message Form
    st.markdown("### 💬 Send Me a Quick Message")
    with st.form("contact_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            user_name = st.text_input("Your Name", placeholder="John Doe")
        with col_form2:
            user_email = st.text_input("Your Email", placeholder="john@example.com")
            
        user_message = st.text_area("Your Message", placeholder="Type your message here...")
        
        submit_btn = st.form_submit_button("🚀 Send Message", use_container_width=True)
        
        if submit_btn:
            if user_name and user_email and user_message:
                st.success(f"Thank you, {user_name}! Your message has been sent successfully.")
            else:
                st.error("Please fill in all the fields before submitting.")
                
# ==========================================
# PROFESSIONAL ADMIN PAGE
# ==========================================

def render_admin():

    # ==========================================
    # ADMIN UI CSS
    # ==========================================

    st.markdown("""
    <style>

    /* ---------- Global Admin Animation ---------- */

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes glow {
        0% {
            box-shadow: 0 0 0 rgba(108, 92, 231, 0);
        }
        50% {
            box-shadow: 0 0 22px rgba(108, 92, 231, 0.18);
        }
        100% {
            box-shadow: 0 0 0 rgba(108, 92, 231, 0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .admin-wrapper {
        animation: fadeIn 0.7s ease-out;
    }

    /* ---------- Main Header ---------- */

    .admin-header {
        padding: 25px 28px;
        border-radius: 18px;
        margin-bottom: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(108, 92, 231, 0.15),
                rgba(0, 206, 201, 0.08)
            );

        border: 1px solid rgba(255,255,255,0.08);

        animation: glow 4s ease-in-out infinite;
    }

    .admin-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .admin-subtitle {
        color: rgba(255,255,255,0.65);
        font-size: 0.95rem;
    }

    /* ---------- Section Cards ---------- */

    .admin-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;

        animation: fadeIn 0.55s ease-out;
    }

    .admin-card:hover {
        transform: translateY(-3px);
        border-color: rgba(108, 92, 231, 0.45);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    /* ---------- Skill Card ---------- */

    .skill-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 13px 17px;
        margin-bottom: 8px;

        transition: all 0.25s ease;
        animation: slideIn 0.4s ease-out;
    }

    .skill-card:hover {
        transform: translateX(5px);
        border-color: rgba(0,206,201,0.45);
    }

    /* ---------- Badges ---------- */

    .level-badge {
        display: inline-block;

        background: rgba(108,92,231,0.15);
        color: #A29BFE;

        border: 1px solid rgba(108,92,231,0.35);

        padding: 4px 10px;
        border-radius: 20px;

        font-size: 0.75rem;
        font-weight: 600;
    }

    .cat-badge {
        display: inline-block;

        background: rgba(0,206,201,0.12);
        color: #00CEC9;

        border: 1px solid rgba(0,206,201,0.25);

        padding: 4px 10px;
        border-radius: 20px;

        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ---------- Login Box ---------- */

    .login-box {
        max-width: 500px;
        margin: 70px auto;

        padding: 35px;

        border-radius: 20px;

        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);

        text-align: center;

        animation: fadeIn 0.8s ease-out;
    }

    .login-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }

    /* ---------- Buttons ---------- */

    div.stButton > button {
        border-radius: 10px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
    }

    /* ---------- Tabs ---------- */

    button[data-baseweb="tab"] {
        transition: all 0.2s ease;
    }

    button[data-baseweb="tab"]:hover {
        transform: translateY(-1px);
    }

    /* ---------- Divider ---------- */

    .admin-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 22px 0;
    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # LOGIN
    # ==========================================

    if not check_admin_auth():

        st.markdown("""
        <div class="login-box">

            <div class="login-icon">🔐</div>

            <h1>Admin Control Panel</h1>

            <p style="color:rgba(255,255,255,0.6);">
                Secure access to your portfolio management system
            </p>

        </div>
        """, unsafe_allow_html=True)

        _, login_col, _ = st.columns([1, 2, 1])

        with login_col:

            with st.form("admin_login"):

                code = st.text_input(
                    "Admin Passcode",
                    type="password",
                    placeholder="Enter your admin code..."
                )

                submit = st.form_submit_button(
                    "🔓 Unlock Admin Panel",
                    use_container_width=True
                )

                if submit:

                    login_admin(code)

                    if check_admin_auth():

                        st.success(
                            "Authenticated successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Invalid Admin Code. Access Denied."
                        )

        return


    import streamlit as st


def admin_dashboard():
    # ---------------------------------------------------------
    # Custom CSS Formatting
    # ---------------------------------------------------------
    st.markdown(
        """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(255,75,75,0.2); }
        50% { box-shadow: 0 0 15px rgba(255,75,75,0.6); }
        100% { box-shadow: 0 0 5px rgba(255,75,75,0.2); }
    }
    .admin-header {
        background: linear-gradient(135deg, #1E1E2E 0%, #2D2D44 100%);
        padding: 24px;
        border-radius: 12px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 25px;
        animation: fadeIn 0.5s ease-out;
    }
    .admin-card {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2D2D44;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .admin-card:hover {
        border-color: #FF4B4B;
    }
    .badge-counter {
        background-color: #FF4B4B;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background-color: #1E1E2E;
        border-radius: 15px;
        border: 1px solid #2D2D44;
        text-align: center;
        animation: glow 3s infinite;
    }
    .admin-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #2D2D44, transparent);
        margin: 20px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Authentication Check
    # ---------------------------------------------------------
    if not check_admin_auth():
        st.markdown(
            """
        <div class="login-container">
            <h2>🔒 Admin Access</h2>
            <p style="color: #888;">Please enter your passcode to access the management portal.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.form("admin_login"):
            passcode = st.text_input(
                "Passcode", type="password", placeholder="Enter passcode..."
            )
            submit = st.form_submit_button("Authenticate", use_container_width=True)

            if submit:
                if login_admin(passcode):
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid Passcode!")
        return

    # ---------------------------------------------------------
    # Sidebar Status & Logout
    # ---------------------------------------------------------
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🟢 Admin Session")
        st.caption("You are logged in as Administrator.")
        if st.button("🚪 Logout", use_container_width=True):
            logout_admin()
            st.rerun()

    # ---------------------------------------------------------
    # Main Header
    # ---------------------------------------------------------
    st.markdown(
        """
    <div class="admin-header">
        <h1 style="margin:0; padding:0; color: white;">⚙️ Portfolio Control Panel</h1>
        <p style="margin:5px 0 0 0; color: #AAA;">Manage your site content, showcase projects, and update profile data dynamically.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Management Tabs
    # ---------------------------------------------------------
    tabs = st.tabs(
        [
            "👤 Profile",
            "🛠️ Skills",
            "🚀 Projects",
            "💼 Services",
            "📜 Experience",
            "🎓 Learning",
            "🔗 Socials",
        ]
    )

    # ==========================================
    # 1. PROFILE TAB
    # ==========================================
    with tabs[0]:
        st.subheader("👤 Manage Profile")
        st.caption("Update your primary personal information.")

        profile_data = get_profile() if "get_profile" in globals() else {}

        with st.form("profile_form"):
            name = st.text_input("Name", value=profile_data.get("name", ""))
            title = st.text_input("Title / Role", value=profile_data.get("title", ""))
            email = st.text_input("Email", value=profile_data.get("email", ""))
            bio = st.text_area("Bio", value=profile_data.get("bio", ""))
            image_url = st.text_input(
                "Profile Image URL", value=profile_data.get("image_url", "")
            )

            cols = st.columns(2)
            with cols[0]:
                years_exp = st.number_input(
                    "Years of Experience",
                    value=int(profile_data.get("years_exp", 0)),
                    min_value=0,
                )
            with cols[1]:
                projects_done = st.number_input(
                    "Projects Completed",
                    value=int(profile_data.get("projects_done", 0)),
                    min_value=0,
                )

            if st.form_submit_button("💾 Save Profile", use_container_width=True):
                if email and not is_valid_email(email):
                    st.error("Invalid email address.")
                else:
                    update_profile(
                        {
                            "name": name,
                            "title": title,
                            "email": email,
                            "bio": bio,
                            "image_url": image_url,
                            "years_exp": years_exp,
                            "projects_done": projects_done,
                        }
                    )
                    st.success("✅ Profile updated successfully!")
                    st.rerun()

    # ==========================================
    # 2. SKILLS TAB
    # ==========================================
    with tabs[1]:
        st.subheader("🛠️ Manage Skills")
        st.caption("Add, categorize, and delete skills.")

        skills = get_skills() if "get_skills" in globals() else []

        if skills:
            for skill in skills:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{skill.get('name', '')}</strong> ({skill.get('category', 'General')}) - Level: {skill.get('level', 'N/A')}%
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_sk_{skill['id']}"):
                        delete_skill(skill["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_skill_form"):
            sk_name = st.text_input("Skill Name")
            sk_category = st.text_input("Category", placeholder="e.g. Frontend, Backend, Tools")
            sk_level = st.slider("Proficiency (%)", 0, 100, 80)

            if st.form_submit_button("➕ Add Skill", use_container_width=True):
                if sk_name:
                    add_skill(
                        {
                            "name": sk_name.strip(),
                            "category": sk_category.strip(),
                            "level": sk_level,
                        }
                    )
                    st.success(f"✅ Skill '{sk_name}' added!")
                    st.rerun()
                else:
                    st.error("Skill name cannot be empty.")

    # ==========================================
    # 3. PROJECTS TAB
    # ==========================================
    with tabs[2]:
        st.subheader("🚀 Manage Projects")
        st.caption("Showcase your recent projects and achievements.")

        projects = get_projects() if "get_projects" in globals() else []

        if projects:
            for proj in projects:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{proj.get('title', '')}</strong><br>
                            <small>{proj.get('description', '')[:100]}...</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_proj_{proj['id']}"):
                        delete_project(proj["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_project_form"):
            p_title = st.text_input("Project Title")
            p_desc = st.text_area("Description")
            p_tech = st.text_input("Technologies (comma separated)", placeholder="Python, Streamlit, PostgreSQL")
            p_image = st.text_input("Image URL")
            p_github = st.text_input("GitHub Repo URL")
            p_live = st.text_input("Live Demo URL")

            if st.form_submit_button("➕ Add Project", use_container_width=True):
                if p_title and p_desc:
                    add_project(
                        {
                            "title": p_title.strip(),
                            "description": p_desc.strip(),
                            "technologies": [t.strip() for t in p_tech.split(",") if t.strip()],
                            "image_url": p_image.strip(),
                            "github_url": p_github.strip(),
                            "live_url": p_live.strip(),
                        }
                    )
                    st.success(f"✅ Project '{p_title}' added!")
                    st.rerun()
                else:
                    st.error("Title and Description are required.")

    # ==========================================
    # 4. SERVICES TAB
    # ==========================================
    with tabs[3]:
        st.subheader("💼 Manage Services")
        st.caption("Outline the services you offer to clients or teams.")

        services = get_services() if "get_services" in globals() else []

        if services:
            for srv in services:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{srv.get('title', '')}</strong><br>
                            <small>{srv.get('description', '')}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_srv_{srv['id']}"):
                        delete_service(srv["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_service_form"):
            s_title = st.text_input("Service Title")
            s_desc = st.text_area("Service Description")
            s_icon = st.text_input("Icon (Emoji or CSS Class)", placeholder="💻")

            if st.form_submit_button("➕ Add Service", use_container_width=True):
                if s_title and s_desc:
                    add_service(
                        {
                            "title": s_title.strip(),
                            "description": s_desc.strip(),
                            "icon": s_icon.strip(),
                        }
                    )
                    st.success(f"✅ Service '{s_title}' added!")
                    st.rerun()
                else:
                    st.error("Title and Description are required.")

    # ==========================================
    # 5. EXPERIENCE TAB
    # ==========================================
    with tabs[4]:
        st.subheader("📜 Manage Work Experience")
        st.caption("Detail your professional background and job roles.")

        experiences = get_experience() if "get_experience" in globals() else []

        if experiences:
            for exp in experiences:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{exp.get('role', '')}</strong> at <em>{exp.get('company', '')}</em> ({exp.get('period', '')})<br>
                            <small>{exp.get('description', '')}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_exp_{exp['id']}"):
                        delete_experience(exp["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_experience_form"):
            e_role = st.text_input("Role / Position")
            e_company = st.text_input("Company / Organization")
            e_period = st.text_input("Period", placeholder="e.g. Jan 2022 - Present")
            e_desc = st.text_area("Responsibilities & Achievements")

            if st.form_submit_button("➕ Add Experience", use_container_width=True):
                if e_role and e_company:
                    add_experience(
                        {
                            "role": e_role.strip(),
                            "company": e_company.strip(),
                            "period": e_period.strip(),
                            "description": e_desc.strip(),
                        }
                    )
                    st.success(f"✅ Experience at '{e_company}' added!")
                    st.rerun()
                else:
                    st.error("Role and Company are required.")

    # ==========================================
    # 6. LEARNING TAB
    # ==========================================
    with tabs[5]:
        st.subheader("🎓 Manage Learning & Certifications")
        st.caption("Track courses, certifications, and learning goals.")

        learning = (
            get_learning_journey() if "get_learning_journey" in globals() else []
        )

        if learning:
            for item in learning:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{item.get('title', '')}</strong> - {item.get('issuer', '')}<br>
                            <small>Date: {item.get('date', 'N/A')}</small>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_learn_{item['id']}"):
                        delete_learning(item["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_learning_form"):
            l_title = st.text_input("Course / Certification Title")
            l_issuer = st.text_input("Platform / Organization", placeholder="e.g. Coursera, Udemy, AWS")
            l_date = st.text_input("Completion Date / Status", placeholder="e.g. 2023, In Progress")
            l_order = st.number_input("Display Order", value=1, min_value=1)

            if st.form_submit_button("➕ Add Learning Item", use_container_width=True):
                if l_title:
                    add_learning(
                        {
                            "title": l_title.strip(),
                            "issuer": l_issuer.strip(),
                            "date": l_date.strip(),
                            "display_order": l_order,
                        }
                    )
                    st.success("✅ Learning item added.")
                    st.rerun()
                else:
                    st.error("Title is required.")

    # ==========================================
    # 7. SOCIALS TAB
    # ==========================================
    with tabs[6]:
        st.subheader("🔗 Manage Social Links")
        st.caption("Update links to your external profiles and social platforms.")

        socials = get_socials() if "get_socials" in globals() else []

        if socials:
            for soc in socials:
                cols = st.columns([4, 1])
                with cols[0]:
                    st.markdown(
                        f"""
                        <div class="admin-card">
                            <strong>{soc.get('platform', 'Link')}</strong>: 
                            <a href="{soc.get('url', '#')}" target="_blank">{soc.get('url', '')}</a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    if st.button("🗑️", key=f"del_soc_{soc['id']}"):
                        delete_social(soc["id"])
                        st.rerun()

        st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

        with st.form("add_social_form"):
            platform = st.text_input("Platform Name", placeholder="e.g. GitHub, LinkedIn, Twitter")
            url = st.text_input("Profile URL", placeholder="https://...")
            s_order = st.number_input("Display Order", value=1, min_value=1)

            if st.form_submit_button("➕ Add Social Link", use_container_width=True):
                if platform and url:
                    if is_valid_url(url):
                        add_social(
                            {
                                "platform": platform.strip(),
                                "url": url.strip(),
                                "display_order": s_order,
                            }
                        )
                        st.success(f"✅ {platform} link added!")
                        st.rerun()
                    else:
                        st.error("Invalid URL format.")
                else:
                    st.error("Please provide both Platform Name and URL.")
                    
# ==========================================
# MAIN APP
# ==========================================
def main():
    if "nav" not in st.session_state:
        st.session_state["nav"] = "Home"

    pages = {
        "Home": render_home,
        "Skills": render_skills,
        "Projects": render_projects,
        "Services": render_services,
        "Experience": render_experience,
        "Contact": render_contact,
        "Admin": render_admin
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()), index=list(pages.keys()).index(st.session_state["nav"]))
    st.session_state["nav"] = selection

    pages[selection]()

if __name__ == "__main__":
    main()
