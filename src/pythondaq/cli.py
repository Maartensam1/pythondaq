"""
In this file the CLI is built. It uses user inputs to run the diode experiment.
It connects to arduino_device.py and diode_experiment.py. 
It provides the commands "list", "info" and "scan". 
It uses ArduinoVISADevice fromarduino_device.py and DiodeExperiment from diode_experiment.py.
"""

import click
import matplotlib.pyplot as plt
import csv
from pythondaq.arduino_device import list_resources, ArduinoVISADevice
from pythondaq.diode_experiment import DiodeExperiment

@click.group()
def cli():
    """
    Command Line Interface for pythondaq.

    Use one of the commands below to list devices or run a measurement.
    """
    pass

@cli.command("list")
def list():
    """Show the ports of the connected devices."""
    rm, ports = list_resources()
    print("The connected ports are:")
    print(ports)

@cli.command("info")
@click.option(
    "-p",
    "--port",
    help = "Port of the device to identify (see the list command)."
)
def info(port):
    """Shows the identificationstring of the port.

    A correct arduino is connect when the following message shows in the terminal:
    "Arduino VISA firmware v1.2.0".
    """
    device = ArduinoVISADevice(port)
    identification = device.get_identification()
    print("The identification string of that port is:")
    print(identification)

@cli.command("scan")
@click.option(
    "-r",
    "--range",
    type = click.FloatRange(0, 3.3),
    nargs = 2,
    default = (0, 3.3),
    help = "Voltage range in V as <start> <end> (0 to 3.3)."
)
@click.option(
    "-n",
    "--repitions",
    type = int,
    default = 3,
    help = "Number of repeated measurements per voltage step."
)
@click.option(
    "-s",
    "--stepsize",
    type = float,
    default = 0.01,
    help = "Step size in V."
)
@click.option(
    "-o",
    "--output",
    "filename",
    default = None,
    help = "Name of the CSV file to save the data in (without .csv)."
)
@click.option(
    "-a",
    "--arduino",
    required = True,
    help = "Port of the Arduino to use (see the list command)."
)
@click.option(
    "-g / -ng",
    "--graph / --no_graph",
    default = True,
    help = "Show or hide the graph of the measured data."
)
@click.option(
    "-f",
    "--figure",
    default = None,
    help = "Name of the PNG file to save the figure in (without .png)."
)
def scan(range, repitions, stepsize, filename, arduino, graph, figure):
    """
    Measure the I,U characteristic of an LED.

    Goes through the voltage over the given range, repeats each step the given number
    of times and prints the mean and standard deviation of voltage and current.
    Optionally saves the data as CSV and the figure as PNG.
    """
    start_range, end_range = range
    port = arduino
    experiment = DiodeExperiment(port)
    mean_list_voltage, mean_list_current, std_list_voltage, std_list_current = experiment.scan(start_range, end_range, repitions, stepsize)

    # Printing the measurements.
    for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
        print(f"average voltage: {u:.3f} +/- {err_u:.3f} V  average current: {i:.6f} +/- {err_i:.6f} A")

    # Saving the measurements in a .csv file.
    if filename is not None:
        with open(f"{filename}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["U (V)", "I (A)", "err_U (V)", "err_I (A)"])
            for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
                writer.writerow([u, i, err_u, err_i])

    # Plotting the data.
    plt.errorbar(mean_list_voltage, mean_list_current, yerr=std_list_current, xerr=std_list_voltage, fmt='o', ecolor='red', markersize=2, capsize=1)
    plt.xlabel("Spanning (V)")
    plt.ylabel("Stroom (A)")
    plt.title("IU-karakteristiek van een LED")
    if figure:
        plt.savefig(f"{figure}.png")
    if graph:
        plt.show()

if __name__ == "__main__":
    cli()