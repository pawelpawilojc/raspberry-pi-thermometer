import subprocess
import RPi.GPIO as GPIO
import time
import os
import glob
import threading
import random
from tkinter import Tk, Label, PhotoImage, StringVar
from PIL import Image, ImageTk

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


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


base_dir = '/sys/bus/w1/devices/'


device_folders = glob.glob(base_dir + '28*')

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if (equals_pos != -1):
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def monitor_temperatures():
    
    if len(device_folders) < 2:
        print("Nie wykryto dwóch termometrów.")
    else:
        
        device_file_1 = device_folders[0] + '/w1_slave'
        device_file_2 = device_folders[1] + '/w1_slave'

       
        while True:
            temp1 = read_temp(device_file_1)
            temp2 = read_temp(device_file_2)
            temperature_label_var.set(f"Termometr 1: {temp1:.2f} °C\nTermometr 2: {temp2:.2f} °C")
            print(f"Termometr 1: {temp1:.2f} °C")
            print(f"Termometr 2: {temp2:.2f} °C")
            time.sleep(10)

def display_random_image():
    while True:
        image_files = glob.glob(image_folder + '/*.jpg') + glob.glob(image_folder + '/*.png')
        if image_files:
            image_path = random.choice(image_files)
            image = Image.open(image_path)
            image = image.resize((1300, 700), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
        time.sleep(30)

if __name__ == "__main__":
    try:
        # Folder z obrazami
        image_folder = 'ramka'  

        # Ustawienia okna
        root = Tk()
        root.title("Układy cyfrowe")

        temperature_label_var = StringVar()
        temperature_label = Label(root, textvariable=temperature_label_var, font=("Helvetica", 16))
        temperature_label.pack()

        image_label = Label(root)
        image_label.pack()

        # Uruchomienie wątków
        ir_thread = threading.Thread(target=listen_for_ir_commands)
        temp_thread = threading.Thread(target=monitor_temperatures)
        image_thread = threading.Thread(target=display_random_image)

        ir_thread.start()
        temp_thread.start()
        image_thread.start()

        # Uruchomienie interfejsu graficznego
        root.mainloop()

        # Czekanie na zakończenie wątków
        ir_thread.join()
        temp_thread.join()
        image_thread.join()

    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        GPIO.cleanup()
