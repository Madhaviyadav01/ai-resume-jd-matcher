# AI Resume–JD Matcher

> **MCA Major Project** | AI-powered application to match resumes against job descriptions and rank candidates automatically.

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

```
AI_resume_jd_matcher/
│
├── app.py                  # Streamlit web application (main entry point)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── modules/
│   ├── __init__.py
│   ├── extractor.py        # PDF & DOCX text extraction
│   ├── preprocessor.py     # NLP preprocessing + skill extraction
│   ├── matcher.py          # Embedding generation + cosine similarity
│   └── recommender.py      # Resume improvement recommendations
│
├── data/
│   └── skills_list.txt     # Curated skills keyword database
│
└── tests/
    └── test_modules.py     # Unit tests for all modules
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
