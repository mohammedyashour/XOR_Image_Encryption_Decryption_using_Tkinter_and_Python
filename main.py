"""
Main entry point for the File Encryptor application.
Connects all modules and starts the application.
"""

import tkinter as tk
import threading
from core.image_crypto import ImageCrypto
from core.video_crypto import VideoCrypto
from gui.app_ui import EncryptionView
from utils import file_utils

class EncryptionController:
    """
    Controller class that connects the model (crypto modules) and view (UI).
    Handles user interactions and business logic.
    """
    def __init__(self, root):
        """
        Initialize the controller with models and view.
        
        Args:
            root: The Tkinter root window
        """
        # Initialize models
        self.image_crypto = ImageCrypto()
        self.video_crypto = VideoCrypto()
        
        # Initialize view
        self.view = EncryptionView(root)
        
        # Bind events
        self.bind_events()
    
    def bind_events(self):
        """Bind UI events to controller methods"""
        # Bind welcome screen buttons
        self.view.encrypt_image_button.config(command=self.show_encrypt_image_screen)
        self.view.decrypt_image_button.config(command=self.show_decrypt_image_screen)
        self.view.encrypt_video_button.config(command=self.show_encrypt_video_screen)
        self.view.decrypt_video_button.config(command=self.show_decrypt_video_screen)
    
    def show_encrypt_image_screen(self):
        """Show the image encryption screen"""
        browse_button = self.view.show_file_selection("Encrypt", "Image", file_utils.IMAGE_FILETYPES)
        browse_button.config(command=lambda: self.browse_file("image", "encrypt"))
        self.view.process_button.config(command=self.start_image_encryption)
    
    def show_decrypt_image_screen(self):
        """Show the image decryption screen"""
        browse_button = self.view.show_file_selection("Decrypt", "Image", file_utils.ENCRYPTED_FILETYPES)
        browse_button.config(command=lambda: self.browse_file("image", "decrypt"))
        self.view.process_button.config(command=self.start_image_decryption)
    
    def show_encrypt_video_screen(self):
        """Show the video encryption screen"""
        browse_button = self.view.show_file_selection("Encrypt", "Video", file_utils.VIDEO_FILETYPES)
        browse_button.config(command=lambda: self.browse_file("video", "encrypt"))
        self.view.process_button.config(command=self.start_video_encryption)
    
    def show_decrypt_video_screen(self):
        """Show the video decryption screen"""
        browse_button = self.view.show_file_selection("Decrypt", "Video", file_utils.ENCRYPTED_FILETYPES)
        browse_button.config(command=lambda: self.browse_file("video", "decrypt"))
        self.view.process_button.config(command=self.start_video_decryption)
    
    def browse_file(self, media_type, operation):
        """
        Open a file dialog to select a file.
        
        Args:
            media_type (str): "image" or "video"
            operation (str): "encrypt" or "decrypt"
        """
        # Determine file types based on media type and operation
        if operation == "encrypt":
            if media_type == "image":
                file_types = file_utils.IMAGE_FILETYPES
            else:  # video
                file_types = file_utils.VIDEO_FILETYPES
        else:  # decrypt
            file_types = file_utils.ENCRYPTED_FILETYPES
        
        # Open file dialog
        file_path = file_utils.browse_for_file(file_types)
        if file_path:
            # Set file in the appropriate model
            if media_type == "image":
                filename = self.image_crypto.set_file(file_path)
                if not filename and operation == "encrypt":
                    self.view.show_message("Invalid File", "Please select a valid image file.", "error")
                    return
            else:  # video
                filename = self.video_crypto.set_file(file_path)
                if not filename and operation == "encrypt":
                    self.view.show_message("Invalid File", "Please select a valid video file.", "error")
                    return
            
            # If we're decrypting, we need to check if it's an encrypted file
            if operation == "decrypt" and not file_utils.is_encrypted_file(file_path):
                self.view.show_message("Invalid File", "Please select a valid encrypted file (.bin).", "error")
                return
            
            # Update the UI
            self.view.update_file_label(os.path.basename(file_path))
    
    def start_image_encryption(self):
        """Start the image encryption process in a separate thread"""
        if self.image_crypto.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start encryption in a separate thread
            thread = threading.Thread(
                target=self.image_crypto.encrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def start_image_decryption(self):
        """Start the image decryption process in a separate thread"""
        if self.image_crypto.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start decryption in a separate thread
            thread = threading.Thread(
                target=self.image_crypto.decrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def start_video_encryption(self):
        """Start the video encryption process in a separate thread"""
        if self.video_crypto.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start encryption in a separate thread
            thread = threading.Thread(
                target=self.video_crypto.encrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def start_video_decryption(self):
        """Start the video decryption process in a separate thread"""
        if self.video_crypto.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start decryption in a separate thread
            thread = threading.Thread(
                target=self.video_crypto.decrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def process_complete(self, success, message):
        """
        Callback for when a process is complete.
        
        Args:
            success (bool): Whether the operation was successful
            message (str): The status message
        """
        self.view.show_progress(False)
        self.view.show_status(success, message)
        self.view.process_button.config(state=tk.NORMAL)


# Import os here to avoid circular imports
import os

# Main application
if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()
    
    # Set icon if available
    if os.path.exists(os.path.join("assets", "icon.png")):
        icon_path = os.path.join("assets", "icon.png")
        try:
            root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except:
            pass  # Ignore if icon can't be loaded
    elif os.path.exists("icon.jpg"):
        try:
            from PIL import Image, ImageTk
            icon = ImageTk.PhotoImage(Image.open("icon.jpg"))
            root.iconphoto(True, icon)
        except:
            pass  # Ignore if icon can't be loaded
    
    # Create the application
    app = EncryptionController(root)
    
    # Start the main loop
    root.mainloop()