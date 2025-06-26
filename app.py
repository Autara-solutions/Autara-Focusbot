import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found. Please check your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_USES_PER_DAY = 5
if st.session_state.usage_count >= MAX_USES_PER_DAY:
    st.warning("You've reached your daily usage limit. Please come back tomorrow!")
    st.stop()

st.set_page_config(page_title="FocusBot by Autara", page_icon="⚡")
st.title("⚡ FocusBot by Autara")
st.subheader("Get clarity on what to do next — based on your time, energy, and goals.")

with st.form("focus_form"):
    energy = st.selectbox("Your energy level:", ["Low", "Medium", "High"])
    time = st.selectbox("How much time do you have?", ["15 minutes", "30 minutes", "1 hour or more"])
    tasks = st.text_area("What tasks are on your mind?")
    submitted = st.form_submit_button("Get My Focus Task")

if submitted:
    st.session_state.usage_count += 1
    with st.spinner("Thinking..."):
        system_prompt = f"""
You are FocusBot, a friendly AI that helps users decide what to focus on next. The user will tell you how much time and energy they have, and a few tasks they’re thinking about. Your job is to suggest a clear, encouraging next step—no fluff, just actionable and supportive.

User input:
Energy: {energy}
Time: {time}
Tasks: {tasks}

Respond in markdown with:
1. Best next step (bolded)
2. Why it’s a good fit
3. A motivation message
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)

st.markdown("---")
st.markdown("⚡ Powered by OpenAI | For inspiration only — not medical or professional advice.")
st.markdown("[☕ Buy Me a Coffee](https://www.buymeacoffee.com/DanDeppert)")