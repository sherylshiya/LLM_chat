import streamlit as st
from openai import OpenAI
import os
st.markdown(
    """
    <style>
    .stApp {
        background-color: #001f3f;  /* Dark blue */
        color: white;
    }

    h1 {
        color: white !important;
    }

    h2, h3, h4, h5, h6, p {
        color: #ffffff;
    }

    .stTextInput > div > input {
        background-color: #003366;
        color: white;
    }

    .stButton > button {
        background-color: #004080;
        color: white;
    }

    .stSelectbox > div > div {
        background-color: #003366;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("LLM Chatbot")

GROQ_API_KEY = "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"  # or paste the key directly for quick testing


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


selected_model = st.selectbox(
    "Choose a Groq-supported model:",
    [
        "llama3-8b-8192",
        "llama3-70b-8192",
        "gemma-7b-it"
    ]
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]


prompt = st.text_input("Ask me anything:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {e}")

# Display the chat history
for msg in st.session_state.messages[1:]:  # skip system message
    st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

