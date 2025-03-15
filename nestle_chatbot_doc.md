1. User Uploads PDFs
The API receives one or multiple PDFs through the /upload/ endpoint.
FastAPI's UploadFile reads the binary content of the PDFs.

2. PDF Text Extraction & Preprocessing
PyMuPDF (fitz) opens the binary PDF stream.
Each page’s text is extracted using .get_text("text").
The text is converted to Markdown format using markdownify for better structuring.
The extracted text is stored in a CustomDocument class (acts as an object with metadata).

3. Text Chunking (LangChain)
Since LLMs perform better on smaller inputs, we split the document into chunks.
RecursiveCharacterTextSplitter is used:
Chunk Size: 1000 characters
Overlap: 200 characters (to maintain context)
These chunks are stored in a global variable (stored_content) for querying.

4. User Asks a Question
The user sends a query via the /ask/ endpoint.
The system first validates if a PDF is uploaded.
The prompt is created dynamically:
It forces the LLM to answer strictly from the extracted text.
Uses pointwise formatting without symbols.

5. Query Processing with OpenAI GPT
OpenAI's ChatCompletion.create() is called:
The prompt includes the entire document as context.
The user question is passed separately.
The model processes the text only within the given context and returns an answer.

6. API Response
The AI-generated answer is returned as a JSON response.
FastAPI ensures that the response is structured and can be consumed by frontend applications.