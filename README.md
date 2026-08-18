AI Resume to Job Description Matcher 🎯📄
An intelligent, AI-powered web application that automatically compares resumes against job descriptions (JD) using Natural Language Processing (NLP) and Sentence-BERT (SBERT). The system provides an instant semantic match score, highlights skill gaps, suggests actionable resume improvements, and recommends relevant certification courses to boost job readiness.
---
🌟 Key Features
Semantic Document Matching: Uses Sentence-BERT (SBERT) and Cosine Similarity to understand the contextual meaning of resumes and job descriptions beyond mere keyword matching.
Multi-Format Document Parsing: Seamlessly extract and process text from PDF and DOCX files using `pdfplumber`, `PyPDF2`, and `python-docx`.
Skill Gap & Keyword Analysis:
🟢 Matched Skills: Identifies existing skills aligned with the job description.
🔴 Missing Skills: Highlights critical requirements missing from the resume.
🟣 Additional Skills: Lists extra candidate strengths.
Personalized Recommendations: Generates actionable suggestions to tailor resume bullet points and recommends online certification courses for missing skills.
User Authentication & History Tracker: Secure registration and login system with a local SQLite database to track, revisit, and manage past analysis records.
Interactive UI/Dashboard: Built with Streamlit for a clean, intuitive, and modern user experience.
---
📊 System Architecture & Workflow
```plaintext
+-------------------------------------------------------------+
|                     Streamlit Frontend                      |
|       (Login / Register / Upload Resume & Enter JD)         |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Text Extraction & Parsing                  |
|               (pdfplumber, PyPDF2, python-docx)             |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   Text Preprocessing Module                 |
|   (Lowercase, Special Character Removal, Normalization)     |
+-------------------------------------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|  Semantic AI Matching |             |    Skill Extraction   |
|   (SBERT Embeddings + |             |  (Regex & Master DB   |
|   Cosine Similarity)  |             |      Comparison)      |
+-----------------------+             +-----------------------+
            |                                     |
            +------------------+------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     Recommendation Engine                   |
|        (Actionable Insights + Course Recommendations)       |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|               SQLite Database (History Storage)             |
|              & Interactive Results Dashboard                |
+-------------------------------------------------------------+
```
---
📈 Performance & Evaluation
The system was evaluated against standard test benchmarks for semantic similarity and candidate shortlisting:
Metric	Score / Result	Details
Accuracy	86.7%	Reliable overall matching performance
Recall	100.0%	Identified all qualified candidates without false negatives
Precision	77.8%	High match relevance
Average Latency	459 ms / query	Real-time response speed
---
🛠️ Tech Stack & Libraries
Language: Python 3.11+
Frontend / UI: Streamlit
NLP & Deep Learning: Sentence-Transformers (`all-MiniLM-L6-v2`), Hugging Face Transformers, Scikit-learn
Document Parsing: `pdfplumber`, `PyPDF2`, `python-docx`
Database: SQLite
Data Manipulation: `pandas`, `numpy`
---
📂 Project Structure
```plaintext
AI_resume_jd_matcher/
├── data/
│   ├── raw_jds/                 # Raw job description inputs
│   ├── raw_resumes/             # Uploaded resume files (PDF/DOCX)
│   ├── Resumes/                 # Processed documents
│   ├── app_database.db          # SQLite database (Users & Analysis History)
│   └── skills_list.txt          # Master technical skills dictionary
│
├── src/
│   ├── __init__.py              # Package initializer
│   ├── auth.py                  # User authentication & password hashing
│   ├── courses_manager.py       # Course & certification recommender
│   ├── database.py              # SQLite CRUD operations
│   ├── matcher.py               # SBERT embeddings & Cosine similarity logic
│   ├── parser.py                # PDF & DOCX text extraction
│   ├── preprocess.py            # Text cleaning & normalization
│   ├── skill_extractor.py       # Skill gap identification
│   └── utils.py                 # Common utility functions
│
├── views/
│   ├── __init__.py              # Views initializer
│   ├── auth_view.py             # Login & Registration UI
│   ├── history_view.py          # Past analysis history UI
│   └── matcher_view.py          # Main dashboard & analysis UI
│
├── .gitignore
├── app.py                       # Main Streamlit application entry point
├── README.md                    # Project documentation
└── requirements.txt             # Python project dependencies
```
---
🚀 Getting Started
Follow these steps to set up and run the project locally.
1. Prerequisites
Python `3.10` or `3.11` installed on your machine.
Git installed.
2. Clone the Repository
```bash
git clone https://github.com/Madhaviyadav01/ai-resume-jd-matcher.git
cd ai-resume-jd-matcher
```
3. Create and Activate a Virtual Environment
On Windows:
```bash
  python -m venv venv
  venv\Scripts\activate
  ```
On macOS / Linux:
```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
5. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.
---
💡 How to Use
Register / Login: Create a new account or log in with your existing credentials.
Upload Resume: Select and upload your resume in `.pdf` or `.docx` format.
Input Job Description: Either upload a job description file or paste the job text directly.
Analyze: Click "Analyze Match" to trigger the AI pipeline.
Review Insights:
View your overall Semantic Match Percentage.
Check Matched vs. Missing Skills.
Read Actionable Tips to tailor your resume.
Explore Recommended Courses to bridge any skill gaps.
Check History: Go to the History tab in the sidebar to review past analyses anytime.

---

🔮 Future Enhancements
Recruiter Dashboard: Enable HR teams to upload a single job description and rank batch/multiple candidate resumes simultaneously.
Layout-Aware OCR Parsing: Improved text extraction for multi-column and heavily styled resumes.
LLM Integration: Provide generative AI feedback, personalized bullet point rewriting, and interview preparation questions.
Cloud Deployment: Containerization with Docker and deployment to AWS / GCP.
---
