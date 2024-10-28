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
        system_message = """You are CellYeah, an extraordinary biology tutor who excels at making complex concepts crystal clear! Your teaching approach:
        [Detailed tutor system message here]"""
        
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
            response = requests.post(self.base_url, headers=self.headers, json=data)
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

def get_random_greeting():
    greetings = [
        "🧬 Hot Tip: Intelligence is Extremely Attractive!", 
        # More greetings...
    ]
    return random.choice(greetings)

def get_success_message():
    messages = [
        "🎯 Your Intelligence is Showing (And We Love It!)",
        # More messages...
    ]
    return random.choice(messages)

def get_medical_applications():
    return {
        "Cancer": "How does this concept relate to cancer development or treatment?",
        # More medical applications...
    }

def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = "General Biology"
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'understanding_level' not in st.session_state:
        st.session_state.understanding_level = "normal"
    if 'prev_prompt' not in st.session_state:
        st.session_state.prev_prompt = None

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Custom styles here */
        </style>
    """, unsafe_allow_html=True)

def show_success_message():
    st.markdown(f""" <div class="success-message"> {get_success_message()} </div> """, unsafe_allow_html=True)

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
    return response

def main():
    st.set_page_config(
        page_title="CellYeah! - Your Friendly Biology & Medical Science Tutor",
        page_icon="🧬",
        layout="wide"
    )
    apply_custom_styles()
    initialize_session_state()

    if 'ANTHROPIC_API_KEY' not in st.secrets:
        st.error("Please set your ANTHROPIC_API_KEY in .streamlit/secrets.toml!")
        st.stop()

    api_key = st.secrets["ANTHROPIC_API_KEY"]
    tutor = BiologyTutor(api_key)

    # Render history, prompt area, buttons, etc.

if __name__ == "__main__":
    main()
