📄 PDF-based AI Chatbot using FastAPI

Welcome to the PDF-based AI Chatbot! This project allows users to upload PDF files and ask AI-powered questions based on their content. The chatbot extracts text, processes it, and provides intelligent responses using OpenAI's API.

🚀 Features

✅ Upload multiple PDFs – Easily upload one or more PDF files.✅ Text extraction & conversion – Converts extracted text into Markdown.✅ AI-powered Q&A – Ask questions, and get responses based on the uploaded document.✅ Efficient text chunking – Uses LangChain to process large documents.

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Vinamra444/Resume_Bot.git
cd Resume_Chatbot

2️⃣ Create a Virtual Environment
python -m venv venv

Activate the virtual environment:
On Windows
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file in the root directory and add your OpenAI API credentials:

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_modelname

5️⃣ Run the FastAPI Server
uvicorn main:app --reload

By default, the API will be available at: http://127.0.0.1:8000

📌 Usage

1️⃣ Upload PDFs

Endpoint: POST /upload/

Upload one or more PDFs.

The backend will extract and process the text.

2️⃣ Ask Questions

Endpoint: POST /ask/

Ask a question based on the uploaded PDFs.

The AI will respond using only the document’s content.

🛠 Technologies Used

🚀 FastAPI – High-performance web framework for APIs.

🤖 OpenAI API – For AI-generated answers.

📄 PyMuPDF (Fitz) – Extracts text from PDFs.

🔗 LangChain – Helps with document chunking.

✍️ Markdownify – Converts text to Markdown.

📜 License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

🌟 Happy Coding! 🚀

