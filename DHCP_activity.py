# -*- coding: utf-8 -*-
import calendar
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ntpath
import math
import pandas as pd
import pytz
import re

class DHCPAnalysis:
    def __init__(self, file):
        self.file = file
        self.traces = pd.read_csv(file)
        
        self.time_zone = pytz.timezone('US/Eastern')
        self.traces['startTime'] = pd.to_datetime(self.traces['startTime'], unit='s')
        self.traces['startTime'] = pd.DatetimeIndex(self.traces['startTime']).tz_localize('UTC')
        self.traces['endTime'] = pd.to_datetime(self.traces['endTime'], unit='s')
        self.traces['endTime'] = pd.DatetimeIndex(self.traces['endTime']).tz_localize('UTC')
        self.earliest_time = self.traces['startTime'].min()
        self.latest_time = self.traces['endTime'].max()
                
        # Get the date from the file name
        fileName = ntpath.basename(self.file)
        date_string = re.findall('[0-9]{8}', fileName)[0]
        self.date = dt.datetime.strptime(date_string, '%Y%m%d')
        
        # Create periods
        start_period = self.date.replace(hour=7, minute=25, tzinfo=pytz.utc)
        self.period_length = 50
        break_length = 15
        num_periods = 11
        self.periods = self.create_periods(start_period, self.period_length, break_length, num_periods)
        
    def calculate_events(self, minutes):
        num_periods = math.floor((self.latest_time - self.earliest_time).total_seconds() / (60.0 * minutes)) - 1
        latest_time_floored = self.earliest_time + dt.timedelta(minutes=minutes * num_periods)
        bins = pd.date_range(start=self.earliest_time, end=latest_time_floored, periods=num_periods + 1)
        bins_array = np.array(bins)
        num_events = np.zeros(bins.size)
        for index, row in self.traces.iterrows():
            start_time = row['startTime'].to_datetime64()
            end_time = row['endTime'].to_datetime64()
            num_bins = math.floor((end_time - start_time) / (minutes * 60 * 1e9)) + 1
            start_index = np.searchsorted(bins_array, start_time, side='right') - 1
            for hist_index in range(start_index, start_index + num_bins):
                hist_index = min(hist_index, num_events.size - 1)
                num_events[hist_index] += 1
        bins = self.get_strings_from_dates(bins)
        return num_events, bins
        
    def get_strings_from_dates(self, dates):
        strings = []
        for index in range(dates.size):
            ts = dates[index]
            date_str = dt.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second).strftime('%H:%M:%S')
            strings.append(date_str)
        return np.array(strings)
    
    def plot_events(self, count, bins, minutes, overlay_periods=True, min_and_max=True, dpi=96):
        fig, ax = plt.subplots()
        fig.set_figheight(1080/dpi)
        fig.set_figwidth(1920/dpi)
        fig.dpi = dpi
                
        plt.bar(bins, count, align='edge', width=1)
        max_value = np.amax(count)
        max_date = bins[np.argmax(count)]
        min_value = np.min(count)
        min_date = bins[np.argmin(count)]
        
        # Add annotations for the min and max 
        if (min_and_max):
            plt.annotate(
                    "value = {0}\ntime = {1}".format(max_value, max_date), 
                    xy=(max_date, max_value), 
                    xytext=[-150, 20],
                    textcoords='offset pixels',
                    bbox=dict(boxstyle='round,pad=0.5', fc='#D4CA3A', alpha=0.5),
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
            plt.annotate(
                    "min = {0}\ntime = {1}".format(min_value, min_date), 
                    xy=(min_date, min_value), 
                    xytext=[-150, 20],
                    textcoords='offset pixels',
                    bbox=dict(boxstyle='round,pad=0.5', fc='#FF6DAE', alpha=0.5),
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
                    
        # Draw vertical lins to indicate the start and stop of periods
        if (overlay_periods):
            for period in self.periods:
                start_epoch_time = period.timestamp()
                period_start = self.translate(start_epoch_time, self.earliest_time.timestamp(), self.latest_time.timestamp(), 0, bins.size)
                plt.axvline(x=period_start, linewidth=2, color='#E28544', alpha=0.5)
                end_epoch_time = start_epoch_time + self.period_length * 60
                period_end = self.translate(end_epoch_time, self.earliest_time.timestamp(), self.latest_time.timestamp(), 0, bins.size)
                plt.axvline(x=period_end, linewidth=2, color='#5DB15A', alpha=0.5)
                                               
        day_title = self.get_day_from_file_name()
        if (minutes == 1):
            plt.title('Number of DHCP Events every minute for {0}'.format(day_title))
        else:
            plt.title('Number of DHCP Events every {0} minutes for {1}'.format(minutes, day_title))
           
        # Add minor ticks if there are too many major ticks
        plt.xlabel('Time (HH:MM:SS)')
        plt.xticks(rotation=70)
        if (minutes >= 60):
            majorLocator = ticker.MultipleLocator(1)
            ax.xaxis.set_major_locator(majorLocator)
        elif (minutes >= 30):
            majorLocator = ticker.MultipleLocator(2)
            minorLocator = ticker.MultipleLocator(1)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
        elif (minutes >= 15):
            majorLocator = ticker.MultipleLocator(4)
            minorLocator = ticker.MultipleLocator(1)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
        elif (minutes >= 10):
            majorLocator = ticker.MultipleLocator(6)
            minorLocator = ticker.MultipleLocator(1)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
        elif (minutes >= 5):
            majorLocator = ticker.MultipleLocator(12)
            minorLocator = ticker.MultipleLocator(1)
            ax.xaxis.set_major_locator(majorLocator)
            ax.xaxis.set_minor_locator(minorLocator)
        else:
            majorLocator = ticker.MultipleLocator(60)
            ax.xaxis.set_major_locator(majorLocator)
        ax.set_ylim([0, max_value * 1.15])
        plt.gcf().subplots_adjust(bottom=0.2)
        
        plt.ylabel('Number of Events')
        return fig
    
    def create_periods(self, start_period, period_length, break_length, num_periods):
        periods = np.empty(num_periods, dtype=dt.datetime)
        for index in range(num_periods):
            minute_offset = index * (period_length + break_length)
            periods[index] = start_period + dt.timedelta(minutes=minute_offset)
        return periods
    
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)
        
    def get_day_from_file_name(self):
        day_of_week = calendar.day_name[self.date.weekday()]
        day_and_date = '{0}, {1}'.format(day_of_week, self.date.date())
        return day_and_date
        
if __name__ == "__main__":
    style_file = 'simple_charts.mplstyle'
#    data_file = '../data/outputwireless-logs-20120407.DHCP_ANON.csv'
    data_file = '../data/outputwireless-logs-20120409.DHCP_ANON.csv'
#    data_file = '../data/sample_20120407.csv'
    minutes = [1, 5, 10, 15, 30, 60]
#    minutes = [5]
    dpi = 96
    
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)
    
    if (ntpath.isfile(data_file)):
        analysis_20120407 = DHCPAnalysis(data_file)
        for minute in minutes:
            num_events, bins = analysis_20120407.calculate_events(minute)
            fig1 = analysis_20120407.plot_events(num_events, bins, minute, False, True, dpi=dpi)
            fig1.savefig("{0}_{1}min".format(analysis_20120407.get_day_from_file_name(), minute), dpi=dpi)
            fig2 = analysis_20120407.plot_events(num_events, bins, minute, True, False, dpi=dpi)
            fig2.savefig("{0}_{1}min_periods".format(analysis_20120407.get_day_from_file_name(), minute), dpi=dpi)
    else:
        print('Error: File {0} does not exist'.format(data_file))
    