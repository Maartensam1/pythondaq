import matplotlib.pyplot as plt
import numpy as np
import csv
from arduino_device import list_resources, ArduinoVISADevice

rm, ports = list_resources()
arduino = ArduinoVISADevice("ASRL/dev/cu.usbmodem1101::INSTR")

# Raket methode
totale_lijst_voltage = []
totale_lijst_current = []
for i in range(3):
    meting_lijst = []
    current_list = []

    for voltage in np.arange(0,3.4,0.01):
        arduino.set_output_voltage(voltage)

        voltage_beide = arduino.get_input_voltage(1)

        voltage_resistor = arduino.get_input_voltage(2)

        meting_lijst.append(voltage_beide-voltage_resistor)
        current = voltage_resistor/220
        current_list.append(current)

    totale_lijst_voltage.append(meting_lijst)
    totale_lijst_current.append(current_list)


mean_list_voltage = []
std_list_voltage = []
mean_list_current = []
std_list_current = []
for i in range(len(totale_lijst_voltage[0])):
    mean_per_value_voltage = []
    mean_per_value_current = []
    for j in range(len(totale_lijst_voltage)):
        mean_per_value_voltage.append(totale_lijst_voltage[j][i])
        mean_per_value_current.append(totale_lijst_current[j][i])
        
    mean_list_voltage.append(np.mean(mean_per_value_voltage))
    std_list_voltage.append(np.std(mean_per_value_voltage))
    mean_list_current.append(np.mean(mean_per_value_current))
    std_list_current.append(np.std(mean_per_value_current))

arduino.set_output_voltage(0)

# metingen opslaan in csv-bestand
with open("metingen.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["U (V)", "I (A)", "err_U (V)", "err_I (A)"])
    for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
        writer.writerow([u, i, err_u, err_i])

# plotten
plt.errorbar(mean_list_voltage, mean_list_current, yerr=std_list_current, xerr=std_list_voltage, fmt='o', ecolor='red', markersize=2, capsize=1)
plt.xlabel("Spanning (V)")
plt.ylabel("Stroom (A)")
plt.title("I,U-karakteristiek van een LED")
plt.show()
