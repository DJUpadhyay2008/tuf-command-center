# 🛡️ ASUS TUF Control Center (Linux)

> A modern, dark Cyberpunk Armoury Crate replacement GUI for ASUS TUF & ROG Gaming Laptops on Linux (Ubuntu/Debian/Arch/Fedora).

Built with Python 3, PyQt6, `asusctl`, `supergfxctl`, and `nvidia-smi`.

---

## ⚡ Features

- **🎮 Armoury Crate Operating Modes**:
  - 🤫 **Silent Mode (WhisperMode 2.0)**: Lowers CPU PL1 (35W) & GPU Dynamic Boost (5W), automatically caps game FPS to **40 FPS** via MangoHud & DXVK to keep CPU & GPU **under 60°C** with near-silent fans.
  - ⚖️ **Performance Mode**: Balances power, heat, and fan sound with standard wattage and a 60 FPS cap.
  - 🔥 **Turbo Mode**: Pushes hardware to maximum power limits (CPU PL1 90W, PL2 135W, Dynamic Boost 15W) with unlimited FPS.
  - ⚙️ **Manual Mode**: Unlocks custom sliders to fine-tune CPU PL1/PL2 & GPU Dynamic Boost power limits.

- **⚡ GPU Graphics Mode Switcher**:
  - Switch between **Integrated (iGPU)**, **Hybrid (Optimus)**, and **Dedicated (MUX)** graphics via `supergfxctl`.

- **🌈 RGB Aura Lighting & Screen Overdrive**:
  - Keyboard backlight brightness levels (Off, Low, Medium, High).
  - Aura RGB lighting modes (Static, Breathe, Rainbow Cycle, Wave, Pulse) & custom RGB color picker.
  - Display Panel Overdrive toggle (3ms Low Latency Mode).

- **🔋 Battery Health Care**:
  - Battery charge threshold limit slider (20% to 100%) and quick eco presets (60%, 80%, 100%).

- **⌨️ Physical Armoury Crate Hardware Key Support**:
  - Dedicated hardware key integration to open the GUI when pressing the physical Armoury Crate button.

---

## 🚀 Installation & Usage

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/asus-tuf-control-center.git
cd asus-tuf-control-center
chmod +x install.sh
./install.sh
```

### 2. Launch
- **Physical Key**: Press the dedicated **Armoury Crate button** on your keyboard.
- **Application Menu**: Open **ASUS TUF Control Center** from your app launcher.
- **Terminal**: Run `asus-tuf-gui`

---

## 📜 License
MIT License. Free and open source for the ASUS ROG / TUF Linux Community.
