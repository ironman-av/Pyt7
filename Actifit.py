import streamlit as st
import time
import random

# --- Page Config ---
st.set_page_config(page_title="Calorie Tracker", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                    url("https://images.pexels.com/photos/414029/pexels-photo-414029.jpeg");
        background-attachment: fixed;
        background-size: cover;
        background-repeat: no-repeat;
        color: white !important;
    }
    label {
        font-weight: bold !important;
        color: #FFD700 !important;
        font-size: 16px !important;
    }
    .stAlert p {
        color: white !important;   /* ✅ error/warning/success text white */
        font-weight: bold;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 6px 14px rgba(0,0,0,0.25);
        margin: 10px;
        text-align: center;
    }
    .result-title {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    .result-value {
        font-size: 36px;
        font-weight: 900;
        color: #000;
    }
    h1 {
        color: #FFDD57 !important;
        text-align: center;
        background: rgba(0,0,0,0.6);
        padding: 12px;
        border-radius: 12px;
        font-size: 38px !important;
        font-weight: bold;
    }
    .highlight-box {
        color: white;
        padding: 20px;
        border-radius: 14px;
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        margin-top: 12px;
        line-height: 1.6;
        box-shadow: 0px 6px 14px rgba(0,0,0,0.4);
    }
    .highlight-box.warning {background: rgba(255, 165, 0, 0.9);}
    .highlight-box.danger {background: rgba(220, 38, 38, 0.9);}
    .highlight-box.success {background: rgba(34, 197, 94, 0.95);}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🔥 ActiFit Planner")
st.markdown("### 🏃‍♂ Enter your details to get started:")

# --- Input Form ---
with st.form("calorie_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("🎂 Age", min_value=1, max_value=100, value=25)
        weight = st.number_input("⚖ Weight (kg)", min_value=10, max_value=200, value=70)
        height = st.number_input("📏 Height (cm)", min_value=100, max_value=220, value=170)
        gender = st.selectbox("🚻 Gender", ["Male", "Female"])
    with col2:
        hours = st.number_input("⏳ Exercise Duration in Hours", min_value=0, max_value=10, value=0)
        minutes = st.number_input("⏳ Exercise Duration in Minutes", min_value=0, max_value=59, value=0)
        exercise_type = st.selectbox("💪 Exercise Type", [
            "Running", "Walking", "Cycling", "Yoga", "Swimming", "Strength Training", "Aerobics", "Dancing", "HIIT",
            "Pilates", "CrossFit", "Boxing", "Kickboxing", "Rowing", "Elliptical Training", "Climbing", "Martial Arts",
            "Football", "Basketball", "Tennis", "Badminton", "Table Tennis", "Skating", "Skiing", "Jump Rope",
            "Stair Climbing", "Stretching", "Golf", "Hiking", "Volleyball"
        ])
    submitted = st.form_submit_button("✨ Calculate My Results")

# --- Logic ---
if submitted:
    # --- BMI (always show) ---
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    st.markdown("## 🧮 Your Results")
    colA, colB = st.columns(2)
    with colA:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">📊 BMI</div>
            <div class="result-value">{bmi:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Check exercise duration ---
    total_minutes = hours * 60 + minutes
    if total_minutes <= 0:
        with colB:
            st.error("⏰ Please enter a valid exercise duration to calculate calories burned.")
    else:
        # --- BMR ---
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # --- Calories Burned ---
        met_values = {"Running": 9.8, "Walking": 3.8, "Cycling": 7.5, "Yoga": 3.0}
        met = met_values.get(exercise_type, 5)
        calories_burned = (met * weight * total_minutes) / 60

        with colB:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">🔥 Calories Burned</div>
                <div class="result-value">{calories_burned:.2f} kcal</div>
            </div>
            """, unsafe_allow_html=True)

        # --- Progress Bar ---
        st.markdown("### ⏱ Progress Towards Hourly Goal")
        goal = bmr / 24
        progress = min(int((calories_burned / goal) * 100), 100)
        progress_bar = st.progress(0)
        for p in range(progress + 1):
            time.sleep(0.01)
            progress_bar.progress(p)

        # --- Performance Feedback ---
        st.markdown("### 🌟 Performance Feedback")
        if calories_burned < 150:
            feedback = '<div class="highlight-box danger">🚨 Keep Going! Try a quick run 🏃, yoga 🧘, or a short HIIT 🔥 session to boost results.</div>'
        elif 150 <= calories_burned < 400:
            feedback = '<div class="highlight-box warning">⚡ Great job! You’re burning energy — push a bit harder with cardio 🚴 or weights 🏋️.</div>'
        else:
            feedback = '<div class="highlight-box success">🌟 Excellent! You’re smashing your goal 🔥 Keep pushing with HIIT or advanced training 💪.</div>'
        st.markdown(feedback, unsafe_allow_html=True)

    # --- Suggestions by BMI (always show) ---
    st.markdown("### 💡 Suggested Exercises for You")
    bmi_suggestions = {
        "underweight": [
            ("Beginner Strength Training 🏋", "https://www.youtube.com/watch?v=U0bhE67HuDY"),
            ("Yoga for Weight Gain 🧘", "https://www.youtube.com/watch?v=7kgZnJqzNaU"),
            ("Resistance Bands 💪", "https://www.youtube.com/watch?v=3G4KpZJYySM")
        ],
        "normal": [
            ("Running for Fitness 🏃", "https://www.youtube.com/watch?v=2O7K-8G2nwU"),
            ("Strength Training 💪", "https://www.youtube.com/watch?v=U0bhE67HuDY"),
            ("Yoga Flexibility 🧘", "https://www.youtube.com/watch?v=v7AYKMP6rOE")
        ],
        "overweight": [
            ("Low-Impact Cardio 🔥", "https://www.youtube.com/watch?v=iNW4lCU693Q"),
            ("Beginner HIIT", "https://www.youtube.com/watch?v=8uVOAhhpEbI"),
            ("Standing Cardio", "https://www.youtube.com/watch?v=WjH-NQDeQ3o")
        ],
        "obese": [
            ("Chair Yoga 🪑", "https://www.youtube.com/watch?v=1DYH5ud3zHo"),
            ("Chair Stretching", "https://www.youtube.com/watch?v=ct9kgaaJW0c"),
            ("Gentle Seated Workout", "https://www.youtube.com/watch?v=WkYz1g47Hj0")
        ]
    }

    if bmi < 18.5:
        category = "underweight"
    elif 18.5 <= bmi < 25:
        category = "normal"
    elif 25 <= bmi < 30:
        category = "overweight"
    else:
        category = "obese"

    videos = random.sample(bmi_suggestions[category], k=min(3, len(bmi_suggestions[category])))

    for title, link in videos:
        st.markdown(f"**{title}** 👉 [Watch Video]({link})")

    st.markdown("---")
    st.markdown("🌟 *Stay Active | Eat Healthy | Track Daily!* 🌟")
