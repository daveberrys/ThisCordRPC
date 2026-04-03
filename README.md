# ThisCordRPC
Just another app that displays your Discord Activity but with presets and mimics the Discord UI. Made with [Pyder](https://github.com/PinpointTools/Pyder).

**PREVIEW**
![preview](readme/preview.png)

---

## Where are the downloads?
We reccomend you building it yourself. Install [python 3.13](https://www.python.org/downloads/release/python-31312/) and [node.js](https://nodejs.org/en/download) and follow these instruction:
- Clone the GitHub repository
- `cd` into the cloned repository in your local files
- Ensure you have pnpm by running `pnpm --version`
  - If you don't, install it by `npm install -g pnpm`. If you're running Linux, use `sudo npm install -g pnpm`.
- Create a virtual environment by running: `py -3.13 -m venv venv`
- Install dependencies for backend with python `venv/bin/pip -r requirements.txt`
- Install dependencies for python with pnpm `cd src/frontend` `pnpm install --frozen-lockfile` `cd ../..`
- Build the app `venv/bin/python run.py compile`
- Check the directory at `dist/ThisCordRPC`. Open the executable! `ThisCordRPC.exe` or `ThisCordRPC` if unix (macOS/Linux).