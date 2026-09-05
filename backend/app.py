from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- Career Quiz Questions & Mappings ---
VALID_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H"]

QUIZ_QUESTIONS = [
    {
        "question": "1. What type of tasks or projects do you find yourself most naturally drawn to?",
        "options": [
            "A) Cleaning messy data sets, building SQL queries, and designing databases.",
            "B) Building predictive models, training machine learning algorithms, and tuning hyperparameters.",
            "C) Creating interactive dashboards, visual charts, and translating data insights for stakeholders.",
            "D) Designing end-to-end data pipelines, setting up Docker containers, and managing cloud infrastructure.",
            "E) Analyzing clinical records, public health statistics, or medical data trends.",
            "F) Working with supply chain logistics, inventory metrics, and operational performance numbers.",
            "G) Structuring unstructured text, cleaning text data, and working with text annotation or NLP pipelines.",
            "H) Exploring general business strategy, user behavior, and exploratory data analysis."
        ]
    },
    {
        "question": "2. Which core programming language or tool stack do you feel most comfortable working with?",
        "options": [
            "A) Advanced SQL, PostgreSQL, and relational database management systems.",
            "B) Python, scikit-learn, Pandas, and NumPy for machine learning modeling.",
            "C) Power BI, Tableau, Advanced Excel, and DAX measures.",
            "D) Python, Docker, FastAPI, Flask, and Git version control.",
            "E) R, SPSS, statistical software, and health information management systems.",
            "F) Excel, supply chain ERP tools, and logistics reporting frameworks.",
            "G) Python text processing libraries, regex, and basic transformer models.",
            "H) VS Code, general Python scripting, and exploratory Jupyter notebooks."
        ]
    },
    {
        "question": "3. How do you prefer to handle and process data when solving a problem?",
        "options": [
            "A) Writing optimized queries to extract, transform, and structure raw data efficiently.",
            "B) Splitting data into training and test sets, evaluating metrics like accuracy, precision, and recall.",
            "C) Transforming numbers into visual stories, KPI cards, and dynamic executive dashboards.",
            "D) Automating workflows, building REST APIs, and containerizing applications for production.",
            "E) Ensuring data compliance, privacy, and accurate health records or statistical reporting.",
            "F) Analyzing bottlenecks, forecasting inventory demand, and optimizing operational flow.",
            "G) Tokenizing words, cleaning text corpora, and preparing datasets for NLP or annotation.",
            "H) Tackling diverse, exploratory data challenges depending on the immediate project need."
        ]
    },
    {
        "question": "4. What kind of final output or deliverable gives you the greatest sense of accomplishment?",
        "options": [
            "A) A robust, well-indexed relational database that runs lightning-fast queries.",
            "B) A high-performing machine learning model that successfully predicts outcomes on unseen data.",
            "C) A clean, interactive executive dashboard that leadership can use to make key business decisions.",
            "D) A fully deployed web app running live on the cloud via Docker and FastAPI.",
            "E) Accurate health data reports or statistical analysis that support clinical or public health insights.",
            "F) A logistics or supply chain report that cuts operational waste or improves delivery times.",
            "G) A clean, accurately annotated text dataset or working NLP text-classification pipeline.",
            "H) A versatile portfolio of varied data science and analytics projects."
        ]
    },
    {
        "question": "5. Which mathematical or statistical concepts do you enjoy applying the most?",
        "options": [
            "A) Set theory, relational algebra, and database normalization logic.",
            "B) Probability, linear algebra, feature selection, and model interpretability (like SHAP).",
            "C) Descriptive statistics, aggregations, ratios, and trend analysis.",
            "D) System architecture logic, networking ports, and container resource allocation.",
            "E) Biostatistics, epidemiological metrics, confidence intervals, and hypothesis testing.",
            "F) Forecasting time series, moving averages, and operational optimization math.",
            "G) Frequency distributions, text similarity metrics, and linguistic token statistics.",
            "H) General applied statistics and data analysis fundamentals."
        ]
    },
    {
        "question": "6. When facing a complex bug or blocker in your workflow, what is your go-to troubleshooting style?",
        "options": [
            "A) Inspecting table schemas, foreign keys, and query execution plans.",
            "B) Debugging model training curves, checking feature shapes, and tuning hyperparameters.",
            "C) Checking data type mismatches in DAX formulas or fixing layout alignment in dashboards.",
            "D) Inspecting server logs, verifying environment variables, and checking Docker container bindings.",
            "E) Cross-verifying health records, data standards, and compliance guidelines.",
            "F) Reviewing supply chain ledger entries and tracing step-by-step operational logs.",
            "G) Inspecting text encoding issues, cleaning irregularities, and checking token lengths.",
            "H) Searching documentation, reading stack traces, and testing systematic fixes."
        ]
    },
    {
        "question": "7. What aspect of software development and data workflows interests you the most?",
        "options": [
            "A) Building scalable data schemas and efficient data storage structures.",
            "B) Experimenting with algorithms like Random Forest, XGBoost, and Logistic Regression.",
            "C) Designing intuitive user experiences through visual charts and data storytelling.",
            "D) Building robust backend APIs, microservices, and smooth deployment pipelines.",
            "E) Managing sensitive health information systems and medical data workflows.",
            "F) Streamlining business operations and data-driven supply chain decisions.",
            "G) Exploring unstructured data, sentiment analysis, and text intelligence.",
            "H) Learning a broad spectrum of data tools from end to end."
        ]
    },
    {
        "question": "8. How do you prefer to collaborate or share your work with others?",
        "options": [
            "A) Documenting data dictionaries, entity-relationship diagrams, and SQL scripts.",
            "B) Sharing Jupyter notebooks, model evaluation metrics, and GitHub repositories.",
            "C) Publishing live interactive Power BI or Streamlit reports for team stakeholders.",
            "D) Sharing containerized applications, GitHub actions, and live API endpoints.",
            "E) Presenting statistical findings to healthcare professionals or administrative teams.",
            "F) Briefing operational managers on inventory forecasts and supply chain KPIs.",
            "G) Sharing annotated datasets or NLP model demo outputs.",
            "H) Sharing clean project codebases and documentation via GitHub."
        ]
    },
    {
        "question": "9. Which career growth path sounds the most exciting for your professional future?",
        "options": [
            "A) Becoming an expert Data Engineer specializing in database architecture and SQL.",
            "B) Becoming a Machine Learning Engineer building advanced predictive and AI models.",
            "C) Becoming a Business Intelligence or Data Analyst mastering visualization and insights.",
            "D) Becoming a Full-Stack MLOps / DevOps Engineer mastering deployment and infrastructure.",
            "E) Becoming a Health Informatics Specialist bridging data science and healthcare.",
            "F) Becoming a Supply Chain Data Analyst optimizing business operations and logistics.",
            "G) Becoming an NLP / Document Intelligence Specialist working with text and LLMs.",
            "H) Becoming a versatile Generalist Data Scientist adaptable across multiple domains."
        ]
    },
    {
        "question": "10. Finally, what is your primary career target or ambition among the following tracks?",
        "options": [
            "A) Data Engineering & Database Management",
            "B) Applied Machine Learning & Predictive Modeling",
            "C) Business Intelligence & Data Visualization",
            "D) MLOps, DevOps & Backend Engineering",
            "E) Health Informatics & Biostatistics",
            "F) Supply Chain Logistics & Business Analysis",
            "G) NLP & Document Intelligence",
            "H) General Data Science & Analytics"
        ]
    }
]

TRACK_MAPPING = {
    'A': ("Data Engineering & Database Management", "Focus heavily on advanced SQL, database design, and pipeline orchestration."),
    'B': ("Applied Machine Learning & Predictive Modeling", "Master feature engineering, algorithm selection, and model interpretability with SHAP."),
    'C': ("Business Intelligence & Data Visualization", "Strengthen your Power BI, DAX proficiency, and executive data storytelling."),
    'D': ("MLOps, DevOps & Backend Engineering", "Build expertise in Docker, FastAPI, CI/CD pipelines, and cloud hosting."),
    'E': ("Health Informatics & Biostatistics", "Deepen your knowledge of public health data standards, R, and statistical analysis."),
    'F': ("Supply Chain Logistics & Business Analysis", "Focus on inventory optimization metrics, operational analytics, and business reporting."),
    'G': ("NLP & Document Intelligence", "Explore text preprocessing, vector databases like ChromaDB, and RAG architectures."),
    'H': ("General Data Science & Analytics", "Maintain a balanced portfolio spanning exploratory analysis, modeling, and visualization.")
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]


@app.post("/chat/")
def chat_endpoint(payload: ChatRequest):
    try:
        user_messages = [m for m in payload.messages if m.role == "user"]
        
        # 1. Handle brand new session
        if len(user_messages) == 0:
            return {
                "reply": "Let's identify your ideal technical career track across 8 specialized domains. There are 10 questions. For each question, simply reply with your choice (A, B, C, D, E, F, G, or H). Respond OK and let's get started!"
            }

        first_user_msg = user_messages[0].content.strip().lower()
        
        # 2. Handle start confirmation
        if len(user_messages) == 1:
            if any(word in first_user_msg for word in ["ok", "start", "yes"]):
                first_q = QUIZ_QUESTIONS[0]
                return {"reply": f"**{first_q['question']}**\n\n" + "\n\n".join(first_q['options'])}
            else:
                return {"reply": "⚠️ **Invalid selection.** Please reply with **OK** to get started with the assessment."}

        # 3. Extract and validate answers strictly from subsequent messages
        valid_answers = []
        for msg in user_messages[1:]:
            cleaned_input = msg.content.strip().upper()
            matched = next((char for char in [cleaned_input] if char in VALID_LETTERS), None)
            if not matched and len(cleaned_input) <= 3:
                matched = next((char for char in cleaned_input if char in VALID_LETTERS), None)
            
            if matched:
                valid_answers.append(matched)

        current_score_count = len(valid_answers)

        # 4. Handle Completion (10 valid answers collected)
        if current_score_count >= 10:
            final_answers = valid_answers[:10]
            behavioral_answers = final_answers[:9]
            target_answer = final_answers[9] # Question 10 selection

            counts = {letter: behavioral_answers.count(letter) for letter in VALID_LETTERS}
            behavioral_top = max(counts, key=counts.get)
            behavioral_track, default_tip = TRACK_MAPPING.get(behavioral_top, TRACK_MAPPING['A'])
            target_track, _ = TRACK_MAPPING.get(target_answer, TRACK_MAPPING['H'])

            latest_text = user_messages[-1].content.strip().lower()
            if any(word in latest_text for word in ["yes", "roadmap", "sure", "please", "start"]):
                active_track_name = target_track if behavioral_top != target_answer else behavioral_track
                roadmap_reply = (
                    f"🗺️ **Step-by-Step Learning Roadmap: {active_track_name}**\n\n"
                    f"1. **Foundations (Weeks 1 to 4):** Master core syntax, data structures, and foundational math or logic relevant to this track.\n"
                    f"2. **Core Tools & Libraries (Weeks 5 to 10):** Build proficiency using standard industry tools, frameworks, and version control.\n"
                    f"3. **Applied Projects (Weeks 11 to 16):** Build 2 to 3 end-to-end portfolio projects applying these exact concepts.\n"
                    f"4. **Deployment & Portfolio (Weeks 17 to 20):** Deploy your projects live using Streamlit, Docker, or Cloud platforms and showcase them.\n\n"
                    f"💡 *Pro-Tip:* {default_tip}"
                )
                return {"reply": roadmap_reply}

            # Reconciliation Analysis
            if behavioral_top != target_answer:
                reconciliation_note = (
                    f"🧠 **Counselor Analysis & Profile Reconciliation:**\n\n"
                    f"Based on your answers to questions 1 through 9, your natural problem-solving strengths and behavioral patterns align most closely with **{behavioral_track}**.\n\n"
                    f"However, you indicated a strong personal career ambition to become a **{target_track}** (Question 10).\n\n"
                    f"### 🛡️ Bridge Your Strengths to Your Goal\n"
                    f"If you are determined to pursue **{target_track}**, your background is a massive asset, but you will intentionally need to develop the core pillars of that specific track.\n\n"
                    "Would you like the step-by-step learning roadmap for your chosen career goal?"
                )
                return {"reply": reconciliation_note}
            else:
                reply = (
                    f"### 🏆 Tech Career Pathway Assessment Results\n\n"
                    f"### 🎯 Recommended Track: {behavioral_track}\n\n"
                    f"💡 **Transition Tip:** {default_tip}\n\n"
                    "Would you like a step-by-step learning roadmap for this specific track?"
                )
                return {"reply": reply}

        # 5. Validate the latest user input if they haven't finished the 10 questions yet
        latest_msg = user_messages[-1].content.strip().upper()
        latest_valid_choice = next((char for char in latest_msg if char in VALID_LETTERS and len(latest_msg) <= 3), None)

        if not latest_valid_choice and current_score_count < 10:
            active_q_index = current_score_count  # Points to the current unanswered question
            curr_q = QUIZ_QUESTIONS[active_q_index]
            reply = (
                "⚠️ **Invalid selection.** Please reply strictly with a single letter from **A** to **H** corresponding to your choice.\n\n"
                f"**{curr_q['question']}**\n\n" + "\n\n".join(curr_q['options'])
            )
            return {"reply": reply}

        # 6. Serve the next question in sequence
        next_q_index = current_score_count
        if next_q_index < len(QUIZ_QUESTIONS):
            next_q = QUIZ_QUESTIONS[next_q_index]
            return {"reply": f"**{next_q['question']}**\n\n" + "\n\n".join(next_q['options'])}
        else:
            return {"reply": "Assessment complete! Type 'roadmap' to view your tailored learning plan."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))