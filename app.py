{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "58d3afbf-6bec-4953-acf1-295ded1fb3a1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import requests\n",
    "import json\n",
    "\n",
    "# Update this with your deployed API Gateway URL\n",
    "LAMBDA_API_URL = \"https://13whbcctze.execute-api.us-east-1.amazonaws.com/\"\n",
    "\n",
    "st.set_page_config(page_title=\"Client Conversation Analyzer\", layout=\"centered\")\n",
    "\n",
    "st.title(\"🧠 Financial Assistant: Client Conversation Analyzer\")\n",
    "\n",
    "with st.form(\"transcript_form\"):\n",
    "    transcript = st.text_area(\"Paste the client-advisor transcript below:\", height=200)\n",
    "    submitted = st.form_submit_button(\"Analyze Transcript\")\n",
    "\n",
    "if submitted and transcript:\n",
    "    with st.spinner(\"Analyzing...\"):\n",
    "        try:\n",
    "            response = requests.post(LAMBDA_API_URL, json={\"transcript\": transcript})\n",
    "            if response.status_code == 200:\n",
    "                result = response.json()\n",
    "                st.success(\"✅ Analysis Complete\")\n",
    "                st.subheader(\"🗣️ Client Tone\")\n",
    "                st.write(result.get(\"client_tone\", \"N/A\"))\n",
    "\n",
    "                st.subheader(\"🎯 Client Intent\")\n",
    "                st.write(result.get(\"client_intent\", \"N/A\"))\n",
    "\n",
    "                st.subheader(\"📈 Client Life Stage\")\n",
    "                st.write(result.get(\"client_life_stage\", \"N/A\"))\n",
    "\n",
    "                st.subheader(\"💡 Advisor Recommendations\")\n",
    "                for idx, rec in enumerate(result.get(\"advisor_recommendations\", []), 1):\n",
    "                    st.markdown(f\"- {rec}\")\n",
    "            else:\n",
    "                st.error(f\"❌ Error: {response.status_code}\")\n",
    "                st.json(response.json())\n",
    "\n",
    "        except Exception as e:\n",
    "            st.error(f\"⚠️ Exception occurred: {str(e)}\")\n",
    "else:\n",
    "    st.info(\"Enter a transcript and click 'Analyze Transcript'.\")\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
