from analysis import BluetoothAnalysis
from sklearn.metrics import mean_absolute_error

import numpy as np
import matplotlib.pyplot as plt
import ntpath
import math

def plot_rssi_p6():
    data_files = ["../data/bluetooth_part6/BluetoothDataUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataMediumPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"]
    record_files = ["../data/bluetooth_part6/recordUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/recordLowPart3_2.txt",
                    "../data/bluetooth_part6/recordMediumPart3_2.txt",
                    "../data/bluetooth_part6/recordHighPart3_2.txt"]
    device_name = 'Galaxy S8'
    plot_rssi(data_files, record_files, device_name)

def plot_rssi_p3():
    data_files = ["../data/bluetooth_part3/BluetoothDataUltraLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataMediumPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataHighPart3.txt"]
    record_files = ["../data/bluetooth_part3/recordUltraLowPart3.txt",
                    "../data/bluetooth_part3/recordLowPart3.txt",
                    "../data/bluetooth_part3/recordMediumPart3.txt",
                    "../data/bluetooth_part3/recordHighPart3.txt"]
    device_name = 'Pocophone F1'
    plot_rssi(data_files, record_files, device_name)

def plot_device_distances():
    data_files_s8 = ["../data/bluetooth_part6/BluetoothDataUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataMediumPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"]
    record_files_s8 = ["../data/bluetooth_part6/recordUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/recordLowPart3_2.txt",
                    "../data/bluetooth_part6/recordMediumPart3_2.txt",
                    "../data/bluetooth_part6/recordHighPart3_2.txt"]
    data_files_poco = ["../data/bluetooth_part3/BluetoothDataUltraLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataMediumPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataHighPart3.txt"]
    record_files_poco = ["../data/bluetooth_part3/recordUltraLowPart3.txt",
                    "../data/bluetooth_part3/recordLowPart3.txt",
                    "../data/bluetooth_part3/recordMediumPart3.txt",
                    "../data/bluetooth_part3/recordHighPart3.txt"]
            
    device_name_s8 = 'Galaxy S8'        
    device_name_poco = 'Pocophone F1'
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    classic = False
    
    fig_model, ax_model = plt.subplots(2, 2, sharex=True, sharey=True)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)

    for index, data_file_s8, record_file_s8, data_file_poco, record_file_poco in zip(range(len(data_files_s8)), data_files_s8, record_files_s8, data_files_poco, record_files_poco):
        analysis_s8 = BluetoothAnalysis(data_file_s8, record_file_s8, classic)
        analysis_poco = BluetoothAnalysis(data_file_poco, record_file_poco, classic)

        # Calculate average mean for s8
        means = []
        for session in analysis_s8.records['session']:
            records = analysis_s8.get_session_traces(session)
            records = analysis_s8.get_name_traces_data(device_name_s8, records)
            means.append(analysis_s8.get_rssi_average_data(records))
            
        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

        # Calculate average mean for poco
        means = []
        for session in analysis_poco.records['session']:
            records = analysis_poco.get_session_traces(session)
            records = analysis_poco.get_name_traces_data(device_name_poco, records)
            means.append(analysis_poco.get_rssi_average_data(records))

        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

    
    fig_model.suptitle('RSSI Level versus Distance')
    ax_model[0, 0].set_title("Ultra Low")
    ax_model[0, 0].set_ylabel('RSSI')
    ax_model[0, 0].legend([device_name_s8, device_name_poco])
    ax_model[0, 1].set_title("Low")
    ax_model[0, 1].legend([device_name_s8, device_name_poco])
    ax_model[1, 0].set_title("Medium")
    ax_model[1, 0].set_ylabel('RSSI')
    ax_model[1, 0].set_xlabel('Distance (meters)')
    ax_model[1, 0].legend([device_name_s8, device_name_poco])
    ax_model[1, 1].set_title("High")
    ax_model[1, 1].set_xlabel('Distance (meters)')
    ax_model[1, 1].legend([device_name_s8, device_name_poco])

    plt.show(block=True)

def fit_line():
    data_file_s8 = "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"
    record_file_s8 = "../data/bluetooth_part6/recordHighPart3_2.txt"
    data_file_poco = "../data/bluetooth_part3/BluetoothDataHighPart3.txt"
    record_file_poco = "../data/bluetooth_part3/recordHighPart3.txt"
            
    device_name_s8 = 'Galaxy S8'        
    device_name_poco = 'Pocophone F1'
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    classic = False

    analysis_s8 = BluetoothAnalysis(data_file_s8, record_file_s8, classic)
    analysis_poco = BluetoothAnalysis(data_file_poco, record_file_poco, classic)

    means_s8 = []
    for session in analysis_s8.records['session']:
        records = analysis_s8.get_session_traces(session)
        records = analysis_s8.get_name_traces_data(device_name_s8, records)
        means_s8.append(analysis_s8.get_rssi_average_data(records))
        
    means_poco = []
    for session in analysis_poco.records['session']:
        records = analysis_poco.get_session_traces(session)
        records = analysis_poco.get_name_traces_data(device_name_poco, records)
        means_poco.append(analysis_poco.get_rssi_average_data(records))

    fit_model(distances, means_s8, device_name_s8)
    fit_model(distances, means_poco, device_name_poco)
    fit_average_model(distances, means_s8, means_poco)

    plt.show(block=True)

def fit_model(distances, mean, device):
    z = np.polyfit(distances, mean, 3)
    model = np.poly1d(z)
    model_x = np.linspace(distances[0], distances[-1], 50)
    model_y = model(model_x)

    fig, ax = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax.plot(distances, mean)
    ax.plot(model_x, model_y)
    legend = [device, 'Model']
    fig.suptitle('3rd Degree Polynomial Fit for the {0} RSSI at Various Distances'.format(device))
    ax.set_xlabel('Distance (meters)')
    ax.set_ylabel('RSSI')
    ax.legend(legend)
    print('Model for the {0}: \n{1}'.format(device, model))
 
def fit_average_model(distances, mean_1, mean_2):
    all_means = np.mean( np.array([ mean_1, mean_2 ]), axis=0 )
    z = np.polyfit(distances, all_means, 3)
    model = np.poly1d(z)
    model_x = np.linspace(distances[0], distances[-1], 50)
    model_y = model(model_x)

    fig, ax = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax.plot(distances, mean_1)
    ax.plot(distances, mean_2)
    ax.plot(model_x, model_y)
    legend = ['Galaxy S8', 'Pocophone F1', 'Model']
    fig.suptitle('3rd Degree Polynomial Fit for the Average RSSI')
    ax.set_xlabel('Distance (meters)')
    ax.set_ylabel('RSSI')
    ax.legend(legend)
    print('General Model: \n{0}'.format(model))

def plot_rssi(data_files, record_files, device_name):
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    model_distances = [0.5, 1, 2, 5, 7.5, 10, 12.5, 15, 20, 25, 30]
    classic = False
    
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
            records = analysis.get_name_traces_data(device_name, records)
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
    fig_rssi.suptitle('Average RSSI Level versus Distance at Different Advertising Settings ({0})'.format(device_name))
    ax_rssi.set_xlabel('Distance (meters)')
    ax_rssi.set_ylabel('RSSI')
    ax_rssi.legend(legend)
    ax_rssi.set_ylim([higher_value * 1.05, smaller_value * 0.95])
    
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model ({0})'.format(device_name))
    ax_model[0, 0].set_title("Ultra Low")
    ax_model[0, 0].set_ylabel('RSSI')
    ax_model[0, 0].legend(['Measured', 'Log Shadowing'])
    ax_model[0, 1].set_title("Low")
    ax_model[0, 1].legend(['Measured', 'Log Shadowing'])
    ax_model[1, 0].set_title("Medium")
    ax_model[1, 0].set_ylabel('RSSI')
    ax_model[1, 0].set_xlabel('Distance (meters)')
    ax_model[1, 0].legend(['Measured', 'Log Shadowing'])
    ax_model[1, 1].set_title("High")
    ax_model[1, 1].set_xlabel('Distance (meters)')
    ax_model[1, 1].legend(['Measured', 'Log Shadowing'])

    fig_error.suptitle('Mean Absolute Error of the Recorded Data versus the Log Shadowing Model ({0})'.format(device_name))
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
    style_file = '../style/simple_charts.mplstyle'
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)

    # plot_device_distances()
    fit_line()