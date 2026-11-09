import pyvisa

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
print(ports)
arduino = ArduinoVISADevice("ASRL/dev/cu.usbmodem1101::INSTR")
arduino.get_identification()
arduino.set_output_value(828)
arduino.get_output_value()
arduino.get_input_value(1)
arduino.get_input_value(2)
arduino.get_input_voltage(1)
arduino.set_output_voltage(2)
arduino.get_output_voltage()
arduino.set_output_voltage(0)

