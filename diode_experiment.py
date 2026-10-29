import pyvisa
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)

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

    # print(voltage_beide, voltage_resistor)

    # print(f"de spanning over beide is:{voltage_beide:.2f} V")
    # print(f"de spanning resistor is:{voltage_resistor:.2f} V")

    device.query(f"OUT:CH0 {0}")