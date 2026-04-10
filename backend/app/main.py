"""Main entry point"""

import uvicorn
from app.config import get_settings


def main():
    """Run the application"""
    settings = get_settings()

    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )


if __name__ == "__main__":
    main()
