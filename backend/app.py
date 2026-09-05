from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

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

def seed_catalog():
    existing_ids = collection.get()["ids"]
    initial_courses = [
        ("c1", "Applied Data Science & Machine Learning", "Statistical modeling, predictive algorithms, data preprocessing, feature engineering, Python, Pandas, and SQL database manipulation.", "Data & AI"),
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
    title="Tech Career Pathway Assessment API",
    description="Interactive backend supporting the 10-question 7-track Tech Career Pathway Assessment with intelligent profile reconciliation.",
    version="4.1.0",
    lifespan=lifespan
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

QUIZ_QUESTIONS = [
    {
        "num": 1,
        "question": "1. When you face a difficult problem, which angle of the situation naturally captures your attention first?",
        "options": [
            "**A)** Finding the underlying pattern, analyzing historical data, or building a statistical formula to predict it.",
            "**B)** Fixing the underlying plumbing and flow, setting up a reliable, automated system to move and organize resources smoothly.",
            "**C)** Thinking about how smart systems or AI tools could be integrated to automatically understand and resolve it.",
            "**D)** Building the actual tangible product or application from scratch so people can interact with it on the web.",
            "**E)** Optimizing the environment it runs in, ensuring the system doesn't crash under pressure and scales automatically.",
            "**F)** Putting yourself in the user's shoes to make the experience smooth, intuitive, and visually effortless.",
            "**G)** Finding the vulnerabilities in the system, securing the parameters, and protecting it from outside threats."
        ]
    },
    {
        "num": 2,
        "question": "2. How do you feel about mathematics, advanced statistics, and complex algorithms?",
        "options": [
            "**A)** I love applied statistics, probability, and using data to train models or find trends.",
            "**B)** I like logical structuring, but I prefer building data pipelines over solving deep theoretical equations.",
            "**C)** I am interested in how mathematical vectors can be used to power smart AI and language search models.",
            "**D)** I prefer practical coding and logic applied to building websites rather than dealing with deep mathematics.",
            "**E)** I lean toward operational logic, structuring servers, automation, and environments rather than math equations.",
            "**F)** Math and formulas don't interest me; I am driven by human psychology, visuals, and user behavior.",
            "**G)** I use analytical patterns to find security blind spots, focusing on system defense rather than standard math."
        ]
    },
    {
        "num": 3,
        "question": "3. If you were part of a team building a new digital application, what would be your dream role?",
        "options": [
            "**A)** Writing the predictive algorithms that learn from user data to recommend features.",
            "**B)** Designing and automating the heavy backend data pipelines that process millions of records seamlessly.",
            "**C)** Connecting large language models and building smart AI agents that understand context.",
            "**D)** Building both the visible web pages and the hidden APIs that handle user interactions.",
            "**E)** Setting up the cloud infrastructure, automation, and continuous delivery pipelines to deploy the app safely.",
            "**F)** Interviewing customers, mapping out wireframes in Figma, and designing beautiful user flows.",
            "**G)** Monitoring the network traffic, performing vulnerability checks, and setting up defenses against hackers."
        ]
    },
    {
        "num": 4,
        "question": "4. Which set of concepts sounds most exciting for you to learn and master?",
        "options": [
            "**A)** Predictive modeling, feature engineering, and data manipulation with Python and Pandas.",
            "**B)** Scalable data warehousing, ETL automation, and big data tools like Apache Spark or Airflow.",
            "**C)** Retrieval-Augmented Generation, vector databases, AI agents, and LangChain.",
            "**D)** Frontend user interfaces with React, backend architecture with Node.js, and HTML/CSS.",
            "**E)** Containerization with Docker, Kubernetes orchestration, and cloud automation.",
            "**F)** User research, prototyping in Figma, typography, and interactive design.",
            "**G)** Network defense, threat detection, penetration testing, and incident response."
        ]
    },
    {
        "num": 5,
        "question": "5. What kind of day-to-day workflow appeals to you the most?",
        "options": [
            "**A)** Cleaning and sorting through messy data to feed into machine learning models.",
            "**B)** Building structural architectures that manage how huge volumes of data flow within a company.",
            "**C)** Training, prompt-engineering, and deploying intelligent AI systems via APIs.",
            "**D)** Writing code to make beautiful, functional web applications come to life on a browser.",
            "**E)** Scripting automation tools to maintain server uptime, cloud storage, and deployment speed.",
            "**F)** Researching human behavior, sketching designs, and analyzing how people feel when using an app.",
            "**G)** Investigating suspicious system activity, analyzing alerts, and patching up network security flaws."
        ]
    },
    {
        "num": 6,
        "question": "6. Choose the scenario that sounds like a fun, satisfying puzzle to solve:",
        "options": [
            "**A)** Teaching a computer program how to accurately categorize thousands of data points on its own.",
            "**B)** Figuring out how to move terabytes of raw data from point A to point B instantly without dropping a single file.",
            "**C)** Fine-tuning a chatbot so it retrieves exactly the right document to answer a highly specific query.",
            "**D)** Debugging a website error where a button clicks perfectly but fails to save information to the database.",
            "**E)** Automating a routine so a development team's new code updates are checked and pushed to live servers with zero downtime.",
            "**F)** Rethinking a cluttered checkout page so users can complete a purchase in fewer clicks.",
            "**G)** Simulating a digital attack on your own network to find out where a malicious hacker could break in."
        ]
    },
    {
        "num": 7,
        "question": "7. What is your ideal balance between coding/programming and other tasks?",
        "options": [
            "**A)** Heavy coding focused purely on data structures, model training, and analytical algorithms.",
            "**B)** Purely programmatic, backend coding focused on data systems, file architecture, and orchestration tools.",
            "**C)** Specialized development focused on engineering AI connections, working with LLMs, and API deployment.",
            "**D)** Broad and versatile software engineering, writing both interactive user interfaces and server logic.",
            "**E)** Infrastructure as Code, spending less time writing standard software and more time scripting system automation.",
            "**F)** Minimal to zero coding, where my main toolkit consists of visual design, user empathy, and prototyping tools.",
            "**G)** Analytical scripting used to trace logs and set defenses, balanced with a deep understanding of network rules."
        ]
    },
    {
        "num": 8,
        "question": "8. Which digital frustration bothers you the most?",
        "options": [
            "**A)** When organizations guess their next business move instead of tracking historical facts and trends.",
            "**B)** When a system runs incredibly slow because its data collection databases are disorganized and clogged.",
            "**C)** When an AI chatbot hallucinates, loses context, or gives generic answers because it lacks access to right data.",
            "**D)** When a web application is glitchy, broken, or fails to properly load its features.",
            "**E)** When an entire online service goes down completely because the servers couldn't handle sudden user traffic.",
            "**F)** When a website looks terrible, has unreadable text, or makes it impossible to locate the primary menu button.",
            "**G)** Reading news about major data breaches where personal customer files are exposed due to weak defense systems."
        ]
    },
    {
        "num": 9,
        "question": "9. If you are transitioning from a non-tech field, which skillset do you want to lean on most?",
        "options": [
            "**A)** My logical problem-solving habits, investigative research, and love for finding patterns.",
            "**B)** My highly organized approach to handling logistics, structural filing, or sorting inventory systems.",
            "**C)** My passion for exploring advanced automation, voice and text systems, and modern AI tools.",
            "**D)** My hands-on builder mindset, wanting to physically create products that connect people.",
            "**E)** My background in managing operations, system maintenance, or keeping environments running smoothly.",
            "**F)** My high levels of empathy, creative eye, human communication, and understanding of consumer choices.",
            "**G)** My sharp attention to detail, rule enforcement, protective instincts, and investigative mindset."
        ]
    },
    {
        "num": 10,
        "question": "10. Looking ahead, who do you want to become? Which job title aligns best with your ultimate career vision?",
        "options": [
            "**A)** **Data Scientist / Machine Learning Engineer** (Building predictive models, training AI algorithms, and uncovering data insights).",
            "**B)** **Data Engineer** (Designing scalable pipelines, data warehouses, and infrastructure for massive data flows).",
            "**C)** **AI / RAG Systems Engineer** (Developing intelligent agents, vector search databases, and LLM-powered applications).",
            "**D)** **Full-Stack Software Engineer** (Building complete end-to-end web platforms, user interfaces, and robust backend APIs).",
            "**E)** **Cloud / DevOps Engineer** (Managing automated deployment pipelines, containerization, and cloud system scale).",
            "**F)** **UI/UX Product Designer** (Crafting intuitive user experiences, wireframes, and design systems).",
            "**G)** **Cybersecurity Analyst / Security Engineer** (Defending networks, patching vulnerabilities, and securing infrastructure)."
        ]
    }
]

VALID_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

TRACK_MAPPING = {
    'A': ("Applied Data Science & Machine Learning", "Focus heavily on mastering Python data libraries, statistics, and machine learning algorithms."),
    'B': ("Data Engineering & Pipeline Architecture", "Learn how databases are structured at scale and master ETL automation and workflow tools."),
    'C': ("AI & RAG Systems Engineering", "Dive straight into learning LangChain frameworks, API engineering, and vector management."),
    'D': ("Full-Stack Web Development", "Start with frontend frameworks and connect them securely to backend database engines."),
    'E': ("Cloud Computing & DevOps Engineering", "Gain certifications in cloud providers alongside Docker and Kubernetes to fast-track this shift."),
    'F': ("UI/UX Design & Product Strategy", "Build a visual portfolio using Figma and leverage human-centric design methodologies."),
    'G': ("Cybersecurity & Threat Analysis", "Gain fundamental networking knowledge and standard entry certifications like Security+.")
}

@app.get("/")
def home():
    return {"status": "online", "message": "Tech Career Pathway Assessment API is running!"}

@app.post("/chat/")
def chat_endpoint(payload: ChatRequest):
    try:
        user_messages = [m for m in payload.messages if m.role == "user"]
        
        if len(user_messages) == 0:
            return {"reply": "Let's identify your ideal technical career track across 7 specialized tech domains. There are 10 questions. For each question, simply reply with your choice (A, B, C, D, E, F, or G). Respond OK and let's get started!"}

        all_user_texts = [m.content.strip() for m in user_messages]
        first_user_msg = all_user_texts[0].lower() if all_user_texts else ""
        
        if len(user_messages) == 1 and ("ok" in first_user_msg or "start" in first_user_msg or "yes" in first_user_msg):
            first_q = QUIZ_QUESTIONS[0]
            return {"reply": f"**{first_q['question']}**\n\n" + "\n\n".join(first_q['options'])}

        if len(user_messages) == 1 and not ("ok" in first_user_msg or "start" in first_user_msg or "yes" in first_user_msg):
            return {"reply": "⚠️ **Invalid selection.** Please reply with **OK** to get started with the assessment."}

        valid_answers = []
        for msg in user_messages[1:]:
            cleaned_input = msg.content.strip().upper()
            matched = next((char for char in cleaned_input if char in VALID_LETTERS), None)
            if matched:
                valid_answers.append(matched)

        current_score_count = len(valid_answers)

        if current_score_count >= 10:
            final_answers = valid_answers[:10]
            behavioral_answers = final_answers[:9]
            target_answer = final_answers[9] # Question 10 selection

            # Tally behavioral strengths (Q1-Q9)
            counts = {letter: behavioral_answers.count(letter) for letter in VALID_LETTERS}
            behavioral_top = max(counts, key=counts.get)
            behavioral_track, default_tip = TRACK_MAPPING.get(behavioral_top, TRACK_MAPPING['A'])
            target_track, _ = TRACK_MAPPING.get(target_answer, TRACK_MAPPING['G'])

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

            # Intelligent Reconciliation Analysis
            if behavioral_top != target_answer:
                reconciliation_note = (
                    f"🧠 **Counselor Analysis & Profile Reconciliation:**\n\n"
                    f"Based on your answers to questions 1 through 9, your natural problem-solving strengths and behavioral patterns align most closely with **{behavioral_track}**.\n\n"
                    f"However, you indicated a strong personal career ambition to become a **{target_track}** (Question 10).\n\n"
                    f"### 🛡️ Bridge Your Strengths to Cybersecurity\n"
                    f"If you are determined to pursue **Cybersecurity & Threat Analysis**, your analytical data background is a massive asset (especially in threat intelligence and log analysis), but you will intentionally need to develop:\n"
                    f"1. **Deep Networking & OS Fundamentals:** Master TCP/IP protocols, DNS, Linux administration, and packet analysis (Wireshark).\n"
                    f"2. **Security Tooling & Frameworks:** Familiarize yourself with SIEM tools (Splunk, Elastic), vulnerability scanners, and penetration testing frameworks.\n"
                    f"3. **Defensive Mindset:** Shift from building predictive patterns to anticipating adversarial tactics (MITRE ATT&CK framework).\n\n"
                    "Would you like the step-by-step learning roadmap for your chosen career goal?"
                )
                return {"reply": reconciliation_note}
            else:
                chroma_results = collection.query(
                    query_texts=[behavioral_track],
                    n_results=1
                )
                db_doc = ""
                if chroma_results and chroma_results.get("documents"):
                    docs = chroma_results["documents"]
                    if docs and len(docs) > 0:
                        db_doc = docs[0][0]

                reply = (
                    f"### 🏆 Tech Career Pathway Assessment Results\n\n"
                    f"### 🎯 Recommended Track: {behavioral_track}\n\n"
                    f"📚 **Catalog Match (ChromaDB RAG):** {db_doc}\n\n"
                    f"💡 **Transition Tip:** {default_tip}\n\n"
                    "Would you like a step-by-step learning roadmap for this specific track?"
                )
                return {"reply": reply}

        latest_msg = user_messages[-1].content.strip().upper()
        latest_valid_choice = next((char for char in latest_msg if char in VALID_LETTERS), None)

        if not latest_valid_choice:
            active_q_index = min(current_score_count, 9)
            curr_q = QUIZ_QUESTIONS[active_q_index]
            reply = (
                "⚠️ **Invalid selection.** Please reply strictly with a single letter from **A** to **G** corresponding to your choice.\n\n"
                f"**{curr_q['question']}**\n\n" + "\n\n".join(curr_q['options'])
            )
            return {"reply": reply}

        if current_score_count == 10:
            # Re-run the reconciliation block immediately on hitting 10 answers
            final_answers = valid_answers[:10]
            behavioral_answers = final_answers[:9]
            target_answer = final_answers[9]

            counts = {letter: behavioral_answers.count(letter) for letter in VALID_LETTERS}
            behavioral_top = max(counts, key=counts.get)
            behavioral_track, default_tip = TRACK_MAPPING.get(behavioral_top, TRACK_MAPPING['A'])
            target_track, _ = TRACK_MAPPING.get(target_answer, TRACK_MAPPING['G'])

            if behavioral_top != target_answer:
                reply = (
                    f"🧠 **Counselor Analysis & Profile Reconciliation:**\n\n"
                    f"Based on your answers to questions 1 through 9, your natural problem-solving strengths and behavioral patterns align most closely with **{behavioral_track}**.\n\n"
                    f"However, you indicated a strong personal career ambition to become a **{target_track}** (Question 10).\n\n"
                    f"### 🛡️ Bridge Your Strengths to Cybersecurity\n"
                    f"If you are determined to pursue **Cybersecurity & Threat Analysis**, your analytical background is a massive asset, but you will intentionally need to develop:\n"
                    f"1. **Deep Networking & OS Fundamentals:** Master TCP/IP, DNS, Linux administration, and packet analysis.\n"
                    f"2. **Security Tooling & Frameworks:** Familiarize yourself with SIEM tools and vulnerability assessment scanners.\n"
                    f"3. **Defensive Mindset:** Shift from predictive modeling to analyzing adversarial tactics using the MITRE ATT&CK framework.\n\n"
                    "Would you like the step-by-step learning roadmap for your chosen career goal?"
                )
                return {"reply": reply}
            else:
                chroma_results = collection.query(
                    query_texts=[behavioral_track],
                    n_results=1
                )
                db_doc = ""
                if chroma_results and chroma_results.get("documents"):
                    docs = chroma_results["documents"]
                    if docs and len(docs) > 0:
                        db_doc = docs[0][0]

                reply = (
                    f"### 🏆 Tech Career Pathway Assessment Results\n\n"
                    f"### 🎯 Recommended Track: {behavioral_track}\n\n"
                    f"📚 **Catalog Match (ChromaDB RAG):** {db_doc}\n\n"
                    f"💡 **Transition Tip:** {default_tip}\n\n"
                    "Would you like a step-by-step learning roadmap for this specific track?"
                )
                return {"reply": reply}

        next_q_index = current_score_count
        next_q = QUIZ_QUESTIONS[next_q_index]
        reply = (
            f"**{next_q['question']}**\n\n" + "\n\n".join(next_q['options'])
        )
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))