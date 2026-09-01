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
    
    # CSS Custom Styling for Animations & Cards
    st.markdown("""
        <style>
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0px;
            background: -webkit-linear-gradient(45deg, #FF4B4B, #FF8F8F);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .profile-card {
            padding: 20px;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }
        .profile-card:hover {
            transform: translateY(-5px);
        }
        .stButton>button {
            border-radius: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    if not profile:
        st.warning("No profile data found. Please add profile info from the Admin panel.")
        return

    # --- HERO SECTION ---
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
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
        
        st.markdown(f'<h1 class="hero-title">{name}</h1>', unsafe_allow_html=True)
        st.subheader(title)
        
        location = profile.get("location", "")
        if location:
            st.markdown(f"📍 **{location}**")
            
        bio = profile.get("bio", "")
        if bio:
            st.write(bio)
            
        st.write("") # Spacer

        # CTA Buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("🚀 View Projects", use_container_width=True):
                st.session_state["nav_selection"] = "Projects" # আপনার নেভিগেশন স্টেটের নাম অনুযায়ী
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

    st.write("---")

    # --- QUICK STATS SECTION ---
    stat_col1, stat_col2, stat_col3 = st.columns([1,2,1])
    
    with stat_col1:
        st.metric(label="Experience", value="1+ Years", delta="Active Learner")
    with stat_col2:
        st.metric(label="Completed Projects", value="10+", delta="Data & ML")
    with stat_col3:
        st.metric(label="Core Expertise", value="Data Analysis", delta="Python | Pandas | Power BI")

    st.write("") # হালকা ফাঁকা জায়গা তৈরির জন্য

    # দ্বিতীয় লাইন: আলাদা কলামে মাঝখানে মেট্রিক রাখার জন্য [1, 2, 1] রেশিও
    left_pad, center_col, right_pad = st.columns([1, 2, 1])
    
    with center_col:
        st.metric(label="Other Expertise", value="ML & DL", delta="Tensorflow | PyTorch | SKLearn")
# ABOUT PAGE
# ==========================================
def render_about():
    profile = get_profile()
    st.title("About Me")
    
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        if profile.get("profile_image"):
            st.image(profile["profile_image"], use_container_width=True)
    with col2:
        st.subheader(profile.get("name", ""))
        st.write(f"**Title:** {profile.get('title', '')}")
        st.write(f"**Location:** {profile.get('location', '')}")
        st.write(f"**Experience:** {profile.get('experience_years', 1)} Year")
        st.write(f"**Email:** {profile.get('email', '')}")
        st.write("---")
        st.write(profile.get("bio", ""))
        
    st.markdown("---")
    st.header("My Analytical & Modeling Approach")
    st.markdown("""
    ```
    Data Collection  ➔  Data Cleaning  ➔  Exploratory Data Analysis
                                                      │
    Insights & Solution  ⬅  Model Evaluation  ⬅  ML/DL Modeling  ⬅  Feature Engineering
    ```
    """)

# ==========================================
# SKILLS PAGE
# ==========================================
def render_skills():
    st.title("Technical Skills")
    skills = get_skills()
    
    if not skills:
        st.info("No skills currently listed.")
        return

    categories = list(set([s["category"] for s in skills]))
    selected_cat = st.selectbox("Filter Category", ["All"] + categories)
    
    filtered_skills = skills if selected_cat == "All" else [s for s in skills if s["category"] == selected_cat]

    for cat in set([s["category"] for s in filtered_skills]):
        st.subheader(cat)
        cat_skills = [s for s in filtered_skills if s["category"] == cat]
        cols = st.columns(4)
        for idx, skill in enumerate(cat_skills):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="custom-card" style="padding:15px; text-align:center;">
                    <h4>{skill['name']}</h4>
                    <span class="badge badge-secondary">{skill['level']}</span>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# PROJECTS PAGE
# ==========================================
def render_projects():
    st.title("Projects")
    projects = get_projects()
    
    if not projects:
        st.info("No projects available.")
        return

    search = st.text_input("🔍 Search Projects", "")
    categories = ["All"] + list(set([p["category"] for p in projects]))
    selected_cat = st.selectbox("Category Filter", categories)
    
    filtered = projects
    if selected_cat != "All":
        filtered = [p for p in filtered if p["category"] == selected_cat]
    if search:
        filtered = [p for p in filtered if search.lower() in p["title"].lower() or search.lower() in p["description"].lower()]

    for proj in filtered:
        with st.container():
            st.markdown(f"""
            <div class="custom-card">
                <h3>{proj['title']} {'⭐' if proj.get('featured') else ''}</h3>
                <span class="badge">{proj['category']}</span>
                <p>{proj['description']}</p>
                <p><strong>Technologies:</strong> {proj.get('technologies', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📄 View Details"):
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
                    
                c1, c2 = st.columns(2)
                with c1:
                    if proj.get("github_url"):
                        st.markdown(f"[🔗 GitHub Repository]({proj['github_url']})")
                with c2:
                    if proj.get("demo_url"):
                        st.markdown(f"[🚀 Live Demo]({proj['demo_url']})")

# ==========================================
# SERVICES PAGE
# ==========================================
def render_services():
    st.title("Services")
    services = get_services()
    
    active_services = [s for s in services if s.get("active", True)]
    
    for srv in active_services:
        st.markdown(f"""
        <div class="custom-card">
            <h3>{srv['title']}</h3>
            <p>{srv['description']}</p>
            <ul>
                {''.join([f'<li>{item}</li>' for item in srv.get('items', [])])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# EXPERIENCE PAGE
# ==========================================
def render_experience():
    st.title("Experience & Learning Journey")
    
    st.subheader("Professional Experience")
    exps = get_experience()
    for exp in exps:
        st.markdown(f"""
        <div class="timeline-item">
            <h4>{exp['position']} - {exp['organization']}</h4>
            <p><em>{exp['start_date']} - {exp['end_date']}</em></p>
            <p>{exp['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Learning Journey Timeline")
    journey = get_learning_journey()
    for item in journey:
        st.markdown(f"""
        <div class="timeline-item">
            <h4>{item['title']}</h4>
            <p>{item['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# CONTACT PAGE
# ==========================================
def render_contact():
    profile = get_profile()
    st.title("Contact Me")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <h3>Contact Information</h3>
            <p>📍 <strong>Location:</strong> {profile.get('location', '')}</p>
            <p>📧 <strong>Email:</strong> {profile.get('email', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"[✉️ Send Direct Email](mailto:{profile.get('email', '')})")

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>Social Profiles</h3>
        </div>
        """, unsafe_allow_html=True)
        socials = get_social_links()
        for soc in socials:
            if soc.get("active", True):
                st.markdown(f"🔗 [{soc['label']}]({soc['url']})")

# ==========================================
# ADMIN PAGE
# ==========================================
def render_admin():
    st.title("🔒 Admin Control Panel")
    
    if not check_admin_auth():
        with st.form("admin_login"):
            code = st.text_input("Enter Admin Passcode", type="password")
            submit = st.form_submit_button("Unlock")
            if submit:
                login_admin(code)
                if check_admin_auth():
                    st.success("Authenticated successfully.")
                    st.rerun()
                else:
                    st.error("Invalid Admin Code. Access Denied.")
        return

    st.sidebar.button("🚪 Logout Admin", on_click=logout_admin)
    
    tabs = st.tabs(["Profile", "Skills", "Projects", "Services", "Experience", "Learning", "Socials"])
    
    # --- Profile Tab ---
    with tabs[0]:
        st.subheader("Edit Profile")
        profile = get_profile()
        if profile:
            with st.form("edit_profile_form"):
                name = st.text_input("Name", profile.get("name", ""))
                title = st.text_input("Title", profile.get("title", ""))
                location = st.text_input("Location", profile.get("location", ""))
                email = st.text_input("Email", profile.get("email", ""))
                image_url = st.text_input("Profile Image URL", profile.get("profile_image", ""))
                exp_years = st.number_input("Years of Experience", value=int(profile.get("experience_years", 1)))
                bio = st.text_area("Bio", profile.get("bio", ""), height=150)
                
                if st.form_submit_button("Save Profile"):
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

    # --- Skills Tab ---
    with tabs[1]:
        st.subheader("Manage Skills")
        skills = get_skills()
        for s in skills:
            cols = st.columns([3, 2, 2, 1])
            cols[0].write(s["name"])
            cols[1].write(s["category"])
            cols[2].write(s["level"])
            if cols[3].button("🗑️", key=f"del_sk_{s['id']}"):
                delete_skill(s["id"])
                st.rerun()
                
        st.write("---")
        st.write("**Add New Skill**")
        with st.form("add_skill_form"):
            sk_name = st.text_input("Skill Name")
            sk_cat = st.text_input("Category")
            sk_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            sk_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("Add Skill"):
                if sk_name and sk_cat:
                    add_skill({"name": sk_name, "category": sk_cat, "level": sk_level, "display_order": sk_order})
                    st.success("Skill added.")
                    st.rerun()

    # --- Projects Tab ---
    with tabs[2]:
        st.subheader("Manage Projects")
        projects = get_projects()
        for p in projects:
            cols = st.columns([4, 2, 1])
            cols[0].write(f"**{p['title']}** ({p['category']})")
            cols[1].write(f"Order: {p.get('display_order', 1)}")
            if cols[2].button("🗑️", key=f"del_proj_{p['id']}"):
                delete_project(p["id"])
                st.rerun()
                
        st.write("---")
        st.write("**Add New Project**")
        with st.form("add_proj_form"):
            p_title = st.text_input("Project Title")
            p_cat = st.selectbox("Category", ["Data Analysis", "Machine Learning", "Deep Learning", "Web Scraping"])
            p_desc = st.text_area("Short Description")
            p_tech = st.text_input("Technologies (comma separated)")
            p_gh = st.text_input("GitHub URL")
            p_demo = st.text_input("Demo URL")
            p_feat = st.checkbox("Featured Project", value=False)
            p_order = st.number_input("Display Order", value=1)
            
            p_overview = st.text_area("Overview")
            p_problem = st.text_area("Problem Statement")
            p_dataset = st.text_area("Dataset Details")
            p_approach = st.text_area("Approach")
            p_results = st.text_area("Results")
            
            if st.form_submit_button("Add Project"):
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
                    st.success("Project added.")
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
                
        st.write("---")
        with st.form("add_srv_form"):
            s_title = st.text_input("Service Title")
            s_desc = st.text_area("Service Description")
            s_items = st.text_area("Service Items (one per line)")
            s_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("Add Service"):
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
                
        st.write("---")
        with st.form("add_exp_form"):
            e_pos = st.text_input("Position")
            e_org = st.text_input("Organization")
            e_start = st.text_input("Start Date")
            e_end = st.text_input("End Date")
            e_desc = st.text_area("Description")
            e_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("Add Experience"):
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
                
        st.write("---")
        with st.form("add_learn_form"):
            l_title = st.text_input("Title")
            l_desc = st.text_area("Description")
            l_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("Add Learning Item"):
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
                
        st.write("---")
        with st.form("add_soc_form"):
            sc_plat = st.text_input("Platform")
            sc_lbl = st.text_input("Label")
            sc_url = st.text_input("URL")
            sc_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("Add Social Link"):
                add_social_link({"platform": sc_plat, "label": sc_lbl, "url": sc_url, "display_order": sc_order, "active": True})
                st.success("Social link added.")
                st.rerun()

# ==========================================
# MAIN APP
# ==========================================
def main():
    if "nav" not in st.session_state:
        st.session_state["nav"] = "Home"

    pages = {
        "Home": render_home,
        "About": render_about,
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
