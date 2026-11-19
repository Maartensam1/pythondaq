"""Model voor het meten van de I,U-karakteristiek van een LED.

Deze module gebruikt de controller (ArduinoVISADevice) om een spanningsscan
uit te voeren en berekent gemiddelden en standaardafwijkingen.
"""

import numpy as np
from pythondaq.arduino_device import ArduinoVISADevice

class DiodeExperiment:
    """Experiment om de stroom en spanning over een LED te meten.

    Attributes:
        arduino (ArduinoVISADevice): De controller waarmee gemeten wordt.
    """

    def __init__(self, port):
        """Maakt het experiment aan en verbindt met de Arduino.

        Args:
            port (str): Naam van de VISA-poort waarop de Arduino zit.
        """
        self.arduino = ArduinoVISADevice(port)

    def scan(self, start, stop, herhalingen, stepsize):
        """Voert een spanningsscan uit en meet de spanning over en stroom door de LED.

        Args:
            start (float): Beginspanning van de scan in volt.
            stop (float): Eindspanning van de scan in volt (niet inbegrepen).
            herhalingen (int): Aantal keer dat de scan herhaald wordt.

        Returns:
            tuple: Vier lijsten (mean_list_voltage, mean_list_current,
            std_list_voltage, std_list_current) met de gemiddelde spanning
            over de LED (V), de gemiddelde stroom (A) en de bijbehorende
            standaardafwijkingen.
        """
        # Raket methode
        totale_lijst_voltage = []
        totale_lijst_current = []
        for i in range(herhalingen):
            meting_lijst = []
            current_list = []

            for voltage in np.arange(start,stop,stepsize):
                self.arduino.set_output_voltage(voltage)

                voltage_beide = self.arduino.get_input_voltage(1)

                voltage_resistor = self.arduino.get_input_voltage(2)

                meting_lijst.append(voltage_beide-voltage_resistor)
                current = voltage_resistor/220
                current_list.append(current)

            totale_lijst_voltage.append(meting_lijst)
            totale_lijst_current.append(current_list)


        mean_list_voltage = []
        std_list_voltage = []
        mean_list_current = []
        std_list_current = []
        for i in range(len(totale_lijst_voltage[0])):
            mean_per_value_voltage = []
            mean_per_value_current = []
            for j in range(len(totale_lijst_voltage)):
                mean_per_value_voltage.append(totale_lijst_voltage[j][i])
                mean_per_value_current.append(totale_lijst_current[j][i])

            mean_list_voltage.append(np.mean(mean_per_value_voltage))
            std_list_voltage.append(np.std(mean_per_value_voltage))
            mean_list_current.append(np.mean(mean_per_value_current))
            std_list_current.append(np.std(mean_per_value_current))

        self.arduino.set_output_voltage(0)

        return mean_list_voltage, mean_list_current, std_list_voltage, std_list_current
