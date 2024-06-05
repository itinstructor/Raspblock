import evdev

device = evdev.InputDevice('/dev/input/event1')
print(device)
# device /dev/input/event0, name "Logitech Gamepad F710", phys "usb-0000:01:00.0-1.3/input0"

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
# pressing 'a' and holding 'space'
