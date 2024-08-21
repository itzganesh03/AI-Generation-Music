from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from helpers import make_audio_list, make_image_list

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the Card and CardDetails models
class Card(BaseModel):
    title: str
    description: str
    audioUrl: str
    imageUrl: str

class CardDetails(BaseModel):
    cards: List[Card]

# Global variable to store card details
stored_card_details = None

# Serve a simple HTML response
@app.get("/")
async def serve_html():
    return {"message": "Hello! This is your server."}

# Handle the submission of card details
@app.post("/submit")
async def submit_handler(card_details: CardDetails):
    global stored_card_details
    # Store the card details in the global variable
    stored_card_details = card_details
    print(f"Received card details: {card_details}")
    return {"status": "success"}

# Fetch and return card details, then reset the stored details
@app.get("/cards")
async def fetch_cards_handler():
    global stored_card_details
    if stored_card_details is None:
        raise HTTPException(status_code=404, detail="No card details available")
    
    response = stored_card_details
    stored_card_details = None

    make_audio_list(response)
    make_image_list(response)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8080)