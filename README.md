# 🎯 AI Resume to Job Description Matcher

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/Model-Sentence--BERT-yellow?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

An intelligent, AI-powered recruitment intelligence tool that evaluates candidate compatibility against Job Descriptions (JDs) using **Natural Language Processing (NLP)** and **Sentence-BERT (SBERT)**. Moving beyond rigid keyword lookups, it measures deep semantic contextual alignment, identifies critical skill gaps, and recommends targeted certifications to optimize applicant success.

---

## 📌 Table of Contents
- [🌟 Key Features](#-key-features)
- [📊 System Architecture & workflow](#-system-architecture-&-workflow)
- [📈 Performance & Evaluation](#-performance-&-evaluation)
- [🛠️ Tech Stack & Dependencies](#️-tech-stack-&-dependencies)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [💡 How to Use](#-how-to-use)
- [🔮 Future Enhanements](#-future-enhancements)
- [📚 References](#-references)

---

## 🌟 Key Features

* **🧠 Context-Aware Semantic Matching:** Employs `all-MiniLM-L6-v2` dense vector embeddings and Cosine Similarity to capture the true semantic intent of qualifications and job requirements.
* **📑 Robust Multi-Format Ingestion:** Extracts structured text cleanly from `.pdf` and `.docx` files using `pdfplumber`, `PyPDF2`, and `python-docx`.
* **🔍 Granular Skill Gap Breakdown:**
  * 🟢 **Matched Skills:** Overlapping competencies identified in both documents.
  * 🔴 **Missing Skills:** Critical requirements missing from the resume.
  * 🟣 **Additional Skills:** Candidate edge-skills outside the direct scope.
* **💡 Actionable Insights & Course Engine:** Delivers dynamic suggestions to refine resume bullet points and maps missing skills to direct certification courses.
* **🔐 Local Persistence & Session Management:** Built-in user authentication and an SQLite database to securely store, review, and delete historical match reports.

---

## 📊 System Architecture & Workflow
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

## 📈 Performance & Evaluation

The system was evaluated against real-world test pairs of resumes and job descriptions to measure semantic matching accuracy, candidate shortlisting reliability, and real-time processing efficiency[cite: 2]:

| Metric | Score / Benchmark | Performance Analysis |
| :--- | :---: | :--- |
| **Accuracy** | **86.7%** | High overall reliability in matching candidate profiles to target job requirements[cite: 2]. |
| **Recall** | **100.0%** | Identified all qualified candidates with zero false negatives[cite: 2]. |
| **Precision** | **77.8%** | High match relevance, with minor false positives caused by closely related domain terms[cite: 2]. |
| **Average Latency** | **459 ms / query** | Sub-second inference speed suitable for real-time interactive usage[cite: 2]. |

### 🔍 Key Evaluation Highlights
* **Zero False Negatives:** The 100% recall ensures no suitable candidate is erroneously rejected during screening[cite: 2].
* **Low-Latency Inference:** Generates SBERT vector embeddings and computes Cosine Similarity in under half a second on standard CPU hardware[cite: 2].
* **Reliable Classification:** Successfully separated suitable candidates from unqualified profiles across multi-domain test inputs[cite: 2].

---

## 🛠️ Tech Stack & Dependencies

Built entirely using an open-source, lightweight Python ecosystem[cite: 2]:

* **🐍 Core & Runtime**
  * `Python 3.11+` – Primary backend programming language[cite: 2]
  * `VS Code` & `Git / GitHub` – Development environment and version control[cite: 2]

* **🖥️ User Interface**
  * `Streamlit` – Interactive frontend web dashboard, routing, and session state management[cite: 2]

* **🧠 AI, NLP & Semantic Matching**
  * `Sentence-Transformers (SBERT)` – Transformer embeddings using the `all-MiniLM-L6-v2` model[cite: 2]
  * `Hugging Face Transformers` – Deep learning model integration[cite: 2]
  * `Scikit-Learn` – Cosine similarity calculation and classification evaluation metrics[cite: 2]

* **📄 Document Ingestion & Parsing**
  * `pdfplumber` & `PyPDF2` – Text and layout extraction from PDF resumes[cite: 2]
  * `python-docx` – Text extraction from Microsoft Word documents[cite: 2]

* **💾 Data Management & Persistence**
  * `SQLite3` – Embedded local database for user authentication and match history logging[cite: 2]
  * `Pandas` & `NumPy` – Structured data manipulation, array operations, and metrics processing[cite: 2]

## 📂 Project Structure
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

## 🚀 Getting Started
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

## 💡 How to Use

Follow this step-by-step workflow to analyze and optimize your resume:

1. **🔐 Authentication & Session Setup**
   * Create a new profile on the registration screen or log in with your existing credentials[cite: 2].
   * All subsequent evaluations will be automatically associated with your user session[cite: 2].

2. **📄 Document Ingestion**
   * **Resume:** Upload your resume document directly in `.pdf` or `.docx` format[cite: 2].
   * **Job Description:** Paste the raw target job description into the text area or upload it as a file[cite: 2].

3. **⚡ Trigger AI Semantic Analysis**
   * Click **Analyze Match** to run the processing pipeline[cite: 2].
   * The system extracts text, normalizes content, encodes SBERT embeddings, and matches domain skills[cite: 2].

4. **📊 Comprehensive Insights & Results Dashboard**
   * **Semantic Match Score:** Check the overall contextual compatibility percentage generated via Cosine Similarity[cite: 2].
   * **Skill Gap Categorization:**
     * 🟢 **Matched Skills:** Identified competencies present in both your resume and the job requirements[cite: 2].
     * 🔴 **Missing Skills:** Critical requirements omitted from your resume[cite: 2].
     * 🟣 **Additional Skills:** Candidate edge-strengths outside the core job description scope[cite: 2].
   * **Actionable Resume Improvements:** Read dynamic, tailored suggestions to optimize your resume bullet points[cite: 2].
   * **Course Recommendations:** Browse curated online certification courses mapped directly to your missing skills[cite: 2].

5. **🕒 Analysis History Management**
   * Switch to the **History** tab via the sidebar navigation[cite: 2].
   * Review past similarity scores, expand detailed breakdowns, or delete outdated analysis logs from your local SQLite database[cite: 2].

---

## 🔮 Future Enhancements

Key features and architectural improvements planned for future releases:

* **👥 Recruiter Mode (Dual-User Platform):**
  * Introduce an HR/Recruiter dashboard allowing batch uploads to rank and screen multiple candidates simultaneously against a single job description[cite: 2].

* **🔍 Layout-Aware Vision & OCR Document Parsing:**
  * Implement advanced layout parsers to preserve reading order in complex multi-column resumes, tables, graphics, and icon-based contact fields[cite: 2].

* **🤖 Large Language Model (LLM) & RAG Integration:**
  * Integrate LLMs to provide automated generative bullet-point rewrites, ATS formatting suggestions, and customized interview preparation questions[cite: 2].

* **🔄 Dynamic Continuous Learning Loop:**
  * Add a human-in-the-loop feedback mechanism to continuously expand the skill ontology and refine semantic scoring thresholds[cite: 2].

* **☁️ Cloud & API Containerization:**
  * Containerize the service with Docker and deploy scalable instances to cloud platforms (AWS / Azure / GCP) with RESTful API endpoints[cite: 2].

## 📚 References

1. **Sentence-BERT:** N. Reimers and I. Gurevych, *"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,"* Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP), Hong Kong, China, 2019, pp. 3982–3992[cite: 2].
2. **Streamlit:** Streamlit Inc., *"Streamlit Documentation,"* Available: [https://docs.streamlit.io/](https://docs.streamlit.io/)[cite: 2].
3. **Sentence-Transformers:** Hugging Face Inc., *"Sentence-Transformers Documentation,"* Available: [https://www.sbert.net/](https://www.sbert.net/)[cite: 2].
