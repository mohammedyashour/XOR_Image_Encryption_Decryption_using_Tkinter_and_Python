"""
User interface module for the encryption application.
Handles the Tkinter UI components and layout.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import threading
from utils import file_utils

# Try to import PIL for image handling, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class EncryptionView:
    """
    View class for the encryption application.
    Handles all UI components and user interactions.
    """
    def __init__(self, root):
        """
        Initialize the view with the root Tkinter window.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.setup_ui()
        
        # Load icons
        self.app_icon = None
        if PIL_AVAILABLE:
            try:
                icon_path = os.path.join("assets", "icon.png")
                if os.path.exists(icon_path):
                    self.app_icon = ImageTk.PhotoImage(Image.open(icon_path).resize((100, 100)))
                else:
                    # Try to use the original icon.jpg if available
                    if os.path.exists("icon.jpg"):
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
        """Set up the main UI components"""
        # Configure root window
        self.root.title("File Encryptor")
        self.root.geometry("600x550")
        self.root.minsize(600, 550)
        self.root.configure(bg="#f0f0f0")
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show welcome screen initially
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Display the welcome screen with all operation options"""
        self.clear_frame()
        
        # App title
        title_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        title_frame.pack(pady=20)
        
        if hasattr(self, 'app_icon') and self.app_icon:
            logo_label = tk.Label(title_frame, image=self.app_icon, bg="#f0f0f0")
            logo_label.pack()
        
        title = tk.Label(
            title_frame, 
            text="File Encryptor", 
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            title_frame,
            text="Secure your files with XOR encryption",
            font=("Helvetica", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        subtitle.pack()
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Image section
        image_section = tk.LabelFrame(
            button_frame,
            text="Image Operations",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        image_section.pack(pady=10, fill=tk.X)
        
        # Encrypt image button
        self.encrypt_image_button = self.create_styled_button(
            image_section, 
            "Encrypt Image", 
            "#3498db", 
            "#2980b9"
        )
        self.encrypt_image_button.pack(pady=5, padx=20, fill=tk.X)
        
        # Decrypt image button
        self.decrypt_image_button = self.create_styled_button(
            image_section, 
            "Decrypt Image", 
            "#2ecc71", 
            "#27ae60"
        )
        self.decrypt_image_button.pack(pady=5, padx=20, fill=tk.X)
        
        # Video section
        video_section = tk.LabelFrame(
            button_frame,
            text="Video Operations",
            font=("Helvetica", 12, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        video_section.pack(pady=10, fill=tk.X)
        
        # Encrypt video button
        self.encrypt_video_button = self.create_styled_button(
            video_section, 
            "Encrypt Video", 
            "#e74c3c", 
            "#c0392b"
        )
        self.encrypt_video_button.pack(pady=5, padx=20, fill=tk.X)
        
        # Decrypt video button
        self.decrypt_video_button = self.create_styled_button(
            video_section, 
            "Decrypt Video", 
            "#9b59b6", 
            "#8e44ad"
        )
        self.decrypt_video_button.pack(pady=5, padx=20, fill=tk.X)
    
    def show_file_selection(self, operation_type, media_type, file_types):
        """
        Display the file selection screen for a specific operation.
        
        Args:
            operation_type (str): "Encrypt" or "Decrypt"
            media_type (str): "Image" or "Video"
            file_types (list): List of file type tuples for the file dialog
        """
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
            text=f"{operation_type} {media_type}",
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
        """
        Update the file label with the selected filename.
        
        Args:
            filename (str): The name of the selected file
        """
        if filename:
            self.file_label.config(text=f"Selected file: {filename}")
            self.process_button.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No file selected")
            self.process_button.config(state=tk.DISABLED)
    
    def show_progress(self, show=True):
        """
        Show or hide the progress bar.
        
        Args:
            show (bool): Whether to show the progress bar
        """
        if show:
            self.progress_frame.pack(pady=10, fill=tk.X, padx=50)
            self.progress_bar['value'] = 0
            self.progress_label.config(text="Processing: 0%")
        else:
            self.progress_frame.pack_forget()
    
    def update_progress(self, value):
        """
        Update the progress bar value.
        
        Args:
            value (float): The progress value (0-100)
        """
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"Processing: {int(value)}%")
        self.root.update_idletasks()
    
    def show_status(self, success, message):
        """
        Show a status message with an icon.
        
        Args:
            success (bool): Whether the operation was successful
            message (str): The status message to display
        """
        self.status_frame.pack(pady=10)
        
        if success:
            self.status_icon.config(text=self.success_icon, fg="#2ecc71")
            self.status_message.config(text=message, fg="#2ecc71")
        else:
            self.status_icon.config(text=self.error_icon, fg="#e74c3c")
            self.status_message.config(text=message, fg="#e74c3c")
    
    def create_styled_button(self, parent, text, bg_color, hover_color, state=tk.NORMAL):
        """
        Create a styled button with hover effects.
        
        Args:
            parent: The parent widget
            text (str): The button text
            bg_color (str): The background color
            hover_color (str): The hover color
            state: The button state (NORMAL or DISABLED)
            
        Returns:
            tk.Button: The created button
        """
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
        button.bind("<Enter>", lambda e, btn=button, color=hover_color: btn.config(bg=color) if btn['state'] == tk.NORMAL else None)
        button.bind("<Leave>", lambda e, btn=button, color=bg_color: btn.config(bg=color) if btn['state'] == tk.NORMAL else None)
        
        return button
    
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_message(self, title, message, message_type="info"):
        """
        Show a message box.
        
        Args:
            title (str): The message box title
            message (str): The message to display
            message_type (str): The message type (info, warning, error)
        """
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)