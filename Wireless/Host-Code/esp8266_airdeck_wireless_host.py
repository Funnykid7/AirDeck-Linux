import socket
import json
import subprocess
import webbrowser
from pynput.keyboard import Controller, Key

keyboard = Controller()    

CONFIG_FILE = 'arduino_streamdeck_config.json'
UDP_IP = "0.0.0.0" # Listens on all available network interfaces
UDP_PORT = 4210

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found. Please create it.")
        exit(1)

def execute_action(action):
    if not action: return

    action_type = action.get("type")
    value = action.get("value")

    if action_type == "command":
        # Runs a shell command
        subprocess.Popen(value, shell=True)
        
    elif action_type == "text":
        # Types out a string
        keyboard.type(value)
        
    elif action_type == "website":
        # Opens a URL in the default browser
        webbrowser.open(value)
        
    elif action_type == "key":
        # Presses a specific key
        key_map = {
            "space": Key.space, "enter": Key.enter, "esc": Key.esc,
            "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right
        }
        if value in key_map:
            keyboard.press(key_map[value])
            keyboard.release(key_map[value])
        else:
            keyboard.press(value)
            keyboard.release(value)

def main():
    config = load_config()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for ESP8266 commands on UDP port {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        char = data.decode('utf-8').strip()
        
        # We trigger actions on the uppercase (Button Press) characters
        if char in config:
            print(f"Action triggered by button {char}")
            execute_action(config[char])

if __name__ == "__main__":
    main()