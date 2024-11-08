import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
client = Groq(
    api_key=os.getenv("API_KEY"),
)

def generate_prompt(diagnosis, patient_info=None):
    prompt = f"""
    Based on the diagnosis of {diagnosis}, recommend the optimal drug treatment options.
    Consider any known guidelines and common drugs for treating this condition.
    """
    if patient_info:
        prompt += f"\nPatient history includes: {patient_info}."
    prompt += "\nPlease provide a recommended drug and any important information on potential side effects or contraindications."

    return prompt

def get_drug_recommendation(diagnosis, patient_info=None):
    prompt = generate_prompt(diagnosis, patient_info)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Be extremely brief and to-the-point. Only state the best drug that would be useful in curing the diagnosis"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content

st.title("Medical Drug Recommendation Chatbot")
st.write("This chatbot provides drug recommendations based on a given diagnosis and patient history.")

diagnosis = st.text_input("Enter diagnosis:")
patient_info = st.text_area("Enter additional patient information (optional):")

if st.button("Get Drug Recommendation"):
    if diagnosis:
        with st.spinner("Fetching recommendation..."):
            recommendation = get_drug_recommendation(diagnosis, patient_info)
        st.write("**Recommendation:**")
        st.write(recommendation)
    else:
        st.warning("Please enter a diagnosis to get a recommendation.")