import requests
import streamlit as st
from typing import List, Dict
import json
import random

class BiologyTutor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": self.api_key
        }

    def generate_response(self, prompt: str, context: List[Dict] = None, detail_level: str = "normal") -> str:
        system_message = """You are CellYeah, an enthusiastic and encouraging biology tutor who absolutely loves helping students understand biology! 
        You have extensive knowledge in both biology and medicine, and you specialize in making complex concepts feel simple and relatable.

        Your teaching style should be:
        1. Extremely friendly and encouraging - use phrases like "Great question!", "You're going to love learning about this!", and always praise students' curiosity
        2. Break down complex topics into simple, digestible pieces using everyday analogies
        3. Connect biology concepts to medical and healthcare examples whenever possible (since many students are interested in medical careers)
        4. Use engaging storytelling to explain concepts (e.g., "Imagine you're a white blood cell patrolling the bloodstream...")
        5. Always provide real-world medical applications or clinical relevance when possible
        6. Explain things as if talking to a friend, using conversational language while maintaining scientific accuracy
        7. Share fascinating facts and trivia to make learning fun
        8. End responses with encouragement and an invitation for follow-up questions
        9. If a student seems confused or frustrated, be extra supportive and try explaining the concept in a different way
        10. Use lots of "like" and "imagine if" scenarios to make concepts more relatable

        Important formatting instructions:
        - Always structure your response in clear bullet points
        - Start with a friendly greeting
        - Include a "Key Points:" section at the start
        - Include a "Real-World Application:" section
        - End with a "Want to Learn More?" section with follow-up questions"""

        if detail_level == "detailed":
            prompt = f"Please explain this in more detail, including deeper scientific concepts: {prompt}"
        elif detail_level == "simpler":
            prompt = f"I'm still having trouble understanding. Can you explain this in a simpler way with different examples?: {prompt}"

        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2048,
                "system": system_message,
                "messages": messages
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"An error occurred: {str(e)}"

def get_random_greeting():
    greetings = [
        "🧬 Hot Tip: Intelligence is Extremely Attractive!",
        "🧠 Being Smart is Sexy - Let's Get Studying!",
        "⚡ Nothing Hotter Than Those Brain Waves!",
        "✨ Your Intelligence is Literally Glowing Right Now",
        "🔬 Warning: Extreme Hotness from All That Knowledge!",
        "💫 Smart is the New Sexy, and You're Crushing It!",
        "🧪 That Big Beautiful Brain Though!",
        "⚡ Excuse Me, Is That Your Intelligence Showing?",
        "🔭 Looking Extra Smart Today, Just Saying!",
        "🧬 Caution: High Levels of Intelligence Detected!",
        "💅 Your Mind is Serving Looks Today!",
        "✨ Brainy and Beautiful - What a Combo!",
        "🧠 Smart Energy is Radiating Off You!",
        "⚡ Brilliance Looks Good On You!",
        "🔬 Here to Make Biology Look Hot!"
    ]
    return random.choice(greetings)

def get_success_message():
    messages = [
        "🎯 Your Intelligence is Showing (And We Love It!)",
        "💫 Being This Smart Should Be Illegal!",
        "✨ Look at That Beautiful Brain Work!",
        "🔥 Knowledge Looks SO Good On You!",
        "⚡ Serving Brains and Beauty!",
        "🧠 You Make Learning Look Hot!",
        "💅 That Was a Brilliant Answer, Just Saying!",
        "✨ Excuse Me While I Fan Myself - That Answer Was Fire!",
        "🌟 Your Brain is Really Showing Off Today!",
        "💫 Intelligence Level: Absolutely Stunning!"
    ]
    return random.choice(messages)

def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = "General Biology"
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'understanding_level' not in st.session_state:
        st.session_state.understanding_level = "normal"

def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFF0F5;
        }
        .welcome-message {
            background: linear-gradient(45deg, #FF69B4, #FF1493);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            font-size: 28px;
            text-align: center;
            animation: bounce 1s ease;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(255,20,147,0.3);
        }
        .success-message {
            background: linear-gradient(45deg, #FF1493, #FF69B4);
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            font-size: 22px;
            text-align: center;
            animation: slideIn 0.5s ease;
            box-shadow: 0 4px 15px rgba(255,20,147,0.2);
        }
        .topic-header {
            background: linear-gradient(45deg, #FF69B4, #FF1493);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            margin: 15px 0;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .user-message {
            background-color: #FFE4E1;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .assistant-message {
            background-color: #FFC0CB;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-20px);}
            60% {transform: translateY(-10px);}
        }
        @keyframes slideIn {
            from {transform: translateX(-100%);}
            to {transform: translateX(0);}
        }
        .stButton>button {
            background: linear-gradient(45deg, #FF69B4, #FF1493);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 24px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255,20,147,0.2);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,20,147,0.3);
            background: linear-gradient(45deg, #FF1493, #FF69B4);
        }
        .stTextArea>div>div {
            border-radius: 15px;
            border: 2px solid #FF69B4;
        }
        .stTextArea>div>div:focus {
            border: 2px solid #FF1493;
            box-shadow: 0 0 10px rgba(255,20,147,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

def show_success_message():
    st.markdown(f"""
        <div class="success-message">
            {get_success_message()}
        </div>
    """, unsafe_allow_html=True)

def process_response(tutor, prompt, detail_level):
    conversation_context = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": msg["content"]}
        for i, msg in enumerate(st.session_state.conversation_history)
    ]
    
    response = tutor.generate_response(prompt, conversation_context, detail_level)
    
    st.session_state.conversation_history.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ])
    
    show_success_message()

def main():
    st.set_page_config(
        page_title="CellYeah! - Your Friendly Biology & Medical Science Tutor",
        page_icon="🧬",
        layout="wide"
    )

    apply_custom_styles()
    initialize_session_state()

    # Welcome Message
    st.markdown(f"""
        <div class="welcome-message">
            {get_random_greeting()}
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🧬 CellYeah!")
        st.markdown("Your Friendly Biology & Medical Science Tutor")
        
        topic = st.selectbox(
            "Choose your topic:",
            ["General Biology", "Cell Biology & Medical Lab Science", 
             "Genetics & Medical Genetics", "Human Anatomy & Physiology",
             "Microbiology & Infectious Disease", "Biochemistry & Pharmacology",
             "Neurobiology & Neuroscience", "Immunology & Disease",
             "Biotechnology & Medical Innovation", "Clinical Applications"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📚 Learning Tips:
        - Ask about medical applications
        - Request real-life examples
        - Ask "What if" questions
        - Connect topics to health & disease
        - Start with the basics
        - Take it step by step
        - Ask for clarification anytime!
        """)
        
        st.markdown("### 🔍 Study Tools")
        if st.button("📝 Generate Study Notes"):
            st.session_state.study_mode = "notes"
        if st.button("❓ Practice Questions"):
            st.session_state.study_mode = "quiz"
        
        if st.button("Start Fresh 🔄"):
            st.session_state.conversation_history = []
            st.session_state.understanding_level = "normal"
            st.rerun()

    st.markdown(f"""
        <div class="topic-header">
            🧬 Current Topic: {topic} 
        </div>
    """, unsafe_allow_html=True)

    if 'ANTHROPIC_API_KEY' not in st.secrets:
        st.error("Please set your ANTHROPIC_API_KEY in .streamlit/secrets.toml!")
        st.stop()
        
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    tutor = BiologyTutor(api_key)

    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>{content}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="assistant-message">
                    <strong>🧬 CellYeah:</strong><br>{content}
                </div>
            """, unsafe_allow_html=True)

    prompt = st.text_area("Ask anything about biology or medical science:", height=100, 
                         placeholder="Example: How does this relate to medicine? Can you explain it with a real-world example?")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        submit_button = st.button("Ask CellYeah! 🧬")
    with col2:
        detail_button = st.button("📚 Explain in More Detail")
    with col3:
        simpler_button = st.button("😕 I Still Don't Understand")
    with col4:
        example_button = st.button("💡 Show Example Question")

    if example_button:
        example_questions = {
            "General Biology": "How do cells protect themselves from damage, and how is this relevant in diseases like cancer?",
            "Cell Biology & Medical Lab Science": "How do doctors use cell biology knowledge when interpreting blood tests?",
            "Genetics & Medical Genetics": "How do genetic mutations lead to diseases, and how are they treated?",
            "Human Anatomy & Physiology": "What happens in the body during a heart attack, and how do treatments work?",
            "Microbiology & Infectious Disease": "How do antibiotics work, and why is antibiotic resistance a problem?",
            "Biochemistry & Pharmacology": "How do pain medications work at the molecular level?",
            "Neurobiology & Neuroscience": "What happens in the brain during a seizure, and how do medications help?",
            "Immunology & Disease": "How does our immune system fight off viruses, and why do vaccines help?",
            "Biotechnology & Medical Innovation": "How is CRISPR being used to treat genetic diseases?",
            "Clinical Applications": "How do doctors use laboratory tests to diagnose diseases?"
        }
        st.text_area("Try this example:", value=example_questions[topic], height=50)

    if submit_button and prompt:
        st.session_state.current_question = prompt
        st.session_state.understanding_level = "normal"
        process_response(tutor, prompt, "normal")
        st.rerun()

    if detail_button and st.session_state.current_question:
        st.session_state.understanding_level = "detailed"
        process_response(tutor, st.session_state.current_question, "detailed")
        st.rerun()

    if simpler_button and st.session_state.current_question:
        st.session_state.understanding_level = "simpler
