import uvicorn

from src.app import settings

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # app = setup_application()
    uvicorn.run(
        "src.app:setup_application",
        workers=settings.app.workers_count,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        log_config=None,
        factory=True,
        log_level="critical",
        reload_dirs=["./src"],
    )
