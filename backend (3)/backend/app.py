from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.prediction_routes import router as prediction_router
from routes.chat_routes import router as chat_router
from routes.notes_routes import router as notes_router

app = FastAPI()

# -----------------------------
# 🔥 CORS — REQUIRED for frontend to connect
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 🏡 Home Route
# -----------------------------
@app.get("/")
def home():
    return {"status": "Backend Running"}

# -----------------------------
# 🔗 API Routers
# -----------------------------
app.include_router(prediction_router)
app.include_router(chat_router)
app.include_router(notes_router)
