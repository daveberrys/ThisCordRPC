import fs from "node:fs";
import path from "node:path";

export class JSONHandler {
  constructor(api) {
    this.api = api;
    this.configPath = api.getProjectConfigPath();
    this.presencePath = path.join(this.configPath, "presence.json");
  }

  defaultJSON() {
    return {
      presets: {}
    };
  }

  ensureStorage() {
    fs.mkdirSync(this.configPath, {
      recursive: true
    });

    if (!fs.existsSync(this.presencePath)) {
      fs.writeFileSync(
        this.presencePath,
        JSON.stringify(this.defaultJSON(), null, 2),
        "utf8"
      );
    }
  }

  loadJSON() {
    this.ensureStorage();

    const fileContent = fs.readFileSync(this.presencePath, "utf8");
    return JSON.parse(fileContent);
  }

  writeJSON(data) {
    this.ensureStorage();
    fs.writeFileSync(this.presencePath, JSON.stringify(data, null, 2), "utf8");
    return data;
  }

  savePreset(title, details, state, largeImage, smallImage, largeImageText = "", smallImageText = "") {
    const cleanTitle = title.trim();
    if (!cleanTitle) {
      throw new Error("Preset title cannot be empty.");
    }

    const data = this.loadJSON();
    data.presets[cleanTitle] = {
      title: cleanTitle,
      details,
      state,
      largeImage,
      smallImage,
      largeImageText,
      smallImageText
    };

    this.writeJSON(data);
    return data.presets[cleanTitle];
  }

  editPreset(oldTitle, title, details, state, largeImage, smallImage, largeImageText = "", smallImageText = "") {
    const cleanOldTitle = oldTitle.trim();
    const cleanTitle = title.trim();

    if (!cleanTitle) {
      throw new Error("Preset title cannot be empty.");
    }

    const data = this.loadJSON();
    if (!data.presets[cleanOldTitle]) {
      throw new Error(`Preset '${cleanOldTitle}' was not found.`);
    }

    if (cleanOldTitle !== cleanTitle) {
      delete data.presets[cleanOldTitle];
    }

    data.presets[cleanTitle] = {
      title: cleanTitle,
      details,
      state,
      largeImage,
      smallImage,
      largeImageText,
      smallImageText
    };

    this.writeJSON(data);
    return data.presets[cleanTitle];
  }

  deletePreset(title) {
    const cleanTitle = title.trim();
    const data = this.loadJSON();

    if (!data.presets[cleanTitle]) {
      throw new Error(`Preset '${cleanTitle}' was not found.`);
    }

    const deletedPreset = data.presets[cleanTitle];
    delete data.presets[cleanTitle];
    this.writeJSON(data);
    return deletedPreset;
  }
}
