"""
ExtendedLoadCheckpoint node: extends ComfyUI's default load checkpoint with model description output.

Overview:
- Loads a checkpoint file and returns MODEL, CLIP, and VAE components like the default node
- Additionally returns a model description string containing the checkpoint name
- Uses ComfyUI core checkpoint loading functionality

Inputs:
- ckpt_name: STRING (checkpoint filename)

Outputs:
- MODEL: Loaded model component
- CLIP: Loaded CLIP component  
- VAE: Loaded VAE component
- STRING: Model description containing checkpoint name
"""

from inspect import cleandoc
from typing import Any, Dict, Tuple
import folder_paths
import comfy.sd
from .constants import NODE_CATEGORY


class ExtendedLoadCheckpoint:
    """
    ExtendedLoadCheckpoint Node: returns model description along with standard outputs.

    This node loads a checkpoint file and returns the standard MODEL, CLIP, and VAE components
    like ComfyUI's default Load Checkpoint node, but also provides a model description string
    that records the name of the loaded checkpoint.

    Inputs:
    - ckpt_name: STRING (checkpoint filename to load)

    Outputs:
    - MODEL: Loaded model component
    - CLIP: Loaded CLIP component
    - VAE: Loaded VAE component
    - STRING: Model description containing checkpoint name
    """

    def __init__(self) -> None:
        """Initialize the ExtendedLoadCheckpoint node."""
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        """
        Define the input types for this node.
        
        Returns:
            Dictionary containing required input field configurations
        """
        # Get list of available checkpoint files
        checkpoints = folder_paths.get_filename_list("checkpoints")
        
        return {
            "required": {
                "ckpt_name": (checkpoints, {"default": checkpoints[0] if checkpoints else ""}),
            }
        }

    RETURN_TYPES: Tuple[str, str, str, str] = ("MODEL", "STRING", "CLIP", "VAE")
    RETURN_NAMES: Tuple[str, ...] = ("model", "model_description", "clip", "vae")
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "load_checkpoint"
    CATEGORY: str = NODE_CATEGORY

    def load_checkpoint(self, ckpt_name: str) -> Tuple[Any, str, Any, Any]:
        """
        Load a checkpoint and return model components with description.
        
        Args:
            ckpt_name: Name of the checkpoint file to load
            
        Returns:
            Tuple containing (model, model_description, clip, vae)
        """
        # Load the checkpoint using ComfyUI's standard method
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        if ckpt_path is None:
            raise FileNotFoundError(f"Checkpoint file not found: {ckpt_name}")
        
        # Load checkpoint components
        # The function returns (model, clip, vae, config) - 4 values, not 3
        model, clip, vae, config = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        
        # Create model description string
        model_description = f"Checkpoint: {ckpt_name}"
        
        return (model, model_description, clip, vae)
