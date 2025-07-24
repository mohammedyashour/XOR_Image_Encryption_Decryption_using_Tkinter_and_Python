import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import time

# Try to import PIL for image handling, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Model - Business Logic
class EncryptionModel:
    def __init__(self, key=25):
        self.key = key
        self.selected_file_path = None
        self.processing = False
        self.operation_successful = False
    
    def set_file(self, file_path):
        self.selected_file_path = file_path
        return os.path.basename(file_path) if file_path else ""
    
    def encrypt(self, callback=None, progress_callback=None):
        if not self.selected_file_path:
            return False, "No file selected"
        
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
            file_name = os.path.basename(self.selected_file_path)
            directory = os.path.dirname(self.selected_file_path)
            new_path = os.path.join(directory, os.path.splitext(file_name)[0] + '.bin')
            os.rename(self.selected_file_path, new_path)
            self.selected_file_path = new_path
            
            self.operation_successful = True
            if progress_callback:
                progress_callback(100)
            
            if callback:
                callback(True, "The image has been encrypted successfully!")
            return True, "The image has been encrypted successfully!"
            
        except Exception as e:
            self.operation_successful = False
            error_msg = f"Error during encryption: {str(e)}"
            if callback:
                callback(False, error_msg)
            return False, error_msg
        finally:
            self.processing = False
    
    def decrypt(self, callback=None, progress_callback=None):
        if not self.selected_file_path:
            return False, "No file selected"
        
        self.processing = True
        try:
            # Rename file with .jpg extension
            file_name = os.path.basename(self.selected_file_path)
            directory = os.path.dirname(self.selected_file_path)
            new_path = os.path.join(directory, os.path.splitext(file_name)[0] + '.jpg')
            os.rename(self.selected_file_path, new_path)
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

# View - User Interface
class EncryptionView:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
        # Load icons
        self.app_icon = None
        if PIL_AVAILABLE:
            try:
                self.app_icon = ImageTk.PhotoImage(Image.open("icon.jpg").resize((100, 100)))
            except Exception:
                # Failed to load icon, continue without it
                pass
                
        # Set success/error icons
        self.success_icon = "✅"
        self.error_icon = "❌"
        # Fallback to simple characters if emoji display is problematic
        if not self._can_display_emoji():
            self.success_icon = "✓"
            self.error_icon = "✗"
            
    def _can_display_emoji(self):
        """Check if the system can likely display emoji characters"""
        try:
            # Simple check - try to create a label with an emoji
            test_label = tk.Label(self.root, text="✅")
            test_label.destroy()
            return True
        except:
            return False
    
    def setup_ui(self):
        # Configure root window
        self.root.title("Image Encryptor")
        self.root.geometry("600x500")
        self.root.minsize(600, 500)
        self.root.configure(bg="#f0f0f0")
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show welcome screen initially
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        self.clear_frame()
        
        # App title
        title_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        title_frame.pack(pady=20)
        
        if hasattr(self, 'app_icon') and self.app_icon:
            logo_label = tk.Label(title_frame, image=self.app_icon, bg="#f0f0f0")
            logo_label.pack()
        
        title = tk.Label(
            title_frame, 
            text="Image Encryptor", 
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            title_frame,
            text="Secure your images with XOR encryption",
            font=("Helvetica", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        subtitle.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(pady=30)
        
        # Encrypt button
        self.encrypt_button = self.create_styled_button(
            button_frame, 
            "Encrypt Image", 
            "#3498db", 
            "#2980b9"
        )
        self.encrypt_button.pack(pady=10, padx=20, fill=tk.X)
        
        # Decrypt button
        self.decrypt_button = self.create_styled_button(
            button_frame, 
            "Decrypt Image", 
            "#2ecc71", 
            "#27ae60"
        )
        self.decrypt_button.pack(pady=10, padx=20, fill=tk.X)
    
    def show_file_selection(self, operation_type, file_types):
        self.clear_frame()
        
        # Back button
        back_button = tk.Button(
            self.main_frame,
            text="← Back",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            relief=tk.FLAT,
            command=self.show_welcome_screen
        )
        back_button.pack(anchor=tk.NW, pady=(0, 20))
        
        # Title
        title = tk.Label(
            self.main_frame,
            text=f"{operation_type} Image",
            font=("Helvetica", 18, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title.pack(pady=10)
        
        # File selection frame
        file_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        file_frame.pack(pady=20, fill=tk.X)
        
        # Selected file label
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Helvetica", 10),
            fg="#7f8c8d",
            bg="#f0f0f0",
            wraplength=400
        )
        self.file_label.pack(pady=5)
        
        # Browse button
        browse_button = self.create_styled_button(
            file_frame,
            "Browse File",
            "#95a5a6",
            "#7f8c8d"
        )
        browse_button.pack(pady=10)
        
        # Process button (initially disabled)
        self.process_button = self.create_styled_button(
            self.main_frame,
            f"{operation_type} Now",
            "#e74c3c" if operation_type == "Encrypt" else "#2ecc71",
            "#c0392b" if operation_type == "Encrypt" else "#27ae60",
            state=tk.DISABLED
        )
        self.process_button.pack(pady=20)
        
        # Progress bar (initially hidden)
        self.progress_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.progress_frame.pack(pady=10, fill=tk.X, padx=50)
        self.progress_frame.pack_forget()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Processing: 0%",
            font=("Helvetica", 10),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        self.progress_label.pack()
        
        # Status message (initially hidden)
        self.status_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.status_frame.pack(pady=10)
        self.status_frame.pack_forget()
        
        self.status_icon = tk.Label(
            self.status_frame,
            text="",
            font=("Helvetica", 24),
            bg="#f0f0f0"
        )
        self.status_icon.pack(side=tk.LEFT, padx=5)
        
        self.status_message = tk.Label(
            self.status_frame,
            text="",
            font=("Helvetica", 12),
            bg="#f0f0f0",
            wraplength=350
        )
        self.status_message.pack(side=tk.LEFT, padx=5)
        
        return browse_button
    
    def update_file_label(self, filename):
        if filename:
            self.file_label.config(text=f"Selected file: {filename}")
            self.process_button.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No file selected")
            self.process_button.config(state=tk.DISABLED)
    
    def show_progress(self, show=True):
        if show:
            self.progress_frame.pack(pady=10, fill=tk.X, padx=50)
            self.progress_bar['value'] = 0
            self.progress_label.config(text="Processing: 0%")
        else:
            self.progress_frame.pack_forget()
    
    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"Processing: {int(value)}%")
        self.root.update_idletasks()
    
    def show_status(self, success, message):
        self.status_frame.pack(pady=10)
        
        if success:
            self.status_icon.config(text=self.success_icon, fg="#2ecc71")
            self.status_message.config(text=message, fg="#2ecc71")
        else:
            self.status_icon.config(text=self.error_icon, fg="#e74c3c")
            self.status_message.config(text=message, fg="#e74c3c")
    
    def create_styled_button(self, parent, text, bg_color, hover_color, state=tk.NORMAL):
        button = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg=bg_color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            state=state
        )
        
        # Add hover effect
        button.bind("<Enter>", lambda e, btn=button, color=hover_color: btn.config(bg=color))
        button.bind("<Leave>", lambda e, btn=button, color=bg_color: btn.config(bg=color))
        
        return button
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Controller - Connects Model and View
class EncryptionController:
    def __init__(self, root):
        self.model = EncryptionModel()
        self.view = EncryptionView(root)
        
        # Bind events
        self.bind_events()
    
    def bind_events(self):
        # Bind welcome screen buttons
        self.view.encrypt_button.config(command=self.show_encrypt_screen)
        self.view.decrypt_button.config(command=self.show_decrypt_screen)
    
    def show_encrypt_screen(self):
        browse_button = self.view.show_file_selection("Encrypt", [("Image files", "*.jpg *.jpeg *.png *.bmp")])
        browse_button.config(command=lambda: self.browse_file([("Image files", "*.jpg *.jpeg *.png *.bmp")]))
        self.view.process_button.config(command=self.start_encryption)
    
    def show_decrypt_screen(self):
        browse_button = self.view.show_file_selection("Decrypt", [("Encrypted files", "*.bin")])
        browse_button.config(command=lambda: self.browse_file([("Encrypted files", "*.bin")]))
        self.view.process_button.config(command=self.start_decryption)
    
    def browse_file(self, file_types):
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            filename = self.model.set_file(file_path)
            self.view.update_file_label(filename)
    
    def start_encryption(self):
        if self.model.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start encryption in a separate thread
            thread = threading.Thread(
                target=self.model.encrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def start_decryption(self):
        if self.model.selected_file_path:
            self.view.show_progress(True)
            self.view.process_button.config(state=tk.DISABLED)
            
            # Start decryption in a separate thread
            thread = threading.Thread(
                target=self.model.decrypt,
                args=(self.process_complete, self.view.update_progress)
            )
            thread.daemon = True
            thread.start()
    
    def process_complete(self, success, message):
        self.view.show_progress(False)
        self.view.show_status(success, message)
        self.view.process_button.config(state=tk.NORMAL)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionController(root)
    root.mainloop()

