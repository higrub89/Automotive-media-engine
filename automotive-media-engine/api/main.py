from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router as video_router

app = FastAPI(
    title="RYA.ai Backend",
    description="Automated Media Engine API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "RYA.ai Media Engine",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
