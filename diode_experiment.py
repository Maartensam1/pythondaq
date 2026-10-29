import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)

for i in range(0,1024):
    device.query(f"OUT:CH0 {i}")
    
    ADC_diode_resistor = device.query(f"MEAS:CH1?")
    voltage_beide = float(ADC_diode_resistor) * (3.3/1023)

    resistor = device.query(f"MEAS:CH2?")
    voltage_resistor = float(ADC_diode_resistor) * (3.3/1023)

    print(f"de spanning over beide is:{voltage_beide}")
    print(f"de spanning resistor is:{voltage_resistor}")


