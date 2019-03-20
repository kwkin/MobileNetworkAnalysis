from colour import Color

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    
    @staticmethod
    def plot_total_events(count, bins, minutes):
        fig, ax = plt.subplots()
                
        plt.bar(bins, count, align='edge', width=1)
        max_value = np.amax(count)
        max_date = bins[np.argmax(count)]
        min_value = np.min(count)
        min_date = bins[np.argmin(count)]                    
        if (minutes == 1):
            plt.title('Number of DHCP Events every minute')
        else:
            plt.title('Number of DHCP Events every {0} minutes')

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
        plt.show()