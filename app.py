import streamlit as st
import requests
import json

# API endpoints
GET_ADVICE_URL = "https://y8us2d1cd4.execute-api.us-east-1.amazonaws.com/default/digitalExperts_getAdvice"
CHOOSE_RECOMMENDATION_URL = "https://y8us2d1cd4.execute-api.us-east-1.amazonaws.com/default/digitalExpert_chooseRecommendation"

st.title("💬 Financial Advisor Assistant")

client_id = st.text_input("Client ID")
bucket = st.text_input("S3 Bucket Name")
key = st.text_input("S3 Key (CSV Path)")
current_message = st.text_area("Current Client Message")

if st.button("Get Advice"):
    with st.spinner("Analyzing conversation..."):
        payload = {
            "client_id": client_id,
            "bucket": bucket,
            "key": key,
            "current_message": current_message
        }
        response = requests.post(GET_ADVICE_URL, json=payload)
        result = response.json()

    if response.status_code == 200:
        st.success("Analysis complete!")
        st.json(result)

        st.session_state["analysis_result"] = result
    else:
        st.error(f"Error: {result.get('error', 'Unknown error')}")

# Allow user to choose one of the recommendations and submit
if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.subheader("Top 3 Recommendations")
    chosen_index = st.radio("Choose a recommendation", range(3), format_func=lambda i: result["recommendations"][i])

    if st.button("Submit Selected Recommendation"):
        submit_payload = {
            "client_id": client_id,
            "bucket": bucket,
            "output_key": "processed_client_data.csv",  # or customize
            "sentiment_score": result.get("sentiment_score"),
            "sentiment_label": result.get("sentiment_label"),
            "client_tone": result.get("client_tone"),
            "client_intent": result.get("client_intent"),
            "client_life_stage": result.get("client_life_stage"),
            "recommendations": result.get("recommendations"),
            "chosen_index": chosen_index,
            "current_message": current_message
        }

        submit_response = requests.post(CHOOSE_RECOMMENDATION_URL, json=submit_payload)
        submit_result = submit_response.json()

        if submit_response.status_code == 200:
            st.success(submit_result["message"])
        else:
            st.error(f"Error: {submit_result.get('error', 'Unknown error')}")
