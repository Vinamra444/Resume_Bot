# 📄 PDF-based AI Chatbot using FastAPI

This project is a **FastAPI-based chatbot** that allows users to upload PDFs and ask questions about their content. The chatbot extracts text from PDFs, processes it, and generates AI-powered responses using OpenAI's API.

---

## 🚀 Features
- 📂 Upload multiple PDF files.
- 📜 Extract text and convert it to Markdown.
- 🔍 Ask questions related to the uploaded PDFs.
- 🤖 Get AI-generated responses based only on the uploaded document content.

---

## ⚙️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Vinamra444/Resume_Bot.git
cd Resume Chatbot

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables
Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_modelname

5️⃣ Run the FastAPI Server
uvicorn main:app --reload
By default, the API will run at: http://127.0.0.1:8000

📌 Usage
1️⃣ Upload PDFs
Use POST /upload/ to upload one or more PDFs.
The backend will extract and process the text.
2️⃣ Ask Questions
Use POST /ask/ to ask a question based on the uploaded PDFs.
The AI will respond with an answer from the document content.

🛠 Technologies Used
FastAPI – For backend API.
OpenAI API – For AI-generated answers.
PyMuPDF (Fitz) – For extracting text from PDFs.
LangChain – For document chunking.
Markdownify – To convert text to Markdown.

🤝 Contributing
Contributions are welcome! If you’d like to improve this project, feel free to fork it, make updates, and submit a pull request.

📜 License
This project is licensed under the MIT License.


