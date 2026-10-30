import pyvisa
import matplotlib.pyplot as plt
import numpy as np

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)

# De I,U-karakteristiek van een LED
current_list = []
voltage_beide_list = []
voltage_led_list = []
def meten():
    for i in range(0,1024):
        device.query(f"OUT:CH0 {i}")

        ADC_diode_resistor = device.query(f"MEAS:CH1?")
        voltage_beide = float(ADC_diode_resistor) * (3.3/1023) # in V
        voltage_beide_list.append(voltage_beide)

        resistor = device.query(f"MEAS:CH2?")
        voltage_resistor = float(resistor) * (3.3/1023) # in V

        voltage_led_list.append(voltage_beide-voltage_resistor)

        current = voltage_resistor/220
        current_list.append(current)

# meten()


# Raket methode
totale_lijst_voltage = []
totale_lijst_current = []
for i in range(3):
    meting_lijst = []
    current_list = []

    for i in range(0,1024):
        device.query(f"OUT:CH0 {i}")

        ADC_diode_resistor = device.query(f"MEAS:CH1?")
        voltage_beide = float(ADC_diode_resistor) * (3.3/1023) # in V

        resistor = device.query(f"MEAS:CH2?")
        voltage_resistor = float(resistor) * (3.3/1023) # in V

        meting_lijst.append(voltage_beide-voltage_resistor)
        current = voltage_resistor/220
        current_list.append(current)

    totale_lijst_voltage.append(meting_lijst)
    totale_lijst_current.append(current_list)

# 
mean_list_voltage = []
std_list_voltage = []
mean_list_current = []
std_list_current = []
for i in range(1024):
    mean_per_value_voltage = []
    mean_per_value_current = []
    for j in range(len(totale_lijst_voltage)):
        mean_per_value_voltage.append(totale_lijst_voltage[j][i])
        mean_per_value_current.append(totale_lijst_current[j][i])
        
    mean_list_voltage.append(np.mean(mean_per_value_voltage))
    std_list_voltage.append(np.std(mean_per_value_voltage))
    mean_list_current.append(np.mean(mean_per_value_current))
    std_list_current.append(np.std(mean_per_value_current))

current_list = []
voltage_beide_list = []
voltage_led_list = []
for i in range(0,1024):
    device.query(f"OUT:CH0 {i}")

    ADC_diode_resistor = device.query(f"MEAS:CH1?")
    voltage_beide = float(ADC_diode_resistor) * (3.3/1023) # in V
    voltage_beide_list.append(voltage_beide)

    resistor = device.query(f"MEAS:CH2?")
    voltage_resistor = float(resistor) * (3.3/1023) # in V

    voltage_led_list.append(voltage_beide-voltage_resistor)

    current = voltage_resistor/220
    current_list.append(current)

device.query(f"OUT:CH0 {0}")

# plotten
plt.errorbar(mean_list_voltage, mean_list_current, yerr=std_list_current, xerr=std_list_voltage, fmt='o', ecolor='red', markersize=2, capsize=1)
plt.xlabel("Spanning (V)")
plt.ylabel("Stroom (A)")
plt.show()
