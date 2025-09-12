"""
Open In File Explorer node for opening paths in the system file explorer.

This module provides a node that opens a given file path in the system's default
file explorer (Windows Explorer, macOS Finder, or Linux file manager).
"""

import os
import platform
import subprocess
import sys
from inspect import cleandoc
from typing import Any, Dict
from .constants import NODE_CATEGORY


class OpenInFileExplorer:
    """
    OpenInFileExplorer: opens a given path in the system file explorer.
    
    This node takes a file or directory path as input and opens it in the
    system's default file explorer application.
    
    Inputs:
    - path: STRING - The file or directory path to open
    
    Outputs:
    - None (this is an action node with no outputs)
    """
    
    def __init__(self) -> None:
        """Initialize the OpenInFileExplorer node."""
        pass

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        """
        Define the input types for this node.
        
        Returns:
            Dictionary containing required input field configurations
        """
        return {
            "required": {
                "path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "forceInput": True
                }),
            }
        }

    RETURN_TYPES: tuple = ()
    RETURN_NAMES: tuple = ()
    DESCRIPTION: str = cleandoc(__doc__)
    FUNCTION: str = "open_path"
    CATEGORY: str = NODE_CATEGORY
    OUTPUT_NODE: bool = True

    def open_path(self, path: str) -> tuple:
        """
        Open the given path in the system file explorer.
        
        Args:
            path: The file or directory path to open
            
        Returns:
            Empty tuple (no outputs)
        """
        if not path or not path.strip():
            print("OpenInFileExplorer: No path provided")
            return ()
        
        path = path.strip()
        
        # Check if path exists
        if not os.path.exists(path):
            print(f"OpenInFileExplorer: Path does not exist: {path}")
            return ()
        
        try:
            system = platform.system().lower()
            
            # Determine if path is a file or directory
            if os.path.isfile(path):
                # If it's a file, open the containing folder and select the file
                folder_path = os.path.dirname(path)
                if system == "windows":
                    # Windows: use explorer with /select to highlight the file
                    os.startfile(folder_path)
                    # Also try to select the specific file
                    try:
                        subprocess.run(["explorer", "/select,", path], check=True)
                    except:
                        pass
                elif system == "darwin":
                    # macOS: use Finder to reveal the file
                    subprocess.run(["open", "-R", path], check=True)
                elif system == "linux":
                    # Linux: try common file managers
                    file_managers = ["xdg-open", "nautilus", "dolphin", "thunar", "pcmanfm"]
                    for manager in file_managers:
                        try:
                            subprocess.run([manager, folder_path], check=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                    else:
                        print(f"OpenInFileExplorer: No suitable file manager found on Linux")
                        return ()
                print(f"OpenInFileExplorer: Opened folder containing file: {path}")
            else:
                # If it's a directory, open it directly
                if system == "windows":
                    # Windows: use explorer
                    os.startfile(path)
                elif system == "darwin":
                    # macOS: use Finder
                    subprocess.run(["open", path], check=True)
                elif system == "linux":
                    # Linux: try common file managers
                    file_managers = ["xdg-open", "nautilus", "dolphin", "thunar", "pcmanfm"]
                    for manager in file_managers:
                        try:
                            subprocess.run([manager, path], check=True)
                            break
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            continue
                    else:
                        print(f"OpenInFileExplorer: No suitable file manager found on Linux")
                        return ()
                print(f"OpenInFileExplorer: Opened folder: {path}")
            
            if system not in ["windows", "darwin", "linux"]:
                print(f"OpenInFileExplorer: Unsupported operating system: {system}")
                return ()
            
        except Exception as e:
            print(f"OpenInFileExplorer: Error opening path '{path}': {str(e)}")
        
        return ()
