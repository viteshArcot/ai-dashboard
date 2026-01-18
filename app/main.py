from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(
    title="AI-Powered Data Insights Dashboard",
    description="Backend API for data analysis and visualization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for charts
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "AI-Powered Data Insights Dashboard API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}