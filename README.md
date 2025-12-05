# AI Engineering Internship Assignment – Fynd

This project implements a complete AI-powered feedback system with two fully deployed dashboards:
- A **Public User Feedback Portal**
- An **Internal Admin Dashboard**

Both dashboards are backed by a single shared data source and use Google Gemini for AI-powered responses, summaries, and business insights.

---

## 🔗 Live Applications

### User Dashboard (Public)
https://fynd-assignment-fwgwkcfa9fbhhckzx35wrs.streamlit.app/

### Admin Dashboard (Internal)
https://fynd-assignment-yrbtvmcjurvfkvssd6wfpi.streamlit.app/

### GitHub Repository
https://github.com/zaidrazavi/fynd-assignment/tree/main

---

## ✅ Features

### User Dashboard
Users can:
- Select a star rating (1–5)
- Submit a review
- Instantly receive an AI-generated response
- All submissions are stored in a shared CSV file

### Admin Dashboard
Admins can view:
- Live table of all feedback
- User ratings & reviews
- AI-generated summaries
- AI-recommended business actions

Additional analytics:
- Total feedback count
- Average rating
- Low-rating count
- Ratings distribution chart
- Recent feedback panel

---

##  AI Usage

Gemini API is used for:
- Generating user replies
- Summarizing reviews
- Suggesting recommended actions for business improvement

---

##  Technologies Used

- Python
- Streamlit
- Google Gemini (google-genai)
- Pandas
- NumPy
- Plotly
- CSV-based data storage

---

## 📂 Project Structure

Fynd_Assessment/
│
├── user_app.py
├── admin_app.py
├── fynd_task1_rating_prompting.ipynb
├── yelp.csv
├── feedback.csv
├── feedback_log.csv
├── Summary_Report.pdf
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚠️ Notes

Feedback is stored in a CSV file. Since Streamlit Cloud uses ephemeral storage, the file may reset on redeployment.
In a production system, this would be replaced with a database such as PostgreSQL or Firebase.

---

## 👤 Author

Mohd Zayed Kazim Shalil 
AI Engineering Intern Applicant – Fynd


