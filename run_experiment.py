import matplotlib.pyplot as plt
import numpy as np
import csv
from arduino_device import list_resources, ArduinoVISADevice
from diode_experiment import DiodeExperiment

rm, ports = list_resources()
arduino = ArduinoVISADevice("ASRL/dev/cu.usbmodem1101::INSTR")

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
