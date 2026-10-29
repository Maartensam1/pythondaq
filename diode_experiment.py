import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL/dev/cu.usbmodem1101::INSTR", read_termination="\r\n", write_termination="\n"
)

for i in range(0,1023):
    device.query(f"OUT:CH0 {i}")
