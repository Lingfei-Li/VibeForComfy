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
                "model_description": ("STRING", {
                    "forceInput": True,
                    "display": "Model Description",
                    "multiline": True
                }),
            },
            "optional": {
                "prompt": ("STRING", {
                    "forceInput": True, 
                    "multiline": True
                }),
            }
        }

        return input_types

    RETURN_TYPES: Tuple[str, str, str] = ("MODEL", "STRING", "STRING")
    RETURN_NAMES: Tuple[str, str, str] = ("model", "model_description", "prompt")
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
        model_description: str,
        prompt: str = ""
    ) -> Tuple[Any, str, str]:
        """
        Execute the LoRA loading and prompt enhancement.
        
        Args:
            model: The base model to apply LoRA to
            lora_name: Name of the LoRA file to load
            strength_model: Strength multiplier for the LoRA
            prompt: Existing prompt to combine with
            prompt_to_append: Additional prompt text to append
            notes: Notes about the LoRA application
            model_description: Current model description
            
        Returns:
            Tuple containing (modified_model, updated_model_description, enhanced_prompt)
        """
        
        model_with_lora, _ = LoraLoader().load_lora(model, None, lora_name, strength_model, None)
        
        # Build enhanced prompt
        prompt_parts = []
        if prompt:
            prompt_parts.append(prompt)
        if prompt_to_append:
            prompt_parts.append(prompt_to_append)
        
        enhanced_prompt = ", ".join(prompt_parts) if prompt_parts else ""
        
        # Update model description
        lora_info = f"LoRA: {lora_name} (strength: {strength_model})"
        
        if model_description:
            updated_description = f"{model_description}\n{lora_info}"
        else:
            updated_description = lora_info
        
        return (model_with_lora, updated_description, enhanced_prompt)
