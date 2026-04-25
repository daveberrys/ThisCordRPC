# Project initialized with Pyder! @ https://github.com/PinpointTools/Pyder
# Pyder is a Python-based tool for building cross-platform desktop applications.
# If you love how Pyder works, please consider starring it on GitHub.

import argparse
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
import window as w
from pyder import *

projectRoot = Path(__file__).resolve().parent
frontendDir = projectRoot / "src" / "frontend"
devServerHost = "localhost"
devServerPort = 5173
packageManager = "pnpm"

def resolveCommand(command):
    commandPath = shutil.which(command)
    if commandPath:
        return commandPath

    if sys.platform == "win32":
        commandPath = shutil.which(f"{command}.cmd")
        if commandPath:
            return commandPath
    return command

packageManager = resolveCommand(packageManager)
def buildFrontend():
    subprocess.run([packageManager, "run", "build"], cwd=frontendDir, check=True)

class SeparateWindow:
    def waitForDevServer(self, timeoutSeconds=20):
        deadline = time.time() + timeoutSeconds
        while time.time() < deadline:
            try:
                with socket.create_connection((devServerHost, devServerPort), timeout=1):
                    return
            except OSError:
                time.sleep(0.25)
                
        raise TimeoutError(
            f"Timed out waiting for the frontend dev server at http://{devServerHost}:{devServerPort}."
        )

    def launchFrontendDevServerInSeparateWindow(self):
        if sys.platform == "win32":
            subprocess.run(
                [
                    "cmd",
                    "/c",
                    "start",
                    "Protux Frontend Dev Server",
                    packageManager,
                    "run",
                    "dev",
                ],
                cwd=frontendDir,
                check=True,
            )
            return
    
        if sys.platform == "darwin":    
            script = (
                f'tell application "Terminal" to do script '
                f'"cd {frontendDir} && {packageManager} run dev"'
            )
            subprocess.run(["osascript", "-e", script], check=True)
            return
    
        for terminal in ("x-terminal-emulator", "gnome-terminal", "konsole", "xterm"):
            terminalPath = shutil.which(terminal)
            if terminalPath:
                subprocess.run(
                    [terminalPath, "-e", packageManager, "run", "dev"],
                    cwd=frontendDir,
                    check=True,
                )
                return
    
        raise RuntimeError(
            "Could not find a terminal emulator to launch the frontend dev server. "
            "Run `python run.py dev backend` in a separate terminal instead."
        )

def runDevServer():
    subprocess.run([packageManager, "run", "dev"], cwd=frontendDir, check=True)

def compileApp():
    buildFrontend()
    separator = ";" if sys.platform == "win32" else ":"
    dataArg = f"{frontendDir / 'dist'}{separator}src/frontend/dist"
    iconArg = f"{'icon'}{separator}icon"
    if sys.platform == "win32":
        pyinstallerIcon = "icon/favicon.ico"
    elif sys.platform == "darwin":
        pyinstallerIcon = "icon/favicon.icns"
    else:
        pyinstallerIcon = "icon/favicon.png"

    pyinstallerArgs = [
        sys.executable,
        "-m",
        "PyInstaller",
        "window.py",
        "--noconfirm",
        "--windowed",
        "--name",
        pyder_projectName,
        "--add-data",
        dataArg,
        "--add-data",
        iconArg,
        f"--icon={pyinstallerIcon}",
    ]

    if sys.platform == "win32":
        pyinstallerArgs.extend(["--collect-all", "winpty"])

    subprocess.run(
        pyinstallerArgs,
        cwd=projectRoot,
        check=True,
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["test", "compile", "dev"])
    parser.add_argument("target", nargs="?", choices=["window", "server"])
    args = parser.parse_args()

    if args.command != "dev" and args.target is not None:
        parser.error("`window` and `server` targets are only valid with `python run.py dev`.")

    if args.command == "test":
        buildFrontend()
        w.startWindow()
    elif args.command == "compile":
        compileApp()
    elif args.command == "dev":
        if args.target == "window":
            w.startWindow(True)
        elif args.target == "server":
            runDevServer()
        else:
            SeparateWindow().launchFrontendDevServerInSeparateWindow()
            SeparateWindow().waitForDevServer()
            w.startWindow(True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        exit(1)