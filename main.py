import os
import sys
import wave

import rumps
from AVFoundation import AVAudioPlayer
from Foundation import NSURL


def resource_path(*parts):
    """Resolve a path relative to the app bundle (py2app) or the source tree."""
    base = getattr(sys, "_MEIPASS", None) or os.environ.get("RESOURCEPATH")
    if not base:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def ensure_silence_wav(path, seconds=10, rate=44100):
    """Generate a silent stereo 16-bit WAV once; AVAudioPlayer loops it forever."""
    if os.path.exists(path):
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"\x00" * (rate * seconds * 2 * 2))
    return path


class App(rumps.App):
    def __init__(self):
        # template=True: macOS tints the icon to match the menu bar (light/dark).
        super().__init__("Active BT Audio", template=True, quit_button=None)
        self.icon_active = resource_path("assets", "icon_active.png")
        self.icon_inactive = resource_path("assets", "icon_inactive.png")
        self.menu = [
            rumps.MenuItem("Start", callback=self.start),
            rumps.MenuItem("Stop", callback=self.stop),
            None,
            rumps.MenuItem("Quit", callback=self.quit),
        ]

        wav = ensure_silence_wav(
            os.path.join(
                os.path.expanduser("~/Library/Caches/keep-bt-audio-on"), "silence.wav"
            )
        )
        self.player, err = AVAudioPlayer.alloc().initWithContentsOfURL_error_(
            NSURL.fileURLWithPath_(wav), None
        )
        if self.player is None:
            raise RuntimeError(f"AVAudioPlayer init failed: {err}")
        # One continuous stream: looping happens inside the audio queue, so
        # macOS never sees a "new audio started" event (no AirPods stealing).
        self.player.setNumberOfLoops_(-1)
        self.player.setVolume_(0.0)
        self.player.prepareToPlay()

        self.start(None)

    def start(self, _):
        self.player.play()
        self.icon = self.icon_active
        self.menu["Start"].set_callback(None)
        self.menu["Stop"].set_callback(self.stop)

    def stop(self, _):
        self.player.stop()
        self.icon = self.icon_inactive
        self.menu["Start"].set_callback(self.start)
        self.menu["Stop"].set_callback(None)

    def quit(self, _):
        self.player.stop()
        rumps.quit_application()


if __name__ == "__main__":
    App().run()
