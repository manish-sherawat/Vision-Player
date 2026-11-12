"""VisionPlayer entry point."""
import sys
import os
import io
import threading
from pathlib import Path

# Explicitly configure FFmpeg media backend for QtMultimedia before Qt application starts
os.environ.setdefault("QT_MEDIA_BACKEND", "ffmpeg")

# Silence known-harmless FFmpeg MFT/codec-probe noise that floods stderr.
# These messages appear when FFmpeg tries Windows Media Foundation hardware
# decoders (av1_mf, hevc_mf, h264_mf) and falls back to software — which is
# perfectly fine.  We capture stderr and re-emit real errors through the logger.
_FFMPEG_NOISE = (
    "could not find any MFT",
    "could not create MFT",
    "[av1_mf @",
    "[hevc_mf @",
    "[h264_mf @",
    "[wmv3_mf @",
    "[vc1_mf @",
    "No accelerated colorspace conversion found",
    "No decoder surfaces left",
)


class _StderrFilter(io.TextIOBase):
    """Forwards stderr lines to the Python logger, dropping known FFmpeg noise."""

    def __init__(self, original: io.TextIOBase):
        self._orig = original
        self._buf = ""
        # Logger is set after setup_logger() is called
        self.logger = None

    def write(self, text: str) -> int:
        self._buf += text
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            self._emit(line)
        return len(text)

    def _emit(self, line: str) -> None:
        if not line.strip():
            return
        # Drop known harmless codec-probe noise
        if any(noise in line for noise in _FFMPEG_NOISE):
            return
        # Everything else goes to original stderr AND logger
        self._orig.write(line + "\n")
        self._orig.flush()
        if self.logger:
            self.logger.debug("[stderr] %s", line.rstrip())

    def flush(self) -> None:
        if self._buf:
            self._emit(self._buf)
            self._buf = ""
        self._orig.flush()

    def fileno(self):
        return self._orig.fileno()


_stderr_filter = _StderrFilter(sys.stderr)
sys.stderr = _stderr_filter

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from app.core.logger import setup_logger
from app.ui.main_window import MainWindow


def main():
    # Setup global logger
    logger = setup_logger("visionplayer")
    _stderr_filter.logger = logger  # attach logger so real stderr lines are captured
    logger.info("Starting VisionPlayer (media backend: %s)...", os.environ.get("QT_MEDIA_BACKEND", "default"))

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("VisionPlayer")
    app.setOrganizationName("VisionPlayer")

    # Check for CLI arguments (video file passed to open or engine override)
    initial_file = None
    override_engine = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--engine="):
            override_engine = arg.split("=", 1)[1].strip()
        elif arg == "--engine" and i + 1 < len(args):
            override_engine = args[i + 1].strip()
            i += 1
        elif os.path.exists(arg):
            initial_file = os.path.abspath(arg)
        i += 1

    window = MainWindow(initial_file=initial_file, engine_override=override_engine)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

