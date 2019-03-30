# -*- coding: utf-8 -*-
from locations import trip_visit as visit
from locations import building

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
        self.dhcp_file = dhcp_file
        self.location_file = location_file
        self.traces = pd.read_csv(dhcp_file)
        self.locations = pd.read_csv(location_file)
        self.earliest_time = self.traces['startTime'].min()
        self.latest_time = self.traces['endTime'].max()
    
    def get_num_events(self, minutes):
        return DHCPAnalysis.get_trace_num_events(self.traces, minutes)
        
    @staticmethod
    def get_trace_num_events(traces, minutes):
        """
        Gets the number of events that occured between the specified minutes

        The events are allocated to each appropriate minute bin.
        """
        seconds = minutes * 60.0
        earliest_time = traces['startTime'].min()
        latest_time = traces['endTime'].max()
        num_periods = math.floor((latest_time - earliest_time) / seconds) + 1
        bins = range(0, num_periods)
        num_events = np.zeros(len(bins))

        for index, row in traces.iterrows():
            start_time = row['startTime']
            end_time = row['endTime']
            num_affected_bins = math.floor((end_time - start_time) / (seconds)) + 1
            start_bin = math.floor((start_time - earliest_time) * minutes / 60)
            for bin_index in range(start_bin, start_bin + num_affected_bins):
                bin_index = min(bin_index, len(bins) - 1)
                num_events[bin_index] += 1
        return num_events, bins

    def get_user_buildings(self, user_id):
        return DHCPAnalysis.get_trace_user_buildings(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_user_buildings(traces, locations, user_id):
        """
        Gets the user's visited buildings and time spent within the building. 

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
                building_name = 'unknown'
            else:
                building_name = building['name'].values[0]
                
            if (building_name not in visited_buildings):
                visited_buildings[building_name] = timespent
            else:
                visited_buildings[building_name] += timespent
        return visited_buildings

    def get_user_visited_buildings(self, user_id):
        return DHCPAnalysis.get_trace_user_buildings(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_user_visited_buildings(traces, locations, user_id):
        """
        Gets the user's visited buildings and time spent within the building. 

        :returns:
            dictionary with keys of building and values with time duration
        """
        user_traces = dhcpf.filter_user(traces, user_id)
        access_points = user_traces['APNAME'].unique()
        visited_buildings = set()
        for access_point in access_points:
            prefix = re.findall('[a-zA-Z]+', access_point)[0]
            building = locations.loc[locations['prefix'] == prefix]
            if (building.size == 0):
                visited_buildings.add('unknown')
            else:
                visited_buildings.add(building['name'].values[0])
        return visited_buildings
    
    def get_user_categories(self, user_id):
        return DHCPAnalysis.get_trace_user_categories(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_user_categories(traces, locations, user_id):
        """
        Gets the users favorite building catogries and time spent within the building category. 

        :returns:
            dictionary with keys of building category and values with time duration
        """
        user_traces = dhcpf.filter_user(traces, user_id)
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
    
    def get_user_trip(self, user_id):
        return DHCPAnalysis.get_trace_user_trip(self.traces, self.locations, user_id)

    @staticmethod
    def get_trace_user_trip(traces, locations, user_id):
        """
        Gets the users path. 
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        previous_lat = ""
        previous_lon = ""
        previous_building = ""

        trip = []
        current_duration = 0
        start_time = 0
        for index, row in user_traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            location = locations.loc[locations['prefix'] == prefix]
            if (location.size > 0):
                building = location['name'].values[0]
            else:
                building = None

            if (index == user_traces.values.size - 1):
                trip.append(visit.Visit(building=previous_building, lat=previous_lat, lon=previous_lon, start=start_time, duration=current_duration))
            elif (previous_building != building):
                # Add visit as a new location if it does not match previous prefix
                previous_building = building
                if (location.size > 0):
                    previous_lat = location['lat'].values[0]
                    previous_lon = location['lon'].values[0]
                else:
                    previous_lat = None
                    previous_lon = None
                start_time = row['startTime']
                current_duration = row['endTime'] - start_time
                trip.append(visit.Visit(building=previous_building, lat=previous_lat, lon=previous_lon, start=start_time, duration=current_duration))
            else:
                # Add to the previous visit duration if it matches previous prefix
                timespent = row['endTime'] - row['startTime']
                current_duration += timespent
        return trip

    @staticmethod
    def trace_refine_trip(trip, threshold):
        refined_trip = []
        for location in trip:
            duration = location.duration
            if (duration >= threshold):
                refined_trip.append(location)
        return refined_trip

    def get_events_per_building(self):
        """
        Calculates the number of events at each building
        
        :returns:
            events (dict): a dictionary with building keys a values with unique events
        """
        buildings = self.locations['name'].values
        building_count = {}
        for building in buildings:
            building_count[building] = 0
        building_count['unknown'] = 0
        
        for index, row in self.traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = self.locations.loc[self.locations['prefix'] == prefix]
            if (building.size == 0):
                building = 'unknown'
            else:
                building = building['name'].values[0]
            building_count[building] += 1
        return building_count

    @staticmethod
    def get_trace_events_per_building(traces, locations):
        buildings = locations['name'].values
        building_count = {}
        for building in buildings:
            building_count[building] = 0
        building_count['unknown'] = 0
        
        for index, row in traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = locations.loc[locations['prefix'] == prefix]
            if (building.size == 0):
                building = 'unknown'
            else:
                building = building['name'].values[0]
            building_count[building] += 1
        return building_count

    def get_unique_events_per_building(self):
        """
        Calculates the number of unique device IDs that visit each building
        
        :returns:
            events (dict): a dictionary with building keys a values with unique events
        """
        return DHCPAnalysis.get_trace_unique_events_per_building(self.traces, self.locations)

    @staticmethod
    def get_trace_unique_events_per_building(traces, locations):
        buildings = locations['name'].values
        building_count = {}
        for building in buildings:
            building_count[building] = 0
        building_count['unknown'] = 0
        
        first_user_id = traces['userMAC'].min()
        last_user_id = traces['userMAC'].max()
        for user_index in range(first_user_id, last_user_id):
            visited_buildings = DHCPAnalysis.get_trace_user_visited_buildings(traces, locations, user_index)
            for visited_building in visited_buildings:
                building_count[visited_building] += 1
        return building_count

    def get_unique_events_per_building_time(self, start_time, seconds):
        """
        Calculates the number of unique device IDs that visit each building in the specified time interval
        
        :returns:
            events (dict): a dictionary with building keys a values with unique events
        """
        return DHCPAnalysis.get_trace_unique_events_per_building_time(self.traces, self.locations, start_time, seconds)

    @staticmethod
    def get_trace_unique_events_per_building_time(traces, locations, start_time, seconds):        
        traces = traces.loc[traces['startTime'] >= start_time]
        traces = traces.loc[traces['endTime'] <= start_time + seconds]
        return DHCPAnalysis.get_trace_unique_events_per_building(traces, locations)

    def get_locations_from_buildings(self, buildings):
        return DHCPAnalysis.get_trace_locations_from_buildings(buildings, self.locations)

    @staticmethod
    def get_trace_locations_from_buildings(buildings, locations):
        buildings_and_locations = []
        for name, density in buildings.items():
            building_row = locations.loc[locations['name'] == name]
            if (building_row.size != 0):
                latitude = building_row['lat'].values[0]
                longitude = building_row['lon'].values[0]
                buildings_and_locations.append(building.Building(building=name, lat=latitude, lon=longitude, density=density))
        return buildings_and_locations
    
    def get_weights(self, start_location, stop_location, start_time, stop_time):
        return DHCPAnalysis.get_trace_weights(self.traces, self.locations, start_location, stop_location, start_time, stop_time)

    @staticmethod
    def get_trace_weights(buildings, locations, start_location, stop_location, start_time, stop_time):
        # Get distance between start and stop

        # Get activity/density between start and stop at the location
        return 0