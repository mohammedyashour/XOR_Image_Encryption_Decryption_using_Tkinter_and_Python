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
                    # Removed time.sleep to prevent UI freezing
            
            # Get original file extension before renaming
            file_info = file_utils.get_file_info(self.selected_file_path)
            original_extension = file_info['extension']
            base_name = file_info['base_name']
            
            # Store original extension in the filename (e.g., image_jpg.bin)
            new_base_name = f"{base_name}_{original_extension[1:]}"  # Remove the dot from extension
            new_path = os.path.join(file_info['directory'], f"{new_base_name}{file_utils.ENCRYPTED_EXTENSION}")
            
            # Write encrypted data
            with open(new_path, 'wb') as fout:
                fout.write(image)
            
            # Remove original file
            try:
                os.remove(self.selected_file_path)
            except:
                pass  # If removal fails, continue anyway
            
            if os.path.exists(new_path):
                self.selected_file_path = new_path
                self.operation_successful = True
                
                if progress_callback:
                    progress_callback(100)
                
                if callback:
                    callback(True, "The image has been encrypted successfully!")
                return True, "The image has been encrypted successfully!"
            else:
                return False, "Failed to create the encrypted file"
            
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
            # Extract original extension from filename (e.g., "image_jpg.bin" -> ".jpg")
            file_info = file_utils.get_file_info(self.selected_file_path)
            base_name = file_info['base_name']
            
            # Check if the filename contains the original extension
            original_extension = None
            if '_' in base_name:
                # Extract the extension part after the last underscore
                ext_part = base_name.split('_')[-1]
                if ext_part:  # Make sure it's not empty
                    original_extension = f".{ext_part}"
            
            # If we couldn't extract the extension, default to .jpg
            if not original_extension:
                original_extension = '.jpg'
                
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
                    # Removed time.sleep to prevent UI freezing
            
            # Create a new filename without the extension marker
            if '_' in base_name:
                new_base_name = '_'.join(base_name.split('_')[:-1])  # Remove the extension part
            else:
                new_base_name = base_name
                
            # Create the new path with the original extension
            new_path = os.path.join(file_info['directory'], f"{new_base_name}{original_extension}")
            
            # Write decrypted data to the new file
            with open(new_path, 'wb') as fout:
                fout.write(image)
                
            # Remove the encrypted file
            try:
                os.remove(self.selected_file_path)
            except:
                pass  # If removal fails, continue anyway
            
            if os.path.exists(new_path):
                self.selected_file_path = new_path
                self.operation_successful = True
                
                if progress_callback:
                    progress_callback(100)
                
                if callback:
                    callback(True, "The image has been decrypted successfully!")
                return True, "The image has been decrypted successfully!"
            else:
                return False, "Failed to create the decrypted file"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during decryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False