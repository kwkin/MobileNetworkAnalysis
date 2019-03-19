# -*- coding: utf-8 -*-
from collections import namedtuple
import calendar
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ntpath
import math
import operator
import pandas as pd
import pytz
import re

class DHCPAnalysis:
    def __init__(self, dhcp_file, location_file):
        self.file = dhcp_file
        self.location_file = location_file
        self.traces = pd.read_csv(dhcp_file)
        self.locations = pd.read_csv(location_file)
    
    def get_user_events(self, user_id):
        return DHCPAnalysis.get_trace_user_events(self.traces, user_id)
    
    @staticmethod
    def get_trace_user_events(traces, user_id):
        user_traces = traces.loc[traces['userMAC'] == user_id]
        return user_traces

    def get_buildings(self, user_id):
        return DHCPAnalysis.get_trace_buildings(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_buildings(traces, locations, user_id):
        """
        Gets the user's favorite building  and time spent within the building. 

        :returns:
            dictionary with keys of building and values with time duration
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        visited_buildings = {}
        for index, row in user_traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = locations.loc[locations['prefix'] == prefix]
            timespent = row['endTime'] - row['startTime']
            if (building.size == 0):
                visited_buildings['unknown'] += timespent
            else:
                building_name = building['name'].values[0]
                if (building_name not in visited_buildings):
                    visited_buildings[building_name] = timespent
                else:
                    visited_buildings[building_name] += timespent
        return visited_buildings
    
    def get_categories(self, user_id):
        return DHCPAnalysis.get_trace_categories(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_categories(traces, locations, user_id):
        """
        Gets the users favorite building catogries and time spent within the building category. 

        :returns:
            dictionary with keys of building category and values with time duration
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        visited_categories = {}
        for index, row in user_traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = locations.loc[locations['prefix'] == prefix]
            timespent = row['endTime'] - row['startTime']
            if (building.size == 0):
                visited_categories['unknown'] += timespent
            else:
                category = building['category'].values[0]
                if (category not in visited_categories):
                    visited_categories[category] = timespent
                else:
                    visited_categories[category] += timespent
        return visited_categories
    
    def get_trip(self, user_id):
        return DHCPAnalysis.get_trace_trip(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_trip(traces, locations, user_id):
        """
        Gets the users path. 
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        previous_lat = ""
        previous_lon = ""
        previous_building = ""

        trip = []
        current_duration = 0
        Visit = namedtuple("Visit", "building lat lon duration")
        for index, row in user_traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            location = locations.loc[locations['prefix'] == prefix]
            if (location.size > 0):
                building = location['name'].values[0]
            else:
                building = None

            if (index == user_traces.values.size - 1):
                trip.append(Visit(building=previous_building, lat=previous_lat, lon=previous_lon, duration=current_duration))
            elif (previous_building != building):
                # Add visit as a new location if it does not match previous prefix
                previous_building = building
                if (location.size > 0):
                    previous_lat = location['lat'].values[0]
                    previous_lon = location['lon'].values[0]
                else:
                    previous_lat = None
                    previous_lon = None
                current_duration = row['endTime'] - row['startTime']
                trip.append(Visit(building=previous_building, lat=previous_lat, lon=previous_lon, duration=current_duration))
            else:
                # Add to the previous visit duration if it matches previous prefix
                timespent = row['endTime'] - row['startTime']
                current_duration += timespent
        return trip

