from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Legal Metrology Compliance Checker",
    description="Backend API for AI-assisted packaged commodity compliance inspection.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "name": "AI-Powered Legal Metrology Compliance Checker",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "api",
    }