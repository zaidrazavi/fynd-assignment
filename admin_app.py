import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
st.title("📊 Feedback Admin Dashboard")

CSV_PATH = "feedback_log.csv"

if not os.path.exists(CSV_PATH):
    st.warning("No feedback data found yet. Ask users to submit some reviews first.")
else:
    
    df = pd.read_csv(CSV_PATH)

    
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    
    has_summary = "ai_summary" in df.columns
    has_action = "ai_action" in df.columns
    has_reply = "ai_reply" in df.columns

    
    st.subheader("Raw Feedback Data")
    st.caption("Includes user rating, review, AI summary, and AI recommended action (when available).")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Feedback Entries", len(df))

    with col2:
        avg_rating = round(df["rating"].mean(), 2) if "rating" in df.columns else 0
        st.metric("Average Rating", avg_rating)

    with col3:
        low_count = int((df["rating"] <= 2).sum()) if "rating" in df.columns else 0
        st.metric("Low Ratings (1–2 stars)", low_count)

    
    st.markdown("---")
    st.subheader("Ratings Distribution")

    if "rating" in df.columns:
        rating_counts = df["rating"].value_counts().sort_index()
        st.bar_chart(rating_counts)
    else:
        st.info("No rating column found in data.")

    
    st.markdown("---")
    st.subheader("Action Items (from Low Ratings)")

    if "rating" in df.columns:
        low_df = df[df["rating"] <= 2]
    else:
        low_df = pd.DataFrame()

    if low_df.empty:
        st.info("No low ratings yet. 🎉")
    else:
        for _, row in low_df.iterrows():
            st.write(f"**Rating:** {row.get('rating', '')}")
            st.write(f"**Review:** {row.get('review', '')}")

            if has_summary and not pd.isna(row.get("ai_summary", "")):
                st.write(f"**AI Summary:** {row.get('ai_summary', '')}")

            if has_action and not pd.isna(row.get("ai_action", "")):
                st.write(f"**AI Recommended Action:** {row.get('ai_action', '')}")

            st.write("---")

    
    st.subheader("Recent Feedback (Latest 10)")

    df_recent = df.copy()
    df_recent = df_recent.sort_index(ascending=False).head(10)

    for _, row in df_recent.iterrows():
        st.write(f"**Rating:** {row.get('rating', '')}")
        st.write(f"**Review:** {row.get('review', '')}")

        if has_summary and not pd.isna(row.get("ai_summary", "")):
            st.write(f"**AI Summary:** {row.get('ai_summary', '')}")

        if has_action and not pd.isna(row.get("ai_action", "")):
            st.write(f"**AI Recommended Action:** {row.get('ai_action', '')}")

        if has_reply and not pd.isna(row.get("ai_reply", "")):
            st.write(f"**AI Reply to User:** {row.get('ai_reply', '')}")

        st.write("---")
