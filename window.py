import os
import sys
import json
from pyder import *

import webview as wv
from src.backend.api import API

if getattr(sys, "frozen", False):
    resourceRoot = os.path.abspath(sys._MEIPASS)
    projectRoot = os.path.dirname(os.path.abspath(sys.executable))
else:
    projectRoot = os.path.dirname(os.path.abspath(__file__))
    resourceRoot = projectRoot

distDir = os.path.join(resourceRoot, "src", "frontend", "dist")

iconPath = ""
if sys.platform == "win32":
    iconPath = os.path.join(resourceRoot, "icon", "512.ico")
elif sys.platform == "darwin":
    iconPath = os.path.join(resourceRoot, "icon", "512.icns")
else:
    iconPath = os.path.join(resourceRoot, "icon", "512.png")

def startWindow(dev=False):
    if dev:
        pathToApp = "http://localhost:5173"
    else:
        pathToApp = os.path.join(distDir, "index.html")
        if not os.path.exists(pathToApp):
            raise FileNotFoundError(
                "Frontend build output was not found. Run `python run.py test` or `python run.py compile` first."
            )

    wv.create_window(
        title=pyder_projectName,
        url=str(pathToApp),
        js_api=API(),
        width=pyder_window_initSize_v1,
        height=pyder_window_initSize_v2,
        min_size=(pyder_window_minSize_v1, pyder_window_minSize_v2),
        resizable=True,
    )

    wv.start(
        http_server=True,
        private_mode=False,
        debug=not getattr(sys, "frozen", False),
        icon=iconPath,
    )

if __name__ == "__main__":
    startWindow()