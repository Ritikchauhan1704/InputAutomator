import pydirectinput as pdi
import time

LOG_FILE = "input_log.txt"

def parse_mouse_move(line):
    try:
        coords = line.split("moveTo (")[1].split(")")[0].split(",")
        x, y = int(coords[0].strip()), int(coords[1].strip())
        pdi.moveTo(x, y, duration=0.2)
    except Exception as e:
        print(f"Error parsing moveTo: {e}")

def parse_mouse_scroll(line):
    try:
        # Scroll not supported in pydirectinput, skip or handle separately
        pass
    except Exception as e:
        print(f"Error parsing scroll: {e}")

def parse_mouse_click(line):
    try:
        if "Button.left" in line:
            button = "left"
        elif "Button.right" in line:
            button = "right"
        else:
            print(f"Unknown button: {line}")
            return

        action = "down" if "Pressed" in line else "up"
        coords = line.split("at (")[1].split(")")[0].split(",")
        x, y = int(coords[0].strip()), int(coords[1].strip())

        pdi.moveTo(x, y, duration=0.1)

        if action == "down":
            pdi.mouseDown(button=button)
        else:
            pdi.mouseUp(button=button)
    except Exception as e:
        print(f"Error parsing click: {e}")

def parse_keyboard_press(line):
    try:
        key = line.split("[KEYBOARD]: ")[1].strip()
        if key.lower() in ("start", "done"):
            return
        pdi.press(key)
    except Exception as e:
        print(f"Error parsing keyboard: {e}")

def replay_actions():
    with open(LOG_FILE, "r") as f:
        for line in f:
            time.sleep(0.2)
            if "[MOUSE]" in line:
                if "moveTo" in line:
                    parse_mouse_move(line)
                elif "Pressed" in line or "Released" in line:
                    parse_mouse_click(line)
            elif "[KEYBOARD]" in line:
                parse_keyboard_press(line)

if __name__ == "__main__":
    print("Replaying actions from log...")
    time.sleep(2)
    replay_actions()
    print("Replay complete.")
