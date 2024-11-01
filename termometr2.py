import os
import glob
import time

# Inicjalizacja modułów jądra
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Ścieżka bazowa do urządzeń
base_dir = '/sys/bus/w1/devices/'

# Wyszukiwanie wszystkich urządzeń 1-Wire
device_folders = glob.glob(base_dir + '28*')

# Funkcja do odczytu surowych danych z pliku urządzenia
def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

# Funkcja do odczytu temperatury z jednego termometru
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Sprawdzenie, czy wykryto dwa termometry
if len(device_folders) < 2:
    print("Nie wykryto dwóch termometrów.")
else:
    # Pliki urządzeń dla obu termometrów
    device_file_1 = device_folders[0] + '/w1_slave'
    device_file_2 = device_folders[1] + '/w1_slave'

    # Główna pętla programu
    while True:
        temp1 = read_temp(device_file_1)
        temp2 = read_temp(device_file_2)
        print(f"Termometr 1: {temp1:.2f} °C")
        print(f"Termometr 2: {temp2:.2f} °C")
        time.sleep(10)