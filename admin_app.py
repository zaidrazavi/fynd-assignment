import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
st.title("📊 Feedback Admin Dashboard")

csv_path = "feedback_log.csv"

if not os.path.exists(csv_path):
    st.warning("No feedback data found yet. Ask users to submit some reviews first.")
else:
    df = pd.read_csv(csv_path)

    # Make sure rating is numeric
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    st.subheader("Raw Feedback Data")
    st.caption("Includes user rating, review, AI summary, and AI recommended action.")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Feedback Entries", len(df))

    with col2:
        avg_rating = round(df["rating"].mean(), 2)
        st.metric("Average Rating", avg_rating)

    with col3:
        low_count = (df["rating"] <= 2).sum()
        st.metric("Low Ratings (1–2 stars)", int(low_count))

    st.markdown("---")
    st.subheader("Ratings Distribution")
    rating_counts = df["rating"].value_counts().sort_index()
    st.bar_chart(rating_counts)

    st.markdown("---")
    st.subheader("Action Items (from Low Ratings)")

    low_df = df[df["rating"] <= 2]
    if low_df.empty:
        st.info("No low ratings yet. 🎉")
    else:
        for _, row in low_df.iterrows():
            st.write(f"**Rating:** {row['rating']}")
            st.write(f"**Review:** {row['review']}")
            if "ai_summary" in row:
                st.write(f"**AI Summary:** {row['ai_summary']}")
            if "ai_action" in row:
                st.write(f"**AI Recommended Action:** {row['ai_action']}")
            st.write("---")

    st.subheader("Recent Feedback (Latest 10)")
    df_recent = df.sort_index(ascending=False).head(10)
    for _, row in df_recent.iterrows():
        st.write(f"**Rating:** {row['rating']}")
        st.write(f"**Review:** {row['review']}")
        if "ai_summary" in row:
            st.write(f"**AI Summary:** {row['ai_summary']}")
        if "ai_action" in row:
            st.write(f"**AI Recommended Action:** {row['ai_action']}")
        st.write(f"**AI Reply to User:** {row.get('ai_reply', '')}")
        st.write("---")
