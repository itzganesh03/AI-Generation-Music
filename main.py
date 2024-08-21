from fastapi import FastAPI, HTTPException, Request
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

# Global variable to store card details
stored_card_details = None

# Serve a simple HTML response
@app.get("/")
async def serve_html():
    return {"message": "Hello! This is your server."}

# Handle the submission of card details
@app.post("/submit")
async def submit_handler(data:Request):
    global stored_card_details
    # Store the card details in the global variable
    stored_card_details = await data.json()
    print(f"Received card details: {stored_card_details}")
    make_image_list(stored_card_details['cards'])
    make_audio_list(stored_card_details['cards'])
    stored_card_details={'cards': [{'title': 'Generated Output', 'description': 'Generated Output', 'audioUrl': 'file:///D:/PY_PROGS/AIGenerationMusic.github.io/output.mp3', 'imageUrl': 'file:///D:/PY_PROGS/AIGenerationMusic.github.io/test.jpg'}]}
    return {"status": "success"}

# Fetch and return card details, then reset the stored details
@app.get("/cards")
async def fetch_cards_handler():
    global stored_card_details
    if stored_card_details is None:
        raise HTTPException(status_code=404, detail="No card details available")
    
    response = stored_card_details
    stored_card_details = None
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8080)