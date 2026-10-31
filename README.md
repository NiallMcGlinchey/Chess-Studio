# Chess Studio – Luxury Edition

A Windows desktop chess application built with Python, PySide6, python-chess and Stockfish.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Stockfish Windows executable

## Setup
1. Install Python.
2. Open PowerShell in this folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Download a Windows build of Stockfish from https://stockfishchess.org/download/
6. Put the engine executable at `stockfish/stockfish.exe`.
7. Start the app:

   ```powershell
   python main.py
   ```

## Current prototype notes
- White plays the human; Stockfish plays Black.
- Promotion currently defaults to a queen. A promotion chooser is planned.
- The first prototype uses SVG chess glyph assets and the installed Windows symbol font.
- Engine strength uses Stockfish's UCI `Skill Level` option.
- This is an early prototype, not a finished release.

## Planned next steps
- Add robust engine cancellation and restart handling.
- Add promotion selection and move animation.
- Improve move-history presentation and game-end dialogs.
- Add additional theme packs and settings persistence.
- Package for Windows with PyInstaller.

## Stockfish licensing
Stockfish is distributed under the GNU General Public License version 3 (GPLv3). If distributing Stockfish with this application, include the required licence notices and comply with the GPL source-code distribution requirements. See the Stockfish website for current details.
