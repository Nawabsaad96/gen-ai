import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Fitness Routine Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

from database.db import (
    init_database,
    create_user,
    update_user,
    add_weight,
    add_water
)


# Create database tables
init_database()


# =========================================================
# LOAD CSS
# =========================================================

try:
    with open("css/style.css", "r", encoding="utf-8") as file:
        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )

except FileNotFoundError:
    pass


# =========================================================
# SESSION STATE
# =========================================================

if "age" not in st.session_state:
    st.session_state.age = 22

if "weight" not in st.session_state:
    st.session_state.weight = 70.0

if "height" not in st.session_state:
    st.session_state.height = 175.0

if "goal" not in st.session_state:
    st.session_state.goal = "Weight Loss"

if "water" not in st.session_state:
    st.session_state.water = 0.0

if "workout_streak" not in st.session_state:
    st.session_state.workout_streak = 14


# =========================================================
# CREATE USER
# =========================================================

if "user_id" not in st.session_state:

    st.session_state.user_id = create_user(
        "Fitness User",
        st.session_state.age,
        st.session_state.weight,
        st.session_state.height,
        st.session_state.goal
    )


# =========================================================
# FUNCTIONS
# =========================================================

def calculate_bmi(weight, height):

    if height <= 0:
        return 0.0

    return weight / ((height / 100) ** 2)


def bmi_status(bmi):

    if bmi < 18.5:
        return "Underweight", "🔵"

    elif bmi < 25:
        return "Normal", "🟢"

    elif bmi < 30:
        return "Overweight", "🟠"

    else:
        return "Obese", "🔴"


# Current BMI
bmi = calculate_bmi(
    st.session_state.weight,
    st.session_state.height
)

status, status_icon = bmi_status(bmi)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # BRAND
    # -----------------------------------------------------

    st.markdown(
        "## 🏋️ Fitness Coach"
    )

    st.caption(
        "AI Personal Trainer"
    )

    st.divider()


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    st.markdown(
        "### 👤 Profile"
    )


    age = st.number_input(
        "Age",
        min_value=13,
        max_value=100,
        value=int(st.session_state.age),
        step=1
    )


    weight = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=250.0,
        value=float(st.session_state.weight),
        step=0.5
    )


    height = st.number_input(
        "Height (cm)",
        min_value=120.0,
        max_value=230.0,
        value=float(st.session_state.height),
        step=1.0
    )


    goals = [
        "Weight Loss",
        "Muscle Gain",
        "Maintain Weight"
    ]


    if st.session_state.goal in goals:
        goal_index = goals.index(
            st.session_state.goal
        )
    else:
        goal_index = 0


    goal = st.selectbox(
        "Fitness Goal",
        goals,
        index=goal_index
    )


    # -----------------------------------------------------
    # SAVE PROFILE
    # -----------------------------------------------------

    if st.button(
        "💾 Save Profile",
        use_container_width=True,
        type="primary"
    ):

        # Update session
        st.session_state.age = age
        st.session_state.weight = weight
        st.session_state.height = height
        st.session_state.goal = goal


        # Save user profile
        update_user(
            st.session_state.user_id,
            "Fitness User",
            age,
            weight,
            height,
            goal
        )


        # Save weight history
        add_weight(
            st.session_state.user_id,
            weight,
            height
        )


        st.success(
            "Profile saved successfully!"
        )


    st.divider()


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    st.markdown(
        "### 📊 BMI"
    )


    current_bmi = calculate_bmi(
        st.session_state.weight,
        st.session_state.height
    )


    current_status, current_icon = bmi_status(
        current_bmi
    )


    st.metric(
        label="Body Mass Index",
        value=f"{current_bmi:.1f}"
    )


    if current_status == "Normal":
        st.success(
            f"{current_icon} {current_status}"
        )

    elif current_status == "Overweight":
        st.warning(
            f"{current_icon} {current_status}"
        )

    elif current_status == "Obese":
        st.error(
            f"{current_icon} {current_status}"
        )

    else:
        st.info(
            f"{current_icon} {current_status}"
        )


    # -----------------------------------------------------
    # WATER
    # -----------------------------------------------------

    st.markdown(
        "### 💧 Water"
    )


    water = st.slider(
        "Today's water intake",
        min_value=0.0,
        max_value=5.0,
        value=float(st.session_state.water),
        step=0.25
    )


    # Save only when changed
    if water != st.session_state.water:

        st.session_state.water = water

        add_water(
            st.session_state.user_id,
            water
        )


    water_goal = 3.0


    st.progress(
        min(water / water_goal, 1.0)
    )


    st.caption(
        f"{water:.2f} L / {water_goal:.1f} L"
    )


    if water >= water_goal:

        st.success(
            "💧 Daily goal reached!"
        )


    # -----------------------------------------------------
    # WORKOUT STREAK
    # -----------------------------------------------------

    st.markdown(
        "### 🔥 Workout Streak"
    )


    st.metric(
        label="Current Streak",
        value=f"{st.session_state.workout_streak} days"
    )


    # -----------------------------------------------------
    # SIDEBAR FOOTER
    # -----------------------------------------------------

    st.divider()

    st.caption(
        "🤖 Powered by Groq AI"
    )

    st.caption(
        "AI Fitness Routine Coach"
    )


# =========================================================
# MAIN HEADER
# =========================================================

# ================= HEADER =================

st.title("🏋️ AI Fitness Routine Coach")

st.markdown(
    "<p style='text-align:center;color:#cbd5e1;font-size:18px;'>"
    "Your personalized AI-powered fitness companion"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>"
    "Personalized Workouts • Smart Diet Plans • BMI Tracking • Daily Motivation"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# NAVIGATION
# =========================================================

st.markdown(
    "### 🧭 Navigation"
)


pages = [
    "🏠 Dashboard",
    "🤖 AI Coach",
    "🏋️ Workout",
    "🥗 Diet",
    "📈 Progress"
]


selected_page = st.radio(
    "Choose a section",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# PAGE FILES
# =========================================================

page_files = {

    "🏠 Dashboard":
        "pages/dashboard.py",

    "🤖 AI Coach":
        "pages/ai_coach.py",

    "🏋️ Workout":
        "pages/workout.py",

    "🥗 Diet":
        "pages/diet.py",

    "📈 Progress":
        "pages/progress.py"

}


# =========================================================
# LOAD SELECTED PAGE
# =========================================================

selected_file = page_files[selected_page]


try:

    with open(
        selected_file,
        "r",
        encoding="utf-8"
    ) as file:

        page_code = file.read()


    exec(
        compile(
            page_code,
            selected_file,
            "exec"
        )
    )


except FileNotFoundError:

    st.error(
        f"Page not found: {selected_file}"
    )


except Exception as error:

    st.error(
        "There was an error loading this page."
    )

    st.exception(error)