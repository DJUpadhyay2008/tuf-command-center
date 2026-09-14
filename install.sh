#!/bin/bash
set -e

# Detect script location and use dynamic paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

echo "=== ASUS TUF Control Center Installation ==="
echo "Installation directory: $APP_DIR"
echo ""

# Check for required system dependencies
echo "Checking system dependencies..."
MISSING_DEPS=()

if ! command -v asusctl &> /dev/null; then
    MISSING_DEPS+=("asusctl")
fi

if ! command -v supergfxctl &> /dev/null; then
    MISSING_DEPS+=("supergfxctl")
fi

if ! command -v python3 &> /dev/null; then
    MISSING_DEPS+=("python3")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "ERROR: Missing required dependencies: ${MISSING_DEPS[*]}"
    echo ""
    echo "Please install them first:"
    echo "  Arch/Manjaro: sudo pacman -S asusctl supergfxctl python"
    echo "  Ubuntu/Debian: sudo apt install asusctl supergfxctl python3 python3-venv"
    exit 1
fi

echo "✓ All system dependencies found"
echo ""

# Create directories
mkdir -p "$BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR"

# Create Python virtual environment
echo "Setting up Python virtual environment..."
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
"$APP_DIR/venv/bin/pip" install --upgrade pip > /dev/null 2>&1
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
echo "✓ Python dependencies installed"
echo ""

echo "Creating launcher wrapper script..."
cat << EOF > "$BIN_DIR/asus-tuf-gui"
#!/bin/bash
export QT_QPA_PLATFORM=xcb
"$APP_DIR/venv/bin/python3" "$APP_DIR/main.py" "\$@"
EOF

chmod +x "$BIN_DIR/asus-tuf-gui"
echo "✓ Launcher created at $BIN_DIR/asus-tuf-gui"

echo "Creating application icon..."
cat << 'EOF' > "$ICON_DIR/asus-tuf-control.svg"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#0A0B10"/>
  <polygon points="50,15 85,35 85,65 50,85 15,65 15,35" fill="none" stroke="#00FF66" stroke-width="6"/>
  <polygon points="50,25 75,40 75,60 50,75 25,60 25,40" fill="#0F111A" stroke="#F59E0B" stroke-width="3"/>
  <text x="50" y="58" font-family="monospace" font-weight="bold" font-size="20" fill="#00FF66" text-anchor="middle">TUF</text>
</svg>
EOF
echo "✓ Icon created"

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
echo "✓ Desktop entry created"

echo "Configuring dedicated physical Armoury Crate keybindings..."
KB_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ name 'ASUS Control Center Launch1'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom0/ binding 'XF86Launch1'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ name 'ASUS Control Center Launch3'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom1/ binding 'XF86Launch3'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ name 'ASUS Control Center Tools'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom2/ binding 'XF86Tools'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ name 'ASUS Control Center VendorHome'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ command "$BIN_DIR/asus-tuf-gui"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$KB_PATH/custom3/ binding 'XF86VendorHome'

echo "✓ Hardware key bindings configured"

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "Launch options:"
echo "  1. Press the physical Armoury Crate button on your keyboard"
echo "  2. Run: asus-tuf-gui"
echo "  3. Search 'ASUS TUF Control Center' in your application menu"
echo ""
