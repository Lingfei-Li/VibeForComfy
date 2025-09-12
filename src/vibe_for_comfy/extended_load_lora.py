"""
ExtendedLoadLoRA node for applying LoRA models with prompt enhancement.

This module provides nodes for loading and applying LoRA models with enhanced functionality
including prompt management and model description tracking.
"""

from inspect import cleandoc
from typing import Any, Dict, List, Tuple
import folder_paths
from .constants import NODE_CATEGORY
import comfy.sd
import comfy.lora
from nodes import LoraLoader
import os

class ExtendedLoadLoRA:
    """
    ExtendedLoadLoRA: loads and applies LoRA models with enhanced functionality.
    
    This node allows users to
    - Select a LoRA model from available models
    - Apply it to a base model with configurable strength
    - Append custom prompts and notes
    - Combine with existing prompts
    - Track model description with LoRA information
    
    The node outputs the modified model, enhanced prompt string, and updated model description.
    """
    
    def __init__(self) -> None:
        """Initialize the ExtendedLoadLoRA node."""
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        """
        Define the input types for this node.
        
        Returns:
            Dictionary containing required and optional input field configurations
        """
        # Get list of available LoRA files
        loras: List[str] = folder_paths.get_filename_list("loras")
        
        input_types = {
            "required": {
                "model": ("MODEL", {"forceInput": True}),
                "lora_name": (loras, {"default": loras[0] if loras else "None"}),
                "strength_model": ("FLOAT", {
                    "default": 1.0, 
                    "min": -20.0, 
                    "max": 20.0, 
                    "step": 0.05
                }),
                "prompt_to_append": ("STRING", {
                    "display": "Prompt to append", 
                    "multiline": True
                }),
                "notes": ("STRING", {
                    "display": "Notes", 
                    "multiline": True
                }),
            },
            "optional": {
                "prompt": ("STRING", {
                    "forceInput": True, 
                    "multiline": True
                }),
                "loaded_lora_names_list": ("CUSTOM_LORA_LIST", {"forceInput": True}),
            }
        }

        return input_types

    RETURN_TYPES: Tuple[str, str, str, str] = ("MODEL", "STRING", "CUSTOM_LORA_LIST")
    RETURN_NAMES: Tuple[str, str, str, str] = ("model", "prompt", "lora_list")
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "exec"
    CATEGORY: str = NODE_CATEGORY

    def exec(
        self, 
        model: Any, 
        lora_name: str, 
        strength_model: float, 
        prompt_to_append: str, 
        notes: str,
        prompt: str = "",
        loaded_lora_names_list: List[str] = []
    ) -> Tuple[Any, str, str, str]:
        
        model_with_lora, _ = LoraLoader().load_lora(model, None, lora_name, strength_model, None)
        
        # Build enhanced prompt
        prompt_parts = []
        if prompt:
            prompt_parts.append(prompt)
        if prompt_to_append:
            prompt_parts.append(prompt_to_append)
        
        enhanced_prompt = "\n".join(prompt_parts) if prompt_parts else ""
        
        # Update lora list - work with list of strings
        new_lora_entry = f"{lora_name}:{strength_model}"            
        
        return (model_with_lora, enhanced_prompt, loaded_lora_names_list + [new_lora_entry])
