from dhcp import dhcp_activity as dhcp
from locations import locations_analysis as loc
from locations import location_plot as locp
from util import image_util as imageu
from util import time_util as timeu

from colour import Color

import gmplot
import numpy as np

# TODO look into density modular
# TODO construct densitiy information for paths at specific times
# TODO get distance between paths (for now use WGS84 reference elipsoid, but later explain how this can be modified for google map routes)
# TODO construct weighted routes between notes based upon density, and map routes
if __name__ == "__main__":
    dhcp_file = "data/dhcp/outputwireless-logs-20120409.DHCP_ANON.csv"
    location_file = "data/prefix_lat_lon_name_category_main_campus.csv"
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

    # 120 is a good path
    start_user = 120
    stop_user = 120
    users = range(start_user, stop_user + 1)
    colors = list(Color("#c92318").range_to(Color("#45c6f9"), len(users)))
    gmap = gmplot.GoogleMapPlotter(29.645,-82.355, 13)
    for user_id in users:
        trip = analysis.get_user_trip(user_id)
        trip = loc.LocationsAnalysis.filter_trips(trip)
        if (len(trip) > 0):
            color = colors[user_id - start_user]
            locp.LocationPlot.plot_trip(gmap, trip, color, True, True)
            # refined_trip = dhcp.DHCPAnalysis.trace_refine_trip(trip, 60)
            # locp.LocationPlot.plot_trip_color(gmap, refined_trip, Color("#ffffff"))
            # for index, location in zip(range(len(trip)), trip):
            #     print("{0}: {1}".format(index, location))
            #     print()
    gmap.draw("map.html")

    # minute = 1
    # events, bins = analysis.get_num_eventsvents(events, bins, minute)
    # fig1 = locp.LocationPlot.plot_total_e
    # buildings = analysis.get_events_per_building()
    # print(buildings)

    # TODO generate heatmap with a weight dependent upon density, distance, and total time spent
    # start_time = analysis.earliest_time
    # duration = 86400
    # buildings = analysis.get_unique_events_per_building_time(start_time, duration)
    # buildings = analysis.get_locations_from_buildings(buildings)
    # locp.LocationPlot.plot_building_heatmap(buildings)
    # print("Finished")
    
    # # TODO merge commands in a single pipeline of generating the heatmap
    # start_time = analysis.earliest_time + 900 * 70
    # stop_time = analysis.latest_time
    # duration = 900
    # starts = np.arange(start_time, stop_time, duration)
    # stop_index = starts.size

    # # 67
    # # Generate heatmaps for each time slot
    # for index, start in zip(range(1, stop_index + 1), starts):
    #     buildings = analysis.get_unique_events_per_building_time(start, duration)
    #     buildings = analysis.get_locations_from_buildings(buildings)
    #     stop = start + duration
    #     # locp.LocationPlot.plot_building_heatmap(buildings, start, stop)
    #     print("Generating Heatmap")
    #     locp.LocationPlot.generate_heatmap(buildings, start, stop)
    #     print("Finished {0} / {1}".format(index, stop_index))

    # # TODO create method to add opacity to the image
    # print("Merging")
    # outputfile = imageu.ImageUtil.convert_images_to_gif("./output", 500)
    # locp.LocationPlot.create_map_overlay(buildings, outputfile, 'map_Monday')
    # print("Finished")