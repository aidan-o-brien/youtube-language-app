import streamlit as st
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Helper Functions ---

def get_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        return parse_qs(query.query).get('v', [None])[0]
    return None

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        st.error(f"Transcript fetch failed: {e}")
        return None

def generate_questions(text, n_questions=3):
    prompt = f"""
Generate {n_questions} multiple-choice questions from the following text.
Format your output as a JSON list, where each item has:
- question: string
- options: list of 4 strings
- answer: the correct option (must match one of the options exactly)

Transcript:
{text[:2000]}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        st.error("❌ Could not parse LLM response as JSON. Try again or adjust prompt.")
    except Exception as e:
        st.error(f"LLM call failed: {e}")
    return []

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
