import streamlit as st
import requests
import os

st.set_page_config(page_title="SelfStarter", page_icon="✨")
st.title("✨ SelfStarter")
st.subheader("Your gentle AI that gives you kind, doable next steps 💛")

# Input fields
name = st.text_input("Your Name", placeholder="e.g., Priyansha")
goal = st.text_area("What's on your mind?", placeholder="e.g., I want to restart my project but feel stuck.")
mood = st.selectbox("How are you feeling?", ["", "Confident", "Clueless", "Low", "Anxious", "Motivated", "Burnt out", "Excited", "Tired", "Overwhelmed"])
time = st.selectbox("How much time do you have?", ["", "5 minutes", "15 minutes", "30 minutes", "45 minutes", "1 hour", "More than 1 hour"])

# Load OpenRouter API Key from secrets
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

# Handle Generate button with validation
if st.button("✨ Generate My Plan"):
    if all([name, goal, mood, time]):
        with st.spinner("Crafting your gentle plan..."):

            prompt = f"""
You are SelfStarter — a warm, emotionally intelligent AI that feels like a best friend or supportive parent.

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
                "HTTP-Referer": "https://your-replit-url.replit.app",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistral/mistral-7b-instruct",
                "messages": [{"role": "user", "content": prompt}]
            }

            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                if response.status_code != 200:
                    st.error(f"⚠️ API Error {response.status_code}. Try again later.")
                else:
                    plan = response.json()['choices'][0]['message']['content']
                    st.markdown("#### Your Personalized Plan 🪄")
                    st.success(plan.strip())

            except Exception as e:
                st.error(f"💥 Something went wrong: {e}")
    else:
        st.warning("Please fill in all the fields before generating your plan.")
