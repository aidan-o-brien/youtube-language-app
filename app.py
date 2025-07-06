import streamlit as st
import json
from utils import get_video_id, fetch_transcript
from openai_client import generate_questions


# --- Streamlit App ---

st.title("🎬 Language Learning with YouTube")
st.markdown("Paste a YouTube video link to generate comprehension questions from its transcript.")

video_url = st.text_input("YouTube Video URL")

if video_url:
    video_id = get_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL.")
    else:
        st.video(video_url)

        if st.button("Generate Questions"):
            with st.spinner("Fetching transcript..."):
                transcript = fetch_transcript(video_id)

            if transcript:
                with st.spinner("Generating questions..."):
                    questions = generate_questions(transcript)

                if questions:
                    st.session_state.questions = questions
                    for idx in range(len(questions)):
                        st.session_state.pop(f"q{idx}_selected", None)
                        st.session_state.pop(f"q{idx}_submitted", None)
                    st.success("✅ Questions generated!")

# --- Display Questions ---
if "questions" in st.session_state:
    questions = st.session_state.questions

    st.markdown("### 🧠 Comprehension Questions")

    for idx, q in enumerate(questions):
        key_selected = f"q{idx}_selected"
        key_submitted = f"q{idx}_submitted"

        st.write(f"**{idx + 1}. {q['question']}**")

        # Safe default index for preselected answer
        try:
            default_index = q["options"].index(st.session_state[key_selected])
        except (KeyError, ValueError, TypeError):
            default_index = None

        selected = st.radio(
            label="Choose an answer:",
            options=q["options"],
            index=default_index,
            key=key_selected,
            disabled=key_submitted in st.session_state
        )

        # Submit button for each question
        if key_submitted not in st.session_state:
            if st.button(f"Submit Answer to Question {idx + 1}", key=f"submit_{idx}"):
                if selected:
                    st.session_state[key_submitted] = True

        # Show feedback only after this question is submitted
        if key_submitted in st.session_state:
            correct = q["answer"]
            user_ans = st.session_state[key_selected]
            if user_ans == correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{correct}**")

    # Reset all answers
    if st.button("🔁 Reset All Answers"):
        for idx in range(len(questions)):
            st.session_state.pop(f"q{idx}_selected", None)
            st.session_state.pop(f"q{idx}_submitted", None)
        st.experimental_rerun()
