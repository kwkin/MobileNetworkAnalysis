from analysis import BluetoothAnalysis
from sklearn.metrics import mean_absolute_error

import numpy as np
import matplotlib.pyplot as plt
import ntpath
import math

def plot_rssi():
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    model_distances = [0.5, 1, 2, 5, 7.5, 10, 12.5, 15, 20, 25, 30]
    classic = False
    data_files = ["../data/bluetooth_part3/BluetoothDataUltraLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataMediumPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataHighPart3.txt"]
    record_files = ["../data/bluetooth_part3/recordUltraLowPart3.txt",
                    "../data/bluetooth_part3/recordLowPart3.txt",
                    "../data/bluetooth_part3/recordMediumPart3.txt",
                    "../data/bluetooth_part3/recordHighPart3.txt"]
    
    fig_rssi, ax_rssi = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    fig_model, ax_model = plt.subplots(2, 2, sharex=True, sharey=True)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    fig_error, ax_error = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)

    mean_errors = []
    for index, data_file, record_file in zip(range(len(data_files)), data_files, record_files):
        analysis = BluetoothAnalysis(data_file, record_file, classic)

        # Calculate average mean
        means = []
        for session in analysis.records['session']:
            records = analysis.get_session_traces(session)
            records = analysis.get_name_traces_data("Pocophone F1", records)
            means.append(analysis.get_rssi_average_data(records))
        ax_rssi.plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

        # Generate log shadowing models for line plotting
        log_shadowing_values_plot = compute_log_shadowing(model_distances, means[1])
        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)
        ax_model[row, col].plot(model_distances, log_shadowing_values_plot)

        # Generate log shadowing models for error plotting
        log_shadowing_values = compute_log_shadowing(distances, means[1])

        truths = []
        actuals = []
        for mean, truth in zip(means, log_shadowing_values):
            if (not math.isnan(mean)):
                truths.append(truth)
                actuals.append(mean)

        mean_errors.append(mean_absolute_error(truths, actuals))

    legend = ['Ultra Low', 'Low', 'Medium', 'High']
    fig_rssi.suptitle('Average RSSI Level versus Distance at Different Advertising Settings')
    ax_rssi.set_xlabel('Distance (meters)')
    ax_rssi.set_ylabel('RSSI')
    ax_rssi.legend(legend)
    ax_rssi.set_ylim([higher_value * 1.05, smaller_value * 0.95])
    
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model')
    ax_model[0, 0].set_title("Ultra Low")
    ax_model[0, 0].set_ylabel('RSSI')
    ax_model[0, 0].legend(['Measured', 'Log Shadowing'])
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model')
    ax_model[0, 1].set_title("Low")
    ax_model[0, 1].legend(['Measured', 'Log Shadowing'])
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model')
    ax_model[1, 0].set_title("Medium")
    ax_model[1, 0].set_ylabel('RSSI')
    ax_model[1, 0].set_xlabel('Distance (meters)')
    ax_model[1, 0].legend(['Measured', 'Log Shadowing'])
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model')
    ax_model[1, 1].set_title("High")
    ax_model[1, 1].set_xlabel('Distance (meters)')
    ax_model[1, 1].legend(['Measured', 'Log Shadowing'])

    fig_error.suptitle('Mean Absolute Error of the Recorded Data versus the Log Shadowing Model')
    ax_error.bar(legend, mean_errors)
    ax_error.set_xlabel("Power Setting")
    ax_error.set_ylabel("Mean Absolute Error")
    highest_error = np.amax(mean_errors)
    ax_error.set_ylim([0, math.ceil(highest_error * 1.05)])

    plt.show(block=True)


def compute_log_shadowing(distances, mean):
    values = []
    n = 2   # Path loss exponent in free space
    for distance in distances:
        values.append(-10 * n * math.log10(distance) + mean)
    return values

if __name__ == "__main__":
    style_file = 'simple_charts.mplstyle'
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)

    plot_rssi()