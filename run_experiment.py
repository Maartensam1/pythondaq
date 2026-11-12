"""View: voert de diodemeting uit en laat de resultaten zien.

Dit script start een scan met DiodeExperiment, print de metingen, slaat ze
op in metingen.csv en plot de I,U-karakteristiek van de LED.
"""

import matplotlib.pyplot as plt
import csv
from arduino_device import list_resources
from diode_experiment import DiodeExperiment

rm, ports = list_resources()
print(ports)
port = "ASRL/dev/cu.usbmodem1101::INSTR"
experiment = DiodeExperiment(port)
mean_list_voltage, mean_list_current, std_list_voltage, std_list_current = experiment.scan(0, 3.4, 3)

# metingen printen
for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
    print(f"average voltage: {u} +/- {err_u} V  average current: {i} +/- {err_i} A")

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
