import streamlit as st
import requests

# App Configuration
st.set_page_config(page_title="SelfStarter", page_icon="✨")
st.title("✨ SelfStarter")
st.subheader("Your gentle AI that gives you kind, doable next steps 💛")

# Input Fields
name = st.text_input("Your Name", placeholder="e.g., Priyansha")
goal = st.text_area("What's on your mind?", placeholder="e.g., I want to restart my project but feel stuck.")
mood = st.selectbox("How are you feeling?", ["", "Confident", "Clueless", "Low", "Anxious", "Motivated", "Burnt out", "Excited", "Tired", "Overwhelmed"])
time = st.selectbox("How much time do you have?", ["", "5 minutes", "15 minutes", "30 minutes", "45 minutes", "1 hour", "More than 1 hour"])

# Load OpenRouter API key from secrets
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

# Function to generate a plan using OpenRouter (Mistral model)
def generate_plan(name, goal, mood, time):
    prompt = f"""
{name} is feeling {mood.lower()} today. They said:
"{goal}"

They have {time} to spare.

Give them:
- A short, doable plan (2–5 steps)
- Use calming, encouraging tone
- End with a gentle motivating message (e.g., “You’ve got this.”)
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://selfstarter-2yurdydamc4qrdnpr4nl5k.streamlit.app/",  # ✅ Replace with your actual Replit URL
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a warm, emotionally intelligent AI assistant. Be kind, concise, and motivating."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code != 200:
            return f"⚠️ API Error {response.status_code}. Try again later."

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"💥 Something went wrong: {e}"

# Handle button click
if st.button("✨ Generate My Plan"):
    if all([name, goal, mood, time]):
        with st.spinner("Crafting your gentle plan..."):
            result = generate_plan(name, goal, mood, time)
            st.markdown("#### Your Personalized Plan 🪄")
            st.success(result.strip())
    else:
        st.warning("Please fill in all the fields before generating your plan.")
