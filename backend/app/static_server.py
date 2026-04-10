"""Static file server for frontend"""

import os
from pathlib import Path
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles


def mount_frontend_static(app, frontend_dist: Path):
    """Mount frontend static files"""

    if not frontend_dist.exists():
        print(f"Warning: Frontend dist not found at {frontend_dist}")
        return

    # Mount static assets
    app.mount(
        "/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets"
    )

    # Serve index.html for all other routes (SPA)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            # Let API routes handle this
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not found")

        # Try to serve the file
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Fall back to index.html for SPA routing
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(index_path, media_type="text/html")

        # If nothing found, serve index.html
        return FileResponse(index_path, media_type="text/html")
