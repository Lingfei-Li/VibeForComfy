"""
Top-level package for vibe_for_comfy.

This package provides ComfyUI nodes for enhanced workflow management,
including LoRA loading with prompt enhancement and folder management utilities.
"""

from typing import Dict, Type, Any

# Import package metadata from constants
from .src.vibe_for_comfy.constants import (
    __version__,
    __author__, 
    __email__,
    WEB_DIRECTORY
)

# Import node classes
from .src.vibe_for_comfy.nodes import StringListJoiner
from .src.vibe_for_comfy.open_folders import OpenFolders
from .src.vibe_for_comfy.open_file_explorer import OpenInFileExplorer
from .src.vibe_for_comfy.extended_load_lora import ExtendedLoadLoRA
from .src.vibe_for_comfy.workflow_snapshot import WorkflowSnapshot
from .src.vibe_for_comfy.extended_ksampler import ExtendedKSampler
from .src.vibe_for_comfy.extended_save_image import (
    ExtendedSaveImage,
    ImageMetadataReader,
    SDParameterGenerator,
    SDTypeConverter,
)
from .src.vibe_for_comfy.extended_load_checkpoint import ExtendedLoadCheckpoint

# Import and register routes
from .src.vibe_for_comfy.routes import register_routes

# Package exports
__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS", 
    "WEB_DIRECTORY",
    "__version__",
    "__author__",
    "__email__",
]

# Node class mappings for ComfyUI
# NOTE: Node names should be globally unique across all ComfyUI custom nodes
NODE_CLASS_MAPPINGS: Dict[str, Type[Any]] = {
    "ExtendedLoadLoRA": ExtendedLoadLoRA,
    "StringListJoiner": StringListJoiner,
    "OpenFolders": OpenFolders,
    "OpenInFileExplorer": OpenInFileExplorer,
    "WorkflowSnapshot": WorkflowSnapshot,
    "ExtendedKSampler": ExtendedKSampler,
    "ExtendedSaveImage": ExtendedSaveImage,
    "ExtendedLoadCheckpoint": ExtendedLoadCheckpoint,
    "ImageMetadataReader": ImageMetadataReader,
    "SDParameterGenerator": SDParameterGenerator,
    "SDTypeConverter": SDTypeConverter,
}

# Human-readable display names for the nodes
NODE_DISPLAY_NAME_MAPPINGS: Dict[str, str] = {
    "ExtendedLoadLoRA": "Extended Load LoRA",
    "ExtendedKSampler": "Extended KSampler",
    "ExtendedSaveImage": "Extended Save Image",
    "ExtendedLoadCheckpoint": "Extended Load Checkpoint",
    "StringListJoiner": "String List Joiner", 
    "OpenFolders": "Open Folders",
    "OpenInFileExplorer": "Open In File Explorer",
    "WorkflowSnapshot": "Workflow Snapshot",
    "ImageMetadataReader": "Image Metadata Reader",
    "SDParameterGenerator": "SD Parameter Generator",
    "SDTypeConverter": "SD Type Converter",
}

# Register backend routes
register_routes()

