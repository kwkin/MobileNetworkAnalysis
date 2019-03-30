import pandas as pd

"""
Contains some common filters for getting data from the dhcp file
"""
class DHCPFilters:    

    @staticmethod
    def filter_time(traces, start_time, duration):
        """
        Filters out all times not within the provided start time and duration

        The ranges are inclusive.

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            start_time (int): starting epoch time
            duration (int): duration of the filter time
        :return:
            pandas dataframe with times only between the start time and duration
        """
        traces = traces.loc[traces['startTime'] >= start_time]
        traces = traces.loc[traces['endTime'] <= start_time + duration]
        return traces
        
    @staticmethod
    def filter_user(traces, user_id):
        """
        Filters out all traces that do not belong to the specific user id

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            user_id (int): the id of the user
        :return:
            pandas dataframe with traces belonging to the user
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        return user_traces
        
    @staticmethod
    def filter_users(traces, user_ids):
        """
        Filters out all traces that do not belong to list of users

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            user_ids (list): the list of user ids
        :return:
            pandas dataframe with traces belonging to the user
        """
        return traces.loc[user_ids.contains(traces['userMAC'])]
    
    @staticmethod
    def filter_building(traces, locations, building_name):
        """
        Filters out all traces that do not visit the specified building

        :parameters:
            traces(pandas dataframe): the dhcp data frame to filter
            locations(pandas dataframe): the locations data
            building_name (str): the name of the building
        :returns:
            pandas dataframe with traces for the specific location
        """
        # TODO
        return traces