# AirDeck: Wireless & Wired Macro Pad for Linux

**AirDeck** is a lightweight, open-source tool that transforms microcontrollers into powerful, customizable macro pads. Map physical button presses to complex Linux actions like running shell commands, system power controls, automated typing, or web shortcuts.

Whether you want a wired connection via an **Arduino Uno** or a wireless setup using an **ESP8266**, AirDeck provides a simple Python-based bridge to automate your workflow.

## Key Features
* **Dual Mode Support:** Use a wired **Arduino** (Serial) or a wireless **ESP8266** (UDP over Wi-Fi).
* **Shell Commands:** Trigger scripts or system commands (e.g., `systemctl reboot` or `apt update`).
* **Automated Typing:** Send strings of text or code snippets to your active window.
* **Key Emulation:** Map buttons to single keys (e.g., `Space`, `Enter`, `F5`).
* **Web Shortcuts:** Launch specific URLs in your default browser instantly.
* **Background Service:** Compatible with `systemd` to run as a persistent background task.

---

## Hardware Requirements

| Component | Wired Setup (Arduino) | Wireless Setup (ESP8266) |
|---|---|---|
| **Controller** | Arduino Uno, Nano, or Mega | NodeMCU, D1 Mini, or ESP-12 |
| **Buttons** | 4x Tactile Push Buttons | 4x Tactile Push Buttons |
| **Connection** | USB Cable (Type A to B) | Wi-Fi Network |
| **Power** | Powered via USB | USB or 3.3V Battery |

---

## Hardware Setup

### Wiring
1. **Buttons:** Place four tactile buttons on a breadboard.
2. **Ground:** Connect one leg of all buttons to a common **GND** rail. Connect this rail to the `GND` pin on your controller.
3. **Signal:** Connect the other leg of each button to the pins below:

| Button | Arduino Pin | ESP8266 Pin | Action Key (JSON) |
|---|:---:|:---:|:---:|
| Button 1 | Pin 2 | D1 | **U** |
| Button 2 | Pin 3 | D2 | **L** |
| Button 3 | Pin 4 | D3 | **D** |
| Button 4 | Pin 5 | D4 | **R** |

> **Note:** Internal pull-up resistors are enabled in the firmware, so **no external resistors are required**.

---

## Software Setup

### 1. Display Server (X11 vs Wayland)
* **X11 (Recommended):** Full functionality. All features, including key emulation and automated typing, work perfectly.
* **Wayland:** Supported for **Shell Commands** and **Websites**. However, Wayland's security model may block `pynput` from injecting keystrokes into certain applications.

### 2. Controller Firmware
* **Arduino:** Upload the sketch in `/Wired/Arduino-Code` via Arduino IDE.
* **ESP8266:** Update the `ssid`, `password`, and `targetIP` (your computers IP) in `/ESP8266-Code` and upload.

### 3. Receiver Installation
1. Install Python dependencies:
   ```bash
   pip install pynput pyserial
   ```
2. Download the Python scripts and either `arduino_airdeck_wired_config.json` or `esp8266_airdeck_wireless_host.py` depending on your requirements, to the same folder.
3. **Run the script:**
   * For Wired: `arduino_airdeck_wired.py`
   * For Wireless: `esp8266_airdeck_wireless_host.py`

---

## Customizing Your Macros
The `.json` file is where you map buttons to actions. 

### Action Types
| Type | Function | Example Value |
|---|---|---|
| `command` | Runs a terminal command | `"systemctl reboot"` |
| `website` | Opens a URL | `"https://github.com"` |
| `text` | Types text into active window | `"sudo apt update"` |
| `key` | Presses a keyboard key | `"space"`, `"enter"`, `"up"` |

### Example Configuration
```json
{
    "U": {
        "type": "command",
        "value": "systemctl poweroff"
    },
    "L": {
        "type": "website",
        "value": "[https://github.com](https://github.com)"
    },
    "D": {
        "type": "command",
        "value": "x-terminal-emulator -e bash -c 'sudo apt update && sudo apt upgrade; exec bash'"
    },
    "R": {
        "type": "key",
        "value": "space"
    }
}
```

---

## Autostart on Boot (Systemd)
To make AirDeck run automatically on every boot:
1. Create a service file: `sudo nano /etc/systemd/system/airdeck.service`
2. Paste the service configuration. **Important:** Ensure `ExecStart` and `WorkingDirectory` point to your actual folder.
3. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable airdeck.service
   sudo systemctl start airdeck.service
   ```
