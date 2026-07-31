# AI Resume–JD Matcher

An AI-powered web application that analyzes how well a resume matches a given job description using **Natural Language Processing (NLP)** and **Sentence-BERT (SBERT)**. The application calculates a semantic match score, identifies skill gaps, provides personalized resume improvement suggestions, recommends relevant certification courses, and stores previous analysis history.

---

## 📌 Project Overview

This application uses **Natural Language Processing (NLP)** and **Machine Learning** to:
- Extract text from resumes (PDF / DOCX) and job descriptions.
- Preprocess and extract relevant skills from both documents.
- Generate **semantic embeddings** using **Sentence Transformers** (`all-MiniLM-L6-v2`).
- Compute **Cosine Similarity** to produce a match score.
- Display matched, missing, and extra skills.
- Rank multiple candidates by their match score.
- Provide **recommendations** to improve a resume for the given JD.

---

## 🗂️ Project Structure

```text
AI_resume_jd_matcher/
├── data/                       # Datasets, Master Skill Files, and Local DB
│   ├── raw_jds/                # Raw job description inputs
│   ├── raw_resumes/            # Raw resume file uploads
│   ├── Resumes/                # Processed resume documents
│   ├── app_database.db         # Local SQLite database
│   └── skills_list.txt         # Master list of target technical skills
│
├── src/                        # Core Application Business & ML Logic
│   ├── __init__.py            
│   ├── auth.py                 # User authentication & password hashing
│   ├── courses_manager.py      # Recommendation engine logic
│   ├── database.py             # SQLite CRUD operations
│   ├── matcher.py              # SBERT embedding generation & Cosine Similarity
│   ├── parser.py               # PDF and DOCX text extraction pipelines
│   ├── preprocess.py           # Text normalization & cleaning
│   ├── skill_extractor.py      # Regex-based skill parsing & gap analysis
│   └── utils.py                # Common helper routines
│
├── views/                      # Frontend UI Views
│   ├── __init__.py            
│   ├── auth_view.py            # Login & Registration interfaces
│   ├── history_view.py         # Analysis history dashboard UI
│   └── matcher_view.py         # Primary upload & execution dashboard UI
│
├── .gitignore                  # Standard Git ignore rules
├── app.py                      # Application entry point & router
├── README.md                   # Project documentation
└── requirements.txt            # Python environment dependencies
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10+ installed
- `pip` and `venv` available

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🧪 Running Tests

```bash
python -m pytest tests/test_modules.py -v
```

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| Python 3.10+ | Backend logic |
| Streamlit | Web UI |
| pdfplumber | PDF text extraction |
| python-docx | DOCX text extraction |
| spaCy (`en_core_web_sm`) | NLP preprocessing & NER |
| Sentence-Transformers | Semantic embeddings |
| scikit-learn | Cosine similarity calculation |
| pandas | Candidate ranking table |
| PyTorch (CPU) | DL backend for Sentence-Transformers |

---

## 📚 Key Concepts Demonstrated

- **NLP Pipeline**: Text cleaning, stopword removal, lemmatization, named entity recognition.
- **Semantic Search**: Dense vector embeddings via transformer models.
- **Similarity Matching**: Cosine similarity between document embeddings.
- **Skill Gap Analysis**: Set operations on extracted skill lists.
- **Candidate Ranking**: Sorted dataframe for multi-resume comparison.

---

## 👨‍💻 Author

MCA Major Project — developed as a demonstration of applied AI and NLP techniques for intelligent recruitment assistance.
