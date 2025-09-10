from inspect import cleandoc


class OpenFolders:
    """
    OpenFolders Node: Utility node exposing buttons (frontend) to open common ComfyUI folders.

    Buttons are added via the frontend extension and trigger a backend route
    with a key indicating which folder to open.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # No inputs; all actions are via buttons
        return {"required": {}}

    RETURN_TYPES = tuple()
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "noop"
    CATEGORY = "Vibe for Comfy"

    def noop(self):
        return tuple()


