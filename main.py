import streamlit as st
import requests
import os

st.set_page_config(page_title="SelfStarter")
st.title("🧠 SelfStarter – Your AI for Actionable Clarity")

name = st.text_input("What’s your name?")
goal = st.text_area("What’s something you’re stuck or confused about?")
mood = st.radio("How are you feeling today?", ["Confused", "Low Energy", "Anxious", "Neutral", "Focused"])
time = st.selectbox("How much time do you have today?", ["15 min", "30 min", "1 hour", "2+ hours"])

HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

def generate_plan(name, goal, mood, time):
    import requests

    prompt = f"""
You are SelfStarter — a warm, emotionally intelligent AI that feels like a best friend or supportive parent.

{name} is feeling {mood} today. They said:
"{goal}"

They have {time} to spare.

Give them:
- A short, doable plan (2–5 steps)
- Use calming, encouraging tone
- End with a gentle motivating message (e.g., “You’ve got this.”)
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-app-url.com",  # Use your Replit or localhost here
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code != 200:
        return f"⚠️ Error: Received status code {response.status_code}. Try again."

    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"💥 Parsing Error: {e}"



if st.button("✨ Generate My Plan"):
    if name and goal:
        with st.spinner("Thinking with you..."):
            plan = generate_plan(name, goal, mood, time)
            st.markdown(f"### Here's your gentle push, {name}:")
            st.write(plan)
    else:
        st.error("Please enter your name and your current struggle.")
