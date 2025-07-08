import streamlit as st
import requests
import os

st.set_page_config(page_title="SelfStarter")
st.title("🧠 SelfStarter – Your AI for Actionable Clarity")

# Input Fields
name = st.text_input("What’s your name?")
goal = st.text_area("What’s something you’re stuck or confused about?")
mood = st.radio("How are you feeling today?",
                ["Confused", "Low Energy", "Anxious", "Neutral", "Focused"])
time = st.selectbox("How much time do you have today?",
                    ["15 min", "30 min", "1 hour", "2+ hours"])

# Load API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


# Function to call Hugging Face Model
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

    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    output = response.json()
    print("DEBUG: ", output)

    try:
        return output[0]["generated_text"]
    except:
        return "Hmm... something went wrong or the model is loading. Try again in a few seconds!"


# Button Logic
if st.button("✨ Generate My Plan"):
    if name and goal:
        with st.spinner("Thinking with you..."):
            plan = generate_plan(name, goal, mood, time)
            st.markdown(f"### Here's your gentle push, {name}:")
            st.write(plan)
    else:
        st.error("Please fill in your name and what's bothering you.")
