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
        system_message = """You are CellYeah, an expert biology tutor specializing in all areas of biology from cellular to ecological levels. 
        Your responses should be:
        1. Scientifically accurate and up-to-date
        2. Educational and engaging
        3. Accompanied by relevant examples from nature
        4. Explained at the appropriate academic level
        5. Connected to practical applications or real-world scenarios when possible
        
        If discussing complex processes, break them down into clear steps. Use analogies to help explain difficult concepts."""

        messages = [{"role": "system", "content": system_message}]
        
        if context:
            messages.extend(context)
            
        messages.append({"role": "user", "content": prompt})

        try:
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2048,
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
        page_title="CellYeah! - Your Biology Learning Assistant",
        page_icon="🧬",
        layout="wide"
    )

    initialize_session_state()

    with st.sidebar:
        st.title("🧬 CellYeah!")
        st.markdown("Your Personal Biology Tutor")
        
        topic = st.selectbox(
            "Choose your topic:",
            ["General Biology", "Cell Biology", "Genetics", "Ecology", 
             "Evolution", "Human Anatomy", "Microbiology", "Plant Biology",
             "Biochemistry", "Biotechnology"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### Study Tips:
        - Ask for real-world examples
        - Request diagrams when needed
        - Break down complex processes
        - Connect concepts together
        - Practice with sample problems
        """)
        
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()

    st.title("CellYeah! 🧬")
    st.markdown(f"Current Topic: **{topic}**")

    if 'ANTHROPIC_API_KEY' not in st.secrets:
        st.error("Please set your ANTHROPIC_API_KEY in .streamlit/secrets.toml!")
        st.stop()
        
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    tutor = BiologyTutor(api_key)

    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown("🧑‍🎓 **You:**")
            st.markdown(content)
        else:
            st.markdown("🧬 **CellYeah:**")
            st.markdown(content)
    
    prompt = st.text_area("Ask your biology question:", height=100)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.button("Ask CellYeah! 🧬")
    with col2:
        example_question = st.button("Show me an example question")
        
    if example_question:
        example_questions = {
            "General Biology": "What are the main differences between prokaryotic and eukaryotic cells?",
            "Cell Biology": "Can you explain the stages of mitosis?",
            "Genetics": "How does DNA replication work?",
            "Ecology": "What is the role of keystone species in an ecosystem?",
            "Evolution": "How does natural selection lead to adaptation?",
            "Human Anatomy": "How does the human heart pump blood through the body?",
            "Microbiology": "What are the different types of bacteria and their characteristics?",
            "Plant Biology": "How do plants perform photosynthesis?",
            "Biochemistry": "What are the main steps in cellular respiration?",
            "Biotechnology": "How does CRISPR gene editing work?"
        }
        st.text_area("Example question for your topic:", value=example_questions[topic], height=50)

    if submit_button and prompt:
        with st.spinner("CellYeah is thinking... 🧬"):
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
    st.markdown("Made with 🧬 | Ask me anything about biology!")

if __name__ == "__main__":
    main()
