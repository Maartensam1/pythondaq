import numpy as np
from arduino_device import ArduinoVISADevice

class DiodeExperiment:
    def __init__(self, port):
        self.arduino = ArduinoVISADevice(port)

    def scan(self, start, stop, herhalingen):
        # Raket methode
        totale_lijst_voltage = []
        totale_lijst_current = []
        for i in range(herhalingen):
            meting_lijst = []
            current_list = []

            for voltage in np.arange(start,stop,0.1):
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
