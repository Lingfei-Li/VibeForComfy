"""
StringListJoiner node for combining multiple string inputs.
"""

from inspect import cleandoc
from typing import Dict, Any, Tuple
from .constants import NODE_CATEGORY


class StringListJoiner:
    """
    A ComfyUI node for joining multiple string inputs into a single string.
    
    This node dynamically creates input slots for string values and combines
    them into a single output string, filtering out empty values.
    """
    
    def __init__(self) -> None:
        """Initialize the StringListJoiner node."""
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        """
        Define the input types for this node.
        
        Returns:
            Dictionary containing required input field configurations
        """
        input_types = {
            "required": {
                "arg1": ("STRING", {"forceInput": True}),
            },
        }

        return input_types

    RETURN_TYPES: Tuple[str] = ("STRING",)
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "join"
    CATEGORY: str = NODE_CATEGORY

    def join(self, **kwargs: str) -> Tuple[str]:
        """
        Join multiple string inputs into a single string.
        
        Args:
            **kwargs: Variable number of string arguments to join
            
        Returns:
            Tuple containing the joined string
        """
        # Filter out empty strings and join with newlines
        separator = "\n"
        non_empty_strings = [s for s in kwargs.values() if s and s.strip()]
        result = separator.join(non_empty_strings)
        return (result,)

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""