import pyvisa

def list_resources():
    rm =pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return rm, ports

class ArduinoVISADevice:
    def __init__(self):
        rm, ports = list_resources()
        self.device = rm.open_resource("ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n")
        
    def get_identification(self):
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        waarde_CH0 = self.device.query(f"OUT:CH0?")
        print(waarde_CH0)

    def get_input_value(self,CH):
        self.spanning_CH = self.device.query(f"MEAS:{f"CH{CH}"}?")
        print(self.spanning_CH)
        return self.spanning_CH

    def get_input_voltage(self):
        self.get_input_value()
        spanning_CH1_V = float(self.spanning_CH1) * (3.3/1023)
        print(f"de spanning in Volt over CH1 is : {spanning_CH1_V}")

    def set_output_voltage(self, voltage):
        value = round(voltage / (3.3/1023))
        self.device.query(f"OUT:CH0 {value}")


arduino = ArduinoVISADevice(port="ASRL3::INSTR")
# arduino.set_output_value(828)
# arduino.get_output_value()
# arduino.get_input_value(1)
# arduino.get_input_voltage()
arduino.set_output_voltage(0)
