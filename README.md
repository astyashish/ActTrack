# ActTrack - Real-Time Body Pose Detection & Motion Capture

[![License: Non-Commercial](https://img.shields.io/badge/License-Non--Commercial-red)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20Detection-green)](https://mediapipe.dev/)

## 📋 Overview

**ActTrack** is an advanced open-source motion capture and body tracking application that leverages Google's MediaPipe for real-time human pose detection. It provides a professional-grade system for capturing human body movements, calculating joint angles, recording motion data, and streaming pose information over UDP to external applications like Unity game engines.

### ⚠️ **Non-Commercial Use Notice**

This project is provided for **educational and research purposes only**. Commercial use, including selling, monetizing, or using this software in commercial products, is **strictly prohibited** without explicit written permission from the author.

**Author**: XeroD  
**License Type**: Non-Commercial/Educational Open Source

---

## 🎯 Features

- **Real-Time Pose Detection**: Capture human body pose at 30+ FPS using advanced MediaPipe models
- **Joint Angle Calculation**: Automatically compute angles between body joints (shoulders, elbows, knees, etc.)
- **Body Landmark Tracking**: Track 33 distinct body landmarks with 3D coordinates (X, Y, Z)
- **Live Data Visualization**: Real-time display of body landmarks with coordinate table overlay
- **UDP Streaming**: Send pose data to external applications (e.g., Unity, VR applications)
- **Motion Data Recording**: Capture and save motion sequences for later analysis
- **Advanced Debug Dashboard**: Monitor performance metrics, FPS, and landmark accuracy
- **Smooth Filtering**: Implement smoothing algorithms to reduce jitter in tracking data
- **Multi-Tab Interface**: Organized UI with debug tables, settings, logs, and games integration
- **Configurable Settings**: Customize camera index, resolution, FPS, and model complexity

---

## 📦 System Requirements

### Hardware
- **Processor**: Intel i5/Ryzen 5 or better (GPU recommended for optimal performance)
- **RAM**: Minimum 8GB (16GB recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended for better FPS)
- **Webcam**: Standard USB webcam or integrated camera with at least 640x480 resolution

### Software
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11, macOS, or Linux

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/astyashish/ActTrack.git
cd ActTrack
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `mediapipe` - Pose detection and landmark tracking
- `opencv-python` - Computer vision and image processing
- `numpy` - Numerical computations
- `tkinter` - GUI framework (usually pre-installed with Python)
- `sv-ttk` - Modern themed tkinter widgets
- `Pillow` - Image processing

### Step 4: Verify Installation

Run the following command to verify all dependencies are installed correctly:

```bash
python -c "import mediapipe; import cv2; import numpy; print('All dependencies installed successfully!')"
```

---

## 📖 Usage Guide

### Basic Usage

#### Option 1: Launch the Advanced Debug Dashboard (Recommended)

```bash
python gui.py
```

This opens a modern dashboard with multiple tabs:
- **Debug Table**: View real-time body landmark coordinates
- **Settings**: Configure camera, resolution, and model parameters
- **Logs**: Monitor application logs and performance metrics
- **Games**: Integrated mini-games for pose-based interaction

#### Option 2: Run the Main Body Tracking Script

```bash
python body.py
```

This script:
- Initializes MediaPipe pose detection
- Captures video from your webcam
- Processes frames in real-time
- Sends tracking data via UDP

#### Option 3: Motion Capture Recording

```bash
python Data_Capture.py
```

This application allows you to:
- Record motion sequences
- Save captured data to JSON files
- Playback recorded movements
- Export motion data for external use

### Configuration

Edit `global_vars.py` to customize application settings:

```python
# Webcam Settings
CAM_INDEX = 0              # Camera device index (0 for default)
WIDTH = 320               # Frame width (default: 640)
HEIGHT = 240              # Frame height (default: 480)
FPS = 60                  # Target frames per second

# UDP Connection
HOST = '127.0.0.1'        # Server IP address
PORT = 52733              # Server port for UDP communication

# Model Settings
MODEL_COMPLEXITY = 2      # 0 (fast), 1 (balanced), or 2 (accurate)

# Debug Mode
DEBUG = True              # Enable/disable debug output
DEBUG_GUI = True          # Enable/disable GUI debug mode
```

---

## 🏗️ Project Architecture

### Core Components

```
ActTrack/
├── body.py              # Main body tracking engine (MediaPipe processing)
├── gui.py               # Advanced debug dashboard UI
├── Data_Capture.py      # Motion data recording and playback
├── clientUDP.py         # UDP communication client
├── global_vars.py       # Shared configuration variables
├── main.py              # CLI entry point
├── main_GUI.py          # Alternative GUI launcher
├── angles.json          # Stored angle calculations
├── saved_dicts.json     # Recorded motion sequences
└── README.md            # This file
```

### Module Descriptions

| Module | Purpose |
|--------|---------|
| **body.py** | Core MediaPipe integration, pose detection, landmark smoothing, angle calculations |
| **gui.py** | Tkinter-based dashboard with tabbed interface for monitoring and control |
| **Data_Capture.py** | UDP listener for capturing motion data and saving to JSON format |
| **clientUDP.py** | Threaded UDP client for streaming pose data to external applications |
| **global_vars.py** | Centralized configuration and shared state variables |

---

## 🔌 UDP Communication Protocol

ActTrack streams pose data via UDP. Use this specification to integrate with other applications:

### Connection Details
- **Protocol**: UDP
- **Default Host**: 127.0.0.1
- **Default Port**: 52733
- **Message Format**: JSON over UDP

### Data Structure
```json
{
  "landmarks": [
    {"name": "nose", "x": 0.5, "y": 0.3, "z": 0.0},
    {"name": "left_shoulder", "x": 0.4, "y": 0.2, "z": -0.1},
    ...
  ],
  "angles": {
    "left_elbow": 75.5,
    "right_knee": 120.3,
    ...
  },
  "timestamp": 1645234567.890
}
```

### Integration Example (Unity C#)

```csharp
using UnityEngine;
using System.Net;
using System.Net.Sockets;

public class ActTrackReceiver : MonoBehaviour {
    private UdpClient client;
    
    void Start() {
        client = new UdpClient(52733);
        client.BeginReceive(ReceiveCallback, null);
    }
    
    void ReceiveCallback(System.IAsyncResult ar) {
        IPEndPoint endpoint = new IPEndPoint(IPAddress.Any, 0);
        byte[] data = client.EndReceive(ar, ref endpoint);
        string json = System.Text.Encoding.UTF8.GetString(data);
        // Parse JSON and apply to character model
    }
}
```

---

## 🎮 Available Body Landmarks (33 Points)

ActTrack tracks the following MediaPipe Pose landmarks:

| Index | Landmark | Index | Landmark |
|-------|----------|-------|----------|
| 0 | Nose | 17 | Right Ear |
| 1 | Left Eye Inner | 18 | Mouth Left |
| 2 | Left Eye | 19 | Mouth Right |
| 3 | Left Eye Outer | 20 | Left Shoulder |
| 4 | Right Eye Inner | 21 | Right Shoulder |
| 5 | Right Eye | 22 | Left Elbow |
| 6 | Right Eye Outer | 23 | Right Elbow |
| 7 | Left Ear | 24 | Left Wrist |
| 8-16 | Mouth/Face | 25-33 | Hip, Knee, Ankle (both sides) |

---

## ⚙️ Advanced Configuration

### Optimizing for Performance

```python
# In global_vars.py for better FPS
MODEL_COMPLEXITY = 0      # Use lite model
WIDTH = 320
HEIGHT = 240
FPS = 30
```

### Optimizing for Accuracy

```python
# For precise joint tracking
MODEL_COMPLEXITY = 2      # Use full model
WIDTH = 640
HEIGHT = 480
FPS = 30
```

### Custom Angle Calculations

Edit the `process_landmarks_and_calculate_angles()` function in [body.py](body.py#L200) to define custom joint angles for your application.

---

## 🐛 Troubleshooting

### Issue: "No module named 'mediapipe'"
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Issue: Webcam not detected
**Solution**: Change `CAM_INDEX` in `global_vars.py`. Try values 0, 1, 2, etc.

### Issue: Low FPS / High CPU Usage
**Solution**: 
- Reduce resolution in `global_vars.py`
- Lower `MODEL_COMPLEXITY` to 0 or 1
- Close unnecessary applications
- Enable GPU acceleration if available

### Issue: UDP messages not received
**Solution**: 
- Verify firewall allows UDP on port 52733
- Confirm receiver application is listening on same IP/port
- Check `global_vars.py` HOST and PORT settings

### Issue: Jerky/Unstable Tracking
**Solution**: 
- Increase smoothing window in [body.py](body.py#L120) `history_length`
- Ensure adequate lighting on subject
- Keep camera steady

---

## 📊 Performance Metrics

Typical performance on recommended hardware:

| Metric | Value |
|--------|-------|
| **FPS** | 30-60 FPS |
| **Latency** | 50-100ms |
| **CPU Usage** | 15-40% |
| **GPU Usage** | 20-50% (with GPU) |
| **Memory Usage** | 300-500MB |

---

## 📝 File Format Reference

### Motion Data Format (saved_dicts.json)

```json
{
  "motion_capture_session_01": {
    "timestamp": "2026-02-25 10:30:00",
    "duration": 5.2,
    "frames": [
      {
        "frame_number": 0,
        "landmarks": [...],
        "angles": {...}
      }
    ]
  }
}
```

### Angles Format (angles.json)

```json
{
  "left_shoulder": 45.3,
  "left_elbow": 120.5,
  "left_wrist": 180.0,
  "right_shoulder": 42.1,
  ...
}
```

---

## 🔗 Integration Examples

### With Python/Flask Backend

```python
from clientUDP import ClientUDP
import json

# Initialize UDP client
client = ClientUDP("127.0.0.1", 52733)
client.start()

# Send pose data to server
pose_data = {"landmarks": [...], "angles": {...}}
client.sendMessage(json.dumps(pose_data))
```

### With Real-Time Analytics

```python
# Process incoming pose data
def analyze_pose(landmarks):
    # Calculate body stability
    # Detect abnormal postures
    # Log metrics to database
    pass
```

---

## 🤝 Contributing

Contributions are welcome! However, please adhere to these guidelines:

1. **Non-Commercial Use Only**: Any contributions must support the educational/non-commercial purpose
2. **Code Style**: Follow PEP 8 guidelines
3. **Documentation**: Include docstrings and comments
4. **Testing**: Include basic tests for new features
5. **License**: All contributions must be compatible with non-commercial use

### How to Contribute

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "Add description of changes"

# 4. Push to your fork
git push origin feature/your-feature-name

# 5. Submit a Pull Request
```

---

## 📄 License

This project is released under a **Non-Commercial Open Source License**.

### License Terms

✅ **Permitted:**
- Educational and research use
- Personal projects and experimentation
- Modification for personal use
- Distribution of source code with attribution

❌ **Prohibited:**
- Commercial use or sold products
- Revenue generation from this software
- Use in commercial applications without explicit permission
- Removal of licensing notices

For commercial use licensing, please contact the author.

---

## 📮 Contact & Support

- **Author**: XeroD
- **Project**: ActTrack - Real-Time Motion Capture
- **License**: Non-Commercial Educational Use

### Getting Help

- 📖 Check the [Troubleshooting](#-troubleshooting) section
- 🔍 Review [Available Body Landmarks](#-available-body-landmarks-33-points)
- ⚙️ Consult [Advanced Configuration](#-advanced-configuration)
- 🐛 Report issues on the project repository

---

## 🙏 Acknowledgments

- **MediaPipe**: Google's powerful pose detection framework
- **OpenCV**: Computer vision library
- **PyQt/Tkinter**: GUI frameworks

---

## 📚 References

- [MediaPipe Pose Documentation](https://mediapipe.dev/solutions/pose)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)

---

## 🔐 Data Privacy

ActTrack operates locally on your machine. No data is automatically sent to external servers. Video feeds are processed in real-time and not permanently stored unless explicitly saved by the user.

---

## ⚡ Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/XeroD/ActTrack.git
cd ActTrack
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run GUI
python gui.py

# Run motion capture
python Data_Capture.py

# Run standalone tracking
python body.py
```

---

**Made by XeroD | For Educational & Research Use Only** ✨

---

*Last Updated: February 25, 2026*
