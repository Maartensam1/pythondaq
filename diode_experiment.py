import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import csv

def list_resources():
    rm =pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return rm, ports

class ArduinoVISADevice:
    def __init__(self, port):
        rm, ports = list_resources()
        self.device = rm.open_resource(port, read_termination="\r\n", write_termination="\n")
        
    def get_identification(self):
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        waarde_CH0 = self.device.query(f"OUT:CH0?")
        print(waarde_CH0)
        return waarde_CH0

    def get_input_value(self,CH):
        self.spanning_CH = self.device.query(f"MEAS:{f"CH{CH}"}?")
        print(self.spanning_CH)
        return self.spanning_CH

    def get_input_voltage(self, CH):
        self.get_input_value(CH)
        spanning_CH_V = float(self.spanning_CH) * (3.3/1023)
        print(f"de spanning in Volt over CH{CH} is : {spanning_CH_V}")
        return spanning_CH_V

    def set_output_voltage(self, voltage):
        value = round(voltage / (3.3/1023))
        self.device.query(f"OUT:CH0 {value}")

    def get_output_voltage(self):
        waarde_CH0 = self.get_output_value()
        spanning_CH0_V = float(waarde_CH0) * (3.3/1023)
        print(f"de spanning in Volt over CH0 is : {spanning_CH0_V}")
        return spanning_CH0_V


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
