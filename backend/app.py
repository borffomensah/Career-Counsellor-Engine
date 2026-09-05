@app.post("/chat/")
def chat_endpoint(payload: ChatRequest):
    try:
        user_messages = [m for m in payload.messages if m.role == "user"]
        
        # 1. Handle brand new session
        if len(user_messages) == 0:
            return {
                "reply": "Let's identify your ideal technical career track across 7 specialized tech domains. There are 10 questions. For each question, simply reply with your choice (A, B, C, D, E, F, or G). Respond OK and let's get started!"
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
        # user_messages[0] was the "OK". user_messages[1:] correspond to Q1 through Q10 responses.
        valid_answers = []
        for msg in user_messages[1:]:
            cleaned_input = msg.content.strip().upper()
            # Check if the cleaned input is strictly a single valid letter choice (or starts with it cleanly)
            matched = next((char for char in [cleaned_input] if char in VALID_LETTERS), None)
            # Fallback for looser inputs if desired, but strictly checking single-letter length prevents keyword bleeding (like 'a' in roadmap)
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

        # 5. Validate the latest user input if they haven't finished the 10 questions yet
        latest_msg = user_messages[-1].content.strip().upper()
        latest_valid_choice = next((char for char in latest_msg if char in VALID_LETTERS and len(latest_msg) <= 3), None)

        if not latest_valid_choice and current_score_count < 10:
            active_q_index = current_score_count  # Points to the current unanswered question
            curr_q = QUIZ_QUESTIONS[active_q_index]
            reply = (
                "⚠️ **Invalid selection.** Please reply strictly with a single letter from **A** to **G** corresponding to your choice.\n\n"
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