# ASUS TUF Control Center

A modern PyQt6-based GUI for managing ASUS TUF gaming laptop hardware on Linux. Provides centralized control for power management, thermal settings, RGB lighting, and GPU switching—a Linux alternative to Windows' Armoury Crate.

## Features

- **Operating Modes**: Silent, Performance, Turbo, and Manual modes with preset power profiles
- **WhisperMode 2.0**: FPS limiting for quieter gaming (40/60/90/120 FPS caps)
- **Manual Tuning**: Granular control of CPU power limits (PL1/PL2) and GPU Dynamic Boost
- **RGB Control**: Keyboard brightness and Aura lighting effects
- **GPU Switching**: Integrated, Hybrid (Optimus), and Dedicated (MUX) modes
- **Battery Health**: Charge limit management for battery longevity
- **Live Telemetry**: Real-time CPU/GPU temps, power draw, and system usage

## Prerequisites

### System Packages
```bash
# Install ASUS control utilities
sudo pacman -S asusctl supergfxctl  # Arch/Manjaro
# OR
sudo apt install asusctl supergfxctl  # Ubuntu/Debian

# Optional: For FPS limiting
sudo pacman -S mangohud  # Arch/Manjaro
sudo apt install mangohud  # Ubuntu/Debian
```

### Permissions
Ensure your user is in the required groups:
```bash
sudo usermod -aG input,video $USER
# Log out and back in for changes to take effect
```

## Installation

1. Clone or download this repository:
```bash
cd ~/
git clone <your-repo-url> Asusctl-gui
cd Asusctl-gui
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

This will:
- Create a Python virtual environment
- Install Python dependencies
- Set up desktop integration
- Configure hardware key bindings for the Armoury Crate button

3. Launch the application:
- Press your laptop's Armoury Crate hardware button (usually top-left corner)
- Or run: `asus-tuf-gui` from terminal
- Or launch from application menu: "ASUS TUF Control Center"

## Usage

### Operating Modes
- **Silent Mode**: 40 FPS cap, low power (35W PL1), quiet fans, <60°C temps
- **Performance Mode**: 60 FPS cap, balanced power (65W PL1), moderate fans
- **Turbo Mode**: Unlimited FPS, max power (90W PL1, 135W PL2), full performance
- **Manual Mode**: Custom power limits and FPS caps

### FPS Limiting (WhisperMode 2.0)
For **Proton/Windows games** (RDR2, Cyberpunk, Witcher 3): Works automatically via DXVK.

For **native Linux games** (CS2, native Vulkan/OpenGL): Add to Steam launch options:
```
mangohud %command%
```

### GPU Switching
- **Integrated**: iGPU only (best battery life)
- **Hybrid**: NVIDIA Optimus (balanced)
- **Dedicated**: Direct MUX switch (best performance, requires reboot)

## Troubleshooting

### Application won't launch
```bash
# Check if dependencies are installed
which asusctl supergfxctl

# Check Python environment
source ~/Asusctl-gui/venv/bin/activate
python -c "import PyQt6, psutil"
```

### Commands failing
```bash
# Verify user permissions
groups | grep -E 'input|video'

# Check service status
systemctl status asusd supergfxd
```

### FPS limiting not working
Ensure DXVK config is being read:
```bash
cat ~/.config/dxvk.conf
cat ~/.config/MangoHud/MangoHud.conf
```

## Uninstallation

```bash
rm -f ~/.local/bin/asus-tuf-gui
rm -f ~/.local/share/applications/asus-tuf-control.desktop
rm -f ~/.local/share/icons/asus-tuf-control.svg
rm -rf ~/Asusctl-gui
```

Reset GNOME keybindings:
```bash
gsettings reset org.gnome.settings-daemon.plugins.media-keys custom-keybindings
```

## Development

### Running from source
```bash
cd ~/Asusctl-gui
source venv/bin/activate
python main.py
```

### Adding features
- Backend logic: Edit `backend.py`
- UI components: Edit `ui_main.py`
- Entry point: `main.py`

## Credits

Built on top of:
- [asusctl](https://gitlab.com/asus-linux/asusctl) - ASUS laptop control
- [supergfxctl](https://gitlab.com/asus-linux/supergfxctl) - GPU switching
- PyQt6 - GUI framework

## License

MIT License - feel free to modify and distribute.
