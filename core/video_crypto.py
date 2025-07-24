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
            if callback:
                callback(False, "No file selected")
            return False, "No file selected"
        
        if not file_utils.is_encrypted_file(self.selected_file_path):
            if callback:
                callback(False, "Selected file is not an encrypted file")
            return False, "Selected file is not an encrypted file"
        
        self.processing = True
        try:
            # First, read the encrypted file
            with open(self.selected_file_path, 'rb') as fin:
                video = fin.read()
            
            # Convert to bytearray for decryption
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
                    # Removed time.sleep to prevent UI freezing
            
            # Get the original file info
            file_info = file_utils.get_file_info(self.selected_file_path)
            base_name = file_info['base_name']
            
            # Extract original extension from filename (e.g., "video_mp4.bin" -> ".mp4")
            original_extension = None
            if '_' in base_name:
                # Extract the extension part after the last underscore
                ext_part = base_name.split('_')[-1]
                if ext_part and ext_part in ['mp4', 'avi', 'mov', 'mkv']:  # Validate it's a known video extension
                    original_extension = f".{ext_part}"
            
            # If we couldn't extract the extension, default to .mp4
            if not original_extension:
                original_extension = '.mp4'
            
            # Create a new filename without the extension marker
            if '_' in base_name:
                new_base_name = '_'.join(base_name.split('_')[:-1])  # Remove the extension part
            else:
                new_base_name = base_name
                
            # Create the new path with the original extension
            new_path = os.path.join(file_info['directory'], f"{new_base_name}{original_extension}")
            
            # Write decrypted data to the new file
            with open(new_path, 'wb') as fout:
                fout.write(video)
            
            # Verify the new file exists before removing the original
            if os.path.exists(new_path):
                # Remove the encrypted file
                try:
                    os.remove(self.selected_file_path)
                except:
                    pass  # If removal fails, continue anyway
                
                self.selected_file_path = new_path
                self.operation_successful = True
                
                if progress_callback:
                    progress_callback(100)
                
                if callback:
                    callback(True, f"The video has been decrypted successfully to {os.path.basename(new_path)}!")
                return True, f"The video has been decrypted successfully to {os.path.basename(new_path)}!"
            else:
                if callback:
                    callback(False, "Failed to create the decrypted file")
                return False, "Failed to create the decrypted file"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during decryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False