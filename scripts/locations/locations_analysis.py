import operator

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
    def get_positions():
        print("Get positions.")
