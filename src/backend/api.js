import path from "node:path";

import { DiscordRPC } from "./handlers/discordRPC.js";
import { JSONHandler } from "./handlers/json.js";

export class API {
  constructor(options) {
    this.app = options.app;
    this.browserWindow = options.browserWindow;
    this.projectConfig = options.projectConfig;
    this.appID = `${this.projectConfig.domainSystem}.${this.projectConfig.projectID}`;
    this.handler = new DiscordRPC();
    this.json = new JSONHandler(this);
  }

  getConfigPath() {
    return this.app.getPath("appData");
  }

  getProjectConfigPath() {
    return path.join(this.getConfigPath(), this.appID);
  }

  getOS() {
    if (process.platform === "win32") {
      return "Windows";
    }

    if (process.platform === "darwin") {
      return "macOS";
    }

    if (process.platform === "linux") {
      return "Linux";
    }

    return "Unknown";
  }

  getVer() {
    return this.projectConfig.version;
  }

  async connectDiscordRPC() {
    return this.handler.connect();
  }

  async updateDiscordRPC(title, details, state, largeImage, smallImage, largeImageText = "", smallImageText = "") {
    return this.handler.update(
      title,
      details,
      state,
      largeImage,
      smallImage,
      largeImageText,
      smallImageText
    );
  }

  async clearDiscordRPC() {
    return this.handler.clear();
  }

  checkConnected() {
    return this.handler.isConnected;
  }

  getDiscordRPCError() {
    return this.handler.lastError;
  }

  loadPresets() {
    return this.json.loadJSON();
  }

  savePreset(title, details, state, largeImage, smallImage, largeImageText = "", smallImageText = "") {
    return this.json.savePreset(title, details, state, largeImage, smallImage, largeImageText, smallImageText);
  }

  editPreset(oldTitle, title, details, state, largeImage, smallImage, largeImageText = "", smallImageText = "") {
    return this.json.editPreset(
      oldTitle,
      title,
      details,
      state,
      largeImage,
      smallImage,
      largeImageText,
      smallImageText
    );
  }

  deletePreset(title) {
    return this.json.deletePreset(title);
  }

  exitApp() {
    if (this.browserWindow === null) {
      console.log("Window was null. App could not exit.");
      return null;
    }

    this.browserWindow.close();
    return true;
  }

  minimizeApp() {
    if (this.browserWindow === null) {
      console.log("Window was null. App could not minimize.");
      return null;
    }

    this.browserWindow.minimize();
    return true;
  }
}
