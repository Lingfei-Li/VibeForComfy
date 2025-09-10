"""
WorkflowSnapshot node that takes sampler-related inputs and returns them unchanged.
"""

from inspect import cleandoc
from typing import Dict, Any, Tuple, List
from .constants import NODE_CATEGORY


class WorkflowSnapshot:
    """
    Pass-through node for capturing a snapshot of workflow sampler configuration.

    Inputs:
    - positive_prompt: STRING
    - negative_prompt: STRING
    - model: MODEL
    - steps: INT
    - cfg: FLOAT
    - sampler_name: COMBO of available sampler names
    - scheduler: COMBO of available schedulers

    Outputs (same as inputs, order standardized):
    - MODEL
    - STRING (positive_prompt)
    - STRING (negative_prompt)
    - INT (steps)
    - FLOAT (cfg)
    - COMBO (sampler_name)
    - COMBO (scheduler)
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        sampler_names: List[str] = [
            "euler", "euler_a", "dpm++_2m", "dpm++_sde", "heun", "lms"
        ]
        schedulers: List[str] = [
            "normal", "karras", "exponential", "polyexponential"
        ]

        return {
            "required": {
                "positive_prompt": ("STRING", {"multiline": True, "display": "Positive Prompt"}),
                "negative_prompt": ("STRING", {"multiline": True, "display": "Negative Prompt"}),
                "model": ("MODEL", {"forceInput": True}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 200, "step": 1}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 30.0, "step": 0.5}),
                "sampler_name": ("COMBO", {"choices": sampler_names, "default": sampler_names[0]}),
                "scheduler": ("COMBO", {"choices": schedulers, "default": schedulers[0]}),
            }
        }

    RETURN_TYPES: Tuple[str, ...] = ("MODEL", "STRING", "STRING", "INT", "FLOAT", "COMBO", "COMBO")
    RETURN_NAMES: Tuple[str, ...] = ("model", "positive_prompt", "negative_prompt", "steps", "cfg", "sampler_name", "scheduler")
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "snapshot"
    CATEGORY: str = NODE_CATEGORY

    def snapshot(
        self,
        positive_prompt: str,
        negative_prompt: str,
        model: Any,
        steps: int,
        cfg: float,
        sampler_name: str,
        scheduler: str,
    ) -> Tuple[Any, str, str, int, float, str, str]:
        return (
            model,
            positive_prompt,
            negative_prompt,
            steps,
            cfg,
            sampler_name,
            scheduler,
        )


