import os
import streamlit as st
from google import genai
import pandas as pd


# ===================== CONFIG =====================

# Try to read key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# If not set, fall back to hard-coded key (replace this with your key)
if not API_KEY:
    API_KEY = "AIzaSyCwXf98t4tz_xCbrruLCaoCbVVVOWyXww0"  # <<< PUT YOUR KEY HERE

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_reply(prompt: str) -> str:
    """
    Call Gemini 2.5 Flash model and return the text reply.
    If something goes wrong, return a readable error message.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        # response.text is a convenience property with concatenated text
        return response.text.strip()
    except Exception as e:
        return f"[AI error] {str(e)}"


# ===================== STREAMLIT UI =====================

st.set_page_config(page_title="User Feedback Portal", page_icon="⭐", layout="centered")

st.title("User Feedback Portal")
st.write("Please rate your experience and leave a short review.")

rating = st.selectbox("Rating (1 = worst, 5 = best)", [1, 2, 3, 4, 5], index=3)
review = st.text_area("Your review", height=120)

if "history" not in st.session_state:
    st.session_state["history"] = []  # store feedback inside the session only


if st.button("Submit"):
    if not review.strip():
        st.warning("Please write a review before submitting.")
    else:
        with st.spinner("Generating AI insights..."):
            # 1) Summary of the feedback
            summary_prompt = (
                f"Summarize this restaurant review in ONE short sentence, "
                f"without adding any new information.\n\n"
                f"Rating: {rating}/5\n"
                f"Review: \"{review}\""
            )
            ai_summary = generate_reply(summary_prompt)

            # 2) Recommended action for the business
            action_prompt = (
                "You are a restaurant operations consultant.\n"
                "Given the following rating and review, suggest ONE clear, "
                "practical action the restaurant should take to improve.\n\n"
                f"Rating: {rating}/5\n"
                f"Review: \"{review}\""
            )
            ai_action = generate_reply(action_prompt)

            # 3) Friendly reply back to the user
            reply_prompt = (
                f"The user gave a rating of {rating} out of 5 and wrote:\n"
                f"\"{review}\"\n\n"
                "Write a short, friendly acknowledgement message for the user. "
                "If they gave a low score (1 or 2), also add one suggestion to improve."
            )
            ai_reply = generate_reply(reply_prompt)

        # Save this feedback in session history (for UI)
        record = {
            "rating": rating,
            "review": review,
            "ai_summary": ai_summary,
            "ai_action": ai_action,
            "ai_reply": ai_reply,
        }
        st.session_state["history"].append(record)

        # Also save to CSV for admin dashboard
        df_new = pd.DataFrame([record])
        csv_path = "feedback_log.csv"

        if os.path.exists(csv_path):
            df_old = pd.read_csv(csv_path)
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(csv_path, index=False)

        st.success("Thank you for your feedback!")
        st.subheader("AI Reply:")
        st.write(ai_reply)




# Show previous feedback in this session
if st.session_state["history"]:
    st.markdown("---")
    st.subheader("Recent Feedback (this session)")
    for i, item in enumerate(reversed(st.session_state["history"]), start=1):
        st.write(f"**#{i} – Rating:** {item['rating']}")
        st.write(f"**Review:** {item['review']}")
        st.write(f"**AI Reply:** {item['ai_reply']}")
        st.write("---")
