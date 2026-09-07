import streamlit as st
import requests

st.title("AI PDF Chatbot")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:

    if st.button("Upload Document"):

        files = {"file": uploaded_file.getvalue()}

        r = requests.post(
            "http://127.0.0.1:8000/upload",
            files={"file": uploaded_file}
        )

        st.write(r.json())


# Ask question
question = st.text_input("Ask something from the document")

if st.button("Ask"):

    r = requests.get(
        "http://127.0.0.1:8000/ask",
        params={"question": question}
    )

    st.write(r.json())