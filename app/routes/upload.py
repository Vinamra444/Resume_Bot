import os
from fastapi import APIRouter, UploadFile, File, HTTPException # type: ignore
from typing import List
# from docling.document_converter import DocumentConverter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.models import CustomDocument
from app.utils import extract_and_convert_to_markdown

router = APIRouter()

# Store uploaded content in memory
stored_content = ""
UPLOAD_DIR = "uploaded_files"  # ✅ Directory to store uploaded files

# ✅ Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    global stored_content
    try:
        # converter = DocumentConverter()
        extracted_texts = []  # ✅ Store extracted text from all files

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)  # ✅ Save file path

            # ✅ Save uploaded file to disk
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # ✅ Use Docling to process the saved file
            # result = converter.convert(file_path)  # ✅ Pass file path instead of bytes
            # extracted_texts.append(result.document.export_to_markdown())  # ✅ Extract text in Markdown format
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
                extracted_text = extract_and_convert_to_markdown(pdf_bytes)  # ✅ Using function from utils.py
                extracted_texts.append(extracted_text)

        # ✅ Store extracted text in CustomDocument format
        docs = [CustomDocument(text, {"source": file.filename}) for text, file in zip(extracted_texts, files)]

        # ✅ Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # ✅ Combine all chunks into a single text block
        stored_content = "\n\n".join(chunk.page_content for chunk in chunks)
        print(stored_content)  # Debugging

        return {"message": "Files uploaded successfully", "file_count": len(files)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# import os
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from typing import List
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from app.models import CustomDocument
# from app.utils import extract_and_convert_to_markdown

# router = APIRouter()

# # Store uploaded content in memory
# stored_content = ""
# UPLOAD_DIR = "uploaded_files"  # Directory to store uploaded files

# # Ensure the upload directory exists
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/upload/")
# async def upload_files(files: List[UploadFile] = File(...)):
#     global stored_content
#     try:
#         extracted_texts = []  # Store extracted text from all files

#         for file in files:
#             file_path = os.path.join(UPLOAD_DIR, file.filename)  # Save file path

#             # Save uploaded file to disk
#             with open(file_path, "wb") as f:
#                 f.write(await file.read())

#             # Read the file as bytes
#             with open(file_path, "rb") as f:
#                 file_bytes = f.read()

#             # Get the file extension
#             file_extension = file.filename.split(".")[-1].lower()

#             # Extract text using the updated function
#             extracted_text = extract_and_convert_to_markdown(file_bytes, file_extension)
#             extracted_texts.append(extracted_text)

#         # Store extracted text in CustomDocument format
#         docs = [CustomDocument(text, {"source": file.filename}) for text, file in zip(extracted_texts, files)]

#         # Split text into chunks
#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = splitter.split_documents(docs)

#         # Combine all chunks into a single text block
#         stored_content = "\n\n".join(chunk.page_content for chunk in chunks)
#         print(stored_content)  # Debugging

#         return {"message": "Files uploaded successfully", "file_count": len(files)}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))