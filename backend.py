oimport subprocess
import re
import os
import psutil
import logging
from typing import Tuple, Dict, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.config/asus-tuf-gui.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants for power limits
class PowerLimits:
    # Silent Mode
    SILENT_PL1 = 35
    SILENT_PL2 = 45
    SILENT_DYNAMIC_BOOST = 5
    SILENT_FPS = 40
    
    # Performance Mode
    PERF_PL1 = 65
    PERF_PL2 = 90
    PERF_DYNAMIC_BOOST = 10
    PERF_FPS = 60
    
    # Turbo Mode
    TURBO_PL1 = 90
    TURBO_PL2 = 135
    TURBO_DYNAMIC_BOOST = 15
    TURBO_FPS = 0  # Unlimited
    
    # Validation ranges
    PL1_MIN = 28
    PL1_MAX = 90
    PL2_MIN = 28
    PL2_MAX = 135
    DYNAMIC_BOOST_MIN = 5
    DYNAMIC_BOOST_MAX = 15
    BATTERY_LIMIT_MIN = 20
    BATTERY_LIMIT_MAX = 100
    FPS_VALID_VALUES = [0, 40, 60, 90, 120, 144, 165, 240]

class AsusBackend:
    def __init__(self):
        """Initialize backend and verify required tools are installed."""
        self._verify_dependencies()
        logger.info("AsusBackend initialized successfully")
    
    def _verify_dependencies(self) -> None:
        """Check if required system tools are available."""
        required_tools = ['asusctl', 'supergfxctl']
        optional_tools = ['nvidia-smi', 'powerprofilesctl']
        
        for tool in required_tools:
            if not self._command_exists(tool):
                logger.error(f"Required tool '{tool}' not found in PATH")
                raise RuntimeError(f"Required dependency '{tool}' is not installed")
        
        for tool in optional_tools:
            if not self._command_exists(tool):
                logger.warning(f"Optional tool '{tool}' not found - some features may not work")
    
    @staticmethod
    def _command_exists(cmd: str) -> bool:
        """Check if a command exists in PATH."""
        return subprocess.run(['which', cmd], capture_output=True).returncode == 0
    
    @staticmethod
    def _run_cmd(cmd: list, timeout: int = 5) -> Tuple[bool, str]:
        """Execute a system command and return success status and output."""
        try:
            logger.debug(f"Executing command: {' '.join(cmd)}")
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            success = res.returncode == 0
            output = res.stdout + res.stderr
            
            if not success:
                logger.warning(f"Command failed: {' '.join(cmd)} - {output}")
            
            return success, output
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            return False, f"Command timed out after {timeout} seconds"
        except FileNotFoundError:
            logger.error(f"Command not found: {cmd[0]}")
            return False, f"Command '{cmd[0]}' not found"
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return False, str(e)
    
    @staticmethod
    def _update_config_file(file_path: str, key: str, value: str, separator: str = "=") -> Tuple[bool, str]:
        """Generic helper to update key-value config files."""
        try:
            path = Path(file_path).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            
            content = ""
            if path.exists():
                content = path.read_text()
            
            pattern = rf"{re.escape(key)}\s*{re.escape(separator)}\s*[^\n]*"
            new_line = f"{key}{separator}{value}"
            
            if re.search(pattern, content):
                content = re.sub(pattern, new_line, content)
            else:
                content += f"\n{new_line}\n"
            
            path.write_text(content)
            logger.info(f"Updated {file_path}: {key}{separator}{value}")
            return True, f"Updated {key} to {value}"
        except Exception as e:
            logger.error(f"Failed to update config file {file_path}: {e}")
            return False, str(e)
    
    @staticmethod
    def _validate_range(value: int, min_val: int, max_val: int, param_name: str) -> None:
        """Validate that a value is within an acceptable range."""
        if not isinstance(value, int):
            raise ValueError(f"{param_name} must be an integer, got {type(value).__name__}")
        if not min_val <= value <= max_val:
            raise ValueError(f"{param_name} must be between {min_val} and {max_val}, got {value}")

    # --- FPS Limiter (WhisperMode 2.0 via DXVK & MangoHud) ---
    def set_fps_limit(self, limit: int) -> Tuple[bool, str]:
        """Set FPS limit for games via MangoHud and DXVK configs."""
        try:
            if limit not in PowerLimits.FPS_VALID_VALUES:
                logger.warning(f"Unusual FPS limit value: {limit}")
            
            # 1. MangoHud config
            mh_path = "~/.config/MangoHud/MangoHud.conf"
            ok1, msg1 = self._update_config_file(mh_path, "fps_limit", str(limit))
            
            # 2. DXVK config (for Proton / DXVK games)
            dxvk_path = "~/.config/dxvk.conf"
            ok2, msg2 = self._update_config_file(dxvk_path, "dxvk.maxFrameRate", str(limit), " = ")
            
            if ok1 and ok2:
                logger.info(f"FPS limit set to {limit if limit > 0 else 'unlimited'}")
                return True, f"FPS limit set to {limit if limit > 0 else 'unlimited'} in MangoHud and DXVK"
            else:
                errors = [msg for ok, msg in [(ok1, msg1), (ok2, msg2)] if not ok]
                return False, "; ".join(errors)
        except Exception as e:
            logger.error(f"Failed to set FPS limit: {e}")or:
            logger.error(f"Command not found: {cmd[0]}")
            return False, f"Command '{cmd[0]}' not found"
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return False, str(e)
    
    @staticmethod
    def _update_config_file(file_path: str, key: str, value: str, separator: str = "=") -> Tuple[bool, str]:
        """Generic helper to update key-value config files."""
        try:
            path = Path(file_path).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            
            content = ""
            if path.exists():
                content = path.read_text()
            
            pattern = rf"{re.escape(key)}\s*{re.escape(separator)}\s*[^\n]*"
            new_line = f"{key}{separator}{value}"
            
            if re.search(pattern, content):
                content = re.sub(pattern, new_line, content)
            else:
                content += f"\n{new_line}\n"
            
            path.write_text(content)
            logger.info(f"Updated {file_path}: {key}{separator}{value}")
            return True, f"Updated {key} to {value}"
        except Exception as e:
            logger.error(f"Failed to update config file {file_path}: {e}")
            return False, str(e)
    
    @staticmethod
    def _validate_range(value: int, min_val: int, max_val: int, param_name: str) -> None:
        """Validate that a value is within an acceptable range."""
        if not isinstance(value, int):
            raise ValueError(f"{param_name} must be an integer, got {type(value).__name__}")
        if not min_val <= value <= max_val:
            raise ValueError(f"{param_name} must be between {min_val} and {max_val}, got {value}")

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
            pass -> int:
        """Get current FPS limit from MangoHud config."""
        mh_path = Path("~/.config/MangoHud/MangoHud.conf").expanduser()
        try:
            if mh_path.exists():: str, fps_override: Optional[int] = None) -> Tuple[bool, str]:
        """Apply a preset operating mode (Silent, Performance, Turbo, or Manual)."""
        mode = mode_name.lower()
        
        try:
            if mode == "silent":
                self.set_profile("Quiet")
                self.set_cpu_pl1(PowerLimits.SILENT_PL1)
                self.set_cpu_pl2(PowerLimits.SILENT_PL2)
                self.set_nv_dynamic_boost(PowerLimits.SILENT_DYNAMIC_BOOST)
                fps_val = PowerLimits.SILENT_FPS if fps_override is None else fps_override
                self.set_fps_limit(fps_val)
                logger.info(f"Silent Mode applied with {fps_val} FPS cap")
                return True, f"Silent Mode applied (PL1 {PowerLimits.SILENT_PL1}W, Dynamic Boost {PowerLimits.SILENT_DYNAMIC_BOOST}W, WhisperMode {fps_val} FPS Cap)."
            
            elif mode == "performance":
                self.set_profile("Balanced")
                self.set_cpu_pl1(PowerLimits.PERF_PL1)
                self.set_cpu_pl2(PowerLimits.PERF_PL2)
                self.set_nv_dynamic_boost(PowerLimits.PERF_DYNAMIC_BOOST)
                fps_val = PowerLimits.PERF_FPS if fps_override is None else fps_override
                self.set_fps_limit(fps_val)
                logger.info(f"Performance Mode applied with {fps_val} FPS cap")
                return True, f"Performance Mode applied (Balanced power, {fps_val if fps_val > 0 else 'Unlimited'} FPS)."
            
            elif mode == "turbo":
                self.set_profile("Turbo")
                self.set_cpu_pl1(PowerLimits.TURBO_PL1)
                self.set_cpu_pl2(PowerLimits.TURBO_PL2)
                self.set_nv_dynamic_boost(PowerLimits.TURBO_DYNAMIC_BOOST)
                fps_val = PowerLimits.TURBO_FPS if fps_override is None else fps_override
                self.set_fps_limit(fps_val)
                logger.in -> str:
        """Get current performance profile."""
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
        logger.warning("Could not determine profile, defaulting to Balanced")
        return "Balanced"

    def set_profile(self, profile: str) -> Tuple[bool, str]:
        """Set performance profile and sync with GNOME power profiles."""
        ok, out = self._run_cmd(["asusctl", "profile", "-P", profile])
        
        # Sync with GNOME power profiles if available
        if self._command_exists('powerprofilesctl'):
            gnome_mode = "balanced"
            if profile.lower() in ["quiet", "silent"]:
                gnome_mode = "power-saver"
            elif profile.l -> str:
        """Get current GPU mode."""
        ok, out = self._run_cmd(["supergfxctl", "-g"])
        if ok:
            lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
            if lines:
                return lines[-1].capitalize()
        logger.warning("Could not determine GPU mode, defaulting to Hybrid")
        return "Hybrid"

    def set_gpu_mode(self, mode: str) -> Tuple[bool, str]:
        """Set GPU mode (Integrated, Hybrid, or AsusMuxDgpu)."""
        valid_modes = ["Integrated", "Hybrid", "AsusMuxDgpu"]
        if mode not in valid_modes:
            logger.error(f"Invalid GPU mode: {mode}")
            return False, f"Invalid GPU mode. Must be one of: {', '.join(valid_modes)}"
        
        ok, out = self._run_cmd(["supergfxctl", "-m", mode])
        if ok:
            logger.info(f"GPU mode set to {mode}")
        return ok, out

    def get_gpu_pending_action(self) -> str:
        """Get pending GPU mode change action."""-1].strip().capitalize()
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

    # --- GPU Mode (supergfxctl -> int:
        """Get current battery charge limit."""
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok:
            match = re.search(r"ChargeControlEndThreshold.*?(\d+)", out)
            if match:
                return int(match.group(1))
        
        # Fallback to sysfs
        try:
            bat_path = Path("/sys/class/power_supply/BAT0/charge_control_end_threshold")
            if bat_path.exists():
                return int(bat_path.read_text().strip())
        except Exception as e:
            logger.warning(f"Could not read battery limit from sysfs: {e}")
        
        logger.warning("Could not determine battery limit, defaulting to 80")
        return 80

    def set_battery_limit(self, limit: int) -> Tuple[bool, str]:
        """Set battery charge limit threshold."""
        try:
            self._validate_range(limit, PowerLimits.BATTERY_LIMIT_MIN, 
                               PowerLimits.BATTERY_LIMIT_MAX, "Battery limit")
            
            ok, out = self._run_cmd(["asusctl", "-c", str(limit)])
            if ok:
                logger.info(f"Battery charge limit set to {limit}%")
            return ok, out
        except ValueError as e:
            logger.error(f"Invalid battery limit: {e}")
            return False, str(e)
            return out.strip()
        return "None"

    # --- Battery Charge Limit ---
    def get_battery_limit(self):
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok: -> str:
        """Get current keyboard backlight brightness level."""
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok:
            match = re.search(r"Keyboard Brightness.*?([A-Za-z]+)", out, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        
        # Fallback to sysfs
        try:
            kbd_path = Path("/sys/class/leds/asus::kbd_backlight/brightness")
            if kbd_path.exists():
                val = int(kbd_path.read_text().strip())
                mapping = {0: "Off", 1: "Low", 2: "Med", 3: "High"}
                return mapping.get(val, "Low")
        except Exception as e:
            logger.warning(f"Could not read keyboard brightness: {e}")
        
        return "Low"

    def set_kbd_brightness(self, level: str) -> Tuple[bool, str]:
        """Set keyboard backlight brightness level."""
        valid_levels = ["Off", "Low", "Med", "High"]
        if level not in valid_levels:
            logger.error(f"Invalid brightness level: {level}")
            return False, f"Invalid level. Must be one of: {', '.join(valid_levels)}"
        
        ok, out = self._run_cmd(["asusctl", "-k", level.lower()])
        if ok:
            logger.info(f"Keyboard brightness set to {level}"
        ok, out = self._run_cmd(["asusctl", "-s"])
        if ok:
            match = re.search(r"Keyboard Brightness.*?([A-Za-z]+)", out, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        try:
            with open("/sys/clas: str, color_hex: str = "FF0000", speed: str = "med") -> Tuple[bool, str]:
        """Set Aura RGB lighting mode and color."""
        mode_lower = mode.lower()
        valid_speeds = ["low", "med", "high"]
        
        if speed not in valid_speeds:
            logger.warning(f"Invalid speed '{speed}', defaulting to 'med'")
            speed = "med"
        
        # Validate hex color
        if not re.match(r'^[0-9A-Fa-f]{6}$', color_hex):
            logger.error(f"Invalid color hex: {color_hex}")
            return False, "Invalid color format. Use 6-digit hex (e.g., FF0000)"
        
        if mode_lower == "static":
            cmd = ["asusctl", "aura", "static", "-c", color_hex]
        elif mode_lower == "breathe":
            cmd = ["asusctl", "aura", "breathe", "-c", color_hex, "-s", speed]
        elif mode_lower in ["rainbowcycle", "rainbow-cycle"]:
            cmd = ["asusctl", "aur -> Dict[str, Any]:
        """Get current Armoury Crate hardware settings."""", "rainbow-cycle", "-s", speed]
        elif mode_lower in ["rainbowwave", "rainbow-wave"]:
            cmd = ["asusctl", "aura", "rainbow-wave", "-s", speed]
        elif mode_lower == "pulse":
            cmd = ["asusctl", "aura", "pulse", "-c", color_hex, "-s", speed]
        else:
            cmd = ["asusctl", "aura", mode_lower]
        
        ok, out = self._run_cmd(cmd)
        if ok:
            logger.info(f"Aura mode set to {mode}"
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
: int) -> Tuple[bool, str]:
        """Set NVIDIA Dynamic Boost wattage."""
        try:
            self._validate_range(watts, PowerLimits.DYNAMIC_BOOST_MIN, 
                               PowerLimits.DYNAMIC_BOOST_MAX, "Dynamic Boost")
            return self.set_armoury_setting("nv_dynamic_boost", watts)
        except ValueError as e:
            logger.error(f"Invalid Dynamic Boost value: {e}")
            return False, str(e)

    def set_cpu_pl1(self, watts: int) -> Tuple[bool, str]:
        """Set CPU PL1 sustained power limit."""
        try:
            self._validate_range(watts, PowerLimits.PL1_MIN, PowerLimits.PL1_MAX, "CPU PL1")
            return self.set_armoury_setting("ppt_pl1_spl", watts)
        except ValueError as e:: str, value: int) -> Tuple[bool, str]:
        """Set an Armoury Crate hardware parameter."""
        ok, out = self._run_cmd(["asusctl", "armoury", name, str(value)])
        if ok:
            logger.info(f"Armoury setting {name} set to {value}"
            return False, str(e)

    def set_cpu_pl2(self, watts: int) -> Tuple[bool, str]:
        """Set CPU PL2 burst power limit."""
        try:
            self._validate_range(watts, PowerLimits.PL2_MIN, PowerLimits.PL2_MAX, "CPU PL2")
            return self.set_armoury_setting("ppt_pl2_sppt", watts)
        except ValueError as e:
            logger.error(f"Invalid PL2 value: {e}")
            return False, str(e)

    def set_panel_overdrive(self, enabled: bool) -> Tuple[bool, str]:
        """Enable or disable panel overdrive for reduced input lag."""
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

    def set_armoury_settin -> Dict[str, str]:
        """Get NVIDIA GPU temperature and power information."""
        if not self._command_exists('nvidia-smi'):
            return {"temp": "N/A", "power_draw": "N/A", "power_limit": "N/A"}
        
        cmd = ["nvidia-smi", "--query-gpu=temperature.gpu,power.draw,power.limit", "--format=csv,noheader,nounits"]
        ok, out = self._run_cmd(cmd)
        temp, power_draw, power_limit = "N/A", "N/A", "N/A
    def set_nv_dynamic_boost(self, watts):
        return self.set_armoury_setting("nv_dynamic_boost", watts)

    def set_cpu_pl1(self, watts):
        return self.set_armoury_setting("ppt_pl1_spl", watts)

    def set_cpu_pl2(self, watts):
        return self.set_armoury_setting("ppt_pl2_sppt", watts)

    def set_panel_overdrive(self, enabled):
        val = 1 if enabled else 0
        return self.set_armoury_setting("panel_overdrive", val)
 -> Dict[str, Any]:
        """Get real-time system telemetry (CPU, GPU, RAM, battery)."""
        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        mem_pct = mem.percent

        cpu_temp = "N/A"
        try:
            temps = psutil.sensors_temperatures()
            # Try different sensor names in order of preference
            for sensor_name in ["k10temp", "coretemp", "acpitz"]:
                if sensor_name in temps and temps[sensor_name]:
                    cpu_temp = f"{temps[sensor_name][0].current:.1f} °C"
                    break
            else:
                # If none of the known sensors found, use first available
                if temps:
                    for key, entries in temps.items():
                        if entries:
                            cpu_temp = f"{entries[0].current:.1f} °C"
                            break
        except AttributeError:
            logger.debug("Sensor temperatures not available on this system")
        except Exception as e:
            logger.warning(f"Failed to read CPU temperature: {e}")

        gpu_info = self.get_gpu_info()
        gpu_temp = f"{gpu_info['temp']} °C" if gpu_info['temp'] != "N/A" else "N/A"

        bat_pct = "N/A"
        try:
            bat = psutil.sensors_battery()
            if bat:
                bat_pct = f"{int(bat.percent)}%"
        except AttributeError:
            logger.debug("Battery sensor not available on this system")
        except Exception as e:
            logger.warning(f"Failed to read battery status: {e}")

        return {
            "cpu_usage": cpu_pct,
            "mem_usage": mem_pct,
            "cpu_temp": cpu_temp,
            "gpu_temp": gpu_temp,
            "gpu_power": f"{gpu_info['power_draw']} W" if gpu_info['power_draw'] != "N/A" else "N/A",
            "battery_pct": bat_pct
        }

if __name__ == "__main__":
    try:
        b = AsusBackend()
        print("Backend ready.")
        print(f"Current profile: {b.get_profile()}")
        print(f"GPU mode: {b.get_gpu_mode()}")
        print(f"Battery limit: {b.get_battery_limit()}%")
        print(f"Telemetry: {b.get_telemetry()}")
    except Exception as e:
        logger.error(f"Backend initialization failed: {e}")
        print(f"Error: {e}et_gpu_info()
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
            "battery_pct": bat_pct
        }

if __name__ == "__main__":
    b = AsusBackend()
    print("Backend ready.")
