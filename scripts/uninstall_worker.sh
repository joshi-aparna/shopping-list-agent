#!/bin/bash
set -euo pipefail

PLIST="$HOME/Library/LaunchAgents/com.shopping-list-agent.worker.plist"

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
rm -f "$PLIST"

echo "Worker stopped and LaunchAgent removed."