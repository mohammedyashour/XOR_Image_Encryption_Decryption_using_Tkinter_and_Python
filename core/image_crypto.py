"""
Image encryption and decryption module.
Handles XOR-based encryption for image files.
"""

import os
import time
from utils import file_utils

class ImageCrypto:
    """
    Class for handling image encryption and decryption using XOR algorithm.
    """
    def __init__(self, key=25):
        """
        Initialize the ImageCrypto with an encryption key.
        
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
        if not file_path or not file_utils.is_image_file(file_path):
            return ""
            
        self.selected_file_path = file_path
        return os.path.basename(file_path) if file_path else ""
    
    def encrypt(self, callback=None, progress_callback=None):
        """
        Encrypt the selected image file using XOR encryption.
        
        Args:
            callback (function): Callback function to be called after encryption
            progress_callback (function): Callback function for progress updates
            
        Returns:
            tuple: (success, message)
        """
        if not self.selected_file_path:
            return False, "No file selected"
        
        if not file_utils.is_image_file(self.selected_file_path):
            return False, "Selected file is not a supported image format"
        
        self.processing = True
        try:
            # Open file for reading
            with open(self.selected_file_path, 'rb') as fin:
                image = fin.read()
            
            # Convert to bytearray
            image = bytearray(image)
            
            # Perform XOR operation with progress updates
            total_bytes = len(image)
            for index, value in enumerate(image):
                image[index] = value ^ self.key
                if index % (total_bytes // 10) == 0 and progress_callback:
                    progress = (index / total_bytes) * 100
                    progress_callback(progress)
                    time.sleep(0.01)  # Small delay to show progress
            
            # Write encrypted data
            with open(self.selected_file_path, 'wb') as fin:
                fin.write(image)
            
            # Rename file with .bin extension
            original_extension = file_utils.get_file_info(self.selected_file_path)['extension']
            new_path = file_utils.rename_file(self.selected_file_path, file_utils.ENCRYPTED_EXTENSION)
            
            if new_path:
                self.selected_file_path = new_path
                self.operation_successful = True
                
                if progress_callback:
                    progress_callback(100)
                
                if callback:
                    callback(True, "The image has been encrypted successfully!")
                return True, "The image has been encrypted successfully!"
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
        Decrypt the selected encrypted file back to an image.
        
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
            # Rename file with original extension (assuming .jpg for now)
            # In a more advanced implementation, we could store the original extension
            new_path = file_utils.rename_file(self.selected_file_path, '.jpg')
            
            if not new_path:
                return False, "Failed to rename the file for decryption"
                
            self.selected_file_path = new_path
            
            # Open file for reading
            with open(self.selected_file_path, 'rb') as fin:
                image = fin.read()
            
            # Convert to bytearray
            image = bytearray(image)
            
            # Perform XOR operation with progress updates
            total_bytes = len(image)
            for index, value in enumerate(image):
                image[index] = value ^ self.key
                if index % (total_bytes // 10) == 0 and progress_callback:
                    progress = (index / total_bytes) * 100
                    progress_callback(progress)
                    time.sleep(0.01)  # Small delay to show progress
            
            # Write decrypted data
            with open(self.selected_file_path, 'wb') as fin:
                fin.write(image)
            
            self.operation_successful = True
            if progress_callback:
                progress_callback(100)
            
            if callback:
                callback(True, "The image has been decrypted successfully!")
            return True, "The image has been decrypted successfully!"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during decryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False