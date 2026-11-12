# VisionPlayer (VisionPlayer)

VisionPlayer is a modern, high-performance Windows desktop video player (Windows 10/11 64-bit) fusing touch-friendly mobile-style controls with desktop power, backed by **libmpv** hardware acceleration (Direct3D 11 / `gpu-next`) and signature **One-Click Vision Enhancement**.

Built with a dark aesthetic (`#06080E`, frosted sheet `rgba(11, 15, 24, 0.94)`, `#3B82F6` accent) and a pure high-DPI vector SVG icon architecture.

---

## Key Features

### 1. Signature One-Click Vision Enhancement
- **Autonomous Scene Analysis**: Samples downscaled video frames using NumPy statistics (luma mean, p2/p98 percentiles, chroma spread, clipping metrics) to calculate optimal color curves.
- **Adaptive Presets**: Instant switching between **Auto**, **Vivid**, **Dark Boost**, and **Cinema**.
- **Hold to Compare (`C`)**: Hold the compare button or the `C` key to instantaneously neutralize enhancement and preview the raw input frame.
- **Night Comfort Mode**: Calibrated warm tint gamma shift for low-strain night viewing.

### 2. Transport & Gesture Engine
- **Center Transport**: 68px circular play/pause button with accent glow; 54px frosted circular -10s / +10s skip buttons with tabular time labels.
- **Double-Tap Seek Ripples**: Animated circular ripple pulses (`-10s` on left double-click/tap, `+10s` on right).
- **Smooth Scrub Bar**: Precision hover time preview and tabular monospace timestamps.
- **Touch & Mouse Gestures**:
  - Horizontal drag across video to seek.
  - Vertical drag on left half to adjust display brightness.
  - Vertical drag on right half to adjust volume.
  - Double click for fullscreen; single click to wake/show controls.
  - Mouse wheel for volume adjustment (Shift + Wheel for fine seeking).

### 3. Frosted Options Drawer (12 Dedicated Subviews)
- **Queue**: Active up-next track queue with add, remove, clear, and instant playback.
- **Audio Streams**: Live stream radio selection from mpv, volume slider, and audio delay slider (`-500ms` to `+500ms`).
- **Subtitles**: Dynamic track radio selection, dedicated "Off" switch, text scale adjustment (`70%` to `160%`), and external subtitle loader (`.srt`, `.vtt`, `.ass`).
- **Aspect Ratio**: One-click toggling between **Fit** (`contain`), **Crop** (`cover`), and **Stretch** (`fill`).
- **Display & Enhancement**: Fine-grained Brightness, Contrast, Saturation sliders, Night Comfort filter, and Vision Enhancement presets.
- **5-Band Equalizer**: Live audio equalization using FFmpeg lavfi filters (`60Hz`, `230Hz`, `910Hz`, `4kHz`, `14kHz`) + presets (**Flat**, **Vocal**, **Bass**, **Cinema**).
- **Audio Booster**: Digital volume booster switch with up to 200% gain headroom.
- **Bookmarks**: Per-video persistent bookmarks stored in `library.json`, jump-to-seek, and timestamp creation.
- **Favourite**: Heart toggle marking favorites in the persistent library.
- **Sleep Timer**: Built-in timers for 15, 30, 45, 60 minutes or end-of-episode playback termination.
- **Information**: Live hardware metadata (Container, Resolution, Codecs, Bitrate, Hardware Decoder).
- **Share & Snapshot**: Copy path with timestamp link to clipboard; lossless PNG snapshot capture.

---

## Running the Application

### 1. Launch with Python Environment
```powershell
.\.venv\Scripts\python.exe main.py
```
Pass an optional file path or stream URL directly:
```powershell
.\.venv\Scripts\python.exe main.py "D:\Movies\sample.mp4"
```

### 2. Execute Test Suite
```powershell
.\.venv\Scripts\pytest.exe tests/ -v
```

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `Space` | Play / Pause |
| `Left` / `Right` | Seek ±5s (Double-tap / buttons for ±10s) |
| `Up` / `Down` | Volume ±5% |
| `N` | Skip to Next track in playlist |
| `P` | Skip to Previous track in playlist |
| `[` / `]` | Cycle A-B Repeat Loop (Point A → Point B → Clear) |
| `E` | Toggle Vision Enhancement on/off |
| `C` | Hold to compare with original video frame |
| `S` | Capture frame snapshot |
| `M` | Mute / Unmute audio |
| `L` | Lock / Unlock player controls |
| `F` | Toggle Fullscreen |
| `Ctrl + O` | Open File dialog |
| `Ctrl + U` | Open URL dialog |
| `Esc` | Close active drawer or exit Fullscreen |

---

## Standalone Packaging & Distribution

### Building the Windows Executable (`.exe`)
VisionPlayer can be bundled into a standalone Windows distribution using the provided PyInstaller spec:
```powershell
.\.venv\Scripts\pyinstaller.exe packaging/visionplayer.spec
```
The output bundle will be generated in `dist/VisionPlayer/` with `libmpv-2.dll` and all required runtimes included.

### Creating the Setup Installer
Compile `packaging/installer.iss` using Inno Setup Compiler to produce `VisionPlayer-Setup-1.0.0.exe` with desktop shortcuts and Windows video file associations (`.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`).
