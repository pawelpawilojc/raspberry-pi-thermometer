import subprocess
import RPi.GPIO as GPIO
import time

# Ustawienia GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 26
GPIO.setup(GPIO_PIN, GPIO.OUT)
GPIO.output(GPIO_PIN, GPIO.LOW)

def toggle_gpio():
    current_state = GPIO.input(GPIO_PIN)
    new_state = GPIO.LOW if current_state == GPIO.HIGH else GPIO.HIGH
    GPIO.output(GPIO_PIN, new_state)
    print(f"GPIO pin {GPIO_PIN} is now {'HIGH' if new_state == GPIO.HIGH else 'LOW'}")

def listen_for_ir_commands():
    process = subprocess.Popen(['irw'], stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'':
            break
        if output:
            print(f"Detected IR command: {output.strip()}")
            toggle_gpio()
            time.sleep(0.05)
            toggle_gpio()

if __name__ == "__main__":
    try:
        listen_for_ir_commands()
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        GPIO.cleanup()