from fastapi import APIRouter, UploadFile, File, HTTPException # type: ignore
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils import extract_and_convert_to_markdown
from app.models import CustomDocument

router = APIRouter()

# Store uploaded content in memory
stored_content = ""

@router.post("/upload/")
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
        print(stored_content)

        return {"message": "PDFs uploaded successfully", "file_count": len(files)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
