from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random
import uuid

# Initialize FastAPI with lifespan explicitly
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

# Store pinned phrases
user_pinned_phrases = []  # List of dictionaries with 'id' and 'phrase'
active_connections = []  # List of WebSocket connections
current_phrase = random.choice(STOIC_PHRASES)  # Initial phrase to send

class PinRequest(BaseModel):
    id: str
    phrase: str

# Background task to update the phrase every 30 seconds
async def update_phrase_periodically():
    global current_phrase
    while True:
        # Pick a random quote from the list
        current_phrase = random.choice(STOIC_PHRASES)
        
        # Broadcast the updated phrase to all connected clients
        for connection in active_connections:
            await connection.send_json(current_phrase)
        
        # Wait 30 seconds before updating again
        await asyncio.sleep(30)

# FastAPI's lifespan management
@app.on_event("startup")
async def start_background_task():
    # Start the background task when the server starts
    asyncio.create_task(update_phrase_periodically())

@app.on_event("shutdown")
async def shutdown():
    # Here you could implement graceful shutdown if necessary
    pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send the current phrase to the client as soon as they connect
        await websocket.send_json(current_phrase)
        
        # Keep the connection alive, waiting for client messages (if any)
        while True:
            await asyncio.sleep(100)

    except WebSocketDisconnect:
        active_connections.remove(websocket)
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