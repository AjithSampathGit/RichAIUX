from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepRequest(BaseModel):
    step: str

class HelpRequest(BaseModel):
    choice: str

@app.post("/ai-suggestion")
def ai_suggestion(req: StepRequest):
    user_states = ["idle", "confused", "interested", "disinterested"]
    user_state = random.choice(user_states)
    suggestion_map = {
        "select-product": ["product_helper"],
        "upload-id": ["save_resume", "live_banker"],
        "terms": ["live_banker", "schedule_appointment"],
        "funding": ["explain_product"],
        "thank-you": ["survey"]
    }
    return {"user_state": user_state, "suggestions": suggestion_map.get(req.step, [])}

@app.post("/ai-help")
def ai_help(req: HelpRequest):
    if req.choice == "fraud_check":
        flagged = random.choice([True, False, False])  # 33% chance fraud
        if flagged:
            return {"type": "fraud"}
        return {"type": "info", "content": "ID verified successfully."}

    if req.choice == "product_helper":
        return {
            "type": "info",
            "content": (
                "🔍 **Checking** is ideal for everyday spending, "
                "while **Savings** helps grow money over time with interest. "
                "AI recommends checking for direct deposits and savings for long-term goals."
            )
        }

    if req.choice == "live_banker":
        return {
            "type": "chatbot",
            "agent_name": "Morgan",
            "agent_avatar": "https://i.imgur.com/AItCxSs.png",
            "messages": ["Hi! I’m Morgan, your virtual banker. How can I assist you today?"]
        }

    if req.choice == "schedule_appointment":
        return {
            "type": "calendar",
            "slots": ["July 8, 10 AM", "July 8, 3 PM", "July 9, 1 PM"]
        }

    if req.choice == "survey":
        return {
            "type": "survey",
            "questions": [
                "What did you like about the experience?",
                "What can we improve?",
                "Would you recommend this process?"
            ]
        }

    if req.choice == "explain_product":
        return {
            "type": "info",
            "content": "Funding allows you to deposit money into your new account using debit, credit, or transfer."
        }

    if req.choice == "save_resume":
        return {"type": "info", "content": "✅ Your application has been saved. You can continue later."}

    return {"type": "info", "content": "We'll assist you shortly."}
