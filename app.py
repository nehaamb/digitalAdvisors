import pandas as pd
from datetime import datetime

st.divider()
st.subheader("🔍 Filter Clients by Priority and Follow-up Date")

filter_bucket = st.text_input("📂 S3 Bucket (for filtering)", value=bucket if "bucket" in locals() else "")
filter_key = st.text_input("📄 Output CSV Key", value="processed_client_data.csv")
filter_btn = st.button("🔎 Load and Filter Client Data")

if filter_btn:
    if not (filter_bucket and filter_key):
        st.warning("⚠️ Please enter both bucket and output file key.")
    else:
        try:
            s3_url = f"https://{filter_bucket}.s3.amazonaws.com/{filter_key}"
            df = pd.read_csv(s3_url)

            if df.empty:
                st.info("ℹ️ No data found in the file.")
            else:
                # Normalize column names
                df.columns = df.columns.str.strip().str.lower()

                # Show available values to filter
                priority_options = sorted(df['priority_level'].dropna().unique())
                selected_priority = st.multiselect("📌 Select Priority Level(s):", options=priority_options, default=priority_options)

                # Date filtering
                df['follow_up_date'] = pd.to_datetime(df['follow_up_date'], errors='coerce')
                min_date = df['follow_up_date'].min()
                max_date = df['follow_up_date'].max()
                selected_date = st.date_input("📅 Show clients with follow-up on or before:", max_date.date() if pd.notnull(max_date) else datetime.today().date())

                # Apply filters
                filtered_df = df[
                    df['priority_level'].isin(selected_priority) &
                    (df['follow_up_date'].dt.date <= selected_date)
                ]

                st.success(f"✅ {len(filtered_df)} client(s) match your filters.")
                st.dataframe(filtered_df)

        except Exception as e:
            st.error(f"❌ Failed to load or process CSV: {str(e)}")
