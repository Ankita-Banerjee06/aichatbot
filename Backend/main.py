from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
import shutil

app = FastAPI()

docs = []

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    global docs
    
    try:
        # save uploaded file
        file_location = f"Documents/{file.filename}"
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # load PDF
        loader = PyPDFLoader(file_location)
        docs = loader.load()

        return {
            "message": "PDF uploaded and loaded successfully",
            "pages": len(docs)
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/ask")
def ask_question(question: str):

    try:
        if len(docs) == 0:
            return {"answer": "Please upload a PDF first"}

        full_text = ""

        for page in docs:
            full_text += page.page_content

        if question.lower() in full_text.lower():

            index = full_text.lower().find(question.lower())
            answer = full_text[index:index+300]

            return {"answer": answer}

        else:
            return {"answer": "Information not found in document"}

    except Exception as e:
        return {"error": str(e)}