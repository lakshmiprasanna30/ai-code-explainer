import streamlit as st
from groq import Groq

# from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"))


st.set_page_config(page_title="AI Code Explainer", page_icon=" ")

st.title("AI Code Explainer Tool")
st.write("Paste your code and get explanation instantly")


code_input = st.text_area("Paste your code here:")


mode = st.selectbox("Select Mode", ["Beginner", "Advanced"])


language = st.selectbox(
    "Select Programming Language",
    ["Auto Detect", "Python", "Java", "JavaScript", "C++"]
)


bug_check = st.checkbox("Detect Bugs & Suggest Fixes")


def get_prompt(code, mode, bug_check, language):

    lang_text = "" if language == "Auto Detect" else f"The code is written in {language}."

    if mode == "Beginner":
        prompt = f"""
{lang_text}
Explain this code in very simple terms step by step.
Use easy language for beginners.

Code:
{code}
"""
    else:
        prompt = f"""
{lang_text}
Explain this code in detail with technical concepts.

Code:
{code}
"""

    if bug_check:
        prompt += "\nAlso find any bugs and suggest fixes."

    return prompt



if st.button("Explain Code"):

    if code_input.strip() == "":
        st.warning("Please paste some code first!")
    else:
        prompt = get_prompt(code_input, mode, bug_check, language)

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            explanation = response.choices[0].message.content

            st.subheader("Explanation")
            st.write(explanation)

        except Exception as e:
            st.error(f"Error: {e}")