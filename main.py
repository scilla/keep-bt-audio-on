import subprocess
from tempfile import NamedTemporaryFile
import rumps
from pydub import AudioSegment
import threading


class App(rumps.App):
    def __init__(self):
        super(App, self).__init__("Active BT Audio")
        self.icon_active = "assets/icon_active.png"
        self.icon_inactive = "assets/icon_inactive.png"
        self.menu.add(rumps.MenuItem("Start", callback=self.start))
        self.menu.add(rumps.MenuItem("Stop", callback=self.stop))
        self.audio_timeout = 15000
        self.silent_audio = AudioSegment.silent(duration=self.audio_timeout)
        self.is_running = False
        self.icon = self.icon_inactive
        self.start(None)

    def start(self, _):
        if not self.is_running:
            self.is_running = True
            self.play_silent_audio_loop()
        self.icon = self.icon_active
        self.menu["Start"].set_callback(None)
        self.menu["Stop"].set_callback(self.stop)

    def stop(self, _):
        self.is_running = False
        self.icon = self.icon_inactive
        self.menu["Start"].set_callback(self.start)
        self.menu["Stop"].set_callback(None)

    def _play(self):
        with NamedTemporaryFile("w+b", suffix=".wav") as f:
            self.silent_audio.export(f.name, "wav")
            subprocess.call(
                [
                    "ffplay",
                    "-nodisp",
                    "-autoexit",
                    "-hide_banner",
                    "-loglevel",
                    "-8",
                    f.name,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def play_silent_audio_loop(self):
        def loop():
            while self.is_running:
                self._play()

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()


if __name__ == "__main__":
    app = App()
    app.run()
