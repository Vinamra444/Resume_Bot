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
