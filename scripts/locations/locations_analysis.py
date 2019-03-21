import operator
import geopy.distance

class LocationsAnalysis:

    @staticmethod
    def get_favorite(keys_and_times):
        """
        Gets the favorite key based upon the most visited time

        :parameters:
            keys_and_times (dict): dictionary with keys of building and value of visited time
        :returns:
            tuple (string, int): the favorite building and time visited
        """
        favorite_building = max(keys_and_times.items(), key=operator.itemgetter(1))[0]
        return favorite_building, keys_and_times[favorite_building]

    @staticmethod
    def get_distances(trip):
        """
        Gets the total distance traveled on the trip

        :returns:
            distance (double): the total distance traveled in miles
        """
        distances = []
        for visit_index in range(len(trip) - 1):
            start = trip[visit_index]    
            stop = trip[visit_index + 1]    
            coords_1 = (start.lat, start.lon)
            coords_2 = (stop.lat, stop.lon)
            distances.append(geopy.distance.vincenty(coords_1, coords_2).miles)
        return distances

    @staticmethod
    def get_total_distance(trip):
        """
        Gets the total distance traveled on the trip

        :returns:
            distance (double): the total distance traveled in miles
        """
        total_distance = 0
        for visit_index in range(len(trip) - 1):
            start = trip[visit_index]    
            stop = trip[visit_index + 1]    
            coords_1 = (start.lat, start.lon)
            coords_2 = (stop.lat, stop.lon)
            total_distance += geopy.distance.vincenty(coords_1, coords_2).miles
        return total_distance

    @staticmethod
    def filter_trips(trip):
        """
        Filters all unknown locations from the trip

        :returns:
            trip (named tuple): The trip without unknown locations
        """
        return list(filter(lambda x: x.building != None, trip))
