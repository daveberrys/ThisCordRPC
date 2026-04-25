import DiscordRPCPackage from "discord-rpc";

const DiscordRPCClient = DiscordRPCPackage;

export class DiscordRPC {
  constructor() {
    this.clientID = "1320113441964429423";
    this.rpc = null;
    this.isConnected = false;
    this.lastError = "";
  }

  async connect() {
    if (this.isConnected && this.rpc !== null) {
      return true;
    }

    try {
      this.rpc = new DiscordRPCClient.Client({
        transport: "ipc"
      });

      this.rpc.on("disconnected", () => {
        this.isConnected = false;
      });

      await this.rpc.login({
        clientId: this.clientID
      });

      this.isConnected = true;
      this.lastError = "";
      return true;
    } catch (error) {
      this.isConnected = false;
      this.lastError = String(error);
      this.rpc = null;
      return false;
    }
  }

  async update(
    title = "ThisCordRPC",
    details = "",
    state = "",
    largeImage = "",
    smallImage = "",
    largeImageText = "",
    smallImageText = ""
  ) {
    if (!this.isConnected || this.rpc === null) {
      return null;
    }

    await this.rpc.setActivity({
      type: 0,
      name: title,
      details: details || null,
      state: state || null,
      largeImageKey: largeImage || null,
      smallImageKey: smallImage || null,
      largeImageText: largeImageText || null,
      smallImageText: smallImageText || null,
      startTimestamp: new Date()
    });

    return true;
  }

  async clear() {
    if (!this.isConnected || this.rpc === null) {
      return null;
    }

    await this.rpc.clearActivity();
    return true;
  }
}
