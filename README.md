# AI PDF Chatbot

## Project Overview

AI PDF Chatbot is a mini AI-powered web application that allows users to upload a PDF document and ask questions about its contents. The system extracts text from the PDF and searches for relevant information to answer the user's query.

The project demonstrates how modern AI-based document processing systems work using a simple architecture with frontend, backend, and document processing components.

---

## Technologies Used

Frontend

* Python
* Streamlit

Backend

* FastAPI

AI / Document Processing

* LangChain
* PyPDFLoader
* pypdf

Other Tools

* Requests
* Uvicorn (ASGI server)

---

## System Architecture

User
↓
Frontend (Streamlit UI)
↓ HTTP Request
Backend API (FastAPI)
↓
LangChain Document Loader
↓
PDF Text Extraction
↓
Keyword Search Engine
↓
Answer Returned to User

---

## Project Structure

```
AI_Chatbot
│
├── Backend
│   └── main.py
│
├── Frontend
│   └── app.py
│
├── Documents
│
├── requirements.txt
│
└── README.md
```

Backend
Handles API requests, loads PDF documents, processes queries.

Frontend
Provides user interface for uploading PDFs and asking questions.

Documents
Stores uploaded PDF files.

requirements.txt
Lists all required Python libraries.

---

## Features

• Upload any PDF document
• Extract text from PDF automatically
• Ask questions about the document
• Simple chatbot-style interface
• Modular architecture (frontend + backend)

---

## Installation Guide

### 1 Clone the repository

```
git clone https://github.com/yourusername/AI-PDF-Chatbot.git
cd AI-PDF-Chatbot
```

### 2 Install dependencies

```
pip install -r requirements.txt
```

### 3 Run the backend server

```
python -m uvicorn Backend.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

### 4 Run the frontend

Open a new terminal and run:

```
python -m streamlit run Frontend/app.py
```

The web interface will open at:

```
http://localhost:8501
```

---

## How the System Works

1. User uploads a PDF file from the Streamlit interface.

2. The frontend sends the file to the FastAPI backend.

3. The backend saves the PDF inside the Documents folder.

4. LangChain loads the document using PyPDFLoader.

5. The text from all pages is extracted.

6. When the user asks a question, the backend searches the text.

7. If relevant information is found, the system returns the answer.

---

## Deployment

The project can be deployed online using cloud platforms.

Recommended setup:

Backend hosting
Render

Frontend hosting
Streamlit Cloud

Steps:

1. Upload project to GitHub
2. Deploy backend on Render
3. Deploy frontend on Streamlit Cloud
4. Update API URLs in frontend

---

## Future Improvements

• Implement vector embeddings for semantic search
• Add LLM-based answer generation
• Support multiple document uploads
• Improve UI/UX design
• Add document summarization feature

---

## Learning Outcomes

This project demonstrates:

• Building REST APIs using FastAPI
• Creating interactive UIs using Streamlit
• Integrating LangChain for document processing
• Designing modular AI systems
• Deploying applications to cloud platforms

---

## Author

Ankita Banerjee
CSE Data Science Student

---

## License

This project is created for educational purposes.
