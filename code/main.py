import board
import usb_hid
import time
import digitalio
import pwmio
from adafruit_hid import keyboard, keyboard_layout_us
from adafruit_hid.keycode import Keycode


DEFAULT_SCRIPT = "main.script"


keyboard = keyboard.Keyboard(usb_hid.devices)
layout = keyboard_layout_us.KeyboardLayoutUS(keyboard)
button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN
rgb_r = pwmio.PWMOut(board.GP25)
rgb_g = pwmio.PWMOut(board.GP23)
rgb_b = pwmio.PWMOut(board.GP24)


def string(text):
    layout.write(text)


def press(*keys):
    keyboard.press(*keys)
    time.sleep(0.01)
    keyboard.release(*keys)


def keydown(*keys):
    keyboard.press(*keys)


def keyup(*keys):
    keyboard.release(*keys)


def allup():
    keyboard.release_all()


def sleep(seconds):
    time.sleep(seconds)


def wait_for_button():
    while not button.value:
        time.sleep(0.01)


def set_rgb(r, g, b):
    assert 0<=r<=255 and 0<=g<=255 and 0<=b<=255
    rgb_r.duty_cycle = int((r/255) * 65535)
    rgb_g.duty_cycle = int((g/255) * 65535)
    rgb_b.duty_cycle = int((b/255) * 65535)


RUN_GLOBALS = {
    "string": string,
    "press": press,
    "keydown": keydown,
    "keyup": keyup,
    "allup": allup,
    "sleep": sleep,
    "wait_for_button": wait_for_button,
    "set_rgb": set_rgb,
}
all_keycodes = {key: getattr(Keycode, key) for key in dir(Keycode) if not key.startswith("_")}
for key in all_keycodes:
    RUN_GLOBALS[key] = all_keycodes[key]


try:
    with open(DEFAULT_SCRIPT, "r") as f:
        exec(f.read(), RUN_GLOBALS)
except Exception as e:
    print(e)
    set_rgb(255, 0, 0)
