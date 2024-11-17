from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import uuid
import datetime

app = FastAPI()

# Allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample Stoic phrases with IDs
STOIC_PHRASES = [
    {"id": str(uuid.uuid4()), "phrase": "The best revenge is not to be like your enemy. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "He who fears death will never do anything worth of a man who is alive. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "Wealth consists not in having great possessions, but in having few wants. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "You have power over your mind - not outside events. Realize this, and you will find strength. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "How long are you going to wait before you demand the best for yourself? — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "Don’t explain your philosophy. Embody it. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "Man is disturbed not by things, but by the views he takes of them. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "Waste no more time arguing what a good man should be. Be one. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "The more we value things outside our control, the less control we have. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "If it is not right, do not do it, if it is not true, do not say it. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "It does not matter what you bear, but how you bear it. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "Luck is what happens when preparation meets opportunity. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "Difficulty strengthens the mind as labor does the body. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "The happiness of your life depends upon the quality of your thoughts. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "First say to yourself what you would be; and then do what you have to do. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "Begin at once to live, and count each separate day as a separate life. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "We suffer more often in imagination than in reality. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "No man is free who is not master of himself. — Epictetus"},
    {"id": str(uuid.uuid4()), "phrase": "Choose not to be harmed—and you won’t feel harmed. Don’t feel harmed—and you haven’t been. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "To love only what happens, what was destined. No greater harmony. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "What we do now echoes in eternity. — Marcus Aurelius"},
    {"id": str(uuid.uuid4()), "phrase": "Nothing, to my way of thinking, is a better proof of a well-ordered mind than a man’s ability to stop just where he is and pass some time in his own company. — Seneca"},
    {"id": str(uuid.uuid4()), "phrase": "Freedom is the only worthy goal in life. It is won by disregarding things that lie beyond our control. — Epictetus"},
]

# Function to map current time to a specific Stoic phrase with added randomness
def get_stoic_phrase_based_on_time():
    current_time = datetime.datetime.now()
    
    # Use only hour and minute for the seed calculation
    random_seed = (current_time.hour * 60 + current_time.minute + random.randint(0, 1000)) % len(STOIC_PHRASES)
    
    # Select the phrase based on the random seed
    return STOIC_PHRASES[random_seed]

# Store pinned phrases
user_pinned_phrases = []  # List of dictionaries with 'id' and 'phrase'

class PinRequest(BaseModel):
    id: str
    phrase: str

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send a random Stoic phrase
            phrase = get_stoic_phrase_based_on_time()
            await websocket.send_text(phrase)
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        print("Client disconnected")

@app.post("/pin")
async def pin_phrase(request: PinRequest):
    # Avoid duplicate phrases
    if any(pinned["id"] == request.id for pinned in user_pinned_phrases):
        return {"message": "Phrase already pinned!"}
    
    # Add to pinned list
    user_pinned_phrases.append({"id": request.id, "phrase": request.phrase})
    return {"message": "Phrase pinned successfully!"}

@app.get("/pinned")
async def get_pinned_phrases():
    return {"pinned_phrases": user_pinned_phrases}
