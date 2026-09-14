# 🚀 ASUS TUF Control Center - Feature Roadmap & Proposals

This document outlines feature proposals for **ASUS TUF Control Center**.

---

## 📋 Proposed Feature List

### [ ] 1. 📌 System Tray / Top Panel Quick Indicator
- **Goal**: Add a top-bar tray icon to Ubuntu's panel (`QSystemTrayIcon` / AppIndicator).
- **Functionality**:
  - 1-click quick menu to switch Operating Modes (**Silent**, **Performance**, **Turbo**, **Manual**).
  - Quick GPU Mode switcher (**Integrated**, **Hybrid**, **MUX**).
  - Quick Battery Limit selector (**60%**, **80%**, **100%**).
  - Hide main window to tray on close/minimize.

---

### [x] 2. 🔌 Automatic AC / Battery Power Switcher (COMPLETED v2.1)
- **Goal**: Automatically switch laptop profiles when plugging or unplugging the AC charger.
- **Functionality**:
  - **Unplugged (On Battery)**: Auto-applies **Silent Mode** + **60Hz Screen** + **40 FPS Cap** to maximize battery life.
  - **Plugged In (AC Charger)**: Auto-applies **Turbo Mode** + **144Hz Screen** + **Unlimited FPS**.

---

### [ ] 3. 🎯 Per-Game Auto-Profile Switching (Game Profiles)
- **Goal**: Detect active running games and automatically tune performance.
- **Functionality**:
  - **Story Games (*RDR2, Cyberpunk, Witcher 3*)**: Auto-activates **Silent Mode (Whisper 40 FPS, <60°C)**.
  - **Esports Games (*CS2, Valorant, Apex*)**: Auto-activates **Turbo Mode (Max Wattage & Max FPS)**.
  - Custom game list configuration in GUI.

### [x] 4. 🖥️ Display Refresh Rate Switcher (60Hz vs 144Hz) (COMPLETED v2.1)
- **Goal**: Add screen refresh rate controls.
- **Functionality**:
  - Automatically switches between **60Hz** (Battery Saver) and **144Hz** (Smooth Gaming) based on AC power status.

---

### [x] 5. 🌀 Custom Fan Curve Graph Editor (COMPLETED v2.6)
- **Goal**: Visual fan curve customizer for ASUS embedded controller (`asusctl fan-curve` / `asusd`).
- **Functionality**:
  - 8-point interactive temperature vs PWM % curve vector graph canvas (`FanCurveGraphWidget`).
  - Presets: *Stealth Quiet*, *Balanced Ramp*, *Aggressive Max Cooling*, *Reset Defaults*.
  - Dual CPU & GPU fan control with `asusd` `/etc/asusd/fan_curves.ron` integration.


---

### [ ] 6. 🔔 Desktop Toast Notifications
- **Goal**: Native Ubuntu notification popups (`notify-send` / `notify2`).
- **Functionality**:
  - Toast alert when changing operating modes or pressing Armoury key.
  - Toast alert when battery reaches set charge threshold.

---

### [x] 8. 🖼️ GameVisual Display Color Profiles (COMPLETED v2.5)
- **Goal**: Armoury Crate GameVisual screen color, contrast, and blue light profiles.
- **Functionality**:
  - 1-click presets: **Default**, **Racing**, **Scenery**, **RTS/RPG**, **FPS (Dark Boost)**, **Cinema**, **Eye Care (Blue Light Filter)**, **Vivid Color**.
  - Dynamic `xrandr` gamma and color temperature tuning for ASUS display panels.

