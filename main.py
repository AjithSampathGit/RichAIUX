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
    if req.choice == "live_banker":
        return {
            "type": "chatbot",
            "agent_name": "Morgan",
            "agent_avatar": "https://i.imgur.com/AItCxSs.png",
            "messages": ["Hi, I’m Morgan, your live banker. How can I assist you today?"]
        }
    elif req.choice == "save_resume":
        return {"type": "info", "content": "Your session has been saved. You can resume later."}
    elif req.choice == "schedule_appointment":
        return {
            "type": "calendar",
            "slots": ["July 7, 10 AM", "July 7, 3 PM", "July 8, 1 PM"]
        }
    elif req.choice == "survey":
        return {
            "type": "survey",
            "questions": [
                "What did you find helpful?",
                "What can we improve?",
                "Would you recommend this to others?"
            ]
        }
    elif req.choice == "Product Helper":
        return {
            "type": "product-help",
            "content": (
                "🧾 *Checking*: Best for daily use, debit card purchases, and paying bills.\n\n"
                "💰 *Savings*: Ideal for earning interest and saving money over time.\n\n"
                "Choose what suits your needs! 💡"
            )
        }
    else:
        return {"type": "info", "content": "We'll assist you shortly."}
