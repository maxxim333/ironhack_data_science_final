import subprocess
import sys
import time
import threading
from datetime import datetime
import string

# Function to install a package using pip
def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

# Check if pynput is installed and install if necessary
try:
    import pynput
except ImportError:
    print("pynput not found. Installing...")
    install_package('pynput')
    import pynput  # Re-import after installation

from pynput import keyboard

class KeyMonitor:
    def __init__(self, duration=1500):  # Set duration to 15 seconds
        self.key_press_times = {}
        self.last_key_time = None
        self.last_release_time = None
        self.last_key_type = None
        self.log_file = 'MAKSYM0000_2008.txt'  # File to write output to
        self.file = None  # File object to manage file operations
        self.duration = duration  # Duration to run the monitor in seconds
        self.stop_event = threading.Event()  # Event to signal stopping

    def setup_log_file(self):
        self.file = open(self.log_file, 'w')

    def log(self, message):
        if self.file:
            self.file.write(message + '\n')
            self.file.flush()  # Ensure that the data is written immediately

    def determine_key_type(self, key_char):
        # Define keys that correspond to "R", "S", and "L"
        r_keys = {'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'o', 'l', 'p', 'ç'}
        l_keys = {'q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g', 'z', 'x', 'c', 'v', 'b'}
        space_key = ''  # Space bar

        if key_char.lower() in r_keys:
            return 'R'
        elif key_char.lower() in l_keys:
            return 'L'
        else:
            return 'S'

    def on_press(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        current_time = time.time()
        self.key_press_times[key_char] = current_time

        # Capture time between keys and the key type for concatenation
        time_between_keys = (current_time - self.last_key_time) * 1000 if self.last_key_time is not None else 0
        time_between_release_and_press = (current_time - self.last_release_time) * 1000 if self.last_release_time is not None else 0
        key_type = self.determine_key_type(key_char)
        concatenated_key_type = (self.last_key_type or key_type) + key_type  # Concatenate last key type with current key type

        # Store the captured data to log on key release
        self.current_key_data = {
            'key_type': key_type,
            'concatenated_key_type': concatenated_key_type,
            'time_between_keys': time_between_keys,
            'time_between_release_and_press': time_between_release_and_press,
            'actual_key': key_char
        }

        self.last_key_time = current_time
        self.last_key_type = key_type

    def on_release(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        current_time = time.time()
        press_time = self.key_press_times.get(key_char, current_time)
        duration = (current_time - press_time) * 1000  # Duration in milliseconds
        date_today = datetime.now().strftime('%d%m%y')  # Format date as DDMMYY
        static_time_string = "10:10:10.111"

        # Log with tab-separated values, including the actual key
        self.log(f"MAKSYM0000\t{date_today}\t{static_time_string}\t"
                 f"{self.current_key_data['key_type']}\t{duration:.2f}\t"
                 f"{self.current_key_data['concatenated_key_type']}\t"
                 f"{self.current_key_data['time_between_keys']:.2f}\t"
                 f"{self.current_key_data['time_between_release_and_press']:.2f}\t"
                 f"{self.current_key_data['actual_key']}")

        self.last_release_time = current_time

        if key == keyboard.Key.esc:
            # Stop listener
            self.stop_event.set()
            return False

    def start(self):
        self.setup_log_file()

        # Set up a timer to stop the script after the specified duration
        timer = threading.Timer(self.duration, self.stop)
        timer.start()

        try:
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                self.stop_event.wait()  # Wait for stop event to be set
                listener.stop()  # Stop the listener if it's still running
        except KeyboardInterrupt:
            # Handle script interruption (Ctrl + C)
            print("\nScript interrupted. Saving results...")
        finally:
            if self.file:
                self.file.close()
                self.remove_first_row()  # Remove the first row after saving
                self.delete_invalid_rows()  # Delete invalid rows after logging
                print(f"Results saved to {self.log_file}")

    def remove_first_row(self):
        # Reopen the file to remove the first line
        with open(self.log_file, 'r') as file:
            lines = file.readlines()
        with open(self.log_file, 'w') as file:
            file.writelines(lines[1:])  # Write back all lines except the first one

    def delete_invalid_rows(self):
        # Reopen the file to read and filter the lines
        with open(self.log_file, 'r') as file:
            lines = file.readlines()

        # List to hold valid lines
        valid_lines = []
        skip_next = False

        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            columns = line.split('\t')
            last_column = columns[-1].strip()  # Get the last column and strip any whitespace

            if last_column.isalpha() or last_column == "Key.space" or last_column == " ":
                valid_lines.append(line)
            else:
                skip_next = True  # Mark the next line to be skipped

        # Write the filtered lines back to the file
        with open(self.log_file, 'w') as file:
            file.writelines(valid_lines)

    def stop(self):
        self.stop_event.set()
        print("\n15 seconds elapsed. Stopping the script...")

if __name__ == "__main__":
    monitor = KeyMonitor()
    monitor.start()
