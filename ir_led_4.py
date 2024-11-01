# Create a CommandSet for your remote control
# GPIO for the IR receiver: 23
# GPIO for the IR transmitter: 22
import time
from ircodec.command import CommandSet
controller = CommandSet(emitter_gpio=18, receiver_gpio=24, name='carmp3')

# Add the volume up key
controller.add('onoff')
# Connected to pigpio
# Detecting IR command...
# Received.


while True:
    controller.emit('onoff')
    print('wait')
    time.sleep(1)