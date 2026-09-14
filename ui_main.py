import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QSlider, QComboBox, QGroupBox, QProgressBar, QFrame,
    QColorDialog, QMessageBox, QGridLayout, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont
from backend import AsusBackend

STYLE_SHEET = """
QMainWindow {
    background-color: #0A0B10;
}
QWidget {
    color: #34D399;
    font-family: 'Ubuntu Mono', 'Cascadia Code', 'Fira Code', 'Monaco', 'Courier New', monospace;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #10B981;
    background-color: #0D0E15;
    border-radius: 6px;
    top: -1px;
}
QTabBar::tab {
    background: #12141D;
    color: #6B7280;
    padding: 8px 18px;
    margin-right: 4px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: bold;
    border: 1px solid #1F2430;
}
QTabBar::tab:selected {
    background: #181B28;
    color: #00FF66;
    border-bottom: 2px solid #00FF66;
    border-top: 1px solid #00FF66;
}
QTabBar::tab:hover {
    background: #1A1D2B;
    color: #34D399;
}
QGroupBox {
    border: 1px solid #1F2430;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 15px;
    background-color: #0F111A;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    color: #00FF66;
    font-size: 13px;
}
QPushButton {
    background-color: #141724;
    border: 1px solid #1F2430;
    color: #E2E8F0;
    padding: 10px 16px;
    border-radius: 4px;
    font-weight: bold;
    font-family: 'Ubuntu Mono', 'Courier New', monospace;
}
QPushButton:hover {
    background-color: #1C2032;
    border-color: #00FF66;
    color: #00FF66;
}
QPushButton:pressed {
    background-color: #00FF66;
    color: #0A0B10;
}
QPushButton#modeBtnSelected {
    background-color: #132A20;
    color: #00FF66;
    border: 2px solid #00FF66;
    font-weight: bold;
}
QSlider::groove:horizontal {
    border: 1px solid #1F2430;
    height: 8px;
    background: #0A0B10;
    border-radius: 4px;
}
QSlider::sub-page:horizontal {
    background: #00FF66;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #0A0B10;
    border: 2px solid #00FF66;
    width: 18px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
}
QProgressBar {
    border: 1px solid #1F2430;
    border-radius: 4px;
    text-align: center;
    background-color: #0A0B10;
    color: #00FF66;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #00FF66;
    border-radius: 3px;
}
QComboBox {
    background-color: #141724;
    border: 1px solid #1F2430;
    border-radius: 4px;
    padding: 6px 12px;
    color: #00FF66;
    font-weight: bold;
}
QComboBox QAbstractItemView {
    background-color: #0F111A;
    selection-background-color: #132A20;
    selection-color: #00FF66;
}
QCheckBox {
    color: #00FF66;
    font-weight: bold;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #1F2430;
    border-radius: 3px;
    background: #141724;
}
QCheckBox::indicator:checked {
    background: #00FF66;
    border: 1px solid #00FF66;
}
"""

class AsusGuiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backend = AsusBackend()
        self.active_mode = "Performance"
        self.last_power_plugged = self.backend.get_power_plugged_status()
        self.setWindowTitle("ASUS TUF Control Center [TERMINAL MODE]")
        self.setMinimumSize(900, 720)
        self.setStyleSheet(STYLE_SHEET)

        # Main widget & layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header Title
        header_layout = QHBoxLayout()
        title_label = QLabel(">_ ASUS TUF CONTROL CENTER // SYSTEM_TERMINAL v2.0")
        title_font = QFont("Ubuntu Mono", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #00FF66; font-weight: bold;")
        
        sub_title = QLabel("[SYS::ONLINE] [HOST::TUF-F15]")
        sub_title.setStyleSheet("color: #F59E0B; font-size: 12px; font-weight: bold;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(sub_title)
        main_layout.addLayout(header_layout)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab_mode = QWidget()
        self.tab_manual = QWidget()
        self.tab_lighting = QWidget()
        self.tab_battery = QWidget()

        self.tabs.addTab(self.tab_mode, "[1] OPERATING_MODE")
        self.tabs.addTab(self.tab_manual, "[2] MANUAL_TUNING")
        self.tabs.addTab(self.tab_lighting, "[3] RGB_DISPLAY")
        self.tabs.addTab(self.tab_battery, "[4] BATTERY_HEALTH")

        self._init_tab_mode()
        self._init_tab_manual()
        self._init_tab_lighting()
        self._init_tab_battery()

        # Terminal Prompt Status Bar
        self.status_bar = QLabel("user@tuf-f15:~$ System Ready.")
        self.status_bar.setStyleSheet("color: #00FF66; font-size: 12px; padding: 6px 12px; background-color: #0F111A; border: 1px solid #1F2430; border-radius: 4px;")
        main_layout.addWidget(self.status_bar)

        # Timer for Telemetry
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self._update_telemetry)
        self.telemetry_timer.start(2000)

        # Initial load
        self.refresh_all_data()

    def show_status(self, message, is_error=False):
        color = "#EF4444" if is_error else "#00FF66"
        prefix = "user@tuf-f15:~$ [ERR] " if is_error else "user@tuf-f15:~$ [OK] "
        self.status_bar.setStyleSheet(f"color: {color}; font-size: 12px; padding: 6px 12px; background-color: #0F111A; border: 1px solid {color}; border-radius: 4px;")
        self.status_bar.setText(prefix + message)

    # ---------------- TAB 1: OPERATING MODE ----------------
    def _init_tab_mode(self):
        layout = QVBoxLayout(self.tab_mode)
        layout.setSpacing(14)

        # Live Monitor Header Card
        tele_group = QGroupBox("[LIVE_SYSTEM_TELEMETRY]")
        tele_layout = QGridLayout(tele_group)
        tele_layout.setSpacing(10)

        tele_layout.addWidget(QLabel("CPU Usage:"), 0, 0)
        self.bar_cpu = QProgressBar()
        self.bar_cpu.setRange(0, 100)
        tele_layout.addWidget(self.bar_cpu, 0, 1)
        self.lbl_cpu_temp = QLabel("CPU Temp: --")
        self.lbl_cpu_temp.setStyleSheet("font-weight: bold; color: #00FF66;")
        tele_layout.addWidget(self.lbl_cpu_temp, 0, 2)

        tele_layout.addWidget(QLabel("RAM Usage:"), 1, 0)
        self.bar_ram = QProgressBar()
        self.bar_ram.setRange(0, 100)
        tele_layout.addWidget(self.bar_ram, 1, 1)

        tele_layout.addWidget(QLabel("GPU Status:"), 2, 0)
        self.lbl_gpu_temp = QLabel("GPU Temp: -- | Power: --")
        self.lbl_gpu_temp.setStyleSheet("font-weight: bold; color: #F59E0B;")
        tele_layout.addWidget(self.lbl_gpu_temp, 2, 1, 1, 2)

        layout.addWidget(tele_group)

        # Operating Mode Selector Cards
        mode_group = QGroupBox("[ARMOURY_OPERATING_MODES]")
        mode_grid = QGridLayout(mode_group)
        mode_grid.setSpacing(10)

        # 1. Silent Card
        self.btn_mode_silent = QPushButton(">_ SILENT_MODE (Whisper 40 FPS)")
        self.btn_mode_silent.setStyleSheet("font-size: 12px; text-align: left; padding-left: 12px;")
        self.btn_mode_silent.clicked.connect(lambda: self._select_operating_mode("Silent"))
        lbl_desc_silent = QLabel("Triggers WhisperMode 2.0 (40 FPS Cap + 5W Dynamic Boost). Keeps CPU/GPU under 60°C with near-silent fans.")
        lbl_desc_silent.setWordWrap(True)
        lbl_desc_silent.setStyleSheet("color: #6B7280; font-size: 11px;")
        mode_grid.addWidget(self.btn_mode_silent, 0, 0)
        mode_grid.addWidget(lbl_desc_silent, 1, 0)

        # 2. Performance Card
        self.btn_mode_perf = QPushButton(">_ PERFORMANCE_MODE (60 FPS Cap)")
        self.btn_mode_perf.setStyleSheet("font-size: 12px; text-align: left; padding-left: 12px;")
        self.btn_mode_perf.clicked.connect(lambda: self._select_operating_mode("Performance"))
        lbl_desc_perf = QLabel("Balances power, heat, and fan sound. Gives hardware 60 FPS cap & standard wattage for smooth gaming.")
        lbl_desc_perf.setWordWrap(True)
        lbl_desc_perf.setStyleSheet("color: #6B7280; font-size: 11px;")
        mode_grid.addWidget(self.btn_mode_perf, 0, 1)
        mode_grid.addWidget(lbl_desc_perf, 1, 1)

        # 3. Turbo Card
        self.btn_mode_turbo = QPushButton(">_ TURBO_MODE (Max FPS)")
        self.btn_mode_turbo.setStyleSheet("font-size: 12px; text-align: left; padding-left: 12px;")
        self.btn_mode_turbo.clicked.connect(lambda: self._select_operating_mode("Turbo"))
        lbl_desc_turbo = QLabel("Pushes hardware to max power limits (PL1 90W, PL2 135W, 15W Boost) & Unlimited FPS for competitive gaming.")
        lbl_desc_turbo.setWordWrap(True)
        lbl_desc_turbo.setStyleSheet("color: #6B7280; font-size: 11px;")
        mode_grid.addWidget(self.btn_mode_turbo, 2, 0)
        mode_grid.addWidget(lbl_desc_turbo, 3, 0)

        # 4. Manual Card
        self.btn_mode_manual = QPushButton(">_ MANUAL_MODE")
        self.btn_mode_manual.setStyleSheet("font-size: 12px; text-align: left; padding-left: 12px;")
        self.btn_mode_manual.clicked.connect(lambda: self._select_operating_mode("Manual"))
        lbl_desc_manual = QLabel("Lets you create custom power targets (CPU PL1/PL2, Dynamic Boost) and custom FPS limits.")
        lbl_desc_manual.setWordWrap(True)
        lbl_desc_manual.setStyleSheet("color: #6B7280; font-size: 11px;")
        mode_grid.addWidget(self.btn_mode_manual, 2, 1)
        mode_grid.addWidget(lbl_desc_manual, 3, 1)

        layout.addWidget(mode_group)

        # Automatic AC / Battery Power Switcher Card
        auto_group = QGroupBox("[AUTOMATIC_POWER_SWITCHER]")
        auto_layout = QVBoxLayout(auto_group)
        auto_layout.setSpacing(6)

        auto_header = QHBoxLayout()
        self.chk_auto_switcher = QCheckBox("Enable Auto AC / Battery Power & Refresh Rate Switcher")
        self.chk_auto_switcher.setChecked(True)
        self.chk_auto_switcher.setStyleSheet("font-weight: bold; color: #00FF66;")
        auto_header.addWidget(self.chk_auto_switcher)

        self.lbl_auto_status = QLabel("[AC: Turbo + 144Hz] <-> [BATTERY: Silent + 60Hz]")
        self.lbl_auto_status.setStyleSheet("color: #F59E0B; font-size: 11px; font-weight: bold;")
        auto_header.addStretch()
        auto_header.addWidget(self.lbl_auto_status)
        auto_layout.addLayout(auto_header)

        lbl_auto_desc = QLabel("Auto-applies Silent Mode (Whisper 40 FPS) + 60Hz refresh rate on battery, and Turbo Mode + 144Hz on AC charger.")
        lbl_auto_desc.setWordWrap(True)
        lbl_auto_desc.setStyleSheet("color: #6B7280; font-size: 11px;")
        auto_layout.addWidget(lbl_auto_desc)

        layout.addWidget(auto_group)

        # WhisperMode 2.0 / FPS Limiter Bar
        fps_group = QGroupBox("[WHISPERMODE_2.0_FPS_LIMITER]")
        fps_layout = QHBoxLayout(fps_group)
        fps_layout.addWidget(QLabel("Target Game FPS Cap:"))

        self.combo_fps = QComboBox()
        self.combo_fps.addItems([
            "40 FPS (Whisper Quiet ~60°C - RDR2 / Story)",
            "60 FPS (Balanced Quiet Gaming)",
            "90 FPS (High Refresh Quiet)",
            "120 FPS",
            "0 (Unlimited FPS)"
        ])
        fps_layout.addWidget(self.combo_fps)

        btn_apply_fps = QPushButton("Apply FPS Cap")
        btn_apply_fps.clicked.connect(self._apply_manual_fps_cap)
        fps_layout.addWidget(btn_apply_fps)

        btn_help_fps = QPushButton("? Setup Info")
        btn_help_fps.clicked.connect(self._show_fps_help_dialog)
        fps_layout.addWidget(btn_help_fps)

        layout.addWidget(fps_group)

        # GPU Graphics Switcher
        gpu_group = QGroupBox("[GPU_GRAPHICS_SWITCHER]")
        gpu_layout = QVBoxLayout(gpu_group)

        gpu_btns_layout = QHBoxLayout()
        self.btn_gpu_igpu = QPushButton(">_ Integrated (iGPU)")
        self.btn_gpu_hybrid = QPushButton(">_ Hybrid (Optimus)")
        self.btn_gpu_dgpu = QPushButton(">_ Dedicated (MUX)")

        self.btn_gpu_igpu.clicked.connect(lambda: self._set_gpu_mode("Integrated"))
        self.btn_gpu_hybrid.clicked.connect(lambda: self._set_gpu_mode("Hybrid"))
        self.btn_gpu_dgpu.clicked.connect(lambda: self._set_gpu_mode("AsusMuxDgpu"))

        gpu_btns_layout.addWidget(self.btn_gpu_igpu)
        gpu_btns_layout.addWidget(self.btn_gpu_hybrid)
        gpu_btns_layout.addWidget(self.btn_gpu_dgpu)
        gpu_layout.addLayout(gpu_btns_layout)

        self.lbl_gpu_pending = QLabel("Pending Action: None")
        self.lbl_gpu_pending.setStyleSheet("color: #6B7280; font-size: 11px; font-style: italic;")
        gpu_layout.addWidget(self.lbl_gpu_pending)

        layout.addWidget(gpu_group)
        layout.addStretch()

    def _show_fps_help_dialog(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Game FPS Limiter Setup Info")
        msg.setText(
            "<b>How Game FPS Limiting Works:</b><br><br>"
            "1. <b>Proton / Windows Games (RDR2, Cyberpunk, Witcher 3):</b><br>"
            "   The 40 FPS / 60 FPS cap applies <i>automatically</i> via <b>DXVK</b> configuration (~/.config/dxvk.conf)!<br><br>"
            "2. <b>Native Vulkan/OpenGL Games (CS2):</b><br>"
            "   In Steam Game Properties -> Launch Options, add:<br>"
            "   <code>mangohud %command%</code><br><br>"
            "This forces the game to cap at 40 FPS in Silent Mode, keeping your CPU & GPU under 60°C with quiet fans!"
        )
        msg.exec()

    def _select_operating_mode(self, mode_name):
        self.active_mode = mode_name
        ok, msg = self.backend.apply_operating_mode(mode_name)
        if ok:
            self.show_status(f"Operating Mode set to {mode_name}: {msg}")
            self._update_mode_card_styles(mode_name)
            self._update_fps_combo_selection()
            if mode_name == "Manual":
                self.tabs.setCurrentIndex(1)
            else:
                self.refresh_manual_sliders_from_armoury()
        else:
            self.show_status(f"Failed to set mode: {msg}", is_error=True)

    def _apply_manual_fps_cap(self):
        val_str = self.combo_fps.currentText()
        if "40 FPS" in val_str:
            val = 40
        elif "60 FPS" in val_str:
            val = 60
        elif "90 FPS" in val_str:
            val = 90
        elif "120 FPS" in val_str:
            val = 120
        else:
            val = 0

        ok, msg = self.backend.set_fps_limit(val)
        if ok:
            self.show_status(f"Game FPS Cap set to {val if val > 0 else 'Unlimited'} (MangoHud & DXVK updated)")
        else:
            self.show_status(f"Failed to set FPS cap: {msg}", is_error=True)

    def _update_fps_combo_selection(self):
        limit = self.backend.get_fps_limit()
        if limit == 40:
            self.combo_fps.setCurrentIndex(0)
        elif limit == 60:
            self.combo_fps.setCurrentIndex(1)
        elif limit == 90:
            self.combo_fps.setCurrentIndex(2)
        elif limit == 120:
            self.combo_fps.setCurrentIndex(3)
        else:
            self.combo_fps.setCurrentIndex(4)

    def _update_mode_card_styles(self, active_mode):
        btns = {
            "Silent": self.btn_mode_silent,
            "Performance": self.btn_mode_perf,
            "Turbo": self.btn_mode_turbo,
            "Manual": self.btn_mode_manual
        }
        for mode, btn in btns.items():
            if mode.lower() == active_mode.lower():
                btn.setObjectName("modeBtnSelected")
                btn.setStyle(btn.style())
            else:
                btn.setObjectName("")
                btn.setStyle(btn.style())

    def _set_gpu_mode(self, mode):
        ok, out = self.backend.set_gpu_mode(mode)
        if ok:
            pending = self.backend.get_gpu_pending_action()
            msg = f"GPU Mode changed to {mode}."
            if pending and pending != "None":
                msg += f" ({pending})"
            self.show_status(msg)
            self._update_gpu_buttons(mode)
            self.lbl_gpu_pending.setText(f"Pending Action: {pending}")
        else:
            self.show_status(f"GPU mode error: {out}", is_error=True)

    def _update_gpu_buttons(self, active_mode):
        btns = {
            "Integrated": self.btn_gpu_igpu,
            "Hybrid": self.btn_gpu_hybrid,
            "AsusMuxDgpu": self.btn_gpu_dgpu
        }
        for mode_key, btn in btns.items():
            if mode_key.lower() == active_mode.lower():
                btn.setObjectName("modeBtnSelected")
                btn.setStyle(btn.style())
            else:
                btn.setObjectName("")
                btn.setStyle(btn.style())

    # ---------------- TAB 2: MANUAL TUNING ----------------
    def _init_tab_manual(self):
        layout = QVBoxLayout(self.tab_manual)
        layout.setSpacing(16)

        info_manual = QLabel(
            ">_ MANUAL_MODE_ACTIVE: Customize CPU PL1/PL2 & GPU Dynamic Boost wattage limits."
        )
        info_manual.setWordWrap(True)
        info_manual.setStyleSheet("color: #00FF66; font-size: 13px; font-weight: bold;")
        layout.addWidget(info_manual)

        # Dynamic Boost Slider
        gpu_power_group = QGroupBox("[NVIDIA_DYNAMIC_BOOST_POWER_TARGET]")
        gpu_power_layout = QGridLayout(gpu_power_group)
        gpu_power_layout.setSpacing(12)

        gpu_power_layout.addWidget(QLabel("NV Dynamic Boost Offset:"), 0, 0)
        self.slider_dyn_boost = QSlider(Qt.Orientation.Horizontal)
        self.slider_dyn_boost.setRange(5, 15)
        self.slider_dyn_boost.setValue(15)
        self.lbl_val_dyn_boost = QLabel("15 W")
        self.lbl_val_dyn_boost.setFixedWidth(45)
        self.lbl_val_dyn_boost.setStyleSheet("font-weight: bold; color: #00FF66;")
        self.slider_dyn_boost.valueChanged.connect(lambda v: self.lbl_val_dyn_boost.setText(f"{v} W"))
        btn_apply_boost = QPushButton("Apply Boost")
        btn_apply_boost.clicked.connect(self._apply_dyn_boost)

        gpu_power_layout.addWidget(self.slider_dyn_boost, 0, 1)
        gpu_power_layout.addWidget(self.lbl_val_dyn_boost, 0, 2)
        gpu_power_layout.addWidget(btn_apply_boost, 0, 3)

        layout.addWidget(gpu_power_group)

        # CPU PL1 & PL2 Sliders
        cpu_power_group = QGroupBox("[CPU_POWER_TARGETS_PL1_PL2]")
        cpu_layout = QGridLayout(cpu_power_group)
        cpu_layout.setSpacing(12)

        # CPU PL1
        cpu_layout.addWidget(QLabel("CPU PL1 Sustained Limit:"), 0, 0)
        self.slider_pl1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_pl1.setRange(28, 90)
        self.slider_pl1.setValue(90)
        self.lbl_val_pl1 = QLabel("90 W")
        self.lbl_val_pl1.setFixedWidth(45)
        self.lbl_val_pl1.setStyleSheet("font-weight: bold; color: #00FF66;")
        self.slider_pl1.valueChanged.connect(lambda v: self.lbl_val_pl1.setText(f"{v} W"))
        btn_apply_pl1 = QPushButton("Apply PL1")
        btn_apply_pl1.clicked.connect(self._apply_pl1)

        cpu_layout.addWidget(self.slider_pl1, 0, 1)
        cpu_layout.addWidget(self.lbl_val_pl1, 0, 2)
        cpu_layout.addWidget(btn_apply_pl1, 0, 3)

        # CPU PL2
        cpu_layout.addWidget(QLabel("CPU PL2 Short Burst Limit:"), 1, 0)
        self.slider_pl2 = QSlider(Qt.Orientation.Horizontal)
        self.slider_pl2.setRange(28, 135)
        self.slider_pl2.setValue(135)
        self.lbl_val_pl2 = QLabel("135 W")
        self.lbl_val_pl2.setFixedWidth(45)
        self.lbl_val_pl2.setStyleSheet("font-weight: bold; color: #00FF66;")
        self.slider_pl2.valueChanged.connect(lambda v: self.lbl_val_pl2.setText(f"{v} W"))
        btn_apply_pl2 = QPushButton("Apply PL2")
        btn_apply_pl2.clicked.connect(self._apply_pl2)

        cpu_layout.addWidget(self.slider_pl2, 1, 1)
        cpu_layout.addWidget(self.lbl_val_pl2, 1, 2)
        cpu_layout.addWidget(btn_apply_pl2, 1, 3)

        layout.addWidget(cpu_power_group)
        layout.addStretch()

    def _apply_dyn_boost(self):
        val = self.slider_dyn_boost.value()
        ok, out = self.backend.set_nv_dynamic_boost(val)
        if ok:
            self._select_operating_mode("Manual")
            self.show_status(f"Manual Mode: NV Dynamic Boost set to {val} W")
        else:
            self.show_status(f"Failed to set Dynamic Boost: {out}", is_error=True)

    def _apply_pl1(self):
        val = self.slider_pl1.value()
        ok, out = self.backend.set_cpu_pl1(val)
        if ok:
            self._select_operating_mode("Manual")
            self.show_status(f"Manual Mode: CPU PL1 limit set to {val} W")
        else:
            self.show_status(f"Failed to set CPU PL1: {out}", is_error=True)

    def _apply_pl2(self):
        val = self.slider_pl2.value()
        ok, out = self.backend.set_cpu_pl2(val)
        if ok:
            self._select_operating_mode("Manual")
            self.show_status(f"Manual Mode: CPU PL2 limit set to {val} W")
        else:
            self.show_status(f"Failed to set CPU PL2: {out}", is_error=True)

    # ---------------- TAB 3: RGB LIGHTING & SCREEN ----------------
    def _init_tab_lighting(self):
        layout = QVBoxLayout(self.tab_lighting)
        layout.setSpacing(16)

        # Keyboard Backlight Brightness
        bright_group = QGroupBox("[KEYBOARD_BRIGHTNESS]")
        bright_layout = QHBoxLayout(bright_group)

        self.btn_k_off = QPushButton(">_ Off")
        self.btn_k_low = QPushButton(">_ Low")
        self.btn_k_med = QPushButton(">_ Medium")
        self.btn_k_high = QPushButton(">_ High")

        self.btn_k_off.clicked.connect(lambda: self._set_kbd_bright("Off"))
        self.btn_k_low.clicked.connect(lambda: self._set_kbd_bright("Low"))
        self.btn_k_med.clicked.connect(lambda: self._set_kbd_bright("Med"))
        self.btn_k_high.clicked.connect(lambda: self._set_kbd_bright("High"))

        bright_layout.addWidget(self.btn_k_off)
        bright_layout.addWidget(self.btn_k_low)
        bright_layout.addWidget(self.btn_k_med)
        bright_layout.addWidget(self.btn_k_high)
        layout.addWidget(bright_group)

        # Aura RGB Lighting Modes
        aura_group = QGroupBox("[AURA_RGB_EFFECTS]")
        aura_layout = QVBoxLayout(aura_group)
        aura_layout.setSpacing(12)

        mode_select_layout = QHBoxLayout()
        mode_select_layout.addWidget(QLabel("Effect Mode:"))
        self.combo_aura_mode = QComboBox()
        self.combo_aura_mode.addItems(["Static", "Breathe", "RainbowCycle", "RainbowWave", "Pulse"])
        mode_select_layout.addWidget(self.combo_aura_mode)

        mode_select_layout.addWidget(QLabel("Speed:"))
        self.combo_aura_speed = QComboBox()
        self.combo_aura_speed.addItems(["low", "med", "high"])
        self.combo_aura_speed.setCurrentText("med")
        mode_select_layout.addWidget(self.combo_aura_speed)

        aura_layout.addLayout(mode_select_layout)

        # Color Selection Swatches
        color_layout = QHBoxLayout()
        self.current_color = "00FF66"
        self.btn_pick_color = QPushButton("Pick Color")
        self.btn_pick_color.setStyleSheet(f"background-color: #141724; color: #{self.current_color}; border: 1px solid #{self.current_color}; font-weight: bold;")
        self.btn_pick_color.clicked.connect(self._pick_color)

        color_layout.addWidget(self.btn_pick_color)

        # Quick Preset Swatches
        swatches = [
            ("Green", "00FF66"), ("Cyan", "00F0FF"), ("Amber", "F59E0B"),
            ("Red", "EF4444"), ("Purple", "A855F7"), ("White", "F8FAFC")
        ]
        for label, hex_c in swatches:
            btn_s = QPushButton(label)
            btn_s.setStyleSheet(f"background-color: #141724; color: #{hex_c}; border: 1px solid #{hex_c}; font-size: 11px;")
            btn_s.clicked.connect(lambda _, c=hex_c: self._set_color_hex(c))
            color_layout.addWidget(btn_s)

        aura_layout.addLayout(color_layout)

        btn_apply_aura = QPushButton("Apply Aura Lighting Effect")
        btn_apply_aura.setStyleSheet("background-color: #132A20; color: #00FF66; border: 1px solid #00FF66; font-size: 13px; font-weight: bold; padding: 10px;")
        btn_apply_aura.clicked.connect(self._apply_aura)
        aura_layout.addWidget(btn_apply_aura)

        layout.addWidget(aura_group)

        # Screen Panel Overdrive
        panel_group = QGroupBox("[DISPLAY_PANEL_OVERDRIVE]")
        panel_layout = QHBoxLayout(panel_group)

        self.btn_overdrive_on = QPushButton(">_ Overdrive ON (3ms Low Latency)")
        self.btn_overdrive_off = QPushButton(">_ Overdrive OFF (Normal)")

        self.btn_overdrive_on.clicked.connect(lambda: self._set_overdrive(True))
        self.btn_overdrive_off.clicked.connect(lambda: self._set_overdrive(False))

        panel_layout.addWidget(self.btn_overdrive_on)
        panel_layout.addWidget(self.btn_overdrive_off)
        layout.addWidget(panel_group)

        layout.addStretch()

    def _set_kbd_bright(self, level):
        ok, out = self.backend.set_kbd_brightness(level)
        if ok:
            self.show_status(f"Keyboard brightness set to {level}")
            self._update_kbd_buttons(level)
        else:
            self.show_status(f"Failed to set brightness: {out}", is_error=True)

    def _update_kbd_buttons(self, active_level):
        btns = {
            "Off": self.btn_k_off,
            "Low": self.btn_k_low,
            "Med": self.btn_k_med,
            "High": self.btn_k_high
        }
        for lvl, btn in btns.items():
            if lvl.lower() == active_level.lower():
                btn.setObjectName("modeBtnSelected")
                btn.setStyle(btn.style())
            else:
                btn.setObjectName("")
                btn.setStyle(btn.style())

    def _pick_color(self):
        col = QColorDialog.getColor(QColor(f"#{self.current_color}"), self, "Select Aura RGB Color")
        if col.isValid():
            self._set_color_hex(col.name().replace("#", "").upper())

    def _set_color_hex(self, hex_code):
        self.current_color = hex_code
        self.btn_pick_color.setStyleSheet(f"background-color: #141724; color: #{hex_code}; border: 1px solid #{hex_code}; font-weight: bold;")

    def _apply_aura(self):
        mode = self.combo_aura_mode.currentText()
        speed = self.combo_aura_speed.currentText()
        ok, out = self.backend.set_aura_mode(mode, self.current_color, speed)
        if ok:
            self.show_status(f"Aura Mode '{mode}' applied!")
        else:
            self.show_status(f"Aura Error: {out}", is_error=True)

    def _set_overdrive(self, enabled):
        ok, out = self.backend.set_panel_overdrive(enabled)
        if ok:
            self.show_status(f"Panel Overdrive {'ENABLED' if enabled else 'DISABLED'}")
        else:
            self.show_status(f"Panel Overdrive Error: {out}", is_error=True)

    # ---------------- TAB 4: BATTERY HEALTH ----------------
    def _init_tab_battery(self):
        layout = QVBoxLayout(self.tab_battery)
        layout.setSpacing(16)

        bat_group = QGroupBox("[BATTERY_CHARGE_LIMIT_THRESHOLD]")
        bat_layout = QVBoxLayout(bat_group)
        bat_layout.setSpacing(16)

        info_lbl = QLabel(
            "Setting a maximum charge limit protects your battery chemistry and significantly prolongs battery health when plugged in for long periods."
        )
        info_lbl.setWordWrap(True)
        info_lbl.setStyleSheet("color: #6B7280;")
        bat_layout.addWidget(info_lbl)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Charge Limit:"))
        self.slider_battery = QSlider(Qt.Orientation.Horizontal)
        self.slider_battery.setRange(20, 100)
        self.slider_battery.setValue(80)
        self.lbl_bat_limit_val = QLabel("80 %")
        self.lbl_bat_limit_val.setStyleSheet("font-weight: bold; color: #00FF66; font-size: 16px;")
        self.lbl_bat_limit_val.setFixedWidth(50)

        self.slider_battery.valueChanged.connect(lambda v: self.lbl_bat_limit_val.setText(f"{v} %"))

        slider_layout.addWidget(self.slider_battery)
        slider_layout.addWidget(self.lbl_bat_limit_val)
        bat_layout.addLayout(slider_layout)

        # Preset Buttons
        preset_layout = QHBoxLayout()
        btn_p60 = QPushButton(">_ 60% Max Lifespan")
        btn_p80 = QPushButton(">_ 80% Balanced Eco")
        btn_p100 = QPushButton(">_ 100% Full Charge")

        btn_p60.clicked.connect(lambda: self.slider_battery.setValue(60))
        btn_p80.clicked.connect(lambda: self.slider_battery.setValue(80))
        btn_p100.clicked.connect(lambda: self.slider_battery.setValue(100))

        preset_layout.addWidget(btn_p60)
        preset_layout.addWidget(btn_p80)
        preset_layout.addWidget(btn_p100)
        bat_layout.addLayout(preset_layout)

        btn_apply_bat = QPushButton("Apply Battery Charge Limit")
        btn_apply_bat.setStyleSheet("background-color: #132A20; color: #00FF66; border: 1px solid #00FF66; font-weight: bold; padding: 10px;")
        btn_apply_bat.clicked.connect(self._apply_battery_limit)
        bat_layout.addWidget(btn_apply_bat)

        layout.addWidget(bat_group)

        self.lbl_bat_status = QLabel("Battery Level: -- | Cap: --")
        self.lbl_bat_status.setStyleSheet("font-size: 13px; font-weight: bold; color: #E2E8F0;")
        layout.addWidget(self.lbl_bat_status)

        layout.addStretch()

    def _apply_battery_limit(self):
        val = self.slider_battery.value()
        ok, out = self.backend.set_battery_limit(val)
        if ok:
            self.show_status(f"Battery charge limit set to {val}%")
        else:
            self.show_status(f"Failed to set battery limit: {out}", is_error=True)

    # ---------------- TELEMETRY & REFRESH ----------------
    def _update_telemetry(self):
        t = self.backend.get_telemetry()
        self.bar_cpu.setValue(int(t["cpu_usage"]))
        self.bar_ram.setValue(int(t["mem_usage"]))
        self.lbl_cpu_temp.setText(f"CPU Temp: {t['cpu_temp']}")
        self.lbl_gpu_temp.setText(f"GPU Temp: {t['gpu_temp']} | Power Draw: {t['gpu_power']}")

        plugged_str = " (AC Plugged)" if t.get("power_plugged") else " (On Battery)"
        self.lbl_bat_status.setText(f"Battery Level: {t['battery_pct']}{plugged_str} | Charge Limit: {self.slider_battery.value()}%")

        # Automatic AC / Battery Power Switcher Logic
        current_plugged = t.get("power_plugged", True)
        if hasattr(self, "chk_auto_switcher") and self.chk_auto_switcher.isChecked():
            if self.last_power_plugged is not None and current_plugged != self.last_power_plugged:
                if current_plugged:
                    self._select_operating_mode("Turbo")
                    self.backend.set_refresh_rate(144)
                    self.show_status("[AUTO-POWER] AC Plugged In -> Auto-applied Turbo Mode + 144Hz!")
                    if hasattr(self, "lbl_auto_status"):
                        self.lbl_auto_status.setText("Status: AC Plugged (Turbo + 144Hz Active)")
                else:
                    self._select_operating_mode("Silent")
                    self.backend.set_refresh_rate(60)
                    self.show_status("[AUTO-POWER] Running on Battery -> Auto-applied Silent Mode (Whisper 40 FPS) + 60Hz!")
                    if hasattr(self, "lbl_auto_status"):
                        self.lbl_auto_status.setText("Status: On Battery (Silent + 60Hz Active)")
        
        self.last_power_plugged = current_plugged

    def refresh_manual_sliders_from_armoury(self):
        arm = self.backend.get_armoury_settings()
        if "nv_dynamic_boost" in arm:
            try:
                self.slider_dyn_boost.setValue(int(arm["nv_dynamic_boost"]))
            except Exception:
                pass
        if "ppt_pl1_spl" in arm:
            try:
                self.slider_pl1.setValue(int(arm["ppt_pl1_spl"]))
            except Exception:
                pass
        if "ppt_pl2_sppt" in arm:
            try:
                self.slider_pl2.setValue(int(arm["ppt_pl2_sppt"]))
            except Exception:
                pass

    def refresh_all_data(self):
        prof = self.backend.get_profile()
        if prof.lower() == "quiet":
            self.active_mode = "Silent"
        elif prof.lower() == "balanced":
            self.active_mode = "Performance"
        elif prof.lower() == "turbo":
            self.active_mode = "Turbo"
        else:
            self.active_mode = "Performance"

        self._update_mode_card_styles(self.active_mode)
        self._update_fps_combo_selection()

        gpu_m = self.backend.get_gpu_mode()
        self._update_gpu_buttons(gpu_m)
        self.lbl_gpu_pending.setText(f"Pending Action: {self.backend.get_gpu_pending_action()}")

        limit = self.backend.get_battery_limit()
        self.slider_battery.setValue(limit)

        bright = self.backend.get_kbd_brightness()
        self._update_kbd_buttons(bright)

        self.refresh_manual_sliders_from_armoury()
        self._update_telemetry()

