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
# import asyncio
# from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
# from typing import List
# from docling.document_converter import DocumentConverter
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from app.models import CustomDocument

# router = APIRouter()

# # Store uploaded content in memory
# stored_content = ""
# UPLOAD_DIR = "uploaded_files"  # Directory to store uploaded files

# # Ensure the upload directory exists
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# async def save_uploaded_file(file: UploadFile) -> str:
#     """Save an uploaded file to disk in chunks."""
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         while chunk := await file.read(1024 * 1024):  # Read in chunks of 1MB
#             f.write(chunk)
#     return file_path

# async def extract_text_with_docling(file_path: str) -> str:
#     """Extract text from a file using Docling."""
#     converter = DocumentConverter()
#     result = converter.convert(file_path)
#     return result.document.export_to_markdown()

# def split_text_into_chunks(text: str, metadata: dict) -> List[str]:
#     """Split text into chunks using LangChain's RecursiveCharacterTextSplitter."""
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     docs = [CustomDocument(text, metadata)]
#     chunks = splitter.split_documents(docs)
#     return [chunk.page_content for chunk in chunks]

# async def process_file(file: UploadFile) -> List[str]:
#     """Process a single file: save, extract text, and split into chunks."""
#     try:
#         # Save the file to disk
#         file_path = await save_uploaded_file(file)

#         # Extract text using Docling
#         extracted_text = await extract_text_with_docling(file_path)

#         # Split text into chunks
#         metadata = {"source": file.filename}
#         chunks = split_text_into_chunks(extracted_text, metadata)

#         return chunks
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

# @router.post("/upload/")
# async def upload_files(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
#     global stored_content
#     try:
#         # Process files in parallel
#         tasks = [process_file(file) for file in files]
#         results = await asyncio.gather(*tasks)

#         # Combine all chunks into a single text block
#         stored_content = "\n\n".join(chunk for result in results for chunk in result)
#         print(stored_content)  # Debugging

#         return {"message": "Files uploaded and processed successfully", "file_count": len(files)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# import os
# import asyncio
# from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
# from typing import List
# from docling.document_converter import DocumentConverter
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from app.models import CustomDocument
# import fitz  # PyMuPDF for splitting PDF into pages

# router = APIRouter()

# # Store uploaded content in memory
# stored_content = ""
# UPLOAD_DIR = "uploaded_files"  # Directory to store uploaded files

# # Ensure the upload directory exists
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# async def save_uploaded_file(file: UploadFile) -> str:
#     """Save an uploaded file to disk in chunks."""
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         while chunk := await file.read(1024 * 1024):  # Read in chunks of 1MB
#             f.write(chunk)
#     return file_path

# def split_pdf_into_pages(file_path: str, batch_size: int = 10) -> List[str]:
#     """Split a PDF into individual pages and save them as temporary files."""
#     doc = fitz.open(file_path)
#     page_files = []
#     for i in range(len(doc)):
#         page = doc.load_page(i)
#         pix = page.get_pixmap()
#         temp_file = os.path.join(UPLOAD_DIR, f"page_{i + 1}.png")
#         pix.save(temp_file)
#         page_files.append(temp_file)
#     return page_files

# async def extract_text_with_docling(file_path: str) -> str:
#     """Extract text from a file using Docling."""
#     converter = DocumentConverter()
#     result = converter.convert(file_path)
#     return result.document.export_to_markdown()

# def split_text_into_chunks(text: str, metadata: dict) -> List[str]:
#     """Split text into chunks using LangChain's RecursiveCharacterTextSplitter."""
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     docs = [CustomDocument(text, metadata)]
#     chunks = splitter.split_documents(docs)
#     return [chunk.page_content for chunk in chunks]

# async def process_pdf_in_batches(file_path: str, filename: str, batch_size: int = 10):
#     """Process a PDF in batches of pages using Docling."""
#     try:
#         # Split the PDF into individual pages
#         page_files = split_pdf_into_pages(file_path, batch_size)

#         # Extract text from each page in parallel
#         tasks = [extract_text_with_docling(page_file) for page_file in page_files]
#         extracted_texts = await asyncio.gather(*tasks)

#         # Combine all extracted text
#         combined_text = "\n\n".join(extracted_texts)

#         # Split text into chunks
#         metadata = {"source": filename}
#         chunks = split_text_into_chunks(combined_text, metadata)

#         # Store the result globally
#         global stored_content
#         stored_content = "\n\n".join(chunks)
#         print(stored_content)  # Debugging

#         # Clean up temporary page files
#         for page_file in page_files:
#             os.remove(page_file)
#     except Exception as e:
#         print(f"Error processing file {filename}: {str(e)}")

# @router.post("/upload/")
# async def upload_files(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
#     try:
#         for file in files:
#             # Save the file to disk
#             file_path = await save_uploaded_file(file)

#             # Offload batch processing to a background task
#             background_tasks.add_task(process_pdf_in_batches, file_path, file.filename)

#         # Respond immediately after files are saved
#         return {"message": "Files uploaded successfully. Processing in the background.", "file_count": len(files)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))