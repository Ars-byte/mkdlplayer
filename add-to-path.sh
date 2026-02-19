#!/bin/bash

APP_PATH=$(pwd)
SCRIPT_NAME="mkdlplayer.py"
ICON_NAME="assets/logo.png"
DESKTOP_FILE="mkdlplayer.desktop"

echo "🔧 Setting up mkdlplayer at: $APP_PATH"

cat <<EOF > $DESKTOP_FILE
[Desktop Entry]
Type=Application
Name=MKDL Player
Comment=Lightweight Music Player with Discord RPC
Exec=python3 $APP_PATH/$SCRIPT_NAME
Path=$APP_PATH
Icon=$APP_PATH/$ICON_NAME
Terminal=false
Categories=AudioVideo;Player;Audio;
EOF

chmod +x "$APP_PATH/$SCRIPT_NAME"
chmod +x "$DESKTOP_FILE"

mkdir -p ~/.local/share/applications
cp "$DESKTOP_FILE" ~/.local/share/applications/

echo "✅ Installation complete!"
echo "🚀 You can now find 'MKDL Player' in your application menu."
