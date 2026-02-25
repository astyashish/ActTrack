# Frequently Asked Questions (FAQ)

## General Questions

### Q: What is ActTrack?
**A:** ActTrack is an open-source motion capture and body tracking application that uses MediaPipe for real-time human pose detection. It's designed for educational and research purposes to capture body movements and send pose data to other applications.

### Q: Is ActTrack free to use?
**A:** Yes! ActTrack is completely free for educational and non-commercial use. See the [LICENSE](LICENSE) for details.

### Q: Can I use ActTrack commercially?
**A:** No. ActTrack is strictly for non-commercial, educational, and research purposes. Commercial use is prohibited without explicit written permission. See the [LICENSE](LICENSE) file.

### Q: Who created ActTrack?
**A:** ActTrack was created by **XeroD** as an educational and research project.

### Q: Is ActTrack open source?
**A:** Yes! ActTrack is open source and you can contribute. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Q: What license does ActTrack use?
**A:** ActTrack uses a Non-Commercial Educational License. See [LICENSE](LICENSE) for full terms.

---

## Technical Questions

### Q: What are the system requirements?
**A:** 
- Python 3.8+
- 8GB RAM minimum (16GB recommended)  
- GPU is optional but recommended
- Standard USB webcam or integrated camera
- Windows, macOS, or Linux

See [SETUP.md](SETUP.md#-prerequisites) for details.

### Q: Can I run ActTrack on macOS/Linux?
**A:** Yes! ActTrack works on Windows, macOS, and Linux. Follow the same installation steps.

### Q: Do I need a GPU?
**A:** No, but it's recommended. A GPU (NVIDIA with CUDA) will significantly improve FPS and tracking smoothness.

### Q: What webcam do I need?
**A:** Any standard USB webcam or integrated camera works. Minimum resolution is 320x240, but 640x480+ is recommended for better accuracy.

### Q: Can I use multiple cameras?
**A:** Yes! Set `CAM_INDEX` in `global_vars.py` to select different cameras (0, 1, 2, etc.).

---

## Installation & Setup

### Q: Where do I download ActTrack?
**A:** Clone from GitHub:
```bash
git clone https://github.com/XeroD/ActTrack.git
```

Or download the ZIP from the GitHub repository.

### Q: I get "module not found" errors
**A:** Make sure:
1. Virtual environment is activated (you see `(venv)` in terminal)
2. Dependencies are installed: `pip install -r requirements.txt`
3. You're in the ActTrack directory

### Q: How do I know if installation was successful?
**A:** Run:
```bash
python -c "import mediapipe; import cv2; import numpy; print('✓ All dependencies installed!')"
```

### Q: Pip install fails with "Permission denied"
**A:**
1. Make sure virtual environment is activated
2. Upgrade pip: `python -m pip install --upgrade pip`
3. Try again: `pip install -r requirements.txt`

### Q: I don't have Git installed
**A:** You can download the ZIP file from the GitHub repository instead and extract it.

---

## Running ActTrack

### Q: What's the difference between the different run options?
**A:**
- `python gui.py` - Full dashboard with all features (recommended)
- `python body.py` - Minimal interface, just tracking
- `python Data_Capture.py` - Motion recording utility
- `python main.py` - Command-line interface

### Q: How do I close ActTrack?
**A:** 
- GUI: Click the close button or File → Exit
- Command line: Press 'q' or Ctrl+C

### Q: Where are motion recordings saved?
**A:** Motion data is saved to `saved_dicts.json` in the project directory. Angle data is stored in `angles.json`.

### Q: Can I use ActTrack without a GUI?
**A:** Yes, run `python body.py` for minimal interface or `python main.py` for CLI.

---

## Troubleshooting

### Q: My webcam is not detected
**A:**
1. Check that your camera is plugged in and working
2. Try different CAM_INDEX values:
   ```python
   # In global_vars.py
   CAM_INDEX = 0  # Try 0, 1, 2, etc.
   ```
3. Verify with:
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
   ```
4. Check Windows permissions (Settings → Privacy & Security → Camera)

### Q: I'm getting low FPS
**A:** Reduce resource usage:
1. Lower resolution in `global_vars.py`:
   ```python
   WIDTH = 320
   HEIGHT = 240
   ```
2. Use faster model:
   ```python
   MODEL_COMPLEXITY = 0  # 0 = fast, 1 = balanced, 2 = accurate
   ```
3. Close other applications
4. Improve lighting

### Q: Tracking is jittery/unstable
**A:**
1. Improve lighting (more light = better tracking)
2. Keep camera steady (use tripod)
3. Increase smoothing buffer in `body.py`:
   ```python
   self.history_length = 15  # Increase from 10
   ```
4. Avoid rapid movements
5. Keep entire body in frame

### Q: "Address already in use" on port 52733
**A:** 
1. Kill the process using that port
2. Or change the port in `global_vars.py`:
   ```python
   PORT = 52734  # Use different port
   ```
3. Update port in other applications using this data

### Q: GUI is very slow/laggy
**A:**
1. Reduce window size
2. Lower resolution
3. Disable debug output
4. Check system resources (CPU/RAM usage)

### Q: Recording isn't working
**A:**
1. Make sure body.py is running
2. Check that Data_Capture.py is listening on correct port
3. Verify firewall isn't blocking UDP on port 52733
4. Check console for error messages

### Q: I see "Connection refused" errors
**A:** 
1. Make sure body.py is running (it sends the data)
2. Verify Data_Capture.py is listening (it receives the data)
3. Check PORT in global_vars.py matches
4. Check HOST is '127.0.0.1' for local connection

---

## Performance & Optimization

### Q: How can I improve tracking accuracy?
**A:**
1. Ensure good lighting
2. Use MODEL_COMPLEXITY = 2
3. Full body in frame
4. Keep camera steady
5. Increase smoothing

### Q: How can I improve FPS?
**A:**
1. Reduce resolution
2. Use MODEL_COMPLEXITY = 0
3. Close other applications
4. Use GPU if available
5. Reduce window size

### Q: What FPS should I expect?
**A:** Typical performance:
- Modern CPU: 20-40 FPS
- With GPU: 40-60+ FPS

Depends on resolution, model complexity, and hardware.

### Q: Can I use this for real-time VR?
**A:** Yes, with good hardware and optimization. VR typically needs 90+ FPS, so:
1. Use powerful GPU
2. Keep resolution moderate
3. Use MODEL_COMPLEXITY = 0 or 1
4. Optimize code for your use case

---

## Data & Integration

### Q: What data does ActTrack send?
**A:** Body landmarks (33 points) with X, Y, Z coordinates and calculated joint angles, sent via UDP as JSON.

### Q: How do I integrate with Unity?
**A:** See [README.md](README.md#integration-examples-unity-c) for example C# code to receive UDP data.

### Q: Can I record to video format?
**A:** Currently saves as JSON. To convert to video, post-process the recorded data with OpenCV.

### Q: Where is my data stored?
**A:** 
- Motion data: `saved_dicts.json`
- Angle data: `angles.json`  
- Logs: Console output

### Q: Does ActTrack store my video?
**A:** No, video is processed in real-time and not permanently stored unless you explicitly record it.

### Q: Is my data private?
**A:** ActTrack runs locally. Data only goes where you send it. No automatic external communication.

---

## Features & Capabilities

### Q: What body parts can ActTrack track?
**A:** 33 landmarks: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles, and mouth. See [README.md](README.md#-available-body-landmarks-33-points) for full list.

### Q: Can ActTrack detect specific poses?
**A:** Not built-in, but you can code custom pose detection by analyzing landmarks and angles.

### Q: Can I export the data?
**A:** Yes, data is stored in JSON format in `saved_dicts.json` and `angles.json`. Easy to export to other formats.

### Q: Does ActTrack support skeleton drawing?
**A:** Yes, the GUI displays skeleton overlay on the webcam feed.

### Q: Can multiple people be tracked?
**A:** MediaPipe Pose tracks one person at a time. For multiple people, you'd need to modify the code.

---

## Contributing & Community

### Q: How can I contribute to ActTrack?
**A:** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Submitting features
- Code contributions
- Documentation improvements

### Q: Can I use ActTrack code in my commercial product?
**A:** No, that's prohibited by the license. See [LICENSE](LICENSE) for terms.

### Q: Where do I report bugs?
**A:** Create an issue on the GitHub repository with:
- Clear description
- Steps to reproduce
- Error messages
- Your environment details

### Q: How do I suggest features?
**A:** Create a GitHub issue with your feature idea and explain why it would be useful.

### Q: Can I translate the documentation?
**A:** Yes! Translations are welcome. Please submit them as pull requests.

---

## Licensing & Legal

### Q: What's the license?
**A:** Non-Commercial Educational License. See [LICENSE](LICENSE) for full text.

### Q: Can I modify the code?
**A:** Yes, for personal/educational use. Modifications must stay non-commercial and include attribution.

### Q: Can I redistribute ActTrack?
**A:** Yes, with proper attribution and maintaining the license. See [LICENSE](LICENSE).

### Q: What if I want commercial use?
**A:** Contact XeroD to discuss commercial licensing options.

### Q: Do I need to include a license notice?
**A:** Yes, all distributions must include the license file and attribution to XeroD.

---

## Not Found What You're Looking For?

- 📖 Full documentation: [README.md](README.md)
- 🚀 Quick start: [QUICK_START.md](QUICK_START.md)
- 🔧 Setup guide: [SETUP.md](SETUP.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Still Have Questions?**

1. Check relevant documentation files
2. Review the code comments
3. Create an issue on GitHub with your question

*Last Updated: February 25, 2026*
