import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QSlider, QComboBox, QGroupBox, QProgressBar, QFrame,
    QColorDialog, QMessageBox, QGridLayout, QCheckBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QBrush, QPainterPath, QLinearGradient
from backend import AsusBackend

STYLE_SHEET = """
QMainWindow {
    background-color: #131722;
}
QWidget {
    color: #F8FAFC;
    font-family: 'Inter', 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    border: none;
    background: #131722;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2D364D;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #38BDF8;
}
QTabWidget::pane {
    border: 1px solid #2B3347;
    background-color: #181D2A;
    border-radius: 8px;
    top: -1px;
}
QTabBar::tab {
    background: #1C2230;
    color: #94A3B8;
    padding: 10px 22px;
    margin-right: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    border: 1px solid #283044;
    font-size: 13px;
}
QTabBar::tab:selected {
    background: #232B3E;
    color: #38BDF8;
    border-bottom: 3px solid #38BDF8;
    border-top: 1px solid #38BDF8;
    font-weight: bold;
}
QTabBar::tab:hover {
    background: #283146;
    color: #F1F5F9;
}
QGroupBox {
    border: 1px solid #2B3347;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 18px;
    background-color: #1D2333;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 3px 12px;
    background-color: #252D40;
    border: 1px solid #36415C;
    color: #38BDF8;
    font-size: 13px;
    font-weight: bold;
    border-radius: 4px;
}
QPushButton {
    background-color: #262E42;
    border: 1px solid #36415C;
    color: #F8FAFC;
    padding: 10px 18px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #303B54;
    border-color: #38BDF8;
    color: #FFFFFF;
}
QPushButton:pressed {
    background-color: #38BDF8;
    color: #0F172A;
}
QPushButton#modeBtnSelected {
    background-color: #0F2D3D;
    border: 2px solid #38BDF8;
    color: #38BDF8;
    font-weight: bold;
}

/* Operating Mode Cards - High Contrast Color-Coded Themes */
QPushButton#modeCard_Silent, QPushButton#modeCard_Performance, QPushButton#modeCard_Turbo, QPushButton#modeCard_Manual {
    background-color: #22293B;
    border: 1px solid #333D56;
    color: #F8FAFC;
    padding: 14px 16px;
    border-radius: 8px;
    text-align: left;
}
QPushButton#modeCard_Silent:hover, QPushButton#modeCard_Performance:hover, QPushButton#modeCard_Turbo:hover, QPushButton#modeCard_Manual:hover {
    background-color: #2B344B;
    border-color: #4B5978;
    color: #FFFFFF;
}

/* Silent Mode: Cool Cyan */
QPushButton#modeCard_Silent_Selected {
    background-color: #0F2D3D;
    border: 2px solid #0EA5E9;
    color: #38BDF8;
    padding: 14px 16px;
    border-radius: 8px;
    font-weight: bold;
    text-align: left;
}

/* Performance Mode: Emerald Green */
QPushButton#modeCard_Performance_Selected {
    background-color: #0F3023;
    border: 2px solid #10B981;
    color: #34D399;
    padding: 14px 16px;
    border-radius: 8px;
    font-weight: bold;
    text-align: left;
}

/* Turbo Mode: Coral Crimson */
QPushButton#modeCard_Turbo_Selected {
    background-color: #3D141C;
    border: 2px solid #F43F5E;
    color: #FB7185;
    padding: 14px 16px;
    border-radius: 8px;
    font-weight: bold;
    text-align: left;
}

/* Manual Mode: Vivid Violet */
QPushButton#modeCard_Manual_Selected {
    background-color: #2D1642;
    border: 2px solid #A855F7;
    color: #C084FC;
    padding: 14px 16px;
    border-radius: 8px;
    font-weight: bold;
    text-align: left;
}

QSlider::groove:horizontal {
    border: 1px solid #2B3347;
    height: 8px;
    background: #131722;
    border-radius: 4px;
}
QSlider::sub-page:horizontal {
    background: #38BDF8;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #181D2A;
    border: 2px solid #38BDF8;
    width: 18px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 9px;
}
QProgressBar {
    border: 1px solid #2B3347;
    border-radius: 6px;
    text-align: center;
    background-color: #131722;
    color: #F8FAFC;
    font-weight: bold;
    min-height: 22px;
}
QProgressBar::chunk {
    background-color: #10B981;
    border-radius: 5px;
}
QComboBox {
    background-color: #242B3D;
    border: 1px solid #333D56;
    border-radius: 6px;
    padding: 7px 14px;
    color: #F8FAFC;
    font-weight: 600;
}
QComboBox QAbstractItemView {
    background-color: #1D2333;
    selection-background-color: #2A3449;
    selection-color: #38BDF8;
    border: 1px solid #36415C;
}
QCheckBox {
    color: #38BDF8;
    font-weight: 600;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #36415C;
    border-radius: 4px;
    background: #242B3D;
}
QCheckBox::indicator:checked {
    background: #38BDF8;
    border: 1px solid #38BDF8;
}
"""

class FanCurveGraphWidget(QWidget):
    point_changed = pyqtSignal(int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(250)
        self.setMouseTracking(True)
        self.points = [
            [30, 15], [45, 25], [55, 40], [65, 55],
            [75, 70], [80, 80], [85, 90], [90, 100]
        ]
        self.fan_name = "CPU Fan"
        self.selected_idx = None
        self.hovered_idx = None
        self.margin_left = 45
        self.margin_bottom = 35
        self.margin_top = 20
        self.margin_right = 25

    def set_points(self, points_list, fan_name="CPU Fan"):
        new_pts = []
        for temp, pwm in points_list:
            pct = round((pwm / 255.0) * 100) if pwm > 100 else pwm
            new_pts.append([int(temp), int(pct)])
        self.points = new_pts
        self.fan_name = fan_name
        self.update()

    def get_points(self):
        res = []
        for temp, pct in self.points:
            pwm_val = round((pct / 100.0) * 255)
            res.append((temp, pwm_val))
        return res

    def _temp_pwm_to_pos(self, temp, pct):
        w = self.width() - self.margin_left - self.margin_right
        h = self.height() - self.margin_top - self.margin_bottom
        x = self.margin_left + ((temp - 20) / 80.0) * w
        y = self.height() - self.margin_bottom - (pct / 100.0) * h
        return QPointF(x, y)

    def _pos_to_temp_pwm(self, pos):
        w = self.width() - self.margin_left - self.margin_right
        h = self.height() - self.margin_top - self.margin_bottom
        temp = 20 + ((pos.x() - self.margin_left) / w) * 80.0
        pct = ((self.height() - self.margin_bottom - pos.y()) / h) * 100.0
        return int(round(temp)), int(round(pct))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        gx = self.margin_left
        gy = self.margin_top
        gw = w - self.margin_left - self.margin_right
        gh = h - self.margin_top - self.margin_bottom

        # Background
        painter.setBrush(QBrush(QColor("#181D2A")))
        painter.setPen(QPen(QColor("#2B3347"), 1))
        painter.drawRoundedRect(0, 0, w, h, 8, 8)

        # Grid lines
        for pct in range(0, 101, 25):
            y = h - self.margin_bottom - (pct / 100.0) * gh
            painter.setPen(QPen(QColor("#252E42"), 1, Qt.PenStyle.DashLine))
            painter.drawLine(int(gx), int(y), int(gx + gw), int(y))
            painter.setPen(QPen(QColor("#64748B"), 1))
            painter.setFont(QFont("Inter", 9))
            painter.drawText(5, int(y) + 4, f"{pct}%")

        for temp in range(30, 100, 10):
            x = gx + ((temp - 20) / 80.0) * gw
            painter.setPen(QPen(QColor("#252E42"), 1, Qt.PenStyle.DashLine))
            painter.drawLine(int(x), int(gy), int(x), int(gy + gh))
            painter.setPen(QPen(QColor("#64748B"), 1))
            painter.setFont(QFont("Inter", 9))
            painter.drawText(int(x) - 10, int(h - 10), f"{temp}°C")

        # Title Label in Canvas
        painter.setPen(QPen(QColor("#38BDF8"), 1))
        painter.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        painter.drawText(int(gx + 10), int(gy + 18), f"{self.fan_name} Dynamic Fan Curve")

        # Polygon path & gradient fill under curve
        if self.points:
            curve_path = QPainterPath()
            p0 = self._temp_pwm_to_pos(*self.points[0])
            curve_path.moveTo(p0)

            pts_pos = [self._temp_pwm_to_pos(*pt) for pt in self.points]
            for pt in pts_pos[1:]:
                curve_path.lineTo(pt)

            fill_path = QPainterPath(curve_path)
            fill_path.lineTo(pts_pos[-1].x(), gy + gh)
            fill_path.lineTo(pts_pos[0].x(), gy + gh)
            fill_path.closeSubpath()

            grad = QLinearGradient(0, gy, 0, gy + gh)
            grad.setColorAt(0.0, QColor(56, 189, 248, 80))
            grad.setColorAt(1.0, QColor(56, 189, 248, 5))
            painter.fillPath(fill_path, QBrush(grad))

            # Draw Main Curve Line
            painter.setPen(QPen(QColor("#38BDF8"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(curve_path)

            # Draw Node Points
            for idx, pt in enumerate(self.points):
                pos = self._temp_pwm_to_pos(*pt)
                is_selected = (idx == self.selected_idx)
                is_hovered = (idx == self.hovered_idx)

                node_r = 7 if (is_selected or is_hovered) else 5
                border_col = QColor("#F59E0B") if (is_selected or is_hovered) else QColor("#38BDF8")
                fill_col = QColor("#FFF") if is_selected else QColor("#0F172A")

                painter.setPen(QPen(border_col, 2))
                painter.setBrush(QBrush(fill_col))
                painter.drawEllipse(pos, float(node_r), float(node_r))

                # Tooltip bubble on hover/drag
                if is_selected or is_hovered:
                    lbl = f"P{idx+1}: {pt[0]}°C → {pt[1]}%"
                    painter.setFont(QFont("Inter", 9, QFont.Weight.Bold))
                    painter.setPen(QPen(QColor("#0F172A")))
                    painter.setBrush(QBrush(QColor("#F59E0B")))
                    rect = QRectF(pos.x() - 45, pos.y() - 28, 90, 20)
                    painter.drawRoundedRect(rect, 4, 4)
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for idx, pt in enumerate(self.points):
                pt_pos = self._temp_pwm_to_pos(*pt)
                dist = (pos.x() - pt_pos.x())**2 + (pos.y() - pt_pos.y())**2
                if dist <= 144:
                    self.selected_idx = idx
                    self.update()
                    break

    def mouseMoveEvent(self, event):
        pos = event.position()
        if self.selected_idx is not None:
            temp, pct = self._pos_to_temp_pwm(pos)
            pct = max(0, min(100, pct))
            min_t = 20 if self.selected_idx == 0 else self.points[self.selected_idx-1][0] + 1
            max_t = 100 if self.selected_idx == len(self.points)-1 else self.points[self.selected_idx+1][0] - 1
            temp = max(min_t, min(max_t, temp))

            self.points[self.selected_idx] = [temp, pct]
            self.point_changed.emit(self.selected_idx, temp, pct)
            self.update()
        else:
            prev_hover = self.hovered_idx
            self.hovered_idx = None
            for idx, pt in enumerate(self.points):
                pt_pos = self._temp_pwm_to_pos(*pt)
                dist = (pos.x() - pt_pos.x())**2 + (pos.y() - pt_pos.y())**2
                if dist <= 144:
                    self.hovered_idx = idx
                    break
            if prev_hover != self.hovered_idx:
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_idx = None
            self.update()


class AsusGuiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backend = AsusBackend()
        self.active_mode = "Performance"
        self.last_power_plugged = self.backend.get_power_plugged_status()
        self.setWindowTitle("ASUS TUF Control Center")
        self.setMinimumSize(920, 720)
        self.setStyleSheet(STYLE_SHEET)

        # Main widget & layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header Title
        header_layout = QHBoxLayout()
        title_label = QLabel("🛡️ ASUS TUF Control Center")
        title_font = QFont("Inter", 15, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #F8FAFC; font-weight: bold;")
        
        sub_title = QLabel("● System Online (TUF Gaming F15)")
        sub_title.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 600;")
        
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

        self.tabs.addTab(self.tab_mode, "⚡ Operating Mode")
        self.tabs.addTab(self.tab_manual, "🎛️ Manual Tuning")
        self.tabs.addTab(self.tab_lighting, "🎨 RGB && Display")
        self.tabs.addTab(self.tab_battery, "🔋 Battery Health")

        self._init_tab_mode()
        self._init_tab_manual()
        self._init_tab_lighting()
        self._init_tab_battery()

        # Modern Status Bar Footer
        self.status_bar = QLabel("System Status: Ready.")
        self.status_bar.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 600; padding: 8px 14px; background-color: #151824; border: 1px solid #1E2333; border-radius: 6px;")
        main_layout.addWidget(self.status_bar)

        # Timer for Telemetry
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self._update_telemetry)
        self.telemetry_timer.start(2000)

        # Initial load
        self.refresh_all_data()

    def show_status(self, message, is_error=False):
        color = "#EF4444" if is_error else "#10B981"
        prefix = "Status [Alert]: " if is_error else "Status: "
        self.status_bar.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: 600; padding: 8px 14px; background-color: #151824; border: 1px solid {color}; border-radius: 6px;")
        self.status_bar.setText(prefix + message)

    # ---------------- TAB 1: OPERATING MODE ----------------
    def _init_tab_mode(self):
        # Wrap tab in scroll area to prevent vertical squishing
        scroll = QScrollArea(self.tab_mode)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        container = QWidget()
        scroll.setWidget(container)
        
        tab_layout = QVBoxLayout(self.tab_mode)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # 1. Live Monitor Header Card
        tele_group = QGroupBox("Live System Telemetry")
        tele_layout = QGridLayout(tele_group)
        tele_layout.setSpacing(10)
        tele_layout.setColumnStretch(1, 1)

        tele_layout.addWidget(QLabel("CPU Usage:"), 0, 0)
        self.bar_cpu = QProgressBar()
        self.bar_cpu.setRange(0, 100)
        tele_layout.addWidget(self.bar_cpu, 0, 1)
        self.lbl_cpu_temp = QLabel("CPU Temp: --")
        self.lbl_cpu_temp.setStyleSheet("font-weight: bold; color: #10B981;")
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

        # 2. Armoury Operating Mode Cards (2x2 Grid)
        mode_group = QGroupBox("Armoury Operating Modes")
        mode_grid = QGridLayout(mode_group)
        mode_grid.setSpacing(10)

        # Silent Card
        self.btn_mode_silent = QPushButton(
            "🤫 Silent Mode (Whisper 40 FPS Cap)\n"
            "• Power Target: PL1 35W | Boost 5W | <60°C Thermals\n"
            "• Low wattage && quiet fans for story games."
        )
        self.btn_mode_silent.setObjectName("modeCard_Silent")
        self.btn_mode_silent.setMinimumHeight(76)
        self.btn_mode_silent.clicked.connect(lambda: self._select_operating_mode("Silent"))
        mode_grid.addWidget(self.btn_mode_silent, 0, 0)

        # Performance Card
        self.btn_mode_perf = QPushButton(
            "⚖️ Performance Mode (60 FPS Cap)\n"
            "• Power Target: PL1 65W | Boost 10W | Balanced\n"
            "• Balanced power, heat && fans for everyday gaming."
        )
        self.btn_mode_perf.setObjectName("modeCard_Performance")
        self.btn_mode_perf.setMinimumHeight(76)
        self.btn_mode_perf.clicked.connect(lambda: self._select_operating_mode("Performance"))
        mode_grid.addWidget(self.btn_mode_perf, 0, 1)

        # Turbo Card
        self.btn_mode_turbo = QPushButton(
            "🔥 Turbo Mode (Unlimited FPS)\n"
            "• Power Target: PL1 90W | PL2 135W | Boost 15W\n"
            "• Maximum power limits && fans for esports gaming."
        )
        self.btn_mode_turbo.setObjectName("modeCard_Turbo")
        self.btn_mode_turbo.setMinimumHeight(76)
        self.btn_mode_turbo.clicked.connect(lambda: self._select_operating_mode("Turbo"))
        mode_grid.addWidget(self.btn_mode_turbo, 1, 0)

        # Manual Card
        self.btn_mode_manual = QPushButton(
            "⚙️ Manual Mode (Custom Power Targets)\n"
            "• Power Target: User Custom PL1/PL2 && Dynamic Boost\n"
            "• Full manual control over power && FPS limits."
        )
        self.btn_mode_manual.setObjectName("modeCard_Manual")
        self.btn_mode_manual.setMinimumHeight(76)
        self.btn_mode_manual.clicked.connect(lambda: self._select_operating_mode("Manual"))
        mode_grid.addWidget(self.btn_mode_manual, 1, 1)

        layout.addWidget(mode_group)

        # 3. Horizontal Split: Auto Power Switcher + WhisperMode FPS Limiter
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(10)

        # Left: Auto Power Switcher
        auto_group = QGroupBox("Automatic AC / Battery Power Switcher")
        auto_layout = QVBoxLayout(auto_group)
        auto_layout.setSpacing(6)

        self.chk_auto_switcher = QCheckBox("Enable Auto Power && Refresh Rate Switcher")
        self.chk_auto_switcher.setChecked(True)
        auto_layout.addWidget(self.chk_auto_switcher)

        self.lbl_auto_status = QLabel("Policy: [AC: Turbo + 144Hz] <-> [Battery: Silent + 60Hz]")
        self.lbl_auto_status.setStyleSheet("color: #F59E0B; font-size: 11px; font-weight: 600;")
        auto_layout.addWidget(self.lbl_auto_status)

        mid_layout.addWidget(auto_group, 1)

        # Right: FPS Limiter
        fps_group = QGroupBox("WhisperMode 2.0 Game FPS Limiter")
        fps_vlayout = QVBoxLayout(fps_group)
        
        fps_controls = QHBoxLayout()
        fps_controls.addWidget(QLabel("Target Game FPS:"))
        self.combo_fps = QComboBox()
        self.combo_fps.addItems([
            "40 FPS (Quiet ~60°C)",
            "60 FPS (Balanced)",
            "90 FPS (High Refresh)",
            "120 FPS",
            "0 (Unlimited FPS)"
        ])
        fps_controls.addWidget(self.combo_fps)

        btn_apply_fps = QPushButton("Apply Cap")
        btn_apply_fps.clicked.connect(self._apply_manual_fps_cap)
        fps_controls.addWidget(btn_apply_fps)

        btn_help_fps = QPushButton("? Setup Info")
        btn_help_fps.clicked.connect(self._show_fps_help_dialog)
        fps_controls.addWidget(btn_help_fps)

        fps_vlayout.addLayout(fps_controls)
        mid_layout.addWidget(fps_group, 1)

        layout.addLayout(mid_layout)

        # 4. GPU Graphics Switcher
        gpu_group = QGroupBox("GPU Graphics Mode (supergfxctl)")
        gpu_layout = QVBoxLayout(gpu_group)

        gpu_btns_layout = QHBoxLayout()
        self.btn_gpu_igpu = QPushButton("Integrated (iGPU)")
        self.btn_gpu_hybrid = QPushButton("Hybrid (Optimus)")
        self.btn_gpu_dgpu = QPushButton("Dedicated (MUX)")
        
        for btn in [self.btn_gpu_igpu, self.btn_gpu_hybrid, self.btn_gpu_dgpu]:
            btn.setMinimumHeight(38)

        self.btn_gpu_igpu.clicked.connect(lambda: self._set_gpu_mode("Integrated"))
        self.btn_gpu_hybrid.clicked.connect(lambda: self._set_gpu_mode("Hybrid"))
        self.btn_gpu_dgpu.clicked.connect(lambda: self._set_gpu_mode("AsusMuxDgpu"))

        gpu_btns_layout.addWidget(self.btn_gpu_igpu)
        gpu_btns_layout.addWidget(self.btn_gpu_hybrid)
        gpu_btns_layout.addWidget(self.btn_gpu_dgpu)
        gpu_layout.addLayout(gpu_btns_layout)

        self.lbl_gpu_pending = QLabel("Pending Action: None")
        self.lbl_gpu_pending.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
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
                btn.setObjectName(f"modeCard_{mode}_Selected")
                btn.setStyle(btn.style())
            else:
                btn.setObjectName(f"modeCard_{mode}")
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
        scroll = QScrollArea(self.tab_manual)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)

        scroll.setWidget(container)
        tab_layout = QVBoxLayout(self.tab_manual)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

        info_manual = QLabel(
            "Manual Power Mode: Customize CPU sustained PL1, short burst PL2, GPU Dynamic Boost, and Custom Fan Curves (asusd)."
        )
        info_manual.setWordWrap(True)
        info_manual.setStyleSheet("color: #10B981; font-size: 13px; font-weight: 600;")
        layout.addWidget(info_manual)

        # Dynamic Boost Slider
        gpu_power_group = QGroupBox("NVIDIA Dynamic Boost Power Target")
        gpu_power_layout = QGridLayout(gpu_power_group)
        gpu_power_layout.setSpacing(12)

        gpu_power_layout.addWidget(QLabel("NV Dynamic Boost Offset:"), 0, 0)
        self.slider_dyn_boost = QSlider(Qt.Orientation.Horizontal)
        self.slider_dyn_boost.setRange(5, 15)
        self.slider_dyn_boost.setValue(15)
        self.lbl_val_dyn_boost = QLabel("15 W")
        self.lbl_val_dyn_boost.setFixedWidth(45)
        self.lbl_val_dyn_boost.setStyleSheet("font-weight: bold; color: #10B981;")
        self.slider_dyn_boost.valueChanged.connect(lambda v: self.lbl_val_dyn_boost.setText(f"{v} W"))
        btn_apply_boost = QPushButton("Apply Boost")
        btn_apply_boost.clicked.connect(self._apply_dyn_boost)

        gpu_power_layout.addWidget(self.slider_dyn_boost, 0, 1)
        gpu_power_layout.addWidget(self.lbl_val_dyn_boost, 0, 2)
        gpu_power_layout.addWidget(btn_apply_boost, 0, 3)

        layout.addWidget(gpu_power_group)

        # CPU PL1 & PL2 Sliders
        cpu_power_group = QGroupBox("CPU Power Limits (PL1 & PL2)")
        cpu_layout = QGridLayout(cpu_power_group)
        cpu_layout.setSpacing(12)

        # CPU PL1
        cpu_layout.addWidget(QLabel("CPU PL1 Sustained Limit:"), 0, 0)
        self.slider_pl1 = QSlider(Qt.Orientation.Horizontal)
        self.slider_pl1.setRange(28, 90)
        self.slider_pl1.setValue(90)
        self.lbl_val_pl1 = QLabel("90 W")
        self.lbl_val_pl1.setFixedWidth(45)
        self.lbl_val_pl1.setStyleSheet("font-weight: bold; color: #10B981;")
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
        self.lbl_val_pl2.setStyleSheet("font-weight: bold; color: #10B981;")
        self.slider_pl2.valueChanged.connect(lambda v: self.lbl_val_pl2.setText(f"{v} W"))
        btn_apply_pl2 = QPushButton("Apply PL2")
        btn_apply_pl2.clicked.connect(self._apply_pl2)

        cpu_layout.addWidget(self.slider_pl2, 1, 1)
        cpu_layout.addWidget(self.lbl_val_pl2, 1, 2)
        cpu_layout.addWidget(btn_apply_pl2, 1, 3)

        layout.addWidget(cpu_power_group)

        # Custom Fan Curve Graph Editor Group
        fan_group = QGroupBox("🌀 Custom Fan Curve Graph Editor (asusctl / asusd)")
        fan_layout = QVBoxLayout(fan_group)
        fan_layout.setSpacing(12)

        # Controls header: Fan selector, Profile selector, Enable checkbox
        fan_controls_layout = QHBoxLayout()

        lbl_prof = QLabel("Profile:")
        lbl_prof.setStyleSheet("font-weight: bold; color: #38BDF8;")
        self.combo_fan_prof = QComboBox()
        self.combo_fan_prof.addItems(["Balanced", "Performance", "Quiet"])
        self.combo_fan_prof.currentTextChanged.connect(self._on_fan_profile_changed)

        self.btn_fan_cpu = QPushButton("💻 CPU Fan")
        self.btn_fan_gpu = QPushButton("🎮 GPU Fan")
        self.btn_fan_cpu.setObjectName("modeBtnSelected")
        
        self.btn_fan_cpu.clicked.connect(lambda: self._select_fan_target("CPU"))
        self.btn_fan_gpu.clicked.connect(lambda: self._select_fan_target("GPU"))

        self.chk_fan_enabled = QCheckBox("Enable Custom Fan Curve")
        self.chk_fan_enabled.stateChanged.connect(self._on_fan_enabled_toggled)

        fan_controls_layout.addWidget(lbl_prof)
        fan_controls_layout.addWidget(self.combo_fan_prof)
        fan_controls_layout.addWidget(self.btn_fan_cpu)
        fan_controls_layout.addWidget(self.btn_fan_gpu)
        fan_controls_layout.addStretch()
        fan_controls_layout.addWidget(self.chk_fan_enabled)

        fan_layout.addLayout(fan_controls_layout)

        # Graph Widget
        self.fan_graph = FanCurveGraphWidget()
        fan_layout.addWidget(self.fan_graph)

        # Presets & Apply Buttons
        preset_layout = QHBoxLayout()
        btn_preset_quiet = QPushButton("🤫 Stealth Quiet")
        btn_preset_balanced = QPushButton("⚖️ Balanced Ramp")
        btn_preset_aggro = QPushButton("🔥 Aggressive Cooling")
        btn_preset_reset = QPushButton("🔄 Reset Factory")
        btn_apply_fan = QPushButton("⚡ Apply Fan Curve")
        btn_apply_fan.setStyleSheet("background-color: #0EA5E9; color: #FFFFFF; font-weight: bold;")

        btn_preset_quiet.clicked.connect(lambda: self._apply_fan_preset("quiet"))
        btn_preset_balanced.clicked.connect(lambda: self._apply_fan_preset("balanced"))
        btn_preset_aggro.clicked.connect(lambda: self._apply_fan_preset("aggro"))
        btn_preset_reset.clicked.connect(self._reset_fan_curve_defaults)
        btn_apply_fan.clicked.connect(self._save_and_apply_fan_curve)

        preset_layout.addWidget(btn_preset_quiet)
        preset_layout.addWidget(btn_preset_balanced)
        preset_layout.addWidget(btn_preset_aggro)
        preset_layout.addWidget(btn_preset_reset)
        preset_layout.addStretch()
        preset_layout.addWidget(btn_apply_fan)

        fan_layout.addLayout(preset_layout)
        layout.addWidget(fan_group)

        # Init fan curve data
        self.active_fan_target = "CPU"
        self.fan_curves_data = self.backend.get_fan_curves()
        self._load_current_fan_curve_to_graph()

    def _select_fan_target(self, target):
        self.active_fan_target = target
        if target == "CPU":
            self.btn_fan_cpu.setObjectName("modeBtnSelected")
            self.btn_fan_gpu.setObjectName("")
        else:
            self.btn_fan_cpu.setObjectName("")
            self.btn_fan_gpu.setObjectName("modeBtnSelected")
        self.btn_fan_cpu.setStyle(self.btn_fan_cpu.style())
        self.btn_fan_gpu.setStyle(self.btn_fan_gpu.style())
        self._load_current_fan_curve_to_graph()

    def _on_fan_profile_changed(self, prof_text):
        self._load_current_fan_curve_to_graph()

    def _load_current_fan_curve_to_graph(self):
        prof = self.combo_fan_prof.currentText().lower()
        fan_info = self.fan_curves_data.get(prof, {}).get(self.active_fan_target, {})
        temps = fan_info.get("temp", [57, 59, 62, 67, 70, 73, 75, 77])
        pwms = fan_info.get("pwm", [40, 66, 84, 84, 109, 147, 155, 181])
        enabled = fan_info.get("enabled", False)

        pts = list(zip(temps, pwms))
        self.fan_graph.set_points(pts, f"{self.active_fan_target} Fan ({self.combo_fan_prof.currentText()})")
        self.chk_fan_enabled.blockSignals(True)
        self.chk_fan_enabled.setChecked(enabled)
        self.chk_fan_enabled.blockSignals(False)

    def _on_fan_enabled_toggled(self, state):
        prof = self.combo_fan_prof.currentText().lower()
        if prof in self.fan_curves_data and self.active_fan_target in self.fan_curves_data[prof]:
            self.fan_curves_data[prof][self.active_fan_target]["enabled"] = (state == 2 or state == True)

    def _apply_fan_preset(self, preset_name):
        if preset_name == "quiet":
            temps = [30, 45, 55, 65, 72, 78, 83, 90]
            pwms = [0, 25, 51, 89, 115, 140, 165, 191] # 0..255
        elif preset_name == "balanced":
            temps = [30, 45, 55, 65, 72, 78, 83, 90]
            pwms = [38, 64, 102, 140, 178, 204, 230, 255]
        elif preset_name == "aggro":
            temps = [30, 45, 55, 65, 70, 75, 80, 85]
            pwms = [64, 102, 153, 204, 255, 255, 255, 255]
        pts = list(zip(temps, pwms))
        self.fan_graph.set_points(pts, f"{self.active_fan_target} Fan ({self.combo_fan_prof.currentText()})")

    def _reset_fan_curve_defaults(self):
        self.fan_curves_data = self.backend.DEFAULT_FAN_CURVES
        self._load_current_fan_curve_to_graph()

    def _save_and_apply_fan_curve(self):
        prof = self.combo_fan_prof.currentText().lower()
        pts = self.fan_graph.get_points()
        temps = [p[0] for p in pts]
        pwms = [p[1] for p in pts]
        is_en = self.chk_fan_enabled.isChecked()

        if prof not in self.fan_curves_data:
            self.fan_curves_data[prof] = {}
        self.fan_curves_data[prof][self.active_fan_target] = {
            "temp": temps,
            "pwm": pwms,
            "enabled": is_en
        }

        ok, msg = self.backend.save_fan_curves(self.fan_curves_data)
        if ok:
            self.show_status(f"Fan Curve saved & applied for {self.active_fan_target} ({prof.capitalize()})! {msg}")
        else:
            self.show_status(f"Failed to save fan curve: {msg}", is_error=True)

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
        scroll = QScrollArea(self.tab_lighting)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        scroll.setWidget(container)
        
        tab_layout = QVBoxLayout(self.tab_lighting)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        # GameVisual Display Profiles Card
        gv_group = QGroupBox("GameVisual Display Modes")
        gv_layout = QVBoxLayout(gv_group)
        gv_layout.setSpacing(10)

        gv_grid = QGridLayout()
        gv_grid.setSpacing(8)

        gv_modes = [
            ("Default", "🎯 Default"),
            ("Racing", "🏎️ Racing"),
            ("Scenery", "🏞️ Scenery"),
            ("RTS/RPG", "⚔️ RTS/RPG"),
            ("FPS", "🎯 FPS (Dark Boost)"),
            ("Cinema", "🎬 Cinema"),
            ("Eye Care", "👁️ Eye Care"),
            ("Vivid", "🎨 Vivid Color")
        ]

        self.gv_buttons = {}
        for idx, (m_key, m_label) in enumerate(gv_modes):
            row = idx // 4
            col = idx % 4
            btn = QPushButton(m_label)
            btn.setMinimumHeight(36)
            btn.clicked.connect(lambda _, k=m_key: self._set_gamevisual_mode(k))
            gv_grid.addWidget(btn, row, col)
            self.gv_buttons[m_key] = btn

        gv_layout.addLayout(gv_grid)

        self.lbl_gv_desc = QLabel("GameVisual: Select a display color profile to enhance screen contrast, saturation and eye care.")
        self.lbl_gv_desc.setStyleSheet("color: #94A3B8; font-size: 11px; font-style: italic;")
        gv_layout.addWidget(self.lbl_gv_desc)

        layout.addWidget(gv_group)

        # Keyboard Backlight Brightness
        bright_group = QGroupBox("Keyboard Backlight Brightness")
        bright_layout = QHBoxLayout(bright_group)

        self.btn_k_off = QPushButton("Off")
        self.btn_k_low = QPushButton("Low")
        self.btn_k_med = QPushButton("Medium")
        self.btn_k_high = QPushButton("High")

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
        aura_group = QGroupBox("Aura RGB Lighting Effects")
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
        self.btn_pick_color.setStyleSheet(f"background-color: #1C2030; color: #{self.current_color}; border: 1px solid #{self.current_color}; font-weight: bold;")
        self.btn_pick_color.clicked.connect(self._pick_color)

        color_layout.addWidget(self.btn_pick_color)

        # Quick Preset Swatches
        swatches = [
            ("Green", "10B981"), ("Cyan", "06B6D4"), ("Amber", "F59E0B"),
            ("Red", "EF4444"), ("Purple", "A855F7"), ("White", "F8FAFC")
        ]
        for label, hex_c in swatches:
            btn_s = QPushButton(label)
            btn_s.setStyleSheet(f"background-color: #1C2030; color: #{hex_c}; border: 1px solid #{hex_c}; font-size: 11px;")
            btn_s.clicked.connect(lambda _, c=hex_c: self._set_color_hex(c))
            color_layout.addWidget(btn_s)

        aura_layout.addLayout(color_layout)

        btn_apply_aura = QPushButton("Apply Aura Lighting Effect")
        btn_apply_aura.setStyleSheet("background-color: #0F2D20; color: #10B981; border: 1px solid #10B981; font-size: 13px; font-weight: bold; padding: 10px;")
        btn_apply_aura.clicked.connect(self._apply_aura)
        aura_layout.addWidget(btn_apply_aura)

        layout.addWidget(aura_group)

        # Screen Panel Overdrive
        panel_group = QGroupBox("Display Panel Overdrive")
        panel_layout = QHBoxLayout(panel_group)

        self.btn_overdrive_on = QPushButton("Overdrive ON (3ms Low Latency)")
        self.btn_overdrive_off = QPushButton("Overdrive OFF (Normal)")

        self.btn_overdrive_on.clicked.connect(lambda: self._set_overdrive(True))
        self.btn_overdrive_off.clicked.connect(lambda: self._set_overdrive(False))

        panel_layout.addWidget(self.btn_overdrive_on)
        panel_layout.addWidget(self.btn_overdrive_off)
        layout.addWidget(panel_group)

        layout.addStretch()

    def _set_gamevisual_mode(self, mode_name):
        ok, msg = self.backend.set_gamevisual_mode(mode_name)
        if ok:
            self.show_status(msg)
            profile = self.backend.GAMEVISUAL_PROFILES.get(mode_name, {})
            if hasattr(self, "lbl_gv_desc"):
                self.lbl_gv_desc.setText(f"GameVisual [{mode_name}]: {profile.get('desc', '')}")
            self._update_gv_buttons(mode_name)
        else:
            self.show_status(f"GameVisual Error: {msg}", is_error=True)

    def _update_gv_buttons(self, active_mode):
        for key, btn in self.gv_buttons.items():
            if key.lower() == active_mode.lower():
                btn.setObjectName("modeBtnSelected")
                btn.setStyle(btn.style())
            else:
                btn.setObjectName("")
                btn.setStyle(btn.style())

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

        bat_group = QGroupBox("Battery Charge Threshold Limit")
        bat_layout = QVBoxLayout(bat_group)
        bat_layout.setSpacing(16)

        info_lbl = QLabel(
            "Setting a maximum charge limit protects battery chemistry and prolongs battery lifespan when connected to AC charger for long periods."
        )
        info_lbl.setWordWrap(True)
        info_lbl.setStyleSheet("color: #94A3B8;")
        bat_layout.addWidget(info_lbl)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Charge Limit Target:"))
        self.slider_battery = QSlider(Qt.Orientation.Horizontal)
        self.slider_battery.setRange(20, 100)
        self.slider_battery.setValue(80)
        self.lbl_bat_limit_val = QLabel("80 %")
        self.lbl_bat_limit_val.setStyleSheet("font-weight: bold; color: #10B981; font-size: 16px;")
        self.lbl_bat_limit_val.setFixedWidth(50)

        self.slider_battery.valueChanged.connect(lambda v: self.lbl_bat_limit_val.setText(f"{v} %"))

        slider_layout.addWidget(self.slider_battery)
        slider_layout.addWidget(self.lbl_bat_limit_val)
        bat_layout.addLayout(slider_layout)

        # Preset Buttons
        preset_layout = QHBoxLayout()
        btn_p60 = QPushButton("60% Maximum Lifespan")
        btn_p80 = QPushButton("80% Balanced Eco")
        btn_p100 = QPushButton("100% Full Charge")

        btn_p60.clicked.connect(lambda: self.slider_battery.setValue(60))
        btn_p80.clicked.connect(lambda: self.slider_battery.setValue(80))
        btn_p100.clicked.connect(lambda: self.slider_battery.setValue(100))

        preset_layout.addWidget(btn_p60)
        preset_layout.addWidget(btn_p80)
        preset_layout.addWidget(btn_p100)
        bat_layout.addLayout(preset_layout)

        btn_apply_bat = QPushButton("Apply Battery Charge Limit")
        btn_apply_bat.setStyleSheet("background-color: #0F2D20; color: #10B981; border: 1px solid #10B981; font-weight: bold; padding: 10px;")
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

