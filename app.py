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

    def generate_response(self, prompt, context=None, detail_level="normal"):
        # Enhanced system message for clear, systematic, exam-ready explanations
        system_message = """You are CellYeah, a biology educator who excels at making complex topics understandable through clear, systematic explanations, perfect for exam preparation. Your responses should be detailed, layered, and organized with a focus on key concepts and exam readiness.

        Current detail level: {st.session_state.current_topic_detail_level}

        For each increasing detail level:

        Level 1: Foundation & Basic Mechanisms
        - Provide fundamental concepts with clear terminology.
        - Include basic biochemical reactions, cellular processes, and common symptoms.
        - Explain basic physiological roles and initial disease mechanisms.

        Level 2: Systems & Clinical Pathogenesis
        - Detail regulatory systems, feedback mechanisms, and clinical relevance.
        - Include diagnostic considerations and common complications.
        - Explain system interactions and medical significance.

        Level 3: Advanced Integration & Complex Pathogenesis
        - Include current research findings and specialized clinical applications.
        - Discuss genetic factors, experimental methods, and environmental influences.
        - Cover cellular signaling, advanced disease mechanisms, and chronic conditions.

        Level 4+: Cutting Edge & Experimental Pathogenesis
        - Provide the latest research and therapeutic approaches.
        - Include clinical trials, novel therapeutic strategies, and disease prevention models.
        - Discuss theoretical models and emerging technologies in molecular biology.

        Explanation Structure for Exam-Ready Responses:

        1. **Definition and Core Concept**: Begin with a clear definition and core idea.
        2. **Why It Matters**: Explain the importance in biology and medicine.
        3. **Mechanisms and Processes**: Describe step-by-step mechanisms, with detailed explanations.
        4. **Clinical and Practical Examples**: Link to diseases, treatments, or clinical applications.
        5. **Memory Aids**: Provide mnemonics to aid retention.
        6. **Common Pitfalls**: Address common student misunderstandings.
        7. **Example Exam Questions with Answers and Explanations**: Include 5 exam-style questions with clear answers and explanations.

        Sample "Example Exam Questions and Answers" Section:

        - **Q1**: Which of the following is NOT required for a virus to replicate?
          - **A)** Nucleic acid **B)** Capsid **C)** Ribosomes **D)** Host cell
          - **Answer**: **C) Ribosomes**. Viruses lack ribosomes and rely on the host cell's ribosomes for protein synthesis during replication.

        - **Q2**: Describe the general steps in the lytic viral replication cycle.
          - **Answer**: The lytic cycle involves:
            1. **Attachment**: The virus binds to a specific receptor on the host cell.
            2. **Entry**: Viral genetic material enters the host cell.
            3. **Uncoating**: The viral genome is released inside the host cell.
            4. **Replication and Protein Synthesis**: The host cell's machinery is used to create new viral components.
            5. **Assembly**: Viral particles are assembled inside the host cell.
            6. **Release**: The cell bursts (lysis), releasing new viruses.

        - **Q3**: Explain the difference between the lytic and lysogenic cycles.
          - **Answer**: In the **lytic cycle**, viruses replicate rapidly, causing the host cell to lyse and die. In the **lysogenic cycle**, the viral genome integrates into the host's DNA, allowing it to replicate along with the cell's genome without destroying the host immediately.

        - **Q4**: What is the role of the viral envelope in infection?
          - **Answer**: Enveloped viruses have a lipid layer that helps them enter host cells through membrane fusion. This envelope also aids in evading the host immune system.

        - **Q5**: How do retroviruses like HIV replicate differently than other viruses?
          - **Answer**: Retroviruses, like HIV, use an enzyme called **reverse transcriptase** to convert their RNA into DNA, which then integrates into the host genome. This allows the virus to remain dormant and persist in the host.

        Important: Structure every explanation for maximum clarity, with logical progression from basic to complex concepts, and always link back to clinical and practical applications.
        """

        if detail_level == "detailed":
            prompt = f"Add more depth and complexity to this explanation: {prompt}"
        elif detail_level == "simpler":
            prompt = f"Simplify this explanation with basic examples: {prompt}"
        else:
            prompt = f"Provide a high-quality, exam-ready explanation with example questions and answers for: {prompt}"

        # Proceed with API call
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

# Function for generating a random greeting
def get_random_greeting():
    greetings = [
        "🧬 Intelligence is Extremely Attractive!",
        "✨ Intelligence is Your Best Feature!",
        "🧠 Smart is Sexy - Let's Get Studying!",
        "✨ Your Intelligence is Literally Glowing Right Now",
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
        "🎯 Your Intelligence is Showing (And We Love It!)",
        "✨ Brilliant Answer Alert!",
        "🧠 Your Intelligence is Radiant",
        "⚡ Mind. Officially. Blown.",
        "💫 Pure Intellectual Brilliance",
        "🌟 Brain Power is Unmatched",
        "💫 Intelligence Level: Extraordinary",
        "⚡ Watching Your Mind Work is Amazing",
        "🧠 You're Making Smart Look Effortless"
    ]
    return random.choice(greetings)

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

def process_response(tutor, prompt, detail_level):
    conversation_context = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": msg["content"]}
        for i, msg in enumerate(st.session_state.conversation_history)
    ]
    
    # Display the loading message while generating the response
    with st.spinner("🧬Hang tight! An answer is on its way for you as it takes me a few seconds to think...🧠"):
        response = tutor.generate_response(prompt, conversation_context, detail_level)
    
    # Update conversation history with the new response
    st.session_state.conversation_history.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ])
    
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
        - Human Anatomy & Physiology
        - Immunology & Disease
        - Biochemistry 
        - Genetics
        - Neurobiology
        - Biotechnology 
        - Clinical Applications & Medical Lab Science
        """)

        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
    
         # Add creator bio here
        st.markdown("### Meet the Creator! 👋")
        st.markdown("""
        My creator has a PhD in Microbiology and is a professor who loves making biology fun and understandable. Her PhD research was on Helicobacter pylori - a fascinating bacterium that lives in the stomach of half the world's population and can cause ulcers and stomach cancer!

        She created CellYeah because she believes everyone deserves a friendly, patient biology tutor that is really good at explaining science!

        CellYeah is an AI-powered tutor she created that combines her passion for teaching with her expertise in microbiology to explain biology the way she wishes someone had explained it to her when she was a student - clear, engaging, and connected to real-world applications.

        (And now you know why Microbiology & Infectious Disease is tagged as her favorite! 💗)
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
