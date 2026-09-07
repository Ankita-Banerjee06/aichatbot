import streamlit as st
import requests

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://127.0.0.1:8000"

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }

        .app-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.25rem;
        }
        .app-header h1 {
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0;
        }
        .app-subtitle {
            color: #6b7280;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }

        .status-pill {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .status-ready {
            background-color: #dcfce7;
            color: #15803d;
        }
        .status-waiting {
            background-color: #fef3c7;
            color: #92400e;
        }
        .status-error {
            background-color: #fee2e2;
            color: #b91c1c;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid #e5e7eb;
        }

        div[data-testid="stChatInput"] {
            border-top: 1px solid #e5e7eb;
            padding-top: 0.75rem;
        }

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "document_pages" not in st.session_state:
    st.session_state.document_pages = None

# ----------------------------------------------------------------------------
# Sidebar — document upload & status
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📁 Document")
    st.caption("Upload a PDF, then ask questions about it in the chat.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file", type=["pdf"], label_visibility="collapsed"
    )

    if uploaded_file is not None:
        upload_clicked = st.button(
            "Upload & Process", type="primary", use_container_width=True
        )

        if upload_clicked:
            with st.spinner("Reading and processing your document..."):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/upload", files=files, timeout=60
                    )
                    result = response.json()

                    if "error" in result:
                        st.session_state.document_loaded = False
                        st.error(f"Failed to process PDF: {result['error']}")
                    else:
                        st.session_state.document_loaded = True
                        st.session_state.document_name = uploaded_file.name
                        st.session_state.document_pages = result.get("pages")
                        st.session_state.messages = []
                        st.success("Document processed successfully.")
                        st.rerun()

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Can't reach the backend. Make sure the FastAPI "
                        "server is running at " + BACKEND_URL
                    )
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    st.divider()

    st.markdown("### Status")
    if st.session_state.document_loaded:
        st.markdown(
            '<span class="status-pill status-ready">● Document ready</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**File:** {st.session_state.document_name}")
        if st.session_state.document_pages is not None:
            st.markdown(f"**Pages:** {st.session_state.document_pages}")
    else:
        st.markdown(
            '<span class="status-pill status-waiting">● No document loaded</span>',
            unsafe_allow_html=True,
        )

    if st.session_state.document_loaded:
        st.divider()
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ----------------------------------------------------------------------------
# Main area — header
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>📄 AI PDF Chatbot</h1>
    </div>
    <div class="app-subtitle">
        Upload a PDF from the sidebar and ask questions about its contents.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Chat history
# ----------------------------------------------------------------------------
if not st.session_state.messages:
    if st.session_state.document_loaded:
        st.info("Document loaded. Ask a question below to get started.")
    else:
        st.info("Upload a PDF from the sidebar to begin.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ----------------------------------------------------------------------------
# Chat input
# ----------------------------------------------------------------------------
question = st.chat_input(
    "Ask something about the document..."
    if st.session_state.document_loaded
    else "Upload a document first...",
    disabled=not st.session_state.document_loaded,
)

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the document..."):
            try:
                response = requests.get(
                    f"{BACKEND_URL}/ask",
                    params={"question": question},
                    timeout=30,
                )
                try:
                    result = response.json()
                except ValueError:
                    answer = (
                        f"Backend returned a non-JSON response "
                        f"(status {response.status_code}): {response.text[:300]}"
                    )
                else:
                    if "answer" in result:
                        answer = result["answer"]
                    elif "error" in result:
                        answer = f"Backend error: {result['error']}"
                    else:
                        answer = (
                            f"Unexpected response from backend "
                            f"(status {response.status_code}): {result}"
                        )
            except requests.exceptions.ConnectionError:
                answer = (
                    "Can't reach the backend right now. Make sure the "
                    "FastAPI server is running at " + BACKEND_URL
                )
            except Exception as e:
                answer = f"Something went wrong: {e}"

        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
