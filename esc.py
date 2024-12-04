import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because it's too impatient
import pigpio  # importing GPIO library

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # Adding delay to avoid errors due to impatience

ESC = 4  # Connect the ESC to this GPIO pin

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)

max_value = 2000  # Change this if your ESC's max value is different
min_value = 700  # Change this if your ESC's min value is different

print("For first-time launch, select calibrate")
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")


def manual_drive():
    """Allows manual control of the ESC."""
    print("You have selected manual. Provide a value between 0 and max_value.")
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            try:
                pulse_width = int(inp)
                pi.set_servo_pulsewidth(ESC, pulse_width)
            except ValueError:
                print("Please enter a valid number or a command ('stop', 'control', 'arm').")


def calibrate():
    """Performs auto-calibration for the ESC."""
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    input()
    pi.set_servo_pulsewidth(ESC, max_value)
    print("Connect the battery NOW. You will hear two beeps, then a gradual falling tone. Press Enter.")
    input()
    pi.set_servo_pulsewidth(ESC, min_value)
    print("Special tone... wait for it.")
    time.sleep(7)
    print("Working... DONT WORRY, JUST WAIT...")
    time.sleep(5)
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(2)
    print("Arming ESC now...")
    pi.set_servo_pulsewidth(ESC, min_value)
    time.sleep(1)
    control()


def control():
    """Starts the motor and provides speed control."""
    print("Starting the motor. Ensure it's calibrated and armed. Type 'x' to restart.")
    time.sleep(1)
    speed = 1500  # Default speed; change as needed
    print("Controls: 'a' to decrease speed, 'd' to increase speed,")
    print("'q' to decrease speed significantly, 'e' to increase speed significantly.")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        if inp == "q":
            speed -= 100
            speed = max(speed, min_value)
            print(f"Speed = {speed}")
        elif inp == "e":
            speed += 100
            speed = min(speed, max_value)
            print(f"Speed = {speed}")
        elif inp == "d":
            speed += 10
            speed = min(speed, max_value)
            print(f"Speed = {speed}")
        elif inp == "a":
            speed -= 10
            speed = max(speed, min_value)
            print(f"Speed = {speed}")
        elif inp == "stop":
            stop()
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print("Invalid input! Use 'a', 'q', 'd', or 'e'.")


def arm():
    """Arms the ESC for operation."""
    print("Connect the battery and press Enter.")
    input()
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, min_value)
    time.sleep(1)
    control()


def stop():
    """Stops all ESC operations."""
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()


# Start of the program
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Invalid input! Restart the program and try again.")
