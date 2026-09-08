# Keep On Mining Autominer

A small Windows automation tool for the browser game **Keep On Mining**. It moves the mouse around the mining board, clicks at a steady interval, dismisses the game's **KEEP ON MINING** prompt, and attempts to click the yellow confirmation button shown by occasional artifact popups.

## Requirements

- Windows 10 or newer
- The game open in a visible browser window
- A display layout and game window similar to the layout used when this tool was configured

For running from Python:

- Python 3.10 or newer
- Python packages: `pyautogui`, `keyboard`, and `Pillow`

## Quick Start

### Use the packaged app

1. Download `KeepOnMining.exe` from the `dist` folder or from the repository's Releases page.
2. Open the game and keep its window visible.
3. Run `KeepOnMining.exe`.
4. Press `F8` to start mining.
5. Press `F9` to stop mining.
6. Press `Esc` to exit the program.

The console prints the current state and reports when it finds a game button or artifact popup.

### Run from source

Open PowerShell in the project folder and install the runtime dependencies:

```powershell
py -m pip install pyautogui keyboard Pillow
```

Start the script:

```powershell
py keep-on-mining.py
```

Then use the same controls: `F8` starts, `F9` stops, and `Esc` exits.

## Build the Windows executable

Install PyInstaller if needed:

```powershell
py -m pip install pyinstaller
```

Build from the included spec file:

```powershell
py -m PyInstaller --clean --noconfirm KeepOnMining.spec
```

The executable is written to `dist\KeepOnMining.exe`.

## How It Works

- A mining thread moves the cursor around four approximate board edges and clicks every 0.20 seconds.
- A separate watcher searches for the normal **KEEP ON MINING** button.
- When that button is not visible, the watcher scans the lower-center area for the artifact popup's yellow confirmation button.
- The screen coordinates are calculated from the current display size, but the game layout still needs to be reasonably close to the configured layout.

## Important Notes

- Keep the game in the foreground and do not move or resize it while the autominer is running.
- Do not use the mouse or keyboard for other tasks while it is active.
- Screen scaling, browser zoom, window size, and display changes can affect detection accuracy.
- The tool performs real mouse movement and clicks. Use it only where automation is permitted by the game and its rules.
- Press `F9` before closing the game or moving the browser window.

## Project Files

- `keep-on-mining.py` - automation source code
- `keep_on_mining.png` - template image for the normal game button
- `KeepOnMining.spec` - PyInstaller build configuration
- `dist\KeepOnMining.exe` - packaged Windows executable
