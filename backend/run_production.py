import uvicorn
import os

if __name__ == "__main__":
    # Production settings
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # No reload in production
        workers=4 if os.getenv("WORKERS") is None else int(os.getenv("WORKERS")),
        log_level="info"
    )
