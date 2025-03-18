import fitz  # PyMuPDF
from markdownify import markdownify as md

def extract_and_convert_to_markdown(pdf_bytes: bytes) -> str:
    """Extract text from a PDF and convert it to Markdown format."""
    text = ""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        page_text = page.get_text("text") or ""  # Extract plain text
        markdown_text = md(page_text, heading_style="ATX")  # Convert to Markdown
        text += markdown_text + "\n\n"
    
    return text

# import fitz  # PyMuPDF for PDFs
# from pptx import Presentation  # For PPT/PPTX files
# import pandas as pd  # For Excel files
# from io import BytesIO
# from markdownify import markdownify as md

# def extract_and_convert_to_markdown(file_bytes: bytes, file_extension: str) -> str:
#     """
#     Extract text from a file (PDF, PPT, Excel) and convert it to Markdown format.
    
#     Args:
#         file_bytes (bytes): The file content as bytes.
#         file_extension (str): The file extension (e.g., 'pdf', 'pptx', 'xlsx').
    
#     Returns:
#         str: The extracted text in Markdown format.
#     """
#     try:
#         text = ""
        
#         if file_extension == "pdf":
#             # Handle PDF files
#             pdf = fitz.open(stream=file_bytes, filetype="pdf")
#             for page_num in range(len(pdf)):
#                 page = pdf.load_page(page_num)
#                 page_text = page.get_text("text") or ""
#                 text += f"# Page {page_num + 1}\n\n{page_text}\n\n"
        
#         elif file_extension in ["pptx", "ppt"]:
#             # Handle PowerPoint files
#             ppt = Presentation(BytesIO(file_bytes))
#             for slide_num, slide in enumerate(ppt.slides):
#                 slide_text = ""
#                 for shape in slide.shapes:
#                     if hasattr(shape, "text"):
#                         slide_text += shape.text + "\n"
#                 text += f"# Slide {slide_num + 1}\n\n{slide_text}\n\n"
        
#         elif file_extension in ["xlsx", "xls"]:
#             # Handle Excel files
#             excel_file = BytesIO(file_bytes)
#             df = pd.read_excel(excel_file, sheet_name=None)  # Read all sheets
#             for sheet_name, sheet_data in df.items():
#                 text += f"# Sheet: {sheet_name}\n\n"
#                 text += sheet_data.to_markdown(index=False) + "\n\n"
        
#         else:
#             raise ValueError(f"Unsupported file type: {file_extension}")
        
#         return text.strip()
    
#     except Exception as e:
#         raise ValueError(f"Failed to process file: {str(e)}")