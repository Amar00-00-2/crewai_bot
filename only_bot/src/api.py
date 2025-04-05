from fastapi import FastAPI
from pydantic import BaseModel
from crewai_fastapi_agent_chat.crew import EmailRagAgent
import os
import logging
import warnings
import traceback

# Suppress warnings and logs for cleaner output
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
logging.basicConfig(level=logging.ERROR)
logging.getLogger('opentelemetry').setLevel(logging.ERROR)
os.environ['OTEL_SDK_DISABLED'] = 'true'  # Disable telemetry if not required
app = FastAPI()

class CrewRequest(BaseModel):
    question: str
    # user_id: str
    username: str
    collection_id: str
    email: str
    mobilenumber: str
    chat_history : list
    prompt: str
    vector_db: str
    productId:list
    productname: list

@app.get('/check')
async def check():
    return "Server is running crewai bot..."


@app.post("/purabot")
async def run_crew(payload: CrewRequest):
    try:
        print(">>>>>>>>>>>>>>>",payload)
        
        if payload.prompt:
            prompt=payload.prompt
        else:
            prompt="""
                # System Message
                You are an AI sales assistant for Tabtree IT Consulting Services, specializing exclusively in Paperless Office AI-Based Enterprise DMS (Document Management System). Your role is to assist potential customers by answering questions strictly related to our DMS solutions, understanding their needs, and guiding them toward a decision.

                # Context
                {context}

                # Instructions
                1. Greet the customer warmly and introduce yourself as an AI assistant.
                2. Ask open-ended questions to understand the customer's needs and situation.
                3. Listen actively and tailor your responses to the customer's specific concerns.
                4. Highlight relevant features and benefits based on the customer's needs.
                5. Address any objections or concerns professionally and empathetically.
                6. If appropriate, guide the customer towards making a purchase or scheduling a demo.
                7. If the customer isn't ready to buy, offer additional resources or follow-up options.
                8. Always maintain a positive, helpful tone throughout the conversation.

                # Conversation History
                {chat_history}
            """
        input_data = {  
            "question": payload.question, 
            "username": payload.username, 
            "collection_id": payload.collection_id,
            "chat_history" :payload.chat_history,
            "email": payload.email, 
            "prompt":prompt,
            "mobilenumber": payload.mobilenumber,
            "product_id":payload.productId,
            "product_name":payload.productname,
            "vector_db":payload.vector_db,

        }
        result = EmailRagAgent().crew().kickoff(inputs=input_data)

        # ✅ Extract only the final task output (last task in the sequence)
        final_output = result.raw
        print(">>>>>>>>>>>",result)
        return {
            "status": "success",
            "message": final_output  # Returning only the final answer
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=7778, reload=True)
