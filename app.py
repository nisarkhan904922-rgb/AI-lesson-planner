import os

import streamlit as st
from groq import Groq

MODEL = "openai/gpt-oss-20b"

st.set_page_config(page_title="40-Minute Lesson Planner", page_icon="📚", layout="centered")


def get_api_key():
    """Read the Groq key from Streamlit secrets, falling back to an env var."""
    try:
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        key = None
    return key or os.getenv("GROQ_API_KEY")


def build_prompt(class_name, subject, topic, level, notes):
    extra = f"\nStudent level: {level}." if level else ""
    if notes.strip():
        extra += f"\nSpecial notes from the teacher: {notes.strip()}"
    return f"""Create a complete, ready-to-teach 40-minute lesson plan.

Class/Grade: {class_name}
Subject: {subject}
Topic: {topic}{extra}

Use exactly this structure in Markdown:

# Lesson Plan: {topic}
**Class:** {class_name} | **Subject:** {subject} | **Duration:** 40 minutes

## 1. Learning Objectives
(2-3 specific, measurable objectives starting with "By the end of the lesson, students will be able to...")

## 2. Materials Needed
(short bullet list)

## 3. Lesson Timeline (40 minutes)
Give a table or list with time ranges (e.g. 0-5 min) whose durations add up to exactly 40 minutes.
Include: Warm-up/Hook, Direct Instruction, Guided Practice, Independent/Group Activity, Check for Understanding, Wrap-up.
For each segment describe what the teacher does and what students do.

## 4. Questions
- 3 recall questions
- 3 understanding/application questions
- 2 higher-order thinking questions
(Include short model answers.)

## 5. Homework
(A meaningful task that takes 15-20 minutes, with clear instructions.)

## 6. Differentiation Tips
(1-2 tips for struggling students and 1-2 for advanced students.)

Keep the language clear, practical and age-appropriate for the class."""


def generate_plan(api_key, prompt):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced teacher and curriculum designer who writes clear, practical lesson plans.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=4000,
        reasoning_effort="low",
    )
    return response.choices[0].message.content


st.title("📚 40-Minute Lesson Planner")
st.caption("Enter the details and get a full lesson plan in seconds.")

with st.form("lesson_form"):
    col1, col2 = st.columns(2)
    class_name = col1.text_input("Class / Grade", placeholder="e.g. Grade 8")
    subject = col2.text_input("Subject", placeholder="e.g. Science")
    topic = st.text_input("Topic", placeholder="e.g. Photosynthesis")
    level = st.selectbox(
        "Student level (optional)", ["", "Beginner", "Intermediate", "Advanced", "Mixed ability"]
    )
    notes = st.text_area("Special notes (optional)", placeholder="e.g. No projector, class of 45 students")
    submitted = st.form_submit_button("Generate Lesson Plan", type="primary")

if submitted:
    api_key = get_api_key()
    if not api_key:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit secrets or as an environment variable.")
    elif not (class_name.strip() and subject.strip() and topic.strip()):
        st.warning("Please fill in Class, Subject and Topic.")
    else:
        with st.spinner("Creating your lesson plan..."):
            try:
                plan = generate_plan(
                    api_key,
                    build_prompt(class_name.strip(), subject.strip(), topic.strip(), level, notes),
                )
                st.session_state["plan"] = plan
                st.session_state["filename"] = f"lesson_plan_{topic.strip().replace(' ', '_')}.md"
            except Exception as e:
                st.error(f"Something went wrong while contacting Groq: {e}")

if "plan" in st.session_state:
    st.divider()
    st.markdown(st.session_state["plan"])
    st.download_button(
        "⬇️ Download as Markdown",
        data=st.session_state["plan"],
        file_name=st.session_state["filename"],
        mime="text/markdown",
    )
