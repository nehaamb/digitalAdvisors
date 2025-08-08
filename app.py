import streamlit as st
import boto3
import json

# AWS Lambda client
lambda_client = boto3.client("lambda", region_name="us-east-1")  # Change to your region

st.set_page_config(page_title="Advisor Assistant", page_icon="💬", layout="centered")
st.title("💬 Advisor Client Conversation Assistant")

# Input section
st.header("Step 1: Provide Client Conversation Details")
client_id = st.text_input("Client ID")
bucket = st.text_input("S3 Bucket Name")
key = st.text_input("Input CSV Key in S3 (e.g., client_history.csv)")
current_message = st.text_area("Current Client Message")

if st.button("Generate Recommendations"):
    if not (client_id and bucket and key and current_message):
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Processing conversation and generating recommendations..."):
            payload = {
                "client_id": client_id,
                "bucket": bucket,
                "key": key,
                "current_message": current_message
            }
            # Invoke Lambda #1
            response = lambda_client.invoke(
                FunctionName="process_client_data_lambda",  # Replace with your Lambda #1 name
                InvocationType="RequestResponse",
                Payload=json.dumps(payload)
            )

            result = json.loads(response['Payload'].read())

            if result.get("statusCode") != 200:
                st.error(f"Error: {result.get('body')}")
            else:
                body = json.loads(result["body"])
                summary = body.get("summary", {})
                st.success("Recommendations generated successfully!")
                st.write("### Conversation Insights")
                st.json(summary)

                top_recommendations = summary.get("top_3_advisor_recommendations", [])
                if isinstance(top_recommendations, str):
                    top_recommendations = [r.strip() for r in top_recommendations.split(",")]

                if top_recommendations:
                    st.session_state["recommendations"] = top_recommendations
                    st.session_state["client_id"] = client_id
                    st.session_state["bucket"] = bucket
                    st.session_state["key"] = key
                    st.session_state["current_message"] = current_message
                else:
                    st.error("No recommendations returned.")

# Step 2: Choose Recommendation
if "recommendations" in st.session_state:
    st.header("Step 2: Choose a Recommendation")
    choice = st.selectbox(
        "Select the best recommendation to proceed with:",
        st.session_state["recommendations"]
    )

    if st.button("Save Selected Recommendation"):
        with st.spinner("Saving selected recommendation..."):
            payload = {
                "client_id": st.session_state["client_id"],
                "bucket": st.session_state["bucket"],
                "key": st.session_state["key"],
                "current_message": st.session_state["current_message"],
                "selected_recommendation": choice
            }
            # Invoke Lambda #2
            response = lambda_client.invoke(
                FunctionName="save_selected_recommendation_lambda",  # Replace with your Lambda #2 name
                InvocationType="RequestResponse",
                Payload=json.dumps(payload)
            )

            result = json.loads(response['Payload'].read())
            if result.get("statusCode") != 200:
                st.error(f"Error: {result.get('body')}")
            else:
                st.success("Selected recommendation saved successfully!")
                st.write(result["body"])
