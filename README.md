# iDownload-lite
The reccomended TUI version of iDownload.

## Installation
iDownload requires Deno, ffmpeg, and get_iplayer. Deno is auto installed when not found. Instructions for installing ffmpeg are present. get_iplayer must be installed separately ([Windows](https://github.com/get-iplayer/get_iplayer_win32/releases/latest), [Mac](https://github.com/get-iplayer/get_iplayer_macos/releases/latest), [Linux - needs hackery magic](https://github.com/get-iplayer/get_iplayer/wiki/unixpkg)).

## Building
**Unix:** Download the latest versions of ```PyInstaller``` and ```auto-py-to-exe``` from PyPi, running on ```Python 3.11.9```. Clone the repo. Use ```pip``` to install the required libraries. Open ```export.json```, and replace every instance of ```<user>``` with your username.<br><br>
**Windows:** Download the latest versions of ```PyInstaller``` and ```auto-py-to-exe``` from PyPi, running on ```Python 3.11.9```. Clone the repo. Use ```pip``` to install the required libraries. Open Command Prompt. Type in auto-py-to-exe. Wait for it to launch. For the script location, use ```main.py```. Change ```One Directory``` to ```One File```. Keep it in ```Console Based``` mode. For ```Icon``` select ```iDownload-lite-logo.ico```. Under ```Advanced```, for ```--name```, type in ```iDownload-lite```. Scroll down to the bottom of the page and click the large ```CONVERT .PY TO .EXE``` button ONCE. Wait.
