import streamlit as st
import requests
import json

# API Gateway endpoint for your Lambda function
API_URL = "https://y8us2d1cd4.execute-api.us-east-1.amazonaws.com/default/digitalExperts_addAdviceWithPrev"

st.set_page_config(page_title="Client Conversation Analyzer", layout="centered")
st.title("💬 Client Conversation Analyzer")

st.markdown("This tool analyzes client conversations and generates smart advisor recommendations.")

# 🧾 Input fields
with st.form("conversation_form"):
    client_id = st.text_input("🔑 Client ID", placeholder="e.g., CL-000052")
    bucket = st.text_input("🪣 S3 Bucket Name", placeholder="e.g., clientadvisorcommunicationdata")
    key = st.text_input("📄 S3 Input Key", placeholder="e.g., communications.csv")
    output_key = st.text_input("💾 Output Key (for processed file)", value="output.csv", placeholder="e.g., output.csv")
    current_message = st.text_area("🗣️ Current Client Message (optional)", placeholder="e.g., I recently sold my business and want to plan for retirement and legacy.")

    submitted = st.form_submit_button("Analyze Conversation")

# 🚀 Trigger analysis
if submitted:
    if not (client_id and bucket and key and output_key):
        st.warning("⚠️ Please fill in all required fields.")
    else:
        payload = {
            "client_id": client_id,
            "bucket": bucket,
            "key": key,
            "output_key": output_key,
            "current_message": current_message.strip()
        }

        try:
            response = requests.post(API_URL, json=payload)

            # Debug output
            st.write("📨 Request Payload:")
            st.code(json.dumps(payload, indent=2))

            st.write("📥 Response Status Code:", response.status_code)

            if response.status_code == 200:
                result = response.json()
                st.success("✅ Analysis complete!")
                st.subheader("🔎 Claude's Summary")
                st.json(result.get("summary", {}))

                st.info(result.get("message", "✅ Data processed successfully."))

            else:
                try:
                    error = response.json().get("error", "Unknown error")
                    st.error(f"❌ Error from Lambda: {error}")
                except Exception:
                    st.error(f"❌ Lambda returned a non-JSON error:\n\n{response.text}")

        except Exception as e:
            st.error(f"❗ Exception occurred while calling Lambda:\n\n{str(e)}")
