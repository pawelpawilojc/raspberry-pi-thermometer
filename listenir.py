import subprocess,time

from gpiozero import LED



def listen_for_ir_commands():
    process = subprocess.Popen(['irw'], stdout=subprocess.PIPE)
    while True:
        led = LED(26)
        output = process.stdout.readline()
        if output == b'':
            break
        if output:
            print(f"Detected IR command: {output.strip()}")
            led.off()
            led.on()
            print("on")
            time.sleep(0.05)
            led.off()
            print("off")
            time.sleep(2)

if __name__ == "__main__":
    listen_for_ir_commands()