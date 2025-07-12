from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, json, os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    states = ["idle", "confused", "interested", "disinterested", "fraud"]
    state = random.choice(states)

    suggestions = {
        "select-product": ["product_help"],
        "upload-id": ["save_resume"] if state != "fraud" else [],
        "terms": ["live_banker", "schedule_appointment"],
        "funding": ["explain_product"],
        "thank-you": ["survey"]
    }

    return {"user_state": state, "suggestions": suggestions.get(req.step, [])}

@app.post("/ai-help")
async def ai_help(req: HelpRequest):
    if req.choice == "live_banker":
        return {"type": "chatbot", "agent_name": "Morgan", "agent_avatar": "", "messages": ["Hi! I'm Morgan, your banker."]}
    elif req.choice == "schedule_appointment":
        return {"type": "calendar", "slots": ["July 6 - 10 AM", "July 6 - 2 PM"]}
    elif req.choice == "survey":
        return {"type": "survey", "questions": ["Was this process helpful?", "What could improve?"]}
    elif req.choice == "product_help":
        return {"type": "info", "content": "Checking: good for daily use.\nSavings: ideal for saving funds with interest."}
    elif req.choice == "save_resume":
        return {"type": "info", "content": "✅ Your application was saved. Resume anytime."}
    else:
        return {"type": "info", "content": "We'll assist you shortly."}

@app.post("/log-interaction")
async def log_interaction(data: InteractionLog):
    log_entry = data.dict()
    log_entry["timestamp"] = datetime.utcnow().isoformat()

    logs = []
    if os.path.exists("interaction_logs.json"):
        with open("interaction_logs.json") as f:
            logs = json.load(f)

    logs.append(log_entry)
    with open("interaction_logs.json", "w") as f:
        json.dump(logs, f, indent=2)

    return {"status": "logged"}
