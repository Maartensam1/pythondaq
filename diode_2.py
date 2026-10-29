import pyvisa
import matplotlib.pyplot as plt
import numpy as np

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)

totale_lijst = []
for i in range(3):
    meting_lijst = []
    for i in range(0,1024):
        device.query(f"OUT:CH0 {i}")

        ADC_diode_resistor = device.query(f"MEAS:CH1?")
        voltage_beide = float(ADC_diode_resistor) * (3.3/1023) # in V

        resistor = device.query(f"MEAS:CH2?")
        voltage_resistor = float(resistor) * (3.3/1023) # in V

        meting_lijst.append(voltage_beide-voltage_resistor)

    totale_lijst.append(meting_lijst)

mean_list = []

for i in range(1024):
    mean_per_value = []
    for j in range(len(totale_lijst)):
        mean_per_value.append(totale_lijst[j][i])
        
    mean_list.append(np.mean(mean_per_value))

# print(mean_list)

x_as = []
for i in range(0,1024):
    x_as.append(i)

print(len(x_as))
print(x_as)

plt.plot(x_as, mean_list)
plt.show()