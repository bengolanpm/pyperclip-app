#!/bin/bash
# Kill any existing instance
pkill -f "clipboard_manager.py" 2>/dev/null

# Launch in background, detached from terminal
nohup /usr/bin/python3 "$(dirname "$0")/clipboard_manager.py" > /tmp/clipboard_manager.log 2>&1 &
echo "Clipboard Manager started (PID $!)"
