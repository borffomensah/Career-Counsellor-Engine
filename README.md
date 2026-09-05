# 🚀 AI Career Path Recommendation & Counseling System

An intelligent, interactive career counseling and roadmap generation web application designed to help professionals and students bridge the gap between their current background and their dream tech domain
🔗 **Live Application:** [https://careercounsellor.streamlit.app/](https://careercounsellor.streamlit.app/)

---

## 📖 Overview
Choosing the right transition path in technology can be overwhelming. This system acts as an **AI Career Counselor**, engaging users in a conversational diagnostic session to understand their background, skills, and goals. Leveraging **Vector Search (ChromaDB)** and custom embeddings, it matches user aspirations against structured technical career tracks and outputs a phase-by-phase actionable learning roadmap.

---

## ✨ Key Features
- **Conversational Guidance:** Interactive chat-style counselor that evaluates your technical readiness and career goals step-by-step.
- **Semantic Vector Matching:** Powered by **ChromaDB** to perform high-dimensional similarity searches matching user inputs to curated career tracks (Data & AI, Software Engineering, Cloud Infrastructure, AI & RAG Engineering, etc.).
- **Lightweight Custom Embeddings:** Uses an optimized **TF-IDF Vectorizer** embedding function designed to bypass heavy neural network dependencies, ensuring lightning-fast execution and compatibility with free-tier cloud constraints.
- **Domain Guardrails:** Built-in keyword validation filters out-of-domain queries to maintain high data relevance.
- **Structured Roadmaps:** Generates granular, multi-phase learning paths complete with key focus areas, essential skills, and milestone projects.
---

## 🏗️ System Architecture
The application is split into a decoupled client-server architecture:
1. **Frontend UI (`Streamlit`):** Manages user interaction, chat session states, and renders responsive recommendation cards and roadmaps.
2. **Backend API (`FastAPI`):** Exposes RESTful endpoints (`/recommend/`), handles request validation using Pydantic, and manages application lifecycle seeding.
3. **Vector Database (`ChromaDB`):** Persists course catalogs on disk and executes vector distance queries to find optimal career track alignments.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Backend Framework:** FastAPI, Uvicorn, Pydantic
- **Frontend Framework:** Streamlit
- **Vector Database & Embeddings:** ChromaDB, Scikit-Learn (TF-IDF Vectorizer)
- **Deployment:** Streamlit Community Cloud & Render

---

👤 Author
Daniel Borffo Mensah

Data Scientist, Statistical Analyst & Machine Learning Engineer


## 🗂️ Project Structure
```text
ai-career-counsellor/
│
├── backend/
│   ├── app.py              # FastAPI application, ChromaDB setup, & endpoints
│   └── requirements.txt    # Backend dependencies
│
├── frontend/
│   ├── frontend.py         # Streamlit UI & conversation handler
│   └── requirements.txt    # Frontend dependencies
│
└── README.md
