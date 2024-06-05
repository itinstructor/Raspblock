from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event0')

print(dev)

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(f"{event} button is pressed")
    elif event.type == ecodes.EV_ABS:
        print(event)
