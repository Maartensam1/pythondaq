"""Controller voor de Arduino die via VISA aangestuurd wordt.

Deze module bevat een functie om beschikbare poorten op te vragen en een
klasse om met de Arduino te communiceren.
"""

import pyvisa

def list_resources():
    """Vraagt alle poorten op.

    Returns:
        tuple: Een tuple (rm, ports) met de namen van alle gevonden poorten.
    """
    rm =pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return rm, ports

class ArduinoVISADevice:
    """Stuurt een Arduino aan.

    Met deze klasse kun je een spanning zetten op kanaal 0 en spanningen
    uitlezen op de inputkanalen.

    Attributes:
        device: de geopende arduino poort waarmee gecommuniceerd wordt.
    """

    def __init__(self, port):
        """Maakt verbinding met de Arduino op de opgegeven poort.

        Args:
            port (str): Naam van de VISA-poort.
        """
        rm =pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(port, read_termination="\r\n", write_termination="\n")
        
    def get_identification(self):
        """Vraagt de identificatiestring van de Arduino op.

        Returns:
            str: De identificatie van het apparaat.
        """
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self, value):
        """Zet een waarde op outputkanaal 0.

        Args:
            value (int): tussen 0 en 1023.
        """
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        """Leest de ruwe waarde die op outputkanaal 0 staat.

        Returns:
            str: De huidige (0-1023) van kanaal 0.
        """
        waarde_CH0 = self.device.query(f"OUT:CH0?")
        # print(waarde_CH0)
        return waarde_CH0

    def get_input_value(self,CH):
        """Meet de ruwe ADC-waarde op een inputkanaal.

        Args:
            CH (int): Nummer van het kanaal dat gemeten wordt.

        Returns:
            str: De gemeten ADC-waarde (0-1023).
        """
        self.spanning_CH = self.device.query(f"MEAS:{f"CH{CH}"}?")
        # print(self.spanning_CH)
        return self.spanning_CH

    def get_input_voltage(self, CH):
        """Meet de spanning in volt op een inputkanaal.

        De ruwe ADC-waarde wordt omgerekend naar volt met de factor 3.3/1023.

        Args:
            CH (int): Nummer van het kanaal dat gemeten wordt.

        Returns:
            float: De gemeten spanning in volt.
        """
        self.get_input_value(CH)
        spanning_CH_V = float(self.spanning_CH) * (3.3/1023)
        # print(f"de spanning in Volt over CH{CH} is : {spanning_CH_V}")
        return spanning_CH_V

    def set_output_voltage(self, voltage):
        """Zet een spanning in volt op outputkanaal 0.

        De spanning wordt omgerekend naar een (0-1023) en
        afgerond op een geheel getal.

        Args:
            voltage (float): Gewenste spaning in volt.
        """
        value = round(voltage / (3.3/1023))
        self.device.query(f"OUT:CH0 {value}")

    def get_output_voltage(self):
        """Leest de spanning in volt die op outputkanaal 0 staat.

        Returns:
            float: De spanning op kanaal 0 in volt.
        """
        waarde_CH0 = self.get_output_value()
        spanning_CH0_V = float(waarde_CH0) * (3.3/1023)
        print(f"de spanning in Volt over CH0 is : {spanning_CH0_V}")
        return spanning_CH0_V

if __name__ == '__main__':
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

