from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

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

@app.post("/ai-suggestion")
async def ai_suggestion(req: StepRequest):
    fraud = False
    if req.step == "upload-id":
        fraud = random.choice([False, False, False, True])  # 25% chance of fraud

    user_state = random.choice(["idle", "confused", "interested", "disinterested"])
    suggestions_map = {
        "upload-id": ["save_resume", "help"],
        "terms": ["live_banker", "schedule_appointment"],
        "funding": ["explain_product"],
        "thank-you": ["survey"]
    }

    return {
        "user_state": user_state,
        "fraud": fraud,
        "suggestions": suggestions_map.get(req.step, [])
    }

@app.post("/ai-help")
async def ai_help(req: HelpRequest):
    choice = req.choice
    if choice == "live_banker":
        return {
            "type": "chatbot",
            "agent_name": "Morgan",
            "agent_avatar": "https://i.imgur.com/AItCxSs.png",
            "messages": ["Hi, I'm Morgan. How can I assist you today?"]
        }
    elif choice == "schedule_appointment":
        return {
            "type": "calendar",
            "slots": ["July 6 - 10:00 AM", "July 6 - 3:00 PM", "July 7 - 1:00 PM"]
        }
    elif choice == "survey":
        return {
            "type": "survey",
            "questions": [
                "What did you like?",
                "What can we improve?",
                "Would you recommend us?"
            ]
        }
    elif choice == "save_resume":
        return {"type": "info", "content": "✅ Your application has been saved for later."}
    elif choice == "explain_product":
        return {"type": "info", "content": "This product gives you easy access to checking and digital banking tools."}
    elif req.choice == "product_help":
    return {
        "type": "info",
        "content": (
            "🧾 Here's a quick breakdown:\n\n"
            "**Checking Account:** Great for daily transactions, no interest but easy access to money.\n\n"
            "**Savings Account:** Ideal for storing money long-term, earns interest, limited withdrawals.\n\n"
            "Still unsure? We can connect you with a banker!"
        )
    }
    else:
        return {"type": "info", "content": "We’re here to help!"}
