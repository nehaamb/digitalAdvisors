import streamlit as st
import requests
import json
from datetime import date

# API Gateway endpoints
GET_ADVICE_URL = "https://y8us2d1cd4.execute-api.us-east-1.amazonaws.com/default/digitalExperts_getAdvice"
CHOOSE_RECOMMENDATION_URL = "https://y8us2d1cd4.execute-api.us-east-1.amazonaws.com/default/digitalExpert_chooseRecommendation"

st.set_page_config(page_title="Client Advisor Assistant", layout="centered")
st.title("💬 Client Advisor Assistant")

st.markdown("Use this tool to analyze a client's conversation history and generate tailored advisor recommendations.")

# === Input Form ===
with st.form("advisor_form"):
    client_id = st.text_input("🔑 Client ID", placeholder="e.g., CL-000052")
    bucket = st.text_input("🪣 S3 Bucket Name", placeholder="e.g., clientadvisorcommunicationdata")
    key = st.text_input("📄 S3 Input Key", placeholder="e.g., communications.csv")
    current_message = st.text_area("🗣️ Current Client Message", placeholder="e.g., I want to start planning for my child’s education.")
    
    # New fields
    priority_level = st.selectbox("🔥 Priority Level", ["Low", "Medium", "High"])
    follow_up_date = st.date_input("📅 Follow-Up Date", min_value=date.today())

    submitted = st.form_submit_button("📊 Analyze Conversation")

# === Process Analysis ===
if submitted:
    if not (client_id and bucket and key):
        st.warning("⚠️ Please fill in all required fields (Client ID, Bucket, Key).")
    else:
        request_payload = {
            "client_id": client_id,
            "bucket": bucket,
            "key": key,
            "current_message": current_message.strip()
        }

        try:
            st.info("📡 Sending request to analyze conversation...")
            response = requests.post(GET_ADVICE_URL, json=request_payload)
            st.write("📨 Request Payload:")
            st.code(json.dumps(request_payload, indent=2))

            if response.status_code == 200:
                result = response.json()

                st.success("✅ Conversation analysis complete!")
                st.subheader("🧠 Claude's Summary")
                st.json({
                    "Tone": result.get("client_tone"),
                    "Intent": result.get("client_intent"),
                    "Life Stage": result.get("client_life_stage"),
                    "Recommendations": result.get("recommendations")
                })

                st.session_state["analysis"] = result
                st.session_state["current_message"] = current_message
                st.session_state["client_id"] = client_id
                st.session_state["bucket"] = bucket
                st.session_state["priority_level"] = priority_level
                st.session_state["follow_up_date"] = follow_up_date.isoformat()

            else:
                error_msg = response.json().get("error", "Unknown error")
                st.error(f"❌ Lambda Error: {error_msg}")

        except Exception as e:
            st.error(f"❗ Exception occurred: {str(e)}")

# === Recommendation Selection ===
if "analysis" in st.session_state:
    st.divider()
    st.subheader("✅ Select a Recommendation to Save")

    analysis = st.session_state["analysis"]
    options = analysis.get("recommendations", [])
    chosen_index = st.radio("💡 Choose the recommendation to save:", range(len(options)), format_func=lambda i: options[i])

    if st.button("💾 Submit Selected Recommendation"):
        try:
            submit_payload = {
                "client_id": st.session_state["client_id"],
                "bucket": st.session_state["bucket"],
                "output_key": "processed_client_data.csv",
                "sentiment_score": analysis.get("sentiment_score"),
                "sentiment_label": analysis.get("sentiment_label"),
                "client_tone": analysis.get("client_tone"),
                "client_intent": analysis.get("client_intent"),
                "client_life_stage": analysis.get("client_life_stage"),
                "recommendations": analysis.get("recommendations"),
                "chosen_index": chosen_index,
                "current_message": st.session_state["current_message"],
                "priority_level": st.session_state["priority_level"],
                "follow_up_date": st.session_state["follow_up_date"]
            }

            st.write("📤 Submit Payload:")
            st.code(json.dumps(submit_payload, indent=2))

            submit_response = requests.post(CHOOSE_RECOMMENDATION_URL, json=submit_payload)

            if submit_response.status_code == 200:
                result = submit_response.json()
                st.success(result.get("message", "✅ Recommendation saved."))
            else:
                st.error(f"❌ Failed to save recommendation: {submit_response.text}")

        except Exception as e:
            st.error(f"❗ Exception occurred during submission: {str(e)}")
