# Python script for both ARM64 and 64-bit Linux machines to emulate a Stream Deck using an Arduino
# Reads button signals ('U/u', 'L/l', 'D/d', 'R/r') via Serial
# Performs actions defined in a JSON config file (key press, commands, text, macros, URLs)

import serial
import time
import json
import os
import subprocess
import webbrowser
import threading
from pynput.keyboard import Controller, Key

# --- Configuration File Handling ---
CONFIG_FILE = 'arduino_streamdeck_config.json'
DEFAULT_CONFIG = {
  "serial_port": "/dev/ttyACM0", # Default, check yours with 'ls /dev/tty*'
  "baud_rate": 9600,
  "mappings": {
    "U": {"type": "key_press", "params": { "key": "up" }},
    "L": {"type": "key_press", "params": { "key": "left" }},
    "D": {"type": "key_press", "params": { "key": "down" }},
    "R": {"type": "key_press", "params": { "key": "right" }}
  },
   "examples": { # Add examples section to default
    "open_google": {"type": "open_url", "params": { "url": "https://google.com" }},
    "launch_terminal": {"type": "run_command", "params": { "command": "lxterminal" }},
    "type_hello": {"type": "type_text", "params": { "text": "Hello World!" }},
    "copy_paste_macro": {
       "type": "key_sequence",
       "params": {
          "sequence": [
             ["press", "ctrl_l"],["press", "c"],["release", "c"],["release", "ctrl_l"],
             ["delay", 0.1],
             ["press", "ctrl_l"],["press", "v"],["release", "v"],["release", "ctrl_l"]
           ]
       }
    }
   }
}

def load_or_create_config(filename):
    # ...(rest of the load_or_create_config function from previous answer)...
    if not os.path.exists(filename):
        print(f"Config file '{filename}' not found. Creating default.")
        try:
            with open(filename, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            print(f"Default config saved. Edit '{filename}' to customize actions.")
            return DEFAULT_CONFIG
        except IOError as e:
            print(f"Error creating default config: {e}. Using fallback.")
            return DEFAULT_CONFIG
    else:
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
                # Basic validation
                if not all(k in config for k in ['serial_port', 'baud_rate', 'mappings']):
                     raise ValueError("Config missing required keys.")
                print(f"Configuration loaded from '{filename}'.")
                return config
        except (IOError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config: {e}. Using fallback.")
            return DEFAULT_CONFIG


# --- Key String Translation ---
def translate_key_string(key_str):
    # ...(rest of the translate_key_string function from previous answer)...
    key_str = str(key_str).strip() # Ensure it's string and stripped
    if len(key_str) == 3 and key_str.startswith("'") and key_str.endswith("'"):
        return key_str[1]
    if len(key_str) == 1:
        return key_str
    try:
        # Handle special keys like shift_l, ctrl_r, etc.
        return getattr(Key, key_str)
    except AttributeError:
        print(f"Warning: Unknown key name '{key_str}'.")
        return None


# --- Action Execution Functions ---
keyboard = Controller() # Global keyboard controller

def execute_key_press(params, press_signal, active_presses):
    # ...(rest of the execute_key_press function from previous answer)...
    key_string = params.get("key")
    if not key_string:
        print("Error: 'key_press' action missing 'key' parameter.")
        return
    pynput_key = translate_key_string(key_string)
    if pynput_key:
        try:
            keyboard.press(pynput_key)
            active_presses[press_signal] = pynput_key # Track for release
            # print(f"Pressed: {pynput_key}") # Debug
        except Exception as e:
            print(f"Error pressing key {pynput_key}: {e}")


def execute_type_text(params):
    # ...(rest of the execute_type_text function from previous answer)...
    text_to_type = params.get("text")
    if text_to_type is not None:
        try:
            # print(f"Typing: {text_to_type}") # Debug
            keyboard.type(text_to_type)
        except Exception as e:
            print(f"Error typing text: {e}")
    else:
        print("Error: 'type_text' action missing 'text' parameter.")


def execute_run_command(params):
    # ...(rest of the execute_run_command function from previous answer)...
    command = params.get("command")
    if command:
        try:
            # print(f"Running command: {command}") # Debug
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        except Exception as e:
            print(f"Error running command '{command}': {e}")
    else:
        print("Error: 'run_command' action missing 'command' parameter.")


def execute_open_url(params):
    # ...(rest of the execute_open_url function from previous answer)...
    url = params.get("url")
    if url:
        try:
            # print(f"Opening URL: {url}") # Debug
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL '{url}': {e}")
    else:
         print("Error: 'open_url' action missing 'url' parameter.")


def execute_key_sequence(params):
    # ...(rest of the execute_key_sequence function from previous answer)...
    sequence = params.get("sequence")
    if not isinstance(sequence, list):
        print("Error: 'key_sequence' action 'sequence' parameter must be a list.")
        return

    # print("Executing sequence...") # Debug
    for action_item in sequence:
        if not isinstance(action_item, list) or len(action_item) != 2:
            print(f"Warning: Invalid item in sequence: {action_item}. Skipping.")
            continue

        action, value = action_item
        try:
            if action == "press":
                key = translate_key_string(value)
                if key: keyboard.press(key)
            elif action == "release":
                key = translate_key_string(value)
                if key: keyboard.release(key)
            elif action == "type":
                 keyboard.type(str(value)) # Ensure value is string
            elif action == "delay":
                time.sleep(float(value))
            else:
                print(f"Warning: Unknown action '{action}' in sequence. Skipping.")
        except Exception as e:
            print(f"Error during sequence action {action_item}: {e}")
            # break # Optional: Stop sequence on error


# --- Main Application Logic ---
if __name__ == "__main__":
    # ...(rest of the main execution block from previous answer)...
    config = load_or_create_config(CONFIG_FILE)
    SERIAL_PORT = config['serial_port']
    BAUD_RATE = config['baud_rate']
    mappings = config.get('mappings', {})

    print("--- Arduino StreamDeck Emulator ---")
    print(f"Monitoring {SERIAL_PORT} at {BAUD_RATE} baud.")
    print(f"Loaded {len(mappings)} mappings.")

    ser = None
    active_presses = {}
    release_signal_map = {s.lower(): s for s in mappings.keys()}

    try:
        while True:
            try:
                if ser is None or not ser.is_open:
                    # print("Attempting serial connection...") # Reduce noise
                    try:
                         ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                         ser.flushInput()
                         print(f"Serial connection successful on {SERIAL_PORT}.")
                         time.sleep(0.5)
                    except serial.SerialException as serial_err:
                         # Don't print stack trace here, handle in outer loop
                         raise serial_err # Re-raise to be caught below

                if ser.in_waiting > 0:
                    serial_byte = ser.read(1)
                    try:
                        data = serial_byte.decode('utf-8')
                        # print(f"Received: {data}") # Debug Raw Signal
                    except UnicodeDecodeError:
                        continue # Ignore weird bytes

                    # --- Handle PRESS Signals ---
                    if data in mappings:
                        action_config = mappings[data]
                        action_type = action_config.get("type")
                        params = action_config.get("params", {})
                        press_signal = data

                        if press_signal in active_presses: continue

                        # print(f"Executing action for {press_signal}: {action_type}") # Debug

                        thread = None
                        if action_type == "key_press":
                           execute_key_press(params, press_signal, active_presses)
                        elif action_type == "type_text":
                            thread = threading.Thread(target=execute_type_text, args=(params,))
                        elif action_type == "run_command":
                            thread = threading.Thread(target=execute_run_command, args=(params,))
                        elif action_type == "open_url":
                             thread = threading.Thread(target=execute_open_url, args=(params,))
                        elif action_type == "key_sequence":
                            thread = threading.Thread(target=execute_key_sequence, args=(params,))
                        else:
                            print(f"Warning: Unknown action type '{action_type}' for signal '{press_signal}'.")

                        if thread:
                            thread.daemon = True
                            thread.start()

                    # --- Handle RELEASE Signals (Only for active 'key_press' actions) ---
                    elif data in release_signal_map:
                        press_signal = release_signal_map[data]
                        if press_signal in active_presses:
                            pynput_key = active_presses[press_signal]
                            try:
                                keyboard.release(pynput_key)
                                # print(f"Released: {pynput_key}") # Debug
                            except Exception as e:
                                print(f"Error releasing key {pynput_key}: {e}")
                            finally:
                                 del active_presses[press_signal]

                elif not ser.is_open: # Check if port closed unexpectedly
                     raise serial.SerialException("Serial port closed.")

            except serial.SerialException as e:
                # Avoid printing stack trace for common connection errors
                if "FileNotFoundError" in str(e):
                    print(f"Serial port {SERIAL_PORT} not found. Check connection and config.")
                elif "PermissionError" in str(e):
                    print(f"Permission denied for {SERIAL_PORT}. Try 'sudo' or check 'dialout' group.")
                else:
                    print(f"Serial error: {e}")

                if ser and ser.is_open: ser.close()
                ser = None
                if active_presses: # Release keys if disconnected
                    # print("Releasing keys due to serial disconnect...")
                    for key in list(active_presses.values()):
                        try: keyboard.release(key)
                        except: pass # Ignore errors here
                    active_presses.clear()
                print("Attempting reconnect in 5 seconds...")
                time.sleep(5)
            except KeyboardInterrupt:
                print("\nExiting script.")
                break
            except Exception as e:
                import traceback
                print(f"An unexpected error occurred:")
                traceback.print_exc() # Print full trace for unexpected errors
                time.sleep(1)

    finally: # Cleanup on exit
        if ser and ser.is_open: ser.close(); print("Serial port closed.")
        if active_presses:
            print("Releasing any potentially stuck keys on exit...")
            for key in list(active_presses.values()):
                 try: keyboard.release(key)
                 except: pass
            active_presses.clear()
        print("Cleanup complete.")
