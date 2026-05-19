from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import hcp_routes, interaction_routes, chat_routes
from app.models.models import HCP, Interaction, FollowUp

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="Healthcare Professional Management System with AI-powered Interaction Logging",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(hcp_routes.router)
app.include_router(interaction_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI-First CRM HCP Module",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
