# Changelog

All notable changes to ActTrack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- [ ] Multi-person pose detection
- [ ] Gesture recognition system
- [ ] Export to multiple video formats
- [ ] Performance benchmarking tools
- [ ] Web-based dashboard
- [ ] REST API for external applications
- [ ] Machine learning-based pose classification
- [ ] 3D pose visualization
- [ ] Custom angle profile system

### Under Investigation
- ONNX model support for better portability
- GPU optimization enhancements
- Mobile app integration

---

## [1.0.0] - 2026-02-25

### Release Type: Initial Release

This is the first stable release of ActTrack, featuring core functionality for real-time body pose detection and motion capture.

### Added

#### Core Features
- Real-time body pose detection using MediaPipe
- 33 body landmark tracking with X, Y, Z coordinates
- Joint angle calculation for key body parts
- Smooth landmark filtering to reduce jitter
- Live visualization of pose data

#### User Interface
- Advanced Debug Dashboard with tabbed interface
- Debug Table Tab - View real-time landmark coordinates
- Settings Tab - Configure camera and model parameters  
- Logs Tab - Monitor system events and metrics
- Games Tab - Interactive pose-based games

#### Data Capture
- Motion sequence recording to JSON format
- Angle data export
- Real-time data visualization
- Data playback and analysis

#### Communication
- UDP-based streaming protocol
- JSON data format for landmarks and angles
- Network-agnostic design for external integration

#### Integration
- Unity C# example code provided
- Flask/Python backend integration examples
- Configurable UDP endpoint

#### Documentation
- Comprehensive README.md
- Quick Start Guide
- Detailed Setup Instructions
- API Documentation
- Contributing Guidelines
- Code of Conduct
- License Documentation (Non-Commercial)
- FAQ with 50+ answers
- Troubleshooting Guide

#### Configuration
- Webcam and resolution settings
- FPS and frame rate control
- Model complexity adjustment (0-2)
- UDP connection settings
- Global debugging options

#### Developer Features
- Multi-threaded architecture for performance
- Comprehensive error handling
- Debug logging system
- Configurable smoothing algorithms

### Features Included

- ✅ Real-time pose detection (30+ FPS)
- ✅ 33-point body landmark tracking
- ✅ Joint angle calculations
- ✅ UDP streaming
- ✅ Motion recording
- ✅ Modern GUI
- ✅ Configuration management
- ✅ Professional documentation

### Technical Specifications

- **Language**: Python 3.8+
- **Dependencies**: MediaPipe, OpenCV, NumPy, Tkinter
- **Architecture**: Multi-threaded
- **License**: Non-Commercial Educational
- **Protocol**: UDP with JSON payload

### Known Limitations

- Single person tracking (MediaPipe Pose limitation)
- No built-in gesture recognition
- Video export requires external processing
- Desktop application only (no mobile support)

### Performance Baseline

- **FPS**: 20-60 depending on hardware
- **Latency**: 50-100ms on typical systems
- **Memory Usage**: 300-500MB
- **CPU Impact**: 15-40% on modern systems
- **GPU Impact**: 20-50% (when available)

### Installation

- Easy virtual environment setup
- Single command dependency installation
- Windows, macOS, and Linux support
- Automated verification script included

### Project Structure
```
ActTrack/
├── Documentation (7 markdown files)
├── Source Code (6 Python modules)
├── Configuration (JSON and Python)
└── Assets (Icon, Data files)
```

### Contributors
- XeroD (Creator and Lead Developer)

### Breaking Changes
- None (initial release)

### Migration Guide
- N/A (initial release)

### Dependencies Added
- mediapipe 0.10.8
- opencv-python 4.8.1
- numpy 1.24.3
- Pillow 10.0.0
- sv-ttk 2.6.0

### Security
- No external web services used
- Local-only processing
- No automatic data transmission
- Privacy-first design

### Accessibility
- Dark and light theme options
- Responsive UI design
- Keyboard navigation support
- Clear visual feedback

---

## Version History

### Version Numbering

We use Semantic Versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Schedule

We aim to release updates quarterly with:
- Bug fixes (patch releases)
- Minor improvements (minor releases)
- Major features (major releases)

---

## Future Roadmap

### Upcoming Features
- [ ] Web dashboard
- [ ] API endpoints
- [ ] Mobile companion app
- [ ] Advanced analytics
- [ ] Multi-pose support
- [ ] Custom model support

### Performance Improvements
- [ ] GPU acceleration optimizations
- [ ] Memory usage reduction
- [ ] Faster initialization
- [ ] Improved smoothing algorithms

### Documentation Enhancements
- [ ] Video tutorials
- [ ] Interactive guides
- [ ] Code examples library
- [ ] API documentation expansion

---

## Report Issues

Found a bug or want to request a feature?

1. Check [FAQ.md](FAQ.md) for common questions
2. Search existing issues in GitHub
3. Create a new issue with detailed information
4. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Requesting features
- Submitting code
- Improving documentation

---

## License

ActTrack is released under a Non-Commercial Educational License.
See [LICENSE](LICENSE) for full terms.

**All versions of ActTrack are for non-commercial use only.**

---

## Support

- 📖 Documentation: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- ❓ FAQ: [FAQ.md](FAQ.md)
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## Acknowledgments

### Technologies
- Google MediaPipe - Pose detection
- OpenCV - Computer vision
- Python community

### Contributors
- XeroD - Creator

### Community
- All users and contributors

---

*Last Updated: February 25, 2026*

[Unreleased]: https://github.com/XeroD/ActTrack/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/XeroD/ActTrack/releases/tag/v1.0.0
