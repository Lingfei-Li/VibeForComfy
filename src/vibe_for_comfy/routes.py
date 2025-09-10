"""
Backend routes for the vibe_for_comfy package.
"""

import os
import sys
import subprocess
from typing import Dict, Any
from aiohttp import web

from .constants import FOLDER_MAP, API_ENDPOINTS


def open_folder_in_explorer(path: str) -> None:
    """
    Open a folder in the system's default file explorer.
    
    Args:
        path: The path to the folder to open
        
    Raises:
        OSError: If the folder cannot be opened
    """
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


async def open_folder_handler(request: web.Request) -> web.Response:
    """
    Handle requests to open folders by key.
    
    Args:
        request: The HTTP request containing the folder key
        
    Returns:
        JSON response indicating success or failure
    """
    try:
        data = await request.json()
        key = data.get("key")
        
        if not key:
            return web.json_response(
                {"success": False, "error": "Missing 'key' parameter"}, 
                status=400
            )
            
        path = FOLDER_MAP.get(key)
        if not path:
            return web.json_response(
                {"success": False, "error": f"Invalid key: {key}"}, 
                status=400
            )
            
        open_folder_in_explorer(path)
        return web.json_response({"success": True})
        
    except Exception as e:
        return web.json_response(
            {"success": False, "error": str(e)}, 
            status=500
        )


def register_routes() -> None:
    """
    Register all backend routes with the ComfyUI server.
    
    This function should be called during package initialization.
    """
    try:
        from server import PromptServer
        
        PromptServer.instance.routes.post(API_ENDPOINTS["open_folder"])(open_folder_handler)
        
    except ImportError:
        # In test or non-server contexts, importing PromptServer may fail
        pass
