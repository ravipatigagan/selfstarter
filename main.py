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
    prompt = f"""
You are SelfStarter — a warm, human-like AI that feels like a best friend or supportive parent.

{name} is feeling {mood} today. They said:
"{goal}"

They have {time} to spare.

Give them:
- A short, doable plan (2-5 steps max)
- Only what’s most relevant
- Use simple, calming language
- End with a single line of real encouragement (e.g., “You’ve got this. One small step is enough.”)

Avoid sounding robotic or like a blog article. Just be real, kind, and practical.
"""

    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=20)

        # Check if response is valid JSON
        if response.status_code != 200:
            return f"⚠️ Error: Received status code {response.status_code}. Try again later."

        output = response.json()

        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        else:
            return "⚠️ Unexpected response format. The model may be warming up. Try again in a few seconds."

    except requests.exceptions.RequestException as e:
        return f"🚫 Network error: {e}"
    except Exception as e:
        return f"💥 Unexpected error: {e}"


if st.button("✨ Generate My Plan"):
    if name and goal:
        with st.spinner("Thinking with you..."):
            plan = generate_plan(name, goal, mood, time)
            st.markdown(f"### Here's your gentle push, {name}:")
            st.write(plan)
    else:
        st.error("Please enter your name and your current struggle.")
