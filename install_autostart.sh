#!/bin/bash
# Installs a LaunchAgent so the clipboard manager starts automatically at login

PLIST="$HOME/Library/LaunchAgents/com.bengolan.clipboardmanager.plist"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bengolan.clipboardmanager</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${SCRIPT_DIR}/clipboard_manager.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/clipboard_manager.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/clipboard_manager.log</string>
</dict>
</plist>
EOF

launchctl load "$PLIST"
echo "Auto-start installed. Clipboard Manager will launch at every login."
echo "To remove: launchctl unload $PLIST && rm $PLIST"
