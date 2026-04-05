import webview as wv
import sys
import os
import ctypes
from pyder import *

import src.backend.handlers.discordRPC as drpc
import src.backend.handlers.json as json_handler

if sys.platform == "win32":
    from ctypes import wintypes

class API:
    def __init__(self):
        self.appID = f"{pyder_domainSystem}.{pyder_projectID}"
        self.handler = drpc.DiscordRPC()
        self.json = json_handler.JSON(self)

    def getWindow(self):
        activeWindow = wv.active_window()

        if activeWindow:
            return activeWindow
        elif len(wv.windows) > 0:
            return wv.windows[0]
        else:
            return None

    def getConfigPath(self):
        if sys.platform == "win32":
            configPath = os.path.join(os.getenv("APPDATA"), self.appID)
        elif sys.platform == "darwin":
            configPath = os.path.join(os.getenv("HOME"), "Library", "Application Support", self.appID)
        elif sys.platform == "linux":
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        else:
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        return configPath
    
    def getOS(self):
        if sys.platform == "win32":
            return "Windows"
        elif sys.platform == "darwin":
            return "macOS"
        elif sys.platform == "linux":
            return "Linux"
        else:
            return "Unknown"

    # pyder
    def getVer(self):
        return pyder_version

    # discord rpc
    def connectDiscordRPC(self):
        return self.handler.connect()
    def updateDiscordRPC(self, title, details, state, largeImage, smallImage, largeImageText="", smallImageText=""):
        self.handler.update(title, details, state, largeImage, smallImage, largeImageText, smallImageText)
    def clearDiscordRPC(self):
        self.handler.clear()
    def checkConnected(self):
        return self.handler.isConnected
    def getDiscordRPCError(self):
        return self.handler.lastError

    # presets
    def loadPresets(self):
        return self.json.loadJSON()
    def savePreset(self, title, details, state, largeImage, smallImage, largeImageText="", smallImageText=""):
        return self.json.savePreset(title, details, state, largeImage, smallImage, largeImageText, smallImageText)
    def editPreset(self, oldTitle, title, details, state, largeImage, smallImage, largeImageText="", smallImageText=""):
        return self.json.editPreset(oldTitle, title, details, state, largeImage, smallImage, largeImageText, smallImageText)
    def deletePreset(self, title):
        return self.json.deletePreset(title)
    
    # system stuff
    def exitApp(self):
        currentWindow = self.getWindow()

        if currentWindow == None:
            print("Window was null. App could not exit.")
            return None
        else:
            currentWindow.destroy()
            return True
    def minimizeApp(self):
        currentWindow = self.getWindow()

        if currentWindow == None:
            print("Window was null. App could not minimize.")
            return None
        else:
            currentWindow.minimize()
            return True
