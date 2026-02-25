# Quick Start Guide - ActTrack

Get up and running with ActTrack in 5 minutes!

## ⚡ 30-Second Setup

```bash
# 1. Get the code
git clone https://github.com/XeroD/ActTrack.git
cd ActTrack

# 2. Setup environment (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Run!
python gui.py
```

For macOS/Linux, use `source venv/bin/activate` instead.

## 🎯 What to Do First

### Launch the Dashboard

```bash
python gui.py
```

This opens the **Advanced Debug Dashboard** with:
- **Debug Table Tab**: See real-time body landmark positions
- **Settings Tab**: Configure camera and performance
- **Logs Tab**: Monitor system events
- **Games Tab**: Try interactive pose-based games

### Configure Your Setup

In the Settings tab:
1. Select your camera (if multiple cameras available)
2. Set resolution (lower = faster, higher = better quality)
3. Adjust model complexity (0 = fast, 2 = accurate)

### Record Motion Data

```bash
python Data_Capture.py
```

- Listens for pose data via UDP
- Saves motion sequences to `saved_dicts.json`
- View captured data in the GUI

## 🎮 Common Tasks

### View Live Pose Tracking

```bash
python gui.py
# Click on "Debug Table" tab
```

### Just See The Webcam With Landmarks

```bash
python body.py
```

### Record a Motion Sequence

```bash
python Data_Capture.py
# Perform your motion
# Data saved as JSON
```

### Check System Configuration

Edit `global_vars.py`:
```python
CAM_INDEX = 0        # Your camera number
WIDTH = 640          # Frame width
HEIGHT = 480         # Frame height
FPS = 30            # Frames per second
```

## 🔗 Send Data to Unity

1. Run ActTrack: `python gui.py`
2. Create C# script in Unity:

```csharp
using UnityEngine;
using System.Net;
using System.Net.Sockets;

void Start() {
    UdpClient client = new UdpClient(52733);
    while (true) {
        IPEndPoint endpoint = new IPEndPoint(IPAddress.Any, 0);
        byte[] data = client.Receive(ref endpoint);
        string json = System.Text.Encoding.UTF8.GetString(data);
        // Parse and use pose data
    }
}
```

## 📊 Understanding the Data

### Landmarks Output

```json
{
  "nose": {"x": 0.5, "y": 0.3, "z": 0.0},
  "left_shoulder": {"x": 0.4, "y": 0.2, "z": -0.1}
}
```

- **x, y**: Screen position (0-1)
- **z**: Depth (-1 to 1)

### Angles Output

```json
{
  "left_elbow": 95.3,
  "right_knee": 120.5,
  "left_wrist": 180.0
}
```

Angles in degrees between joints.

## ⚙️ Basic Troubleshooting

### No Camera Detected?

Try different camera indices in `global_vars.py`:
```python
CAM_INDEX = 0  # Try 0, 1, 2, etc.
```

### Laggy / Low FPS?

In `global_vars.py`:
```python
MODEL_COMPLEXITY = 0    # Fast mode
WIDTH = 320            # Lower resolution
HEIGHT = 240
FPS = 30              # Lower FPS target
```

### Jerky Tracking?

Improve lighting and ensure camera is stable.

## 📚 Next Steps

1. **Read Full Documentation**: [README.md](README.md)
2. **Learn Setup Details**: [SETUP.md](SETUP.md)
3. **View All Landmarks**: [Body Landmarks Reference](README.md#-available-body-landmarks-33-points)
4. **Contribute**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🎓 Learning Resources

### Understand Pose Detection
- MediaPipe official: https://mediapipe.dev/solutions/pose

### Key Concepts
- **Landmarks**: 33 body points (nose, shoulders, elbows, knees, etc.)
- **Angles**: Joint angles computed from landmarks
- **Smoothing**: Algorithm to reduce tracking jitter
- **UDP**: Network protocol for sending data to other apps

### Project Structure
```
ActTrack/
├── body.py          → Main pose detection engine
├── gui.py           → Dashboard interface  
├── Data_Capture.py  → Motion recording
└── global_vars.py   → Configuration
```

## 💡 Pro Tips

1. **Better Lighting**: More light = better tracking
2. **Full Body**: Keep entire body in frame for best results
3. **Steady Camera**: Use tripod for stable tracking
4. **Smooth Movements**: Jerky motions are harder to track
5. **Check Console**: Error messages appear in terminal

## 🚀 Example Use Cases

### Motion Capture for Games
- Use for avatar control in games
- Record animations
- Real-time player input

### Fitness Tracking
- Analyze exercise form
- Count repetitions
- Joint angle monitoring

### Gesture Recognition
- Detect specific poses
- Create gesture commands
- Interactive applications

### Research & Education
- Study body mechanics
- Computer vision learning
- Human-computer interaction

## ⏱️ First Time Running: Checklist

- [ ] Cloned repository
- [ ] Created virtual environment
- [ ] Installed requirements
- [ ] Ran `python gui.py`
- [ ] Dashboard opened successfully
- [ ] Camera feed showing
- [ ] Landmarks visible on body

## 🆘 Still Having Issues?

1. **Installation Problem?** → See [SETUP.md](SETUP.md#-troubleshooting-setup-issues)
2. **Usage Problem?** → See [README.md](README.md#-troubleshooting)
3. **Want to Contribute?** → See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📞 Quick Links

- 📖 Full Documentation: [README.md](README.md)
- 🔧 Setup Guide: [SETUP.md](SETUP.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 📜 License: [LICENSE](LICENSE)

---

**You're All Set!** 🎉

Run `python gui.py` and start tracking!

*Last Updated: February 25, 2026*
