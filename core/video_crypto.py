"""
Video encryption and decryption module.
Handles XOR-based encryption for video files.
"""

import os
import time
from utils import file_utils

class VideoCrypto:
    """
    Class for handling video encryption and decryption using XOR algorithm.
    """
    def __init__(self, key=25):
        """
        Initialize the VideoCrypto with an encryption key.
        
        Args:
            key (int): The XOR encryption key (default: 25)
        """
        self.key = key
        self.selected_file_path = None
        self.processing = False
        self.operation_successful = False
    
    def set_file(self, file_path):
        """
        Set the file to be processed and return the filename.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Filename or empty string if no file
        """
        if not file_path or not file_utils.is_video_file(file_path):
            return ""
            
        self.selected_file_path = file_path
        return os.path.basename(file_path) if file_path else ""
    
    def encrypt(self, callback=None, progress_callback=None):
        """
        Encrypt the selected video file using XOR encryption.
        
        Args:
            callback (function): Callback function to be called after encryption
            progress_callback (function): Callback function for progress updates
            
        Returns:
            tuple: (success, message)
        """
        if not self.selected_file_path:
            return False, "No file selected"
        
        if not file_utils.is_video_file(self.selected_file_path):
            return False, "Selected file is not a supported video format"
        
        self.processing = True
        try:
            # Store original extension for later recovery
            original_extension = file_utils.get_file_info(self.selected_file_path)['extension']
            
            # Open file for reading
            with open(self.selected_file_path, 'rb') as fin:
                video = fin.read()
            
            # Convert to bytearray
            video = bytearray(video)
            
            # Perform XOR operation with progress updates
            total_bytes = len(video)
            chunk_size = max(1, total_bytes // 100)  # Update progress every 1%
            
            for index in range(0, total_bytes, chunk_size):
                end_index = min(index + chunk_size, total_bytes)
                for i in range(index, end_index):
                    video[i] = video[i] ^ self.key
                
                if progress_callback:
                    progress = (index / total_bytes) * 100
                    progress_callback(progress)
                    time.sleep(0.01)  # Small delay to show progress
            
            # Write encrypted data
            with open(self.selected_file_path, 'wb') as fin:
                fin.write(video)
            
            # Rename file with .bin extension
            new_path = file_utils.rename_file(self.selected_file_path, file_utils.ENCRYPTED_EXTENSION)
            
            if new_path:
                self.selected_file_path = new_path
                self.operation_successful = True
                
                if progress_callback:
                    progress_callback(100)
                
                if callback:
                    callback(True, "The video has been encrypted successfully!")
                return True, "The video has been encrypted successfully!"
            else:
                return False, "Failed to rename the encrypted file"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during encryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False
    
    def decrypt(self, callback=None, progress_callback=None):
        """
        Decrypt the selected encrypted file back to a video.
        
        Args:
            callback (function): Callback function to be called after decryption
            progress_callback (function): Callback function for progress updates
            
        Returns:
            tuple: (success, message)
        """
        if not self.selected_file_path:
            return False, "No file selected"
        
        if not file_utils.is_encrypted_file(self.selected_file_path):
            return False, "Selected file is not an encrypted file"
        
        self.processing = True
        try:
            # Get the original file info
            file_info = file_utils.get_file_info(self.selected_file_path)
            
            # Determine the original extension
            # In a real implementation, we might store this information in metadata
            # For now, we'll ask the user or use a default extension
            original_extension = '.mp4'  # Default to .mp4
            
            # Rename file with original extension
            new_path = file_utils.rename_file(self.selected_file_path, original_extension)
            
            if not new_path:
                return False, "Failed to rename the file for decryption"
                
            self.selected_file_path = new_path
            
            # Open file for reading
            with open(self.selected_file_path, 'rb') as fin:
                video = fin.read()
            
            # Convert to bytearray
            video = bytearray(video)
            
            # Perform XOR operation with progress updates
            total_bytes = len(video)
            chunk_size = max(1, total_bytes // 100)  # Update progress every 1%
            
            for index in range(0, total_bytes, chunk_size):
                end_index = min(index + chunk_size, total_bytes)
                for i in range(index, end_index):
                    video[i] = video[i] ^ self.key
                
                if progress_callback:
                    progress = (index / total_bytes) * 100
                    progress_callback(progress)
                    time.sleep(0.01)  # Small delay to show progress
            
            # Write decrypted data
            with open(self.selected_file_path, 'wb') as fin:
                fin.write(video)
            
            self.operation_successful = True
            if progress_callback:
                progress_callback(100)
            
            if callback:
                callback(True, "The video has been decrypted successfully!")
            return True, "The video has been decrypted successfully!"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during decryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False