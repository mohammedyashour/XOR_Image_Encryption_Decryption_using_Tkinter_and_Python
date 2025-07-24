"""
File utility functions for the encryption application.
Handles file dialogs, file extension operations, and other file-related tasks.
"""

import os
from tkinter import filedialog

# File type definitions
IMAGE_FILETYPES = [("Image files", "*.jpg *.jpeg *.png *.bmp")]
VIDEO_FILETYPES = [("Video files", "*.mp4 *.avi *.mov *.mkv")]
ENCRYPTED_FILETYPES = [("Encrypted files", "*.bin")]
ALL_SUPPORTED_FILETYPES = [
    ("All supported files", "*.jpg *.jpeg *.png *.bmp *.mp4 *.avi *.mov *.mkv *.bin"),
    *IMAGE_FILETYPES,
    *VIDEO_FILETYPES,
    *ENCRYPTED_FILETYPES
]

# File extension mappings
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']
ENCRYPTED_EXTENSION = '.bin'

def is_image_file(file_path):
    """Check if the file is an image based on its extension."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext in IMAGE_EXTENSIONS

def is_video_file(file_path):
    """Check if the file is a video based on its extension."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext in VIDEO_EXTENSIONS

def is_encrypted_file(file_path):
    """Check if the file is an encrypted file based on its extension."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext == ENCRYPTED_EXTENSION

def get_original_extension(file_path):
    """
    Try to determine the original extension of an encrypted file
    based on naming convention or metadata.
    """
    # For now, we'll assume it's an image file (.jpg)
    # In a more advanced implementation, we could store the original extension
    # in the encrypted file's metadata or filename
    return '.jpg'

def browse_for_file(file_types=None):
    """Open a file dialog and return the selected file path."""
    if file_types is None:
        file_types = ALL_SUPPORTED_FILETYPES
    
    file_path = filedialog.askopenfilename(filetypes=file_types)
    return file_path if file_path else None

def get_file_info(file_path):
    """Get file information including name, directory, and extension."""
    if not file_path:
        return None
    
    file_name = os.path.basename(file_path)
    directory = os.path.dirname(file_path)
    base_name, extension = os.path.splitext(file_name)
    
    return {
        'full_path': file_path,
        'directory': directory,
        'file_name': file_name,
        'base_name': base_name,
        'extension': extension.lower()
    }

def rename_file(file_path, new_extension):
    """Rename a file with a new extension and return the new path."""
    if not file_path:
        return None
    
    file_info = get_file_info(file_path)
    new_path = os.path.join(
        file_info['directory'], 
        f"{file_info['base_name']}{new_extension}"
    )
    
    try:
        os.rename(file_path, new_path)
        return new_path
    except Exception as e:
        print(f"Error renaming file: {str(e)}")
        return None