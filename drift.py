import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import time

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)
aantal_metingen = 3000
counter = 0
metingen_reeks = []
voltage_beide_list = []
voltage_led_list = []
for i in range(aantal_metingen):
    device.query(f"OUT:CH0 {1023}")   

    ADC_diode_resistor = device.query(f"MEAS:CH1?")
    voltage_beide = float(ADC_diode_resistor) * (3.3/1023) # in V
    voltage_beide_list.append(voltage_beide)

    resistor = device.query(f"MEAS:CH2?")
    voltage_resistor = float(resistor) * (3.3/1023) # in V

    metingen_reeks.append(voltage_beide-voltage_resistor)

    counter +=1
    print(counter)
    time.sleep(0.1) 

x_as = []
for i in range(aantal_metingen):
    x_as.append(i)

plt.scatter(x_as, metingen_reeks)
plt.show()

