import streamlit as st
import anthropic
import os
import pandas as pd

# Replace with your actual API key
api_key = "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"
client = anthropic.Client(api_key=api_key)

# Function to generate the prompt based on user input
def generate_prompt(diagnosis, patient_history=None):
     matching_drugs = df[df['Diagnosis'].str.contains(diagnosis, case=False, na=False)]
     drug_summary = ""
     for index, row in matching_drugs.iterrows():
         drug_summary += f" - {row['Drug Name']}: Dosage: {row['Dosage']}, Side Effects: {row['Side Effects']}, Contraindications: {row['Contraindications']}\n"
     prompt = f"""
     Based on the diagnosis of {diagnosis}, recommend the optimal drug treatment options.
     Consider any known guidelines and common drugs for treating this condition.
     """
     if patient_history:
         prompt += f"\nPatient history includes: {patient_history}."
     prompt += "\nPlease provide a recommended drug and any important information on potential side effects or contraindications."

    return prompt

# Function to get a drug recommendation from the Anthropic API
def get_drug_recommendation(diagnosis, patient_history=None):
    prompt = generate_prompt(diagnosis, patient_history)
    response = client.completions.create(
        model="claude-v1",
        prompt=prompt,
        max_tokens_to_sample=300,
        temperature=0.7
    )
    return response["completion"]

# Streamlit app setup
st.title("Medical Drug Recommendation Chatbot")
st.write("This chatbot provides drug recommendations based on a given diagnosis and patient history.")

# Text inputs for diagnosis and patient history
diagnosis = st.text_input("Enter diagnosis:")
patient_history = st.text_area("Enter patient history (optional):")

# Chatbot logic
if st.button("Get Drug Recommendation"):
    if diagnosis:
        with st.spinner("Fetching recommendation..."):
            recommendation = get_drug_recommendation(diagnosis, patient_history)
        st.write("**Recommendation:**")
        st.write(recommendation)
    else:
        st.warning("Please enter a diagnosis to get a recommendation.")
