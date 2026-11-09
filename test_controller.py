import pyvisa

def list_resources():
    rm =pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return rm, ports

class ArduinoVISADevice:
    def __init__(self, port):
        rm, ports = list_resources()
        self.device = rm.open_resource("ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n")
        
    def get_identification(self):
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self):
        self.device.query(f"OUT:CH0 {828}")

    def get_output_value(self):
        waarde_CH0 = self.device.query(f"OUT:CH0?")
        print(waarde_CH0)

    def get_input_value(self):
        self.spanning_CH1 = self.device.query(f"MEAS:CH1?")
        spanning_CH2 = self.device.query(f"MEAS:CH2?")
        print(self.spanning_CH1)
        print(spanning_CH2)

    def get_input_voltage(self):
        self.get_input_value()
        spanning_CH1_V = float(self.spanning_CH1) * (3.3/1023)
        print(f"de spanning in Volt over CH1 is : {spanning_CH1_V}")

    def set_output_voltage(self, voltage):
        value = round(voltage / (3.3/1023))
        self.device.query(f"OUT:CH0 {value}")


device = ArduinoVISADevice(port="ASRL3::INSTR")
# device.set_output_value()
# device.get_output_value()
# device.get_input_value()
# device.get_input_voltage()
device.set_output_voltage(0)
