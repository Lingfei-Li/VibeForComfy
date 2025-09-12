"""
ExtendedKSampler node: wraps core KSampler, encodes prompts with CLIP, and decodes with VAE.

Overview:
- Uses ComfyUI core `CLIPTextEncode` to encode the provided `positive_prompt` and `negative_prompt` with the given `clip`.
- Calls ComfyUI core `common_ksampler` with the encoded positive/negative conditionings.
- Uses ComfyUI core `VAEDecode` to decode the sampled latents into an image.

Inputs (all in "required"):
- model: MODEL
- seed: INT
- steps: INT
- cfg: FLOAT
- sampler_name: COMBO
- scheduler: COMBO
- clip: CLIP (forceInput)
- latent: LATENT (initial latent)
- denoise: FLOAT (0..1)
- vae: VAE (forceInput)
- positive_prompt: STRING (forceInput)
- negative_prompt: STRING (forceInput)

Outputs:
- IMAGE: Decoded image via VAE (final generated image)
- STRING: Positive prompt (passthrough)
- STRING: Negative prompt (passthrough)
- INT: Steps (passthrough)
- FLOAT: CFG (passthrough)
- COMBO: Sampler name (passthrough)
- COMBO: Scheduler name (passthrough)
"""

from inspect import cleandoc
from typing import Any, Dict, Tuple
from .constants import NODE_CATEGORY
import comfy.samplers


try:
    # ComfyUI core nodes module
    from nodes import common_ksampler  # type: ignore
    from nodes import VAEDecode  # type: ignore
    from nodes import CLIPTextEncode  # type: ignore
except Exception as import_error:  # pragma: no cover
    common_ksampler = None  # type: ignore
    VAEDecode = None  # type: ignore
    CLIPTextEncode = None  # type: ignore


class ExtendedKSampler:
    """
    ExtendedKSampler Node: returns the sampled image and latent along with key settings.

    Inputs:
    - model: MODEL
    - seed: INT
    - steps: INT
    - cfg: FLOAT
    - sampler_name: COMBO
    - scheduler: COMBO
    - clip: CLIP
    - latent_image: LATENT
    - denoise: FLOAT
    - vae: VAE
    - positive_prompt: STRING (for metadata/output convenience)
    - negative_prompt: STRING (for metadata/output convenience)

    Outputs:
    - IMAGE: Sampled image
    - STRING: Positive prompt
    - STRING: Negative prompt
    - INT: Steps
    - FLOAT: CFG
    - COMBO: Sampler name
    - COMBO: Scheduler name
    - MODEL: Model used (passthrough)
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:

        return {
            "required": {
                "model": ("MODEL", {"forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 200, "step": 1}),
                "cfg": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 30.0, "step": 0.5}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "clip": ("CLIP", {"forceInput": True}),
                "latent": ("LATENT", {"forceInput": True}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "vae": ("VAE", {"forceInput": True}),
                "positive_prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "negative_prompt": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES: Tuple[str, ...] = ("IMAGE",)
    RETURN_NAMES: Tuple[str, ...] = ("image",)
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "run"
    CATEGORY: str = NODE_CATEGORY

    def run(
        self,
        model: Any,
        seed: int,
        steps: int,
        cfg: float,
        sampler_name: str,
        scheduler: str,
        clip: Any,
        latent: Any,
        denoise: float,
        vae: Any,
        positive_prompt: str,
        negative_prompt: str,
    ) -> Tuple[Any]:
        if common_ksampler is None or VAEDecode is None or CLIPTextEncode is None:
            raise RuntimeError("ComfyUI core nodes module is not available: required imports failed")

        # Encode prompts using CLIP (unwrap to first element which is CONDITIONING)
        text_encoder = CLIPTextEncode()
        positive_cond_out = text_encoder.encode(clip, positive_prompt)
        negative_cond_out = text_encoder.encode(clip, negative_prompt)

        positive_cond = positive_cond_out[0] if isinstance(positive_cond_out, (list, tuple)) else positive_cond_out
        negative_cond = negative_cond_out[0] if isinstance(negative_cond_out, (list, tuple)) else negative_cond_out

        ks_result = common_ksampler(
            model=model,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name=sampler_name,
            scheduler=scheduler,
            positive=positive_cond,
            negative=negative_cond,
            latent=latent,
            denoise=denoise,
        )

        # Some Comfy versions return only samples, others return (samples, latent)
        if isinstance(ks_result, tuple):
            samples = ks_result[0]
        else:
            samples = ks_result

        # Decode to image using provided VAE
        decoder = VAEDecode()
        decoded_image_tuple = decoder.decode(vae, samples)
        decoded_image = decoded_image_tuple[0] if isinstance(decoded_image_tuple, tuple) else decoded_image_tuple

        return (decoded_image,)


