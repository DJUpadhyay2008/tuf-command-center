#!/bin/bash
set -e

echo "=== ASUS TUF Control Center Uninstallation ==="
echo ""

BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"
KB_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

# Remove launcher script
if [ -f "$BIN_DIR/asus-tuf-gui" ]; then
    rm -f "$BIN_DIR/asus-tuf-gui"
    echo "✓ Removed launcher script"
fi

# Remove desktop entry
if [ -f "$DESKTOP_DIR/asus-tuf-control.desktop" ]; then
    rm -f "$DESKTOP_DIR/asus-tuf-control.desktop"
    echo "✓ Removed desktop entry"
fi

# Remove icon
if [ -f "$ICON_DIR/asus-tuf-control.svg" ]; then
    rm -f "$ICON_DIR/asus-tuf-control.svg"
    echo "✓ Removed application icon"
fi

# Reset GNOME keybindings
if command -v gsettings &> /dev/null; then
    gsettings reset org.gnome.settings-daemon.plugins.media-keys custom-keybindings
    echo "✓ Reset hardware key bindings"
fi

# Remove log file
if [ -f "$HOME/.config/asus-tuf-gui.log" ]; then
    rm -f "$HOME/.config/asus-tuf-gui.log"
    echo "✓ Removed log file"
fi

echo ""
echo "=== Uninstallation Complete! ==="
echo ""
echo "Note: Application files in the installation directory were NOT removed."
echo "To completely remove the application, delete the installation folder manually:"
echo "  rm -rf ~/Asusctl-gui"
echo ""
