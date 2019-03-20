from dhcp import dhcp_activity as dhcp
from util import time_util as timeu
from locations import locations_analysis as loc
from locations import location_plot as locp

from colour import Color

import gmplot

if __name__ == "__main__":
    dhcp_file = "data/dhcp/outputwireless-logs-20120409.DHCP_ANON.csv"
    location_file = "data/prefix_lat_lon_name_category.csv"
    analysis = dhcp.DHCPAnalysis(dhcp_file, location_file)

    # buildings = analysis.get_buildings(1)
    # categories = analysis.get_categories(1)
    # fav_building = loc.LocationsAnalysis.get_favorite(buildings)
    # fav_category = loc.LocationsAnalysis.get_favorite(categories)    

    # trip = analysis.get_trip(1)
    # trip = loc.LocationsAnalysis.filter_trips(trip)
    # for index, location in zip(range(len(trip)), trip):
    #     print("{0}: {1}".format(index, location))
    #     print()
    # print("Total: {0}".format(loc.LocationsAnalysis.get_total_distance(trip)))

    # start_user = 602
    # stop_user = 602
    # users = range(start_user, stop_user + 1)
    # colors = list(Color("#c92318").range_to(Color("#45c6f9"), len(users)))
    # gmap = gmplot.GoogleMapPlotter(29.645,-82.355, 13)
    # for user_id in users:
    #     trip = analysis.get_trip(user_id)
    #     trip = loc.LocationsAnalysis.filter_trips(trip)
    #     if (len(trip) > 0):
    #         color = colors[user_id - start_user]
    #         locp.LocationPlot.plot_trip_color(gmap, trip, color)
            
    #         for index, location in zip(range(len(trip)), trip):
    #             print("{0}: {1}".format(index, location))
    #             print()
    # gmap.draw("map.html")

    minute = 1
    events, bins = analysis.get_num_events(minute)

    fig1 = locp.LocationPlot.plot_total_events(events, bins, minute, False, True)