from fastapi import FastAPI
from app.chat_routes import router as chat_router



app = FastAPI()


@app.get("/")
def home():
    return {"message": "HealthTrackIA Backend (MongoDB) OK"}


app.include_router(chat_router)
