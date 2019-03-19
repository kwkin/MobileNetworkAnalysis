from colour import Color

import gmplot
import numpy as np

class LocationPlot:

    @staticmethod
    def plot_trip(gmap, trip, multi_color=True):
        latitudes = [visit.lat for visit in trip]
        longitudes = [visit.lon for visit in trip]
        if (multi_color):
            colors = list(Color("#c92318").range_to(Color("#45c6f9"), len(latitudes)))

        sizes = np.linspace(15, 5, len(latitudes))
        last_index = len(latitudes) - 1
        for position_index in range(last_index):
            start_lat = trip[position_index].lat
            start_lon = trip[position_index].lon
            stop_lat = trip[position_index + 1].lat
            stop_lon = trip[position_index + 1].lon
            lats = [start_lat, stop_lat]
            lons = [start_lon, stop_lon]
            if (multi_color):
                color = colors[position_index]
            else:
                color = Color("#50cefc")
            size = sizes[position_index]
            gmap.plot(lats, lons, color.hex_l, edge_width=4, alpha=0.5)
            gmap.scatter([start_lat], [start_lon], color.hex_l, size=size, marker=False)
            
        if (multi_color):
            color = colors[last_index]
        else:
            color = Color("#50cefc")
        gmap.scatter([latitudes[last_index]], [longitudes[last_index]], color.hex_l, size=sizes[last_index], marker=False)
        

    @staticmethod
    def plot_trip_color(gmap, trip, color):
        latitudes = [visit.lat for visit in trip]
        longitudes = [visit.lon for visit in trip]

        sizes = np.linspace(15, 5, len(latitudes))
        last_index = len(latitudes) - 1
        for position_index in range(last_index):
            start_lat = trip[position_index].lat
            start_lon = trip[position_index].lon
            stop_lat = trip[position_index + 1].lat
            stop_lon = trip[position_index + 1].lon
            lats = [start_lat, stop_lat]
            lons = [start_lon, stop_lon]
            size = sizes[position_index]
            gmap.plot(lats, lons, color.hex_l, edge_width=4, alpha=0.5)
            gmap.scatter([start_lat], [start_lon], color.hex_l, size=size, marker=False)
        
        gmap.scatter([latitudes[last_index]], [longitudes[last_index]], color.hex_l, size=sizes[last_index], marker=False)
        