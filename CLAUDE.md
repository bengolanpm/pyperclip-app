# pyperclip app

Clipboard manager menubar app for macOS. Stores up to 25 clipboard items (text and images) and lets you re-paste any of them from the menubar icon.

## Files
- `clipboard_manager.py` — main app (uses NSPasteboard + rumps)
- `clipboard_manager.py.bak` — previous text-only version
- `start.sh` — restart the app
- `install_autostart.sh` — install as a login item via LaunchAgent

## Run
```bash
~/clipboard_manager/start.sh
```
