# Created this to farm XP and coins in Sekiro.

# InputAutomator - Record & Replay Mouse/Keyboard Actions

Simple Python tool to record and replay keyboard/mouse inputs for automation.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Record actions:
   ```bash
   python record.py
   ```
   - Type `start` to begin recording
   - Perform your actions
   - Type `done` to stop

3. Replay actions:
   ```bash
   python follow.py
   ```

## Files

- `record.py` - Records input to `input_log.txt`
- `follow.py` - Replays actions from log file
- `requirements.txt` - Dependencies (pynput, pyautogui)

## Safety Warning

⚠️ The replay script controls your mouse and keyboard. Test carefully and ensure you can regain control.
