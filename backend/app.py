from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Union
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

### Custom dummy embedding function to prevent external downloads/network calls on Render
class CustomLightweightEmbedding(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = [float(ord(c)) for c in text[:16].ljust(16, ' ')]
            embeddings.append(vec)
        return embeddings

DB_DIR = "./course_db"
embedding_fn = CustomLightweightEmbedding()
client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(
    name="career_catalog",
    embedding_function=embedding_fn
)

ROADMAP_DATA: Dict[str, dict] = {
    "c1": {
        "career_track": "Data & AI",
        "title": "Applied Data Science & Machine Learning",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {"phase": "Phase 1: Foundations", "focus": "Python, Data Manipulation & EDA", "key_skills": ["Python", "Pandas", "NumPy", "SQL Basics"], "milestone": "Perform EDA on real-world tabular datasets."},
            {"phase": "Phase 2: Core Machine Learning", "focus": "Supervised & Unsupervised Models", "key_skills": ["Scikit-Learn", "Regression", "Classification", "Evaluation"], "milestone": "Build and tune cross-validated predictive ML models."},
            {"phase": "Phase 3: Advanced Capstone", "focus": "Model Interpretability & Deployment", "key_skills": ["SHAP", "FastAPI", "Docker", "GitHub"], "milestone": "Deploy a containerized machine learning web app."}
        ]
    },
    "c2": {
        "career_track": "Quantitative Finance",
        "title": "Quantitative Analysis & Financial Econometrics",
        "estimated_duration": "5 - 7 Months",
        "phases": [
            {"phase": "Phase 1: Foundations", "focus": "Probability, Linear Algebra & Econometrics", "key_skills": ["Statistics", "Linear Models", "Time Series", "Python/R"], "milestone": "Analyze structural breaks and cointegration."},
            {"phase": "Phase 2: Volatility & Forecasting", "focus": "GARCH Models & Risk Evaluation", "key_skills": ["ARCH/GARCH", "VaR", "Forecasting"], "milestone": "Construct time-series econometric models for market volatility."},
            {"phase": "Phase 3: Portfolio & Strategy", "focus": "Algorithmic Backtesting", "key_skills": ["Backtesting", "Portfolio Optimization"], "milestone": "Publish an empirical econometric research paper."}
        ]
    },
    "c3": {
        "career_track": "Data Infrastructure",
        "title": "Data Engineering & Pipeline Architecture",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {"phase": "Phase 1: Foundations", "focus": "Advanced SQL & Relational Modeling", "key_skills": ["Complex SQL", "Database Design", "Python Scripting"], "milestone": "Design an optimized relational schema."},
            {"phase": "Phase 2: Orchestration & ETL", "focus": "Batch & Stream Processing", "key_skills": ["Apache Airflow", "Apache Spark", "ETL", "Docker"], "milestone": "Build automated ETL pipelines via Airflow DAGs."},
            {"phase": "Phase 3: Cloud Infrastructure", "focus": "Cloud Warehousing & Big Data", "key_skills": ["Snowflake / BigQuery", "AWS", "CI/CD"], "milestone": "Deploy an enterprise cloud data pipeline."}
        ]
    },
    "c4": {
        "career_track": "Artificial Intelligence",
        "title": "AI & RAG Systems Engineering",
        "estimated_duration": "3 - 5 Months",
        "phases": [
            {"phase": "Phase 1: Foundations", "focus": "Vector Embeddings & Ingestion", "key_skills": ["Python", "Hugging Face", "ChromaDB", "FastAPI"], "milestone": "Build a local vector similarity search engine."},
            {"phase": "Phase 2: RAG Pipeline Design", "focus": "Retrieval-Augmented Generation", "key_skills": ["LangChain", "Context Retrieval", "LLM APIs"], "milestone": "Create an AI Q&A system with grounding."},
            {"phase": "Phase 3: Autonomous Agents", "focus": "Tool Calling & Memory Systems", "key_skills": ["AI Agents", "Function Calling", "Docker"], "milestone": "Deploy a multi-agent conversational assistant."}
        ]
    },
    "c5": {
        "career_track": "Software Engineering",
        "title": "Full-Stack Web Development",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {"phase": "Phase 1: Frontend", "focus": "UI Development & Responsive Design", "key_skills": ["HTML5/CSS3", "JavaScript", "Responsive UI"], "milestone": "Build responsive frontend interfaces."},
            {"phase": "Phase 2: Backend", "focus": "RESTful API Architecture", "key_skills": ["Node.js", "FastAPI", "PostgreSQL"], "milestone": "Develop secure backend APIs with database integration."},
            {"phase": "Phase 3: Integration", "focus": "State Management & Deployment", "key_skills": ["React", "Docker", "Render"], "milestone": "Launch a full-stack web application."}
        ]
    },
    "c6": {
        "career_track": "Cloud & Infrastructure",
        "title": "Cloud Computing & DevOps Engineering",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {"phase": "Phase 1: Systems & Networking", "focus": "Linux Administration", "key_skills": ["Linux Shell", "Bash", "Git"], "milestone": "Automate server configurations."},
            {"phase": "Phase 2: Containerization", "focus": "Docker & Kubernetes", "key_skills": ["Docker", "Kubernetes", "Terraform"], "milestone": "Containerize multi-container applications."},
            {"phase": "Phase 3: CI/CD & Operations", "focus": "Automated Pipelines", "key_skills": ["GitHub Actions", "Prometheus"], "milestone": "Build automated CI/CD deployment pipelines."}
        ]
    },
    "c7": {
        "career_track": "Product & Design",
        "title": "UI/UX Design & Product Strategy",
        "estimated_duration": "3 - 5 Months",
        "phases": [
            {"phase": "Phase 1: Research", "focus": "User Research & Wireframing", "key_skills": ["Personas", "Wireframing", "Figma"], "milestone": "Produce user journey maps."},
            {"phase": "Phase 2: Prototyping", "focus": "Design Systems & Interaction", "key_skills": ["Prototyping", "Design Systems"], "milestone": "Create clickable high-fidelity prototypes in Figma."},
            {"phase": "Phase 3: Testing", "focus": "Usability Testing & Hand-Off", "key_skills": ["Usability Testing", "Specs"], "milestone": "Publish a comprehensive UI/UX case study."}
        ]
    },
    "c8": {
        "career_track": "Cybersecurity",
        "title": "Cybersecurity & Threat Analysis",
        "estimated_duration": "5 - 7 Months",
        "phases": [
            {"phase": "Phase 1: Fundamentals", "focus": "Network & OS Defense", "key_skills": ["TCP/IP", "Linux Security", "Cryptography"], "milestone": "Perform network vulnerability identification."},
            {"phase": "Phase 2: Defense", "focus": "Threat Detection & SIEM", "key_skills": ["SIEM", "Log Analysis", "Incident Playbooks"], "milestone": "Analyze intrusion logs and configure alerts."},
            {"phase": "Phase 3: Testing", "focus": "Penetration Testing & Compliance", "key_skills": ["Metasploit", "Auditing"], "milestone": "Deliver a vulnerability assessment report."}
        ]
    }
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatSessionPayload(BaseModel):
    messages: List[ChatMessage]

def seed_catalog():
    """Populates the vector store if records do not exist."""
    existing_ids = collection.get()["ids"]
    initial_courses = [
        ("c1", "Applied Data Science & Machine Learning", "Statistical modeling, predictive algorithms, data preprocessing, feature engineering, Python, Pandas, and SQL database manipulation.", "Data & AI"),
        ("c2", "Quantitative Analysis & Financial Econometrics", "Advanced mathematical modeling, time-series forecasting, GARCH modeling, macro-financial risk evaluation, and economic data analysis.", "Quantitative Finance"),
        ("c3", "Data Engineering & Pipeline Architecture", "Scalable data pipelines, ETL automation, data warehousing, Apache Spark, Airflow, and cloud database infrastructure.", "Data Infrastructure"),
        ("c4", "AI & RAG Systems Engineering", "LLM integration, Retrieval-Augmented Generation, vector database indexing, AI agents, LangChain, and FastAPI deployment.", "Artificial Intelligence"),
        ("c5", "Full-Stack Web Development", "End-to-end web applications, React frontend interfaces, Node.js REST API architecture, HTML/CSS, and database management.", "Software Engineering"),
        ("c6", "Cloud Computing & DevOps Engineering", "Infrastructure automation, CI/CD pipelines, containerization with Docker, Kubernetes, and cloud system architecture.", "Cloud & Infrastructure"),
        ("c7", "UI/UX Design & Product Strategy", "User research, wireframing, Figma prototyping, visual interaction design, information architecture, and usability testing.", "Product & Design"),
        ("c8", "Cybersecurity & Threat Analysis", "Network defense, vulnerability assessments, security monitoring, threat detection, penetration testing, and incident response.", "Cybersecurity")
    ]
    for c_id, title, desc, track in initial_courses:
        if c_id not in existing_ids:
            collection.add(
                ids=[c_id],
                documents=[f"Course: {title}. Career Track: {track}. Summary: {desc}"],
                metadatas=[{"title": title, "track": track}]
            )
    print("🚀 Catalog successfully loaded into ChromaDB!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_catalog()
    yield

app = FastAPI(
    title="Conversational Career Counselor API",
    description="Multi-turn conversational backend integrating vector search and career roadmap recommendations.",
    version="2.0.0",
    lifespan=lifespan
)

@app.post("/chat")
@app.post("/chat/")
def career_counselor_chat(payload: ChatSessionPayload):
    """Handles multi-turn conversational queries with greeting checks and vector retrieval."""
    messages = payload.messages
    latest_message = messages[-1].content.strip() if messages else ""
    
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "greetings"]
    if latest_message.lower() in greetings and len(messages) <= 2:
        reply_text = (
            "Hello! I am your AI Career Counselor. I'm here to help you navigate your professional growth, "
            "explore technical tracks, and build a step-by-step roadmap.\n\n"
            "To get started, tell me a bit about yourself: What is your current background, and what career path or tech domain are you looking to pivot into?"
        )
        return {
            "reply": reply_text,
            "retrieved_track": "General Greeting"
        }

    vector_results = collection.query(query_texts=[latest_message], n_results=1)
    matched_track = "General Tech Career"
    matched_title = "Technology Career Path"
    
    if vector_results["ids"] and vector_results["ids"][0]:
        matched_id = vector_results["ids"][0][0]
        meta = vector_results["metadatas"][0][0]
        matched_title = meta.get("title")
        matched_track = meta.get("track")
        roadmap_info = ROADMAP_DATA.get(matched_id, {})
    else:
        roadmap_info = {}

    duration = roadmap_info.get("estimated_duration", "3 - 6 Months")
    phases = roadmap_info.get("phases", [])
    
    phases_text = "\n".join([f"- **{p['phase']}**: {p['focus']} (Milestone: {p['milestone']})" for p in phases])
    
    reply_text = (
        f"Based on your query, the most relevant track is **{matched_title}** under the **{matched_track}** domain "
        f"(Estimated Duration: {duration}).\n\n"
        f"Here is how you can approach this:\n{phases_text}\n\n"
        "Would you like to drill down into the specific tools or project deliverables for any of these phases?"
    )

    return {
        "reply": reply_text,
        "retrieved_track": matched_title
    }