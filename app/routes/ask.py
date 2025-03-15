from fastapi import APIRouter, HTTPException, Form # type: ignore
import openai
from app.config import API_KEY, MODEL_NAME
from app.routes import upload

# Set OpenAI API key
openai.api_key = API_KEY

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    global stored_content
    stored_content = upload.stored_content
    if not stored_content:
        raise HTTPException(status_code=400, detail="No document uploaded yet. Please upload a PDF first.")

    try:
        llm_prompt = f"""
        You have to provide an answer to the user's question **only from the given text**.
        Answers should be pointwise and well-presented without any special tags (*, **, #, ##):

        {stored_content}
        """

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": llm_prompt},
                {"role": "user", "content": question}
            ]
        )
        return {"answer": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
