import numpy as np
import matplotlib.pyplot as plt
import ntpath
import pandas as pd

class BluetoothAnalysis:
    def __init__(self, data_file, record_file, classic=False):
        self.data_file = data_file
        self.record_file = record_file

        self.data = pd.read_csv(self.data_file, sep='\t', header=None)
        self.records = pd.read_csv(self.record_file, sep='\t', header=None)

        if (classic):
            self.data.columns = ['timestamp', 'scanner', 'scanned', 'name', 'rssi']
        else:
            self.data.columns = ['timestamp', 'name', 'mac', 'power', 'rssi']
        
        self.records.columns = ['session', 'start', 'stop']
    

    def get_session_traces(self, session):
        return self.get_session_traces_data(session, self.data)

    def get_session_traces_data(self, session, data):
        """
        Gets the traces within the specified session number.

        The data will be obtained for multiple session numbers.
        """
        record_traces = self.records[self.records['session'] == session]
        start_times = record_traces['start'].values
        stop_times = record_traces['stop'].values

        for index, start, stop in zip(range(start_times.size), start_times, stop_times):            
            if (index == 0):
                session_data = data[(data['timestamp'] >= start) & (data['timestamp'] <= stop)]
            else:
                session_data = session_data.append(data[(data['timestamp'] >= start) & (data['timestamp'] <= stop)])

        return session_data

    def get_name_traces(self, name):
        return self.get_name_traces_data(name, self.data)
        
    def get_name_traces_data(self, name, data):
        return data[data['name'] == name]

    def get_rssi_average(self):
        return self.get_rssi_average_data(self.data)

    def get_rssi_average_data(self, data):
        return data['rssi'].mean()