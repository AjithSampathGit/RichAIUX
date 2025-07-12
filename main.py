from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random, json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = "interaction_logs.json"

class StepRequest(BaseModel):
    step: str

class HelpRequest(BaseModel):
    choice: str

class InteractionLog(BaseModel):
    step: str
    user_state: str
    action_taken: str

@app.post("/ai-suggestion")
async def ai_suggestion(req: StepRequest):
    user_states = ["idle", "confused", "interested", "disinterested"]
    user_state = random.choice(user_states)

    suggestion_map = {
        "select-product": ["explain_product"],
        "upload-id": ["live_banker", "save_resume"],
        "terms": ["live_banker", "schedule_appointment"],
        "funding": ["explain_product", "save_resume"],
        "thank-you": ["survey"]
    }

    return {
        "user_state": user_state,
        "suggestions": suggestion_map.get(req.step, [])
    }

@app.post("/ai-help")
async def ai_help(req: HelpRequest):
    if req.choice == "live_banker":
        return {
            "type": "chatbot",
            "agent_name": "Morgan",
            "agent_avatar": "https://i.imgur.com/AItCxSs.png",
            "messages": ["Hi, I’m Morgan, your live banker. How can I assist you today?"]
        }
    elif req.choice == "save_resume":
        return {"type": "info", "content": "✅ Your session has been saved. Resume anytime."}
    elif req.choice == "schedule_appointment":
        return {
            "type": "calendar",
            "slots": ["July 9 - 10 AM", "July 10 - 3 PM", "July 11 - 1 PM"]
        }
    elif req.choice == "survey":
        return {
            "type": "survey",
            "questions": [
                "🔍 What was helpful in this application?",
                "🤔 What can be improved?",
                "⭐ Would you recommend this to others?"
            ]
        }
    elif req.choice == "explain_product":
        return {
            "type": "info",
            "content": (
                "💼 *Checking accounts* are best for daily transactions—paying bills, debit card use, etc.\n\n"
                "💰 *Savings accounts* help you earn interest over time and are good for setting money aside.\n\n"
                "Choose based on your financial goals!"
            )
        }
    else:
        return {"type": "info", "content": "We'll assist you shortly."}

@app.post("/fraud-check")
async def fraud_check(req: Request):
    body = await req.json()
    filename = body.get("filename", "")
    # Fake logic: files named 'fraud.jpg' are flagged
    is_fraud = "fraud" in filename.lower()
    return { "fraud": is_fraud }


@app.post("/log-interaction")
async def log_interaction(data: InteractionLog):
    payload = data.dict()
    payload["timestamp"] = datetime.utcnow().isoformat()

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(payload)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    return {"status": "logged"}
