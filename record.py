from pynput import keyboard, mouse
import threading
import time

LOG_FILE = "input_log.txt"

with open(LOG_FILE, "w") as f:
    f.truncate(0)

typed_chars = []
started = False
last_move = None
move_lock = threading.Lock()
move_timer = None
move_delay = 0.5  # Seconds to wait before logging last move
from pynput.keyboard import Key

SPECIAL_KEY_MAP = {
    Key.cmd: "win",
    Key.ctrl_l: "ctrl",
    Key.ctrl_r: "ctrl",
    Key.alt_l: "alt",
    Key.alt_r: "alt",
    Key.enter: "enter",
    Key.space: "space",
    Key.tab: "tab",
    Key.esc: "esc",
    Key.shift: "shift",
    Key.shift_l: "shift",
    Key.shift_r: "shift",
    Key.backspace: "backspace",
    Key.delete: "delete",
    Key.up: "up",
    Key.down: "down",
    Key.left: "left",
    Key.right: "right",
    Key.caps_lock: "capslock",
    Key.media_volume_up: "volumeup",
    Key.media_volume_down: "volumedown",
    Key.media_volume_mute: "volumemute",
    # Add more as needed
}

def log_event(event_str):
    with open(LOG_FILE, "a") as f:
        f.write(f"{event_str}\n")

def check_for_sequence(seq: str):
    return ''.join(typed_chars[-len(seq):]).lower() == seq

def flush_last_move():
    global last_move
    with move_lock:
        if last_move and started:
            x, y = last_move
            log_event(f"[MOUSE] moveTo ({x}, {y})")
            last_move = None

def on_key_press(key):
    global started

    try:
        # Normal character
        char = key.char
        typed_chars.append(char)
        if len(typed_chars) > 20:
            del typed_chars[:-20]

        if not started and check_for_sequence("start"):
            print("You typed 'start'. Now logging input...")
            started = True
            remove_last_n_keyboard_entries(5)
            return

        if started and check_for_sequence("done"):
            print("You typed 'done'. Exiting.")
            remove_last_n_keyboard_entries(4)
            keyboard_listener.stop()
            mouse_listener.stop()
            return

        if started:
            log_event(f"[KEYBOARD]: {char}")

    except AttributeError:
        key_name = SPECIAL_KEY_MAP.get(key, str(key).replace("Key.", ""))
        typed_chars.append(key_name[0] if key_name else "?")

        if len(typed_chars) > 20:
            del typed_chars[:-20]

        if not started and check_for_sequence("start"):
            print("You typed 'start'. Now logging input...")
            started = True
            remove_last_n_keyboard_entries(5)
            return

        if started and check_for_sequence("done"):
            print("You typed 'done'. Exiting.")
            remove_last_n_keyboard_entries(4)
            keyboard_listener.stop()
            mouse_listener.stop()
            return

        if started:
            log_event(f"[KEYBOARD]: {key_name}")

def on_click(x, y, button, pressed):
    flush_last_move()
    if started:
        action = "Pressed" if pressed else "Released"
        log_event(f"[MOUSE] {action} {button} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    flush_last_move()
    if started:
        log_event(f"[MOUSE] scroll ({x}, {y}) by ({dx}, {dy})")

def on_move(x, y):
    global last_move, move_timer

    if not started:
        return

    with move_lock:
        if last_move is None:
            log_event(f"[MOUSE] moveTo ({x}, {y})")  # First move
        last_move = (x, y)

        # Cancel and reset the timer
        if move_timer:
            move_timer.cancel()
        move_timer = threading.Timer(move_delay, flush_last_move)
        move_timer.start()

def remove_last_n_keyboard_entries(n):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        new_lines = []
        removed = 0
        for line in reversed(lines):
            if removed >= n:
                new_lines.insert(0, line)
            elif line.startswith("[KEYBOARD]: ") and len(line.strip()) <= 14:
                removed += 1
            else:
                new_lines.insert(0, line)
        with open(LOG_FILE, "w") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"Error cleaning log: {e}")

# Set up listeners
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

print(f"Waiting for 'start'... Then listening to input. Type 'done' to exit.")
keyboard_listener.join()
mouse_listener.join()
