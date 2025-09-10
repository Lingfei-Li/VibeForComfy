"""
Constants and configuration for the vibe_for_comfy package.
"""

from typing import Dict, Tuple

# Package metadata
__version__ = "0.0.1"
__author__ = "vibe-for-comfy"
__email__ = "cslilingfei@outlook.com"

# Node category
NODE_CATEGORY = "Vibe for Comfy"

# Web directory for frontend assets
WEB_DIRECTORY = "./js"

# Folder mappings for the OpenFolders node
FOLDER_MAP: Dict[str, str] = {
    "loras": r"C:\Users\cslil\Documents\ComfyUI\models\loras",
    "embeddings": r"C:\Users\cslil\Documents\ComfyUI\models\embeddings", 
    "checkpoints": r"C:\Users\cslil\Documents\ComfyUI\models\checkpoints",
    "workflows": r"C:\Users\cslil\Documents\ComfyUI\user\default\workflows",
    "outputs": r"C:\Users\cslil\Documents\ComfyUI\output",
    "logs": r"C:\Users\cslil\AppData\Roaming\ComfyUI\logs",
}

# API endpoints
API_ENDPOINTS = {
    "open_folder": "/vibe_for_comfy/open_folder",
    "refresh": "/vibe_for_comfy/refresh",
}

# Frontend button configurations for OpenFolders node
FOLDER_BUTTONS: Tuple[Dict[str, str], ...] = (
    {"label": "LoRAs", "key": "loras"},
    {"label": "Embeddings", "key": "embeddings"},
    {"label": "Checkpoints", "key": "checkpoints"},
    {"label": "Workflows", "key": "workflows"},
    {"label": "Outputs", "key": "outputs"},
    {"label": "Logs", "key": "logs"},
)
