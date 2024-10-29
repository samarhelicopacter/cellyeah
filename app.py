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
        self.detail_levels = {
            0: "Initial explanation",
            1: "Foundation & Basic Mechanisms",
            2: "Systems & Clinical Pathogenesis",
            3: "Advanced Integration & Complex Pathogenesis",
            4: "Cutting Edge & Experimental Pathogenesis"
        }

    def generate_response(self, prompt: str, context: List[Dict] = None, detail_level: str = "normal") -> str:
        system_message = """You are CellYeah, a biology educator who excels at making complex topics understandable through clear, systematic explanations. You have deep expertise across all biology fields and clinical medicine.

Current detail level: {st.session_state.current_topic_detail_level}

For each increasing detail level:

Level 1: Foundation & Basic Mechanisms
- Add molecular mechanisms and deeper scientific terminology
- Explain key cellular processes involved
- Include basic biochemical reactions
- Define specialized vocabulary
- Provide structural details
- Explain basic physiological roles
- Basic disease mechanisms
- Initial pathogenic events
- Common symptoms and signs
- Basic host responses
- Simple disease progression patterns

Level 2: Systems & Clinical Pathogenesis
- Include detailed pathways and regulatory systems
- Add clinical correlations and medical significance
- Explain feedback mechanisms and control systems
- Discuss related disorders and pathologies
- Include diagnostic considerations
- Add therapeutic applications
- Explain system interactions
- Include relevant lab values and clinical markers
- Detailed pathogenic mechanisms
- Host-pathogen interactions
- Disease progression timelines
- Inflammatory responses
- Immune system involvement
- Tissue damage mechanisms
- Organ system effects
- Common complications
- Risk factors and triggers

Level 3: Advanced Integration & Complex Pathogenesis
- Introduce current research findings
- Explain complex molecular interactions
- Add specialized clinical applications
- Include experimental methods
- Discuss emerging therapies
- Add detailed molecular pathways
- Include genetic and epigenetic factors
- Explain systems biology perspectives
- Add biotechnology applications
- Advanced pathogenic mechanisms
- Cellular signaling in disease
- Molecular basis of symptoms
- Disease modification factors
- Genetic susceptibility
- Environmental influences
- Progression markers
- Subcellular pathology
- Tissue-specific responses
- Multi-organ involvement
- Chronic disease mechanisms

Level 4+: Cutting Edge & Experimental Pathogenesis
- Include latest research developments
- Add specialized therapeutic approaches
- Explain advanced molecular techniques
- Include current clinical trials
- Add computational biology aspects
- Discuss emerging technologies
- Include pharmacological developments
- Add research methodologies
- Explain theoretical models
- Include future directions in the field
- Novel pathogenic pathways
- Experimental disease models
- Drug resistance mechanisms
- Advanced therapeutic targets
- Emerging biomarkers
- Disease prediction models
- Systems pathology
- Molecular epidemiology
- Population-specific factors
- Precision medicine approaches
- Novel therapeutic strategies
- Disease prevention advances

Important: Build upon previous explanations rather than restating them. Add new layers of complexity and depth with each level. Connect new information to previously explained concepts. For pathogenesis, ensure each level builds a more complete understanding of disease mechanisms and progression.

Your explanation approach:

1. Start With Clear Definitions
- Begin by stating exactly what the concept is in simple terms
- Explain why it's important
- Provide context for where this fits in biology
Example: "Cell metabolism simply means all the chemical reactions happening inside a cell. This is crucial because cells need energy to function and stay alive."

2. Then Build Understanding
- Layer in more detailed explanations
- Introduce technical terminology gradually
- Include all mechanisms and processes
- Connect concepts to broader biological systems
Example: "Innate immunity is one part of our immune system. It provides immediate defense against pathogens using pre-existing mechanisms, unlike adaptive immunity which develops specific responses."

3. Cover All Details Thoroughly
- Break down complex mechanisms
- Explain step-by-step processes
- Include molecular and cellular details
- Cover regulatory pathways
- Discuss relevant clinical applications
- Ensure all exam-relevant content is covered

4. Keep Language Clear Yet Complete
- Use precise scientific terms with clear explanations
- Include analogies when they genuinely aid understanding
- Connect abstract concepts to concrete examples
- Address common misconceptions
- Highlight key points for exams

5. Maintain Logical Flow
- Progress from basic to complex
- Connect related concepts
- Explain cause and effect relationships
- Show how systems interact
- Summarize key points

Remember:
- Always start with "This means..." or "This is..."
- Explain why each concept matters
- Include all technical details students need
- Keep explanations thorough but accessible
- Connect to practical applications or clinical relevance."""

        if detail_level == "detailed":
            prompt = f"Add more detail and complexity to this explanation: {prompt}"
        elif detail_level == "simpler":
            prompt = f"Break this down into simpler terms with clear examples: {prompt}"

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
        "🧬 Intelligence is Extremely Attractive!",
         "✨ Intelligence is Your Best Feature!",
        "🧠 Being Smart is Sexy - Let's Get Studying!",
        "✨ Your Intelligence is Literally Glowing Right Now",
        "💫 Smart is the New Sexy, and You're Crushing It!",
        "🧪 That Big Beautiful Brain Though!",
        "🔭 Looking Extra Smart Today, Just Saying!",
        "🧬 Caution: High Levels of Intelligence Detected!",
        "🧠 Smart Energy is Radiating Off You!",
        "⚡ Brilliance Looks Good On You!",
        "✨ Intelligence is Your Best Feature!",
        "🧬 Smart Looks Good On You",
        "🧠 Brilliance is Beautiful",
        "⚡ Your Mind is Magnetic",
        "💫 Knowledge is Your Superpower",
        "✨ That Intelligence Though!",
        "🧬 Brilliance in Action",
        "🧠 Mind Goals",
        "⚡ Intelligence Never Goes Out of Style",
        "💫 Your Brain is a Masterpiece",
        "✨ Smart is the New Cool",
        "🧬 Brainpower is Beautiful",
        "⚡ Brilliance Unlocked",
        "💫 Your Mind Shines",
        "🧠 Intelligence is Irresistible"
    ]
    return random.choice(greetings)

def get_success_message():
    messages = [
        "🎯 Your Intelligence is Showing (And We Love It!)",
        "✨ Brilliant Answer Alert!",
        "🧠 Your Intelligence is Radiant",
        "⚡ Mind. Officially. Blown.",
        "💫 Pure Intellectual Brilliance",
        "✨ That Answer Was Everything",
        "🌟 Your Brain Power is Unmatched",
        "💫 Intelligence Level: Extraordinary",
        "⚡ Watching Your Mind Work is Amazing",
        "✨ This is Genius in Action",
        "🧠 You're Making Smart Look Effortless"
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
    if 'practice_question' not in st.session_state:
        st.session_state.practice_question = None  # To store the current practice question

def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        .welcome-message {
            background: linear-gradient(45deg, #F8F9FA, #FFC6D9);
            color: #2C3E50;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            font-size: 28px;
            text-align: center;
            animation: bounce 1s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,154,190,0.3);
        }
        .success-message {
            background: linear-gradient(45deg, #FFFFFF, #FFC6D9);
            color: #2C3E50;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            font-size: 22px;
            text-align: center;
            animation: slideIn 0.5s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid rgba(255,154,190,0.2);
        }
        .topic-header {
            background: #FFFFFF;
            color: #2C3E50;
            padding: 10px 20px;
            border-radius: 25px;
            margin: 15px 0;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            border: 1px solid rgba(255,154,190,0.3);
        }
        .user-message {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
        }
        .assistant-message {
            background-color: #FFE6EE;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid rgba(255,154,190,0.2);
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
            background: linear-gradient(45deg, #FFFFFF, #FFC6D9);
            color: #2C3E50;
            border: 1px solid rgba(255,154,190,0.3);
            border-radius: 25px;
            padding: 12px 24px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,154,190,0.2);
            background: linear-gradient(45deg, #FFC6D9, #FFFFFF);
            border-color: rgba(255,154,190,0.5);
        }
        .stTextArea>div>div {
            border-radius: 15px;
            border: 1px solid rgba(255,154,190,0.3);
        }
        .stTextArea>div>div:focus {
            border: 1px solid rgba(255,154,190,0.5);
            box-shadow: 0 0 10px rgba(255,154,190,0.1);
        }
        .sidebar .sidebar-content {
            background-color: #FFFFFF;
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

    # Initialize tutor instance
    if 'ANTHROPIC_API_KEY' not in st.secrets:
        st.error("Please set your ANTHROPIC_API_KEY in .streamlit/secrets.toml!")
        st.stop()
        
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    tutor = BiologyTutor(api_key)  # Initialize tutor here

    # Welcome Message
    st.markdown(f"""
        <div class="welcome-message">
            {get_random_greeting()}
        </div>
    """, unsafe_allow_html=True)

    # Sidebar for Learning Tips and Expertise
    with st.sidebar:
        st.markdown("### 🧬 CellYeah is an Expert in:")
        st.markdown("""
        - General Biology
        - Cell & Molecular Biology
        - Microbiology & Infectious Disease (my creator's favorite! 💗)
        - Biochemistry & Pharmacology
        - Human Anatomy & Physiology
        - Immunology & Disease
        - Neurobiology & Neuroscience
        - Genetics
        - Biotechnology & Medical Innovation
        - Clinical Applications & Medical Lab Science
        """)

        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
    
         # Add creator bio here
        st.markdown("### Meet the Creator! 👋")
        st.markdown("""
        Hi! I'm Samar, a Microbiologist and college professor who loves making biology fun and accessible. I created CellYeah because I believe everyone deserves a friendly, patient biology tutor available 24/7!

        My background? I have a PhD in Microbiology, where I studied Helicobacter pylori - a fascinating bacterium that lives in the stomach of half the world's population and can cause ulcers and stomach cancer.

        As a professor, I love connecting biology to medical relevance and real-world applications. My favorite part? Seeing that 'aha!' moment when complex concepts finally click!

        CellYeah is an AI-powered tutor I created that combines my passion for teaching with my expertise in microbiology to explain biology the way I wish someone had explained it to me when I was a student - clear, engaging, and connected to real-world applications.

        (And now you know why Microbiology & Infectious Disease is tagged as my favorite! 💗)
        """)

    # Display user interactions
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

    # Display Practice Question and Answer below interactions
    if st.session_state.practice_question:
        st.markdown("### 🧠 Practice Question")
        st.write(f"**Question:** {st.session_state.practice_question['question']}")
        st.write("**Answer:**")
        st.write(st.session_state.practice_question['answer'])

    # Input for asking questions
    prompt = st.text_input("Ask anything about biology or medical science:", 
                           placeholder="Example: How does this relate to medicine? Can you explain it with a real-world example?",
                           on_change=lambda: process_response(tutor, st.session_state.current_question, "normal"),
                           key="current_question")
    
    # Action Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        submit_button = st.button("Ask CellYeah! 🧬")
    with col2:
        detail_button = st.button("Add Detail 📚 More Depth 🤓")
    with col3:
        simpler_button = st.button("Simplify This 💡 I Still Don't Get It 🤔")
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start Fresh button centered below
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        if st.button("Start Fresh 🔄"):
            st.session_state.conversation_history = []
            st.session_state.understanding_level = "normal"
            st.rerun()

   # Handle button clicks
    if submit_button and st.session_state.current_question:
        st.session_state.understanding_level = "normal"
        process_response(tutor, st.session_state.current_question, "normal")
        st.rerun()

    if detail_button and len(st.session_state.conversation_history) > 0:
        # Get the last question from conversation history
        last_question = None
        for message in reversed(st.session_state.conversation_history):
            if message["role"] == "user":
                last_question = message["content"]
                break
        
        if last_question:
            process_response(tutor, f"Please explain this in more detail, including deeper scientific concepts: {last_question}", "detailed")
            st.rerun()

    if simpler_button and len(st.session_state.conversation_history) > 0:
        # Get the last question from conversation history
        last_question = None
        for message in reversed(st.session_state.conversation_history):
            if message["role"] == "user":
                last_question = message["content"]
                break
        
        if last_question:
            process_response(tutor, f"I'm still having trouble understanding. Can you explain this in a simpler way with different examples?: {last_question}", "simpler")
            st.rerun()

    st.markdown("---")
    st.markdown("🧬 Understanding Biology, One Cell at a Time! 🔬")

    # Floating help button
    st.markdown("""
        <div style="position: fixed; bottom: 20px; right: 20px;">
            <button style="
                background-color: #FF69B4;
                color: white;
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            ">?</button>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
