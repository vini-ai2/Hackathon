import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(
    api_key=os.getenv("API_KEY"),
)

def generate_prompt(diagnosis, patient_info=None, follow_up=None):
    prompt = f"""
    Based on the diagnosis of {diagnosis}, recommend the optimal drug treatment options.
    Consider any known guidelines and common drugs for treating this condition.
    """
    if patient_info:
        prompt += f"\nPatient history includes: {patient_info}."
    if follow_up:
        prompt += f"\nAdditional user question or request: {follow_up}"
    prompt += "\nPlease provide a recommended drug and any important information on potential side effects or contraindications."

    return prompt

def get_drug_recommendation(diagnosis, patient_info=None, follow_up=None):
    prompt = generate_prompt(diagnosis, patient_info, follow_up)
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
        temperature=0.5
    )
    return response.choices[0].message.content

st.title("Medical Drug Recommendation Chatbot")
st.write("This chatbot provides drug recommendations based on a given diagnosis and patient history.")

if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = ""
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = ""
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'first_recommendation_given' not in st.session_state:
    st.session_state.first_recommendation_given = False

st.session_state.diagnosis = st.text_input("Enter diagnosis:", st.session_state.diagnosis)
st.session_state.patient_info = st.text_area("Enter additional patient information (optional):", st.session_state.patient_info)

if st.button("Get Drug Recommendation", key="get_recommendation"):
    if st.session_state.diagnosis:
        with st.spinner("Fetching recommendation..."):
            recommendation = get_drug_recommendation(st.session_state.diagnosis, st.session_state.patient_info)
        st.session_state.conversation.append({"role": "bot", "message": recommendation})
        st.session_state.first_recommendation_given = True
        st.write("**Recommendation:**")
        st.write(recommendation)
    else:
        st.warning("Please enter a diagnosis to get a recommendation.")

st.write("### Conversation History")
for message in st.session_state.conversation:
    role = "User" if message["role"] == "user" else "Chatbot"
    st.write(f"**{role}:** {message['message']}")

if st.session_state.first_recommendation_given:
    follow_up = st.text_input("Ask a follow-up question or request more details:", key="follow_up")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Continue Conversation", key="continue_conversation") and follow_up:
            st.session_state.conversation.append({"role": "user", "message": follow_up})
            
            with st.spinner("Fetching follow-up response..."):
                follow_up_response = get_drug_recommendation(st.session_state.diagnosis, st.session_state.patient_info, follow_up)
            st.session_state.conversation.append({"role": "bot", "message": follow_up_response})
            
            st.write("**Chatbot:**")
            st.write(follow_up_response)

    with col2:
        if st.button("Reset Conversation", key="reset_conversation"):
            st.session_state.diagnosis = ""
            st.session_state.patient_info = ""
            st.session_state.conversation = []
            st.session_state.first_recommendation_given = False
            st.write("Conversation reset. Please enter a new diagnosis to begin.")