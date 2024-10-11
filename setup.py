from setuptools import setup

APP = ['main.py']
OPTIONS = {
	'argv_emulation': True,
	'plist': {
		'LSUIElement': True,
	},
	'packages': ['rumps', 'pydub'],
}

setup(
	app=APP,
	options={'py2app': OPTIONS},
	setup_requires=['py2app'],
)
