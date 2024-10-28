import requests
import streamlit as st
from typing import List, Dict
import json

class BiologyTutor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": self.api_key
        }

    def generate_response(self, prompt: str, context: List[Dict] = None) -> str:
        # Create a biology-focused system message
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
        10. Use lots of "like" and "imagine if" scenarios to make concepts more relatable"""

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

def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = "General Biology"

def main():
    st.set_page_config(
        page_title="CellYeah! - Your Friendly Biology & Medical Science Tutor",
        page_icon="🧬",
        layout="wide"
    )

    initialize_session_state()

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
        ### Learning Tips:
        - Ask about medical applications
        - Request real-life examples
        - Ask "What if" questions
        - Connect topics to health & disease
        - Start with the basics
        - Take it step by step
        - Ask for clarification anytime!
        """)
        
        if st.button("Start Fresh 🔄"):
            st.session_state.conversation_history = []
            st.rerun()

    st.title("CellYeah! 🧬")
    st.markdown(f"Current Topic: **{topic}** 📚")

    if 'ANTHROPIC_API_KEY' not in st.secrets:
        st.error("Please set your ANTHROPIC_API_KEY in .streamlit/secrets.toml!")
        st.stop()
        
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    tutor = BiologyTutor(api_key)

    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown("👤 **You:**")
            st.markdown(content)
        else:
            st.markdown("🧬 **CellYeah:**")
            st.markdown(content)
    
    prompt = st.text_area("Ask anything about biology or medical science:", height=100, 
                         placeholder="Example: How does this relate to medicine? Can you explain it with a real-world example?")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.button("Ask CellYeah! 🧬")
    with col2:
        example_question = st.button("Show me an example question")
        
    if example_question:
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
        with st.spinner("CellYeah is excited to help you learn! 🧬"):
            conversation_context = [
                {"role": "user" if i % 2 == 0 else "assistant", "content": msg["content"]}
                for i, msg in enumerate(st.session_state.conversation_history)
            ]
            
            response = tutor.generate_response(prompt, conversation_context)
            
            st.session_state.conversation_history.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response}
            ])
            
            st.rerun()

    st.markdown("---")
    st.markdown("🧬 Understanding Biology, One Cell at a Time! 🔬")

if __name__ == "__main__":
    main()
