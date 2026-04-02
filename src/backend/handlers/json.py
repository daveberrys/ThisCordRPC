import json
import os

class JSON:
    def __init__(self, api):
        self.api = api
        self.configPath = api.getConfigPath()
        self.presetPath = os.path.join(self.configPath, "presets.json")

    def _defaultJSON(self):
        return {"presets": {}}

    def _ensureStorage(self):
        os.makedirs(self.configPath, exist_ok=True)

        if not os.path.exists(self.presetPath):
            with open(self.presetPath, "w", encoding="utf-8") as f:
                json.dump(self._defaultJSON(), f, indent=2)
    
    def loadJSON(self):
        self._ensureStorage()

        with open(self.presetPath, encoding="utf-8") as f:
            return json.load(f)
    
    def writeJSON(self, data):
        self._ensureStorage()

        with open(self.presetPath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return data

    def getPresets(self):
        return self.loadJSON()["presets"]

    def savePreset(self, title, details, state, largeImage, smallImage, largeImageText="", smallImageText=""):
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Preset title cannot be empty.")

        data = self.loadJSON()
        data["presets"][clean_title] = {
            "title": clean_title,
            "details": details,
            "state": state,
            "largeImage": largeImage,
            "smallImage": smallImage,
            "largeImageText": largeImageText,
            "smallImageText": smallImageText,
        }
        self.writeJSON(data)
        return data["presets"][clean_title]

    def editPreset(
        self,
        oldTitle,
        title,
        details,
        state,
        largeImage,
        smallImage,
        largeImageText="",
        smallImageText="",
    ):
        clean_old_title = oldTitle.strip()
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Preset title cannot be empty.")

        data = self.loadJSON()
        if clean_old_title not in data["presets"]:
            raise KeyError(f"Preset '{clean_old_title}' was not found.")

        if clean_old_title != clean_title:
            del data["presets"][clean_old_title]

        data["presets"][clean_title] = {
            "title": clean_title,
            "details": details,
            "state": state,
            "largeImage": largeImage,
            "smallImage": smallImage,
            "largeImageText": largeImageText,
            "smallImageText": smallImageText,
        }
        self.writeJSON(data)
        return data["presets"][clean_title]

    def deletePreset(self, title):
        clean_title = title.strip()
        data = self.loadJSON()

        if clean_title not in data["presets"]:
            raise KeyError(f"Preset '{clean_title}' was not found.")

        deleted_preset = data["presets"].pop(clean_title)
        self.writeJSON(data)
        return deleted_preset
