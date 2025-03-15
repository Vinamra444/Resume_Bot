import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Form # type: ignore
import os
import openai
import fitz  # PyMuPDF to extract text from PDFs
from markdownify import markdownify as md  # Convert text to Markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For text chunking
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('OPENAI_MODEL')

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Set OpenAI API key
openai.api_key = api_key

# Define a custom class to store document text and metadata
class CustomDocument:
    def __init__(self, text, metadata):
        self.page_content = text
        self.metadata = metadata

# Function to extract and convert text from PDFs
def extract_and_convert_to_markdown(pdf_bytes):
    text = ""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        page_text = page.get_text("text") or ""  # Extract plain text
        markdown_text = md(page_text, heading_style="ATX")  # Convert to Markdown
        text += markdown_text + "\n\n"
    return text

# Store uploaded content in memory
stored_content = ""

@app.post("/upload/")
async def upload_pdf(files: List[UploadFile] = File(...)):
    global stored_content
    try:
        docs = []
        for file in files:
            pdf_bytes = await file.read()
            extracted_text = extract_and_convert_to_markdown(pdf_bytes)
            docs.append(CustomDocument(extracted_text, {"source": file.filename}))

        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # Combine chunks into one text block
        stored_content = "".join(chunk.page_content for chunk in chunks)

        return {"message": "PDFs uploaded successfully", "file_count": len(files)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    global stored_content
    if not stored_content:
        raise HTTPException(status_code=400, detail="No document uploaded yet. Please upload a PDF first.")

    try:
        llm_prompt = f"""
        You have to provide an answer to the user's question **only from the given text**.
        Answers should be pointwise and well-presented without any special tags (*, **, #, ##):

        {stored_content}
        """

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": llm_prompt},
                {"role": "user", "content": question}
            ]
        )
        return {"answer": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
