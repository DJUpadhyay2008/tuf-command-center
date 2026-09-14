import subprocess
import re
import os
import psutil

class AsusBackend:
    @staticmethod
    def _run_cmd(cmd):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return res.returncode == 0, res.stdout + res.stderr
        except Exception as e:
            return False, str(e)

    # --- FPS Limiter (WhisperMode 2.0 via DXVK & MangoHud) ---
    def set_fps_limit(self, limit):
        try:
            # 1. MangoHud config
            mh_path = os.path.expanduser("~/.config/MangoHud/MangoHud.conf")
            os.makedirs(os.path.dirname(mh_path), exist_ok=True)
            mh_content = ""
            if os.path.exists(mh_path):
                with open(mh_path, "r") as f:
                    mh_content = f.read()
            if "fps_limit=" in mh_content:
                mh_content = re.sub(r"fps_limit=\d+", f"fps_limit={limit}", mh_content)
            else:
                mh_content += f"\nfps_limit={limit}\n"
            with open(mh_path, "w") as f:
                f.write(mh_content)

            # 2. DXVK config (for Proton / DXVK games like RDR2, Witcher 3, Cyberpunk)
            dxvk_path = os.path.expanduser("~/.config/dxvk.conf")
            os.makedirs(os.path.dirname(dxvk_path), exist_ok=True)
            dxvk_content = ""
            if os.path.exists(dxvk_path):
                with open(dxvk_path, "r") as f:
                    dxvk_content = f.read()
            if "dxvk.maxFrameRate" in dxvk_content:
                dxvk_content = re.sub(r"dxvk\.maxFrameRate\s*=\s*\d+", f"dxvk.maxFrameRate = {limit}", dxvk_content)
            else:
                dxvk_content += f"\ndxvk.maxFrameRate = {limit}\n"
            with open(dxvk_path, "w") as f:
                f.write(dxvk_content)

            return True, f"FPS limit set to {limit} in MangoHud and DXVK"
        except Exception as e:
            return False, str(e)

    def get_fps_limit(self):
        mh_path = os.path.expanduser("~/.config/MangoHud/MangoHud.conf")
        try:
            if os.path.exists(mh_path):
                with open(mh_path, "r") as f:
                    content = f.read()
                m = re.search(r"fps_limit=(\d+)", content)
                if m:
                    return int(m.group(1))
        except Exception:
            pass
        return 0

    # --- Operating Modes (Armoury Crate Presets with WhisperMode) ---
    def apply_operating_mode(self, mode_name, fps_override=None):
        mode = mode_name.lower()
        if mode == "silent":
            self.set_profile("Quiet")
            self.set_cpu_pl1(35)
            self.set_cpu_pl2(45)
            self.set_nv_dynamic_boost(5)
            fps_val = 40 if fps_override is None else fps_override
            self.set_fps_limit(fps_val)
            return True, f"Silent Mode applied (PL1 35W, Dynamic Boost 5W, WhisperMode {fps_val} FPS Cap)."
        elif mode == "performance":
            self.set_profile("Balanced")
            self.set_cpu_pl1(65)
            self.set_cpu_pl2(90)
            self.set_nv_dynamic_boost(10)
            fps_val = 60 if fps_override is None else fps_override
            self.set_fps_limit(fps_val)
            return True, f"Performance Mode applied (Balanced power, {fps_val if fps_val > 0 else 'Unlimited'} FPS)."
        elif mode == "turbo":
            self.set_profile("Turbo")
            self.set_cpu_pl1(90)
            self.set_cpu_pl2(135)
            self.set_nv_dynamic_boost(15)
            fps_val = 0 if fps_override is None else fps_override
            self.set_fps_limit(fps_val)
            return True, "Turbo Mode applied (Max hardware limits & Unlimited FPS)."
        elif mode == "manual":
            self.set_profile("Performance")
            return True, "Manual Mode enabled (Custom power limits & fan control unlocked)."
        return False, "Unknown mode"

    # --- Performance Profile ---
    def get_profile(self):
        ok, out = self._run_cmd(["asusctl", "profile", "-p"])
        if ok:
            match = re.search(r"Active profile is\s+([A-Za-z]+)", out, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
            for line in out.splitlines():
                if "active profile" in line.lower() or "current profile" in line.lower():
                    parts = line.split(":")
                    if len(parts) > 1:
                        return parts[-1].strip().capitalize()
        return "Balanced"

    def set_profile(self, profile):
        ok, out = self._run_cmd(["asusctl", "profile", "-P", profile])
        gnome_mode = "balanced"
        if profile.lower() in ["quiet", "silent"]:
            gnome_mode = "power-saver"
        elif profile.lower() in ["performance", "turbo"]:
            gnome_mode = "performance"
        self._run_cmd(["powerprofilesctl", "set", gnome_mode])
        return ok, out

    # --- GPU Mode (supergfxctl) ---
    def get_gpu_mode(self):
        ok, out = self._run_cmd(["supergfxctl", "-g"])
        if ok:
            lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
            if lines:
                return lines[-1].capitalize()
        return "Hybrid"

    def set_gpu_mode(self, mode):
        ok, out = self._run_cmd(["supergfxctl", "-m", mode])
        return ok, out

    def get_gpu_pending_action(self):
        ok, out = self._run_cmd(["supergfxctl", "-p"])
        if ok:
            return out.strip()
        return "None"

    # --- Battery Charge Limit ---
    def get_battery_limit(self):
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok:
            match = re.search(r"ChargeControlEndThreshold.*?(\d+)", out)
            if match:
                return int(match.group(1))
        for b_name in ["BAT1", "BAT0"]:
            try:
                with open(f"/sys/class/power_supply/{b_name}/charge_control_end_threshold", "r") as f:
                    return int(f.read().strip())
            except Exception:
                pass
        return 80

    def set_battery_limit(self, limit):
        ok, out = self._run_cmd(["asusctl", "-c", str(limit)])
        return ok, out

    # --- Keyboard Brightness ---
    def get_kbd_brightness(self):
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok:
            match = re.search(r"Keyboard Brightness.*?([A-Za-z]+)", out, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        try:
            with open("/sys/class/leds/asus::kbd_backlight/brightness", "r") as f:
                val = int(f.read().strip())
                mapping = {0: "Off", 1: "Low", 2: "Med", 3: "High"}
                return mapping.get(val, "Low")
        except Exception:
            pass
        return "Low"

    def set_kbd_brightness(self, level):
        ok, out = self._run_cmd(["asusctl", "-k", level.lower()])
        return ok, out

    # --- Aura RGB Lighting ---
    def set_aura_mode(self, mode, color_hex="FF0000", speed="med"):
        mode_lower = mode.lower()
        if mode_lower == "static":
            cmd = ["asusctl", "aura", "static", "-c", color_hex]
        elif mode_lower == "breathe":
            cmd = ["asusctl", "aura", "breathe", "-c", color_hex, "-s", speed]
        elif mode_lower in ["rainbowcycle", "rainbow-cycle"]:
            cmd = ["asusctl", "aura", "rainbow-cycle", "-s", speed]
        elif mode_lower in ["rainbowwave", "rainbow-wave"]:
            cmd = ["asusctl", "aura", "rainbow-wave", "-s", speed]
        elif mode_lower == "pulse":
            cmd = ["asusctl", "aura", "pulse", "-c", color_hex, "-s", speed]
        else:
            cmd = ["asusctl", "aura", mode_lower]
        
        ok, out = self._run_cmd(cmd)
        return ok, out

    # --- Armoury Settings ---
    def get_armoury_settings(self):
        ok, out = self._run_cmd(["asusctl", "armoury"])
        settings = {}
        if ok:
            current_attr = None
            for line in out.splitlines():
                line_str = line.strip()
                if line_str.endswith(":"):
                    current_attr = line_str[:-1]
                elif current_attr and "current:" in line_str:
                    val_str = line_str.split("current:")[-1].strip()
                    m_range = re.search(r"\[(\d+)\]", val_str)
                    m_sel = re.search(r"\(([0-9]+)\)", val_str)
                    if m_range:
                        settings[current_attr] = int(m_range.group(1))
                    elif m_sel:
                        settings[current_attr] = int(m_sel.group(1))
                    else:
                        settings[current_attr] = val_str
        return settings

    def set_armoury_setting(self, name, value):
        ok, out = self._run_cmd(["asusctl", "armoury", name, str(value)])
        return ok, out

    def set_nv_dynamic_boost(self, watts):
        return self.set_armoury_setting("nv_dynamic_boost", watts)

    def set_cpu_pl1(self, watts):
        return self.set_armoury_setting("ppt_pl1_spl", watts)

    def set_cpu_pl2(self, watts):
        return self.set_armoury_setting("ppt_pl2_sppt", watts)

    def set_panel_overdrive(self, enabled):
        val = 1 if enabled else 0
        return self.set_armoury_setting("panel_overdrive", val)

    # --- NVIDIA SMI Controls ---
    def get_gpu_info(self):
        cmd = ["nvidia-smi", "--query-gpu=temperature.gpu,power.draw,power.limit", "--format=csv,noheader,nounits"]
        ok, out = self._run_cmd(cmd)
        temp, power_draw, power_limit = "N/A", "N/A", "80"

        if ok and out.strip():
            parts = [p.strip() for p in out.strip().split(",")]
            if len(parts) >= 2:
                temp = parts[0]
                power_draw = parts[1]
                if len(parts) >= 3 and parts[2] not in ["N/A", "[N/A]"]:
                    power_limit = parts[2]

        return {
            "temp": temp,
            "power_draw": power_draw,
            "power_limit": power_limit
        }

    # --- System Telemetry ---
    def get_telemetry(self):
        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        mem_pct = mem.percent

        cpu_temp = "N/A"
        try:
            temps = psutil.sensors_temperatures()
            if "k10temp" in temps and temps["k10temp"]:
                cpu_temp = f"{temps['k10temp'][0].current:.1f} °C"
            elif "coretemp" in temps and temps["coretemp"]:
                cpu_temp = f"{temps['coretemp'][0].current:.1f} °C"
            elif "acpitz" in temps and temps["acpitz"]:
                cpu_temp = f"{temps['acpitz'][0].current:.1f} °C"
            elif temps:
                for key, entries in temps.items():
                    if entries:
                        cpu_temp = f"{entries[0].current:.1f} °C"
                        break
        except Exception:
            pass

        gpu_info = self.get_gpu_info()
        gpu_temp = f"{gpu_info['temp']} °C" if gpu_info['temp'] != "N/A" else "N/A"

        bat_pct = "N/A"
        try:
            bat = psutil.sensors_battery()
            if bat:
                bat_pct = f"{int(bat.percent)}%"
        except Exception:
            pass

        return {
            "cpu_usage": cpu_pct,
            "mem_usage": mem_pct,
            "cpu_temp": cpu_temp,
            "gpu_temp": gpu_temp,
            "gpu_power": f"{gpu_info['power_draw']} W" if gpu_info['power_draw'] != "N/A" else "N/A",
            "battery_pct": bat_pct,
            "power_plugged": self.get_power_plugged_status()
        }

    # --- Power AC / Battery Status ---
    def get_power_plugged_status(self):
        try:
            bat = psutil.sensors_battery()
            if bat and bat.power_plugged is not None:
                return bat.power_plugged
        except Exception:
            pass
        
        # Check sysfs AC adapter status
        for ac in ["ACAD", "AC", "ADP1", "AC0"]:
            path = f"/sys/class/power_supply/{ac}/online"
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        return f.read().strip() == "1"
                except Exception:
                    pass

        # Check sysfs battery discharge status fallback
        for b_name in ["BAT1", "BAT0"]:
            path = f"/sys/class/power_supply/{b_name}/status"
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        return f.read().strip().lower() != "discharging"
                except Exception:
                    pass
        return True

    # --- Display Refresh Rate (xrandr eDP-1) ---
    def get_refresh_rate(self):
        ok, out = self._run_cmd(["xrandr"])
        if ok:
            for line in out.splitlines():
                if "*" in line:
                    match = re.search(r"(\d+\.\d+)\*", line)
                    if match:
                        return float(match.group(1))
        return 144.0

    def set_refresh_rate(self, rate):
        rate_str = f"{float(rate):.2f}"
        cmd = ["xrandr", "--output", "eDP-1", "--mode", "1920x1080", "--rate", rate_str]
        ok, out = self._run_cmd(cmd)
        return ok, out

if __name__ == "__main__":
    b = AsusBackend()
    print("Backend ready. Plugged:", b.get_power_plugged_status(), "Refresh Rate:", b.get_refresh_rate())
