from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chat_routes import router as chat_router
from app.router_chatbot import router as chatbot_router
from app.test_routes import router as test_router


app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "HealthTrackIA Backend (MongoDB) OK"}


app.include_router(chat_router)
app.include_router(chatbot_router)
app.include_router(test_router)
