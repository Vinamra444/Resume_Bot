import openai #To use API of openai
import streamlit as st
import os #to make web apps interactive
import fitz  #Use when, to open and read the pdfs
from markdownify import markdownify as md #to convert HTML content to markdown format
from langchain.text_splitter import RecursiveCharacterTextSplitter #to break large pdfs into small small docs type
from dotenv import load_dotenv # to use the environment variables


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('OPENAI_MODEL')

# Use the API key with OpenAI client
openai.api_key = api_key

st.set_page_config(page_title="LLM Assistant", page_icon=":bot:", layout="centered")

st.markdown('<div class="centered-title"><h1>Employee Lifecycle Management Platform</h1></div>', unsafe_allow_html=True)

con=""

# Define a custom class to wrap document text and metadata
class CustomDocument:
    def __init__(self, text, metadata):
        self.page_content = text
        self.metadata = metadata

# Specify the folder path containing the PDFs
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/TransOrg.png")
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    uploaded_files = st.file_uploader(
                "", accept_multiple_files=True, label_visibility="collapsed")
        
pdf_files = []

if uploaded_files:
    folder_path = "uploaded_pdfs"  # Create a temp folder
    os.makedirs(folder_path, exist_ok=True)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Save uploaded file locally
        pdf_files.append(file_path)
else:
    folder_path = r"D:\Transorg\VAT_2.0\Resume Chatbot\data"  # Default path
    pdf_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.pdf')]

# Function to extract and convert text to Markdown
def extract_and_convert_to_markdown(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            page_text = page.get_text("text") or ""  # Extract plain text
            markdown_text = md(page_text, heading_style="ATX")  # Convert to Markdown, use ATX style for headings
            text += markdown_text + "\n\n"  # Ensure separation between pages
    return text

# Load all documents and prepare for text splitting
docs = []
for file_path in pdf_files:
    text = extract_and_convert_to_markdown(file_path)
    # Create an instance of CustomDocument with Markdown text
    docs.append(CustomDocument(text, {"source": file_path}))

# Initialize the splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split documents into chunks
chunks = splitter.split_documents(docs)

# Print or further process the chunks
for chunk in chunks:
    print(chunk.page_content)  # Output or further process the text chunks
    con=con+(chunk.page_content)

llm_prompt1 = f"""
You have to provide answers for user questions **extremely accurately** and **only from the given text**.  
⚠️ **Do not generate responses from outside the prompt.**  
✅ Answers should be **pointwise and well-presented**, but **without symbols like `*`, `#`, or `##`.**

{con}
"""


def outp(user_input):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "system", "content": llm_prompt1},
        {"role": "user", "content": user_input}]
    )
    final=response.choices[0].message.content
    return final


# Custom CSS styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom styles
local_css("imj.css")

st.markdown("""
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

user_input = st.text_input("",value="", placeholder="Ask a question...")
st.markdown('</div>', unsafe_allow_html=True)

# Submit button
if st.button("Process"):
    if user_input:
        # Send request to your processing function
        response = outp(user_input)
        # st.write(response)
        st.markdown(f'<div class="centered-response">{response}</div>', unsafe_allow_html=True)