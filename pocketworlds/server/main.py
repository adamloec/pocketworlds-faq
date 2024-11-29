import os
import shutil
import glob
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
import openai

from chat.chat_bot import ChatBot
from chat.models import ChatBotResponse, ChatBotRequest
from logger import Logger

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://pocketworlds-ah72e4vue-adamloeckle-gmailcoms-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot_instance: Optional[ChatBot] = None
logger: Optional[Logger] = None

@app.post("/initialize")
def initialize_chatbot():
    global chatbot_instance, logger
    chatbot_instance = ChatBot()
    chat_logger = Logger(name="chat_instance")
    logger = chat_logger.get_logger()
    logger.log_with_context("Chatbot and logger reinitialized.")

@app.post("/chat", response_model=ChatBotResponse)
def chat(request: ChatBotRequest):
    global chatbot_instance
    try:
        logger.log_with_context(f"User: {request.user_message}", metadata={
            'message_type': 'user_input',
            'message_length': len(request.user_message)
        })
        
        chatbot_response = chatbot_instance.process_message(request.user_message)
        
        logger.log_with_context(f"Chatbot: {chatbot_response.system_response}", metadata={
            'message_type': 'system_response',
            'completed': chatbot_response.completed,
            'supporting_urls': chatbot_response.supporting_urls if chatbot_response.supporting_urls else []
        })
        
        if not chatbot_response.completed:
            os.makedirs("logs/needs_context", exist_ok=True)
            log_files = glob.glob("logs/*.log")
            if log_files:
                latest_log = max(log_files, key=os.path.getctime)
                destination = f"logs/needs_context/{os.path.basename(latest_log)}"
                shutil.copy2(latest_log, destination)
                logger.log_with_context("Question marked as needing more context", level='warning')
        
        return chatbot_response
        
    except Exception as e:
        logger.log_with_context(f"Error: {str(e)}", level='error')
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/feedback/{feedback_type}")
async def handle_feedback(feedback_type: str):
    for dir_name in ["logs/liked", "logs/disliked"]:
        os.makedirs(dir_name, exist_ok=True)
    
    log_files = glob.glob("logs/*.log")
    if not log_files:
        raise HTTPException(status_code=404, detail="No log file found")
    
    latest_log = max(log_files, key=os.path.getctime)
    
    destination = f"logs/{feedback_type}/{os.path.basename(latest_log)}"
    shutil.copy2(latest_log, destination)
    
    return {"status": "success", "message": f"Feedback recorded as {feedback_type}"}