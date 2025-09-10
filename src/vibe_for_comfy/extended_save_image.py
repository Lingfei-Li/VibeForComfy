"""
ExtendedSaveImage node: custom save that enforces a forced image input and a
string filename prefix, embeds metadata, and writes PNGs to the output folder.

Inputs:
- image: IMAGE (forceInput)
- filename_prefix: STRING
- positive_prompt: STRING (multiline)
- negative_prompt: STRING (multiline)
- steps: INT
- cfg: FLOAT
- sampler_name: STRING
- scheduler: STRING
- model_description: STRING (multiline)

Outputs:
- metadata: STRING - Formatted metadata as a string

Behavior:
- Computes the next sequence number for files with the given prefix in the
  output directory and generates filenames like: <prefix>_<seq>.png
- Embeds provided fields as PNG metadata and saves images in PNG format.
- Creates sidecar Markdown files with metadata for each saved image.
- Returns the metadata as a formatted string output.
"""

from inspect import cleandoc
from typing import Any, Dict
import os
import re
from pathlib import Path
from typing import Iterable, List, Tuple

from PIL import Image  # type: ignore
from PIL.PngImagePlugin import PngInfo  # type: ignore

from .constants import NODE_CATEGORY, FOLDER_MAP
from nodes import SaveImage


try:  # Optional, for tensor conversions
    import torch  # type: ignore
except Exception:  # pragma: no cover
    torch = None  # type: ignore
try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None  # type: ignore


class ExtendedSaveImage:
    """
    ExtendedLoadLoRA Node: Output node that saves provided images using ComfyUI's core SaveImage logic.

    This node simply enforces an image input and forwards the call to the
    upstream implementation for consistent file naming and output directory usage.
    """

    def __init__(self) -> None:
        pass


    # This node produces a metadata string output
    RETURN_TYPES: tuple = ("STRING",)
    RETURN_NAMES: tuple = ("metadata",)
    OUTPUT_NODE: bool = False
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "save"
    CATEGORY: str = NODE_CATEGORY

    @classmethod
    def IS_CHANGED(cls, **kwargs: Any) -> str:
        # Force re-run when inputs change by returning a string representation
        return str(hash(tuple(sorted(kwargs.items()))))

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True}),
                "filename_prefix": ("STRING", {"default": ""}),
                "positive_prompt": ("STRING", {"forceInput": True, "multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"forceInput": True, "multiline": True, "default": ""}),
                "steps": ("INT", {"forceInput": True, "default": 20, "min": 1, "max": 10000, "step": 1}),
                "cfg": ("FLOAT", {"forceInput": True, "default": 7.0, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sampler_name": ("STRING", {"forceInput": True, "default": "euler"}),
                "scheduler": ("STRING", {"forceInput": True, "default": "normal"}),
                "model_description": ("STRING", {"multiline": True, "forceInput": True, "default": ""}),
            }
        }

    def _to_pil_list(self, image: Any) -> List[Image.Image]:
        # Handle batch of images in common Comfy formats
        if isinstance(image, Image.Image):
            return [image]

        # If list/tuple of PIL
        if isinstance(image, (list, tuple)) and len(image) > 0 and isinstance(image[0], Image.Image):
            return list(image)

        # If dict-like with 'images'
        if isinstance(image, dict) and "images" in image:
            return self._to_pil_list(image["images"])  # type: ignore[index]

        # If torch tensor [B,H,W,C] float 0..1
        if torch is not None and isinstance(image, torch.Tensor):  # type: ignore[attr-defined]
            tensor = image
            if tensor.ndim == 3:
                tensor = tensor.unsqueeze(0)
            pil_images: List[Image.Image] = []
            for t in tensor:  # type: ignore[assignment]
                arr = t
                if arr.ndim == 3 and arr.shape[-1] in (1, 3, 4):
                    arr = arr.detach().cpu().clamp(0, 1)
                    arr = (arr * 255.0).round().byte().numpy()
                    if arr.shape[-1] == 1:
                        arr = arr[:, :, 0]
                    pil_images.append(Image.fromarray(arr))
            if pil_images:
                return pil_images

        # If numpy array [B,H,W,C]
        if np is not None and isinstance(image, np.ndarray):  # type: ignore[attr-defined]
            array = image
            if array.ndim == 3:
                array = np.expand_dims(array, 0)
            pil_images: List[Image.Image] = []
            for arr in array:
                arr = np.clip(arr, 0.0, 1.0)
                arr = (arr * 255.0).round().astype("uint8")
                if arr.shape[-1] == 1:
                    arr = arr[:, :, 0]
                pil_images.append(Image.fromarray(arr))
            if pil_images:
                return pil_images

        # Unknown format
        raise TypeError("Unsupported image format for saving")

    def _next_sequence_number(self, directory: Path, prefix: str) -> int:
        # Try to find the highest numeric suffix among files that start with prefix_
        # and end with .png, capturing the last digit group before the extension.
        pattern = re.compile(rf"^{re.escape(prefix)}_(?:.*?)(\d+)\.png$", re.IGNORECASE)
        max_n = 0
        if directory.exists():
            for name in os.listdir(directory):
                if not (name.lower().startswith(f"{prefix.lower()}_") and name.lower().endswith(".png")):
                    continue
                m = pattern.match(name)
                if m:
                    try:
                        n = int(m.group(1))
                        if n > max_n:
                            max_n = n
                    except ValueError:
                        continue
        # Start from max+1, but ensure we pick a filename that does not exist (robust to non-matching patterns)
        candidate = max_n + 1
        while (directory / f"{prefix}_{candidate:05d}.png").exists():
            candidate += 1
        return candidate

    def _build_pnginfo(self, metadata: Dict[str, Any]) -> PngInfo:
        info = PngInfo()
        for k, v in metadata.items():
            info.add_text(k, str(v))
        return info

    def _format_metadata_as_markdown(self, metadata: Dict[str, Any]) -> str:
        """Format metadata dictionary as Markdown."""
        lines = ["# Image Metadata", ""]
        
        for key, value in metadata.items():
            # Convert key to title case and replace underscores with spaces
            title = key.replace("_", " ").title()
            lines.append(f"## {title}")
            lines.append("")
            
            # Handle multiline strings (like prompts)
            if isinstance(value, str) and "\n" in value:
                lines.append("```")
                lines.append(value)
                lines.append("```")
            else:
                lines.append(str(value))
            
            lines.append("")
            lines.append("")  # Additional line break after each section
        
        return "\n".join(lines)

    def _format_metadata_as_string(self, metadata: Dict[str, Any]) -> str:
        """Format metadata dictionary as a readable string."""
        lines = []
        
        for key, value in metadata.items():
            # Convert key to title case and replace underscores with spaces
            title = key.replace("_", " ").title()
            lines.append(f"{title}: {value}")
        
        return "\n".join(lines)


    def save(
        self,
        image: Any,
        filename_prefix: str = "",
        positive_prompt: str = "",
        negative_prompt: str = "",
        steps: int = 20,
        cfg: float = 7.0,
        sampler_name: str = "euler",
        scheduler: str = "normal",
        model_description: str = "",
    ) -> tuple:
        output_dir = Path(FOLDER_MAP.get("outputs") or "./output").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        prefix = filename_prefix.strip() or "ComfyUI"
        seq = self._next_sequence_number(output_dir, prefix)

        pil_images = self._to_pil_list(image)
        saved_paths: List[str] = []


        SaveImage().save_image(image, filename_prefix)

        # Shared metadata
        meta = {
            "model_description": model_description,
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg": cfg,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
        }
        pnginfo = self._build_pnginfo(meta)

        for idx, im in enumerate(pil_images):
            # Ensure uniqueness per image (check existence again in case of concurrent writes)
            candidate = seq + idx
            while (output_dir / f"{prefix}_{candidate:05d}.png").exists():
                candidate += 1
            filename = f"{prefix}_{candidate:05d}.png"
            path = output_dir / filename
            im.save(path, format="PNG", pnginfo=pnginfo)
            saved_paths.append(str(path))

            # Write sidecar Markdown with the same base filename
            md_path = path.with_suffix('.md')
            try:
                with md_path.open('w', encoding='utf-8') as f:
                    markdown_content = self._format_metadata_as_markdown(meta)
                    f.write(markdown_content)
            except Exception:
                # Best-effort; do not fail the node if Markdown writing fails
                pass

        # Return the metadata as a formatted string
        metadata_string = self._format_metadata_as_string(meta)
        return (metadata_string,)


