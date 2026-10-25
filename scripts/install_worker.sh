#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"
PLIST="$HOME/Library/LaunchAgents/com.shopping-agent.worker.plist"
LABEL="com.shopping-agent.worker"

if [[ ! -x "$PYTHON" ]]; then
    echo "Python not found at $PYTHON"
    echo "Update PYTHON in this script to your environment's interpreter."
    exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$HOME/Library/Logs/shopping-agent"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>

    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>-m</string>
        <string>src.worker</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$ROOT</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

plutil -lint "$PLIST"

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "Worker installed and started."
echo "Logs: $HOME/Library/Logs/shopping-agent/worker.log"