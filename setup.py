from setuptools import setup

APP = ["main.py"]
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "LSUIElement": True,
    },
    "packages": ["rumps", "pydub", "subprocess", "threading", "tempfile"],
}

DATA_FILES = [("assets", ["assets/icon_active.png", "assets/icon_inactive.png"])]

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
	data_files=DATA_FILES,
)
