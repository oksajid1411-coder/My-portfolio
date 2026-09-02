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


    # ==========================================
    # ADMIN HEADER
    # ==========================================

    st.markdown("""
    <div class="admin-wrapper">

        <div class="admin-header">

            <div class="admin-title">
                ⚙️ Portfolio Admin
            </div>

            <div class="admin-subtitle">
                Manage your portfolio content, projects,
                skills and professional information.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # SIDEBAR
    # ==========================================

    st.sidebar.markdown("### ⚙️ Admin")

    st.sidebar.success("🟢 Authenticated")

    st.sidebar.button(
        "🚪 Logout Admin",
        on_click=logout_admin,
        use_container_width=True
    )


    # ==========================================
    # TABS
    # ==========================================

    tabs = st.tabs([
        "👤 Profile",
        "🛠️ Skills",
        "🚀 Projects",
        "💼 Services",
        "📈 Experience",
        "📚 Learning",
        "🔗 Socials"
    ])


    # ==========================================
    # PROFILE
    # ==========================================

    with tabs[0]:

        st.subheader("👤 Profile Information")

        st.caption(
            "Update your personal and professional information."
        )

        profile = get_profile()

        if profile:

            with st.form("edit_profile_form"):

                col1, col2 = st.columns(2)

                with col1:

                    name = st.text_input(
                        "Full Name",
                        profile.get("name", "")
                    )

                    title = st.text_input(
                        "Professional Title",
                        profile.get("title", "")
                    )

                    location = st.text_input(
                        "Location",
                        profile.get("location", "")
                    )

                    email = st.text_input(
                        "Email",
                        profile.get("email", "")
                    )

                with col2:

                    image_url = st.text_input(
                        "Profile Image URL",
                        profile.get("profile_image", "")
                    )

                    exp_years = st.number_input(
                        "Years of Experience",
                        min_value=0,
                        value=int(
                            profile.get(
                                "experience_years",
                                1
                            )
                        )
                    )

                    bio = st.text_area(
                        "Professional Bio",
                        profile.get("bio", ""),
                        height=150
                    )

                st.markdown(
                    '<div class="admin-divider"></div>',
                    unsafe_allow_html=True
                )

                if st.form_submit_button(
                    "💾 Save Profile",
                    use_container_width=True
                ):

                    if not is_valid_email(email):

                        st.error(
                            "Invalid email address format."
                        )

                    elif not is_valid_url(image_url):

                        st.error(
                            "Invalid image URL format."
                        )

                    else:

                        update_profile(
                            profile["id"],
                            {
                                "name": name,
                                "title": title,
                                "location": location,
                                "email": email,
                                "profile_image": image_url,
                                "experience_years": exp_years,
                                "bio": bio
                            }
                        )

                        st.success(
                            "✅ Profile updated successfully!"
                        )

                        st.rerun()


    # ==========================================
    # SKILLS
    # ==========================================

    with tabs[1]:

        st.subheader("🛠️ Manage Skills")

        st.caption(
            "Add and manage your technical skills."
        )

        skills = get_skills()

        if skills:

            st.markdown("### Current Skills")

            for s in skills:

                with st.container():

                    cols = st.columns(
                        [3, 2, 2, 1]
                    )

                    with cols[0]:

                        st.markdown(
                            f"""
                            <div class="skill-card">
                                <strong>
                                    {s.get('name')}
                                </strong>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with cols[1]:

                        cat = s.get(
                            "category",
                            "N/A"
                        )

                        st.markdown(
                            f"""
                            <span class="cat-badge">
                                📂 {cat}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                    with cols[2]:

                        lvl = s.get(
                            "level",
                            "N/A"
                        )

                        st.markdown(
                            f"""
                            <span class="level-badge">
                                ⭐ {lvl}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                    with cols[3]:

                        if st.button(
                            "🗑️",
                            key=f"del_sk_{s['id']}",
                            help="Delete Skill"
                        ):

                            delete_skill(
                                s["id"]
                            )

                            st.toast(
                                f"Skill '{s.get('name')}' deleted!",
                                icon="🗑️"
                            )

                            st.rerun()

        else:

            st.info(
                "No skills added yet."
            )


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )


        # Add Skill

        st.markdown("### ➕ Add New Skill")

        existing_skill_cats = list(
            set(
                [
                    s.get("category")
                    for s in skills
                    if s.get("category")
                ]
            )
        )

        default_skill_cats = [
            "Programming",
            "Data Analysis",
            "Machine Learning",
            "Databases",
            "Tools & Frameworks"
        ]

        all_skill_cats = sorted(
            list(
                set(
                    default_skill_cats
                    + existing_skill_cats
                )
            )
        )

        cat_options = (
            ["-- Select Category --"]
            + all_skill_cats
            + ["+ Add New Category"]
        )


        with st.form(
            "add_skill_form",
            clear_on_submit=True
        ):

            col_a, col_b = st.columns(2)

            with col_a:

                sk_name = st.text_input(
                    "Skill Name",
                    placeholder="e.g. Python, SQL, Power BI"
                )

                sk_level = st.selectbox(
                    "Proficiency Level",
                    [
                        "Beginner",
                        "Intermediate",
                        "Advanced"
                    ],
                    index=1
                )

            with col_b:

                selected_sk_cat = st.selectbox(
                    "Category",
                    cat_options
                )

                new_sk_cat = st.text_input(
                    "New Category Name",
                    placeholder="Enter new category..."
                )

            sk_order = st.number_input(
                "Display Order",
                value=1,
                min_value=1
            )

            submit_btn = st.form_submit_button(
                "🚀 Add Skill",
                use_container_width=True
            )

            if submit_btn:

                final_sk_cat = ""

                if selected_sk_cat == "+ Add New Category":

                    final_sk_cat = new_sk_cat.strip()

                elif selected_sk_cat != "-- Select Category --":

                    final_sk_cat = selected_sk_cat


                if sk_name and final_sk_cat:

                    add_skill(
                        {
                            "name": sk_name.strip(),
                            "category": final_sk_cat,
                            "level": sk_level,
                            "display_order": sk_order
                        }
                    )

                    st.success(
                        f"✅ Skill '{sk_name}' added!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "⚠️ Please provide Skill Name "
                        "and Category."
                    )


    # ==========================================
    # PROJECTS
    # ==========================================

    with tabs[2]:

        st.subheader("🚀 Manage Projects")

        st.caption(
            "Showcase and organize your portfolio projects."
        )

        projects = get_projects()

        if projects:

            for p in projects:

                with st.container():

                    cols = st.columns(
                        [4, 2, 1]
                    )

                    with cols[0]:

                        st.markdown(
                            f"""
                            <div class="admin-card">
                                <strong>
                                    {p['title']}
                                </strong>
                                <br>
                                <small>
                                    📂 {p.get('category', 'N/A')}
                                </small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with cols[1]:

                        st.caption(
                            f"Display Order: "
                            f"{p.get('display_order', 1)}"
                        )

                    with cols[2]:

                        if st.button(
                            "🗑️",
                            key=f"del_proj_{p['id']}"
                        ):

                            delete_project(
                                p["id"]
                            )

                            st.rerun()

        else:

            st.info(
                "No projects added yet."
            )


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ➕ Add New Project"
        )


        existing_proj_cats = list(
            set(
                [
                    p.get("category")
                    for p in projects
                    if p.get("category")
                ]
            )
        )

        default_cats = [
            "Data Analysis",
            "Machine Learning",
            "Deep Learning",
            "Data collection"
        ]

        all_cats = list(
            set(
                default_cats
                + existing_proj_cats
            )
        )

        cat_options = (
            ["-- Select Category --"]
            + all_cats
            + ["+ Add New Category"]
        )


        with st.form("add_proj_form"):

            p_title = st.text_input(
                "Project Title"
            )

            selected_p_cat = st.selectbox(
                "Category",
                cat_options
            )

            new_p_cat = st.text_input(
                "New Category Name"
            )

            p_desc = st.text_area(
                "Short Description"
            )

            p_tech = st.text_input(
                "Technologies",
                placeholder="Python, Pandas, Streamlit..."
            )

            col1, col2 = st.columns(2)

            with col1:

                p_gh = st.text_input(
                    "GitHub URL"
                )

            with col2:

                p_demo = st.text_input(
                    "Demo URL"
                )

            p_feat = st.checkbox(
                "⭐ Featured Project"
            )

            p_order = st.number_input(
                "Display Order",
                value=1
            )

            st.markdown(
                "#### Project Details"
            )

            p_overview = st.text_area(
                "Overview"
            )

            p_problem = st.text_area(
                "Problem Statement"
            )

            p_dataset = st.text_area(
                "Dataset Details"
            )

            p_approach = st.text_area(
                "Approach"
            )

            p_results = st.text_area(
                "Results"
            )


            if st.form_submit_button(
                "🚀 Add Project",
                use_container_width=True
            ):

                final_p_cat = ""

                if selected_p_cat == "+ Add New Category":

                    final_p_cat = new_p_cat.strip()

                elif selected_p_cat != "-- Select Category --":

                    final_p_cat = selected_p_cat


                if p_gh and not is_valid_url(p_gh):

                    st.error(
                        "Invalid GitHub URL."
                    )

                elif p_demo and not is_valid_url(p_demo):

                    st.error(
                        "Invalid Demo URL."
                    )

                elif (
                    p_title
                    and p_desc
                    and final_p_cat
                ):

                    add_project(
                        {
                            "title": p_title,
                            "category": final_p_cat,
                            "description": p_desc,
                            "technologies": p_tech,
                            "github_url": p_gh,
                            "demo_url": p_demo,
                            "featured": p_feat,
                            "display_order": p_order,
                            "overview": p_overview,
                            "problem": p_problem,
                            "dataset": p_dataset,
                            "approach": p_approach,
                            "results": p_results
                        }
                    )

                    st.success(
                        "✅ Project added successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Please fill in Project Title, "
                        "Description and Category."
                    )


    # ==========================================
    # SERVICES
    # ==========================================

    with tabs[3]:

        st.subheader("💼 Manage Services")

        st.caption(
            "Manage the professional services displayed "
            "on your portfolio."
        )

        services = get_services()

        for srv in services:

            cols = st.columns([4, 1])

            with cols[0]:

                st.markdown(
                    f"""
                    <div class="admin-card">
                        <strong>
                            {srv['title']}
                        </strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with cols[1]:

                if st.button(
                    "🗑️",
                    key=f"del_srv_{srv['id']}"
                ):

                    delete_service(
                        srv["id"]
                    )

                    st.rerun()


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )


        with st.form("add_srv_form"):

            s_title = st.text_input(
                "Service Title"
            )

            s_desc = st.text_area(
                "Service Description"
            )

            s_items = st.text_area(
                "Service Items",
                placeholder="One item per line..."
            )

            s_order = st.number_input(
                "Display Order",
                value=1
            )

            if st.form_submit_button(
                "➕ Add Service",
                use_container_width=True
            ):

                items_list = [
                    i.strip()
                    for i in s_items.split("\n")
                    if i.strip()
                ]

                add_service(
                    {
                        "title": s_title,
                        "description": s_desc,
                        "items": items_list,
                        "display_order": s_order,
                        "active": True
                    }
                )

                st.success(
                    "✅ Service added."
                )

                st.rerun()


    # ==========================================
    # EXPERIENCE
    # ==========================================

    with tabs[4]:

        st.subheader("📈 Manage Experience")

        exps = get_experience()

        for e in exps:

            cols = st.columns([4, 1])

            with cols[0]:

                st.markdown(
                    f"""
                    <div class="admin-card">
                        <strong>
                            {e['position']}
                        </strong>
                        <br>
                        <small>
                            🏢 {e['organization']}
                        </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with cols[1]:

                if st.button(
                    "🗑️",
                    key=f"del_exp_{e['id']}"
                ):

                    delete_experience(
                        e["id"]
                    )

                    st.rerun()


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )


        with st.form("add_exp_form"):

            e_pos = st.text_input(
                "Position"
            )

            e_org = st.text_input(
                "Organization"
            )

            col1, col2 = st.columns(2)

            with col1:

                e_start = st.text_input(
                    "Start Date"
                )

            with col2:

                e_end = st.text_input(
                    "End Date"
                )

            e_desc = st.text_area(
                "Description"
            )

            e_order = st.number_input(
                "Display Order",
                value=1
            )

            if st.form_submit_button(
                "➕ Add Experience",
                use_container_width=True
            ):

                add_experience(
                    {
                        "position": e_pos,
                        "organization": e_org,
                        "start_date": e_start,
                        "end_date": e_end,
                        "description": e_desc,
                        "display_order": e_order
                    }
                )

                st.success(
                    "✅ Experience added."
                )

                st.rerun()


    # ==========================================
    # LEARNING JOURNEY
    # ==========================================

    with tabs[5]:

        st.subheader("📚 Manage Learning Journey")

        items = get_learning_journey()

        for item in items:

            cols = st.columns([4, 1])

            with cols[0]:

                st.markdown(
                    f"""
                    <div class="admin-card">
                        <strong>
                            {item['title']}
                        </strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with cols[1]:

                if st.button(
                    "🗑️",
                    key=f"del_learn_{item['id']}"
                ):

                    delete_learning_item(
                        item["id"]
                    )

                    st.rerun()


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )


        with st.form("add_learn_form"):

            l_title = st.text_input(
                "Title"
            )

            l_desc = st.text_area(
                "Description"
            )

            l_order = st.number_input(
                "Display Order",
                value=1
            )

            if st.form_submit_button(
                "➕ Add Learning Item",
                use_container_width=True
            ):

                add_learning_item(
                    {
                        "title": l_title,
                        "description": l_desc,
                        "display_order": l_order
                    }
                )

                st.success(
                    "✅ Learning item added."
                )

                st.rerun()


    # ==========================================
    # SOCIAL LINKS
    # ==========================================

    with tabs[6]:

        st.subheader("🔗 Manage Social Links")

        socials = get_social_links()

        for soc in socials:

            cols = st.columns([3, 3, 1])

            with cols[0]:

                st.markdown(
                    f"**{soc['platform']}**"
                )

                st.caption(
                    soc.get("label", "")
                )

            with cols[1]:

                st.code(
                    soc["url"],
                    language="text"
                )

            with cols[2]:

                if st.button(
                    "🗑️",
                    key=f"del_soc_{soc['id']}"
                ):

                    delete_social_link(
                        soc["id"]
                    )

                    st.rerun()


        st.markdown(
            '<div class="admin-divider"></div>',
            unsafe_allow_html=True
        )


        with st.form("add_soc_form"):

            col1, col2 = st.columns(2)

            with col1:

                sc_plat = st.text_input(
                    "Platform"
                )

            with col2:

                sc_lbl = st.text_input(
                    "Label"
                )

            sc_url = st.text_input(
                "URL"
            )

            sc_order = st.number_input(
                "Display Order",
                value=1
            )

            if st.form_submit_button(
                "➕ Add Social Link",
                use_container_width=True
            ):

                add_social_link(
                    {
                        "platform": sc_plat,
                        "label": sc_lbl,
                        "url": sc_url,
                        "display_order": sc_order,
                        "active": True
                    }
                )

                st.success(
                    "✅ Social link added."
                )

                st.rerun()
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
