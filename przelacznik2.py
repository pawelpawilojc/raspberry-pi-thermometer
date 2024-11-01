import time
from gpiozero import LED

led = LED(26)
led.on()
print("on")
time.sleep(0.05)
led.off()
print("off")