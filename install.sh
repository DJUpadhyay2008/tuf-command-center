#!/bin/bash
set -e

APP_DIR="/home/dutt/Asusctl-gui"
BIN_DIR="/home/dutt/.local/bin"
DESKTOP_DIR="/home/dutt/.local/share/applications"
ICON_DIR="/home/dutt/.local/share/icons"

mkdir -p "$BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR"

echo "Creating launcher wrapper script..."
cat << 'EOF' > "$BIN_DIR/asus-tuf-gui"
#!/bin/bash
export QT_QPA_PLATFORM=xcb
/home/dutt/Asusctl-gui/venv/bin/python3 /home/dutt/Asusctl-gui/main.py "$@"
EOF

chmod +x "$BIN_DIR/asus-tuf-gui"

echo "Creating application icon..."
cat << 'EOF' > "$ICON_DIR/asus-tuf-control.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#0A0B10"/>
  <polygon points="50,15 85,35 85,65 50,85 15,65 15,35" fill="none" stroke="#00FF66" stroke-width="6"/>
  <polygon points="50,25 75,40 75,60 50,75 25,60 25,40" fill="#0F111A" stroke="#F59E0B" stroke-width="3"/>
  <text x="50" y="58" font-family="monospace" font-weight="bold" font-size="20" fill="#00FF66" text-anchor="middle">TUF</text>
</svg>
EOF

echo "Creating desktop entry..."
cat << EOF > "$DESKTOP_DIR/asus-tuf-control.desktop"
[Desktop Entry]
Name=ASUS TUF Control Center
Comment=Gaming Laptop Performance, Thermal & RGB Control GUI
Exec=$BIN_DIR/asus-tuf-gui
Icon=$ICON_DIR/asus-tuf-control.svg
Terminal=false
Type=Application
Categories=System;Settings;HardwareSettings;
Keywords=asus;asusctl;armoury;supergfxctl;gpu;fan;tuf;rgb;
EOF

chmod +x "$DESKTOP_DIR/asus-tuf-control.desktop"

echo "Configuring dedicated physical Armoury Crate keybindings..."
KB_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ name 'ASUS Control Center Launch1'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ binding 'XF86Launch1'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ name 'ASUS Control Center Launch2'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ binding 'XF86Launch2'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ name 'ASUS Control Center Launch3'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ binding 'XF86Launch3'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ name 'ASUS Control Center Tools'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ binding 'XF86Tools'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom4/ name 'ASUS Control Center VendorHome'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom4/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom4/ binding 'XF86VendorHome'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom5/ name 'ASUS Control Center Search'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom5/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom5/ binding 'XF86Search'

gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['$KB_PATH/custom0/', '$KB_PATH/custom1/', '$KB_PATH/custom2/', '$KB_PATH/custom3/', '$KB_PATH/custom4/', '$KB_PATH/custom5/']"

echo "Installation complete!"
echo "You can now press the physical dedicated Armoury Crate key (top-left 4th key)!"
