import time
from gpiozero import LED
led = LED(26)
while True:
    led.on()
    print("on")
    time.sleep(5)
    led.off()
    print("off")
    time.sleep(5)