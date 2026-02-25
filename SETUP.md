# Installation & Setup Guide for ActTrack

This guide provides detailed step-by-step instructions for setting up ActTrack on your system.

## 📋 Prerequisites

Before installing ActTrack, ensure your system meets these requirements:

### System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: 2-3GB for dependencies
- **Webcam**: USB webcam or integrated camera (minimum 320x240 resolution)

### Check Your Python Version

```bash
python --version
```

If you don't have Python installed or have an older version, download it from [python.org](https://www.python.org/downloads/)

## 🔧 Installation Steps

### Step 1: Clone the Repository

**Using Git (Recommended)**

```bash
git clone https://github.com/XeroD/ActTrack.git
cd ActTrack
```

**Without Git**

1. Go to [GitHub Repository](https://github.com/XeroD/ActTrack)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal in the extracted folder

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

#### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your terminal line.

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Upgrade pip

Ensure you have the latest pip version:

#### Windows

```bash
python -m pip install --upgrade pip
```

#### macOS/Linux

```bash
python3 -m pip install --upgrade pip
```

### Step 4: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- mediapipe (pose detection)
- opencv-python (computer vision)
- numpy (numerical computing)
- Pillow (image processing)
- sv-ttk (UI theme)

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
python -c "import mediapipe; import cv2; import numpy; print('✓ All dependencies installed successfully!')"
```

If you see "All dependencies installed successfully!" you're good to go.

## ⚙️ Configuration

### Basic Configuration

Open `global_vars.py` and review the default settings:

```python
# Webcam settings
CAM_INDEX = 0              # 0 = default camera, try 1 or 2 if not working
WIDTH = 640                # Frame width (lower = faster)
HEIGHT = 480               # Frame height (lower = faster)
FPS = 30                   # Frames per second (30 or 60)

# UDP Communication
HOST = '127.0.0.1'        # Localhost
PORT = 52733              # Port for UDP messages

# Model complexity (0=fast, 1=balanced, 2=accurate)
MODEL_COMPLEXITY = 1
```

### Testing Webcam

If you're unsure which camera index to use:

```bash
python -c "
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        print(f'Camera {i}: Working')
        cap.release()
    else:
        print(f'Camera {i}: Not available')
"
```

## 🚀 Running ActTrack

### Option 1: GUI Dashboard (Recommended for First-Time Users)

```bash
python gui.py
```

The dashboard provides:
- Real-time pose visualization
- Debug information
- Configuration options
- Performance monitoring

### Option 2: Body Tracking (Minimal Interface)

```bash
python body.py
```

Shows live webcam feed with pose landmarks overlay.

### Option 3: Motion Capture Recording

```bash
python Data_Capture.py
```

Records and saves motion sequences to JSON files.

### Option 4: Command Line Interface

```bash
python main.py
```

Entry point for various modes (press 'q' to quit).

## 🎯 First-Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Installation verified
- [ ] `global_vars.py` configured
- [ ] Webcam tested and working
- [ ] Run `python gui.py`

## 🐛 Troubleshooting Setup Issues

### Issue: "Python: command not found"

**Solution**: Python is not in your PATH
1. Reinstall Python and check "Add Python to PATH" during installation
2. Or use full path: `C:\Python39\python.exe gui.py`

### Issue: "No module named 'venv'"

**Solution**: Virtual environment module not available
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

### Issue: Pip install fails / "Permission denied"

**Solution**: Upgrade pip and try again
```bash
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### Issue: "No module named 'mediapipe'"

**Solution**: Dependencies not installed in virtual environment
1. Make sure virtual environment is activated (see `(venv)` prefix)
2. Run: `pip install -r requirements.txt`
3. Verify: `pip list` should show mediapipe

### Issue: Webcam not detected

**Solution**:
1. Check camera is plugged in and working
2. Try different `CAM_INDEX` values in `global_vars.py`
3. Test with: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`
4. Check OS permissions (Windows might ask for camera access)

### Issue: "Address already in use" error

**Solution**: Port 52733 is already in use
```bash
# Windows - find what's using the port
netstat -ano | findstr :52733

# macOS/Linux
lsof -i :52733

# Change PORT in global_vars.py to a different value like 52734
```

### Issue: Low FPS or high CPU usage

**Solution**: Reduce resource usage
- Lower `WIDTH` and `HEIGHT` in `global_vars.py`
- Change `MODEL_COMPLEXITY` to 0 or 1
- Close other applications
- Improve lighting (better lighting = better performance)

### Issue: GPU not being used (if available)

**Note**: On Windows with NVIDIA GPU, install CUDA:
```bash
pip install nvidia-cuda-runtime nvidia-cuda-toolkit
```

For detailed GPU setup, see your GPU manufacturer's documentation.

## 🔄 Updating ActTrack

To update to the latest version:

```bash
# Navigate to project folder
cd ActTrack

# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart virtual environment
deactivate
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux
```

## 📦 Optional: GPU Acceleration

For faster performance with NVIDIA GPU:

```bash
# Windows
pip install torch torchvision torchaudio

# macOS/Linux
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 🧹 Cleaning Up

### Deactivate Virtual Environment

```bash
deactivate
```

### Remove Virtual Environment

```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Clear Cache

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Or
python -c "import py_compile; py_compile.compile('*.py', doraise=True)"
```

## ✅ Verify Full Installation

Run this comprehensive check:

```python
import sys
print(f"Python version: {sys.version}")

import mediapipe as mp
print("✓ MediaPipe installed")

import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✓ Webcam detected")
    cap.release()
else:
    print("✗ Webcam not detected")

import numpy as np
print("✓ NumPy installed")

print("\n🎉 ActTrack is ready to use!")
```

## 📞 Getting Help

If you encounter issues:
1. Check [Troubleshooting](#-troubleshooting-setup-issues) section
2. See [README.md](README.md#-troubleshooting)
3. Review [Logs](#logs) from dashboard
4. Check GitHub issues

## Next Steps

After successful installation:
1. Read [README.md](README.md)
2. Start with `python gui.py`
3. Review [Usage Guide](README.md#-usage-guide)
4. Try different features
5. Explore configuration options

---

**Setup Complete!** 🎉

You're now ready to use ActTrack. Start with `python gui.py` to launch the dashboard.

*Last Updated: February 25, 2026*
