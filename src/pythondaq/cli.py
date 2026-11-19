"""
In this file the CLI is build. It uses user inputs to run the diode experiment. 
It connects to arduino_device.py and diode_experiment.py
""" 

import click
import matplotlib.pyplot as plt
import csv
from pythondaq.arduino_device import list_resources, ArduinoVISADevice
from pythondaq.diode_experiment import DiodeExperiment

@click.group()
def cli():
    """ command line interface for pythondaq """
    pass

@cli.command("list")
def list():
    """ shows the connected devices """
    rm, ports = list_resources()
    print(f"The connected ports are:")
    print(ports)

@cli.command("info")
@click.option(
    "-p",
    "--port",
    help = "put the port you want to identify here"
)
def info(port):
    """ shows the identificationstring of the port """
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
    help = "input a voltage range, two values: <start> <end>"
)
@click.option(
    "-n",
    "--repitions",
    type = int,
    default = 3,
    help = "input the number of runs you would like the measurements to do"
)
@click.option(
    "-s",
    "--stepsize",
    type = float,
    default = 0.01,
    help = "input the size of step you want to use for the measurements"
)
@click.option(
    "-o",
    "--output",
    "filename",
    default = None,
    help = "use this if you want the data to be stored in a .csv file for the input choose the name you want your file to have"
)
def scan(range, repitions, stepsize, filename):
    """measures the I,U characteristics of the diode"""
    start_range, end_range = range
    port = "ASRL/dev/cu.usbmodem1101::INSTR"
    experiment = DiodeExperiment(port)
    mean_list_voltage, mean_list_current, std_list_voltage, std_list_current = experiment.scan(start_range, end_range, repitions, stepsize)

    # metingen printen
    for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
        print(f"average voltage: {u:.3f} +/- {err_u:.3f} V  average current: {i:.6f} +/- {err_i:.6f} A")

    # metingen opslaan in csv-bestand
    if filename is not None:
        with open(f"{filename}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["U (V)", "I (A)", "err_U (V)", "err_I (A)"])
            for u, i, err_u, err_i in zip(mean_list_voltage, mean_list_current, std_list_voltage, std_list_current):
                writer.writerow([u, i, err_u, err_i])

    # plotten
    plt.errorbar(mean_list_voltage, mean_list_current, yerr=std_list_current, xerr=std_list_voltage, fmt='o', ecolor='red', markersize=2, capsize=1)
    plt.xlabel("Spanning (V)")
    plt.ylabel("Stroom (A)")
    plt.title("I,U-karakteristiek van een LED")
    plt.show()

if __name__ == "__main__":
    cli()