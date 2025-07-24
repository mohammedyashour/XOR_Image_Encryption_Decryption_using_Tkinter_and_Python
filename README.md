# XOR File Encryption/Decryption

<img src="https://cdn.dribbble.com/users/1579931/screenshots/3839034/2keyencryption_v5.gif" alt="encrypt" width="500" height="400">

## Overview

A secure file encryption application that uses XOR encryption to protect your images and videos. The application features a modern, user-friendly interface built with Tkinter and provides real-time progress updates during encryption and decryption operations.

## Features

- **Image Encryption/Decryption**: Encrypt and decrypt image files (.jpg, .jpeg, .png, .bmp)
- **Video Encryption/Decryption**: Encrypt and decrypt video files (.mp4, .avi, .mov, .mkv)
- **Simple XOR Encryption**: Fast and effective encryption for personal use
- **User-Friendly Interface**: Clean, modern UI with progress tracking
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Project Structure

The project follows a modular architecture for better maintainability and scalability:

```
project/
│
├── core/
│   ├── image_crypto.py       # Image encryption/decryption logic
│   └── video_crypto.py       # Video encryption/decryption logic
│
├── gui/
│   └── app_ui.py             # Tkinter UI components
│
├── utils/
│   └── file_utils.py         # File handling utilities
│
├── assets/
│   └── icon.png              # Application icon (optional)
│
├── .github/
│   └── workflows/
│       └── build-exe.yml     # GitHub Actions workflow for building .exe
│
├── main.py                   # Application entry point
└── requirements.txt          # Project dependencies
```

## How It Works

1. **Encryption Process**:
   - Select an image or video file
   - The file is read as a binary stream
   - XOR operation is applied to each byte using a key
   - The encrypted file is saved with a .bin extension

2. **Decryption Process**:
   - Select an encrypted .bin file
   - The file is read as a binary stream
   - The same XOR operation is applied to reverse the encryption
   - The file is restored with its original extension

## Installation

### Option 1: Run from Source

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/XOR_File_Encryption.git
   cd XOR_File_Encryption
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

### Option 2: Download Executable (Windows)

1. Go to the "Actions" tab in the GitHub repository
2. Select the latest successful workflow run
3. Download the "encrypted-app-exe" artifact
4. Extract and run main.exe

## Building the Executable

The project includes a GitHub Actions workflow that automatically builds a Windows executable (.exe) file when changes are pushed to the main branch.

To build manually with PyInstaller:

```
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed main.py
```

The executable will be created in the `dist` directory.

## Usage

1. Launch the application
2. Choose the operation you want to perform:
   - Encrypt Image
   - Decrypt Image
   - Encrypt Video
   - Decrypt Video
3. Select the file using the file browser
4. Click the process button and wait for the operation to complete
5. Check the status message for results

## Security Note

This application uses a simple XOR encryption algorithm which is suitable for basic privacy protection but not for highly sensitive data. For critical security needs, consider using industry-standard encryption libraries.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
