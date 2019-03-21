from colour import Color
from scipy import stats

import math
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

    @staticmethod
    def plot_building_heatmap(densities):
        grid_points = 150
        lats = np.array([visit.lat for visit in densities])
        lons = np.array([visit.lon for visit in densities])
        events = np.array([visit.density for visit in densities])

        lon_range = np.ptp(lons)
        lon_min = lons.min() - lon_range / 3
        lon_max = lons.max() + lon_range / 3
        lon_step = lon_range / grid_points
        lon_center = np.median(lons)
        lon_midpt = np.mean([lon_min, lon_max])

        lat_range = np.ptp(lats)
        lat_min = lats.min() - lat_range / 3
        lat_max = lats.max() + lat_range / 3
        lat_step = lat_range / grid_points
        lat_center = np.median(lats)
        lat_midpt = np.mean([lat_min, lat_max])

        # Generate heatmap values
        lon_grid, lat_grid = np.mgrid[lon_min:lon_max:lon_step, lat_min:lat_max:lat_step]
        positions = np.vstack([lon_grid.ravel(), lat_grid.ravel()])
        values = np.vstack([lons, lats])
        kernel = stats.gaussian_kde(values, weights=events)
        heatmap = np.reshape(kernel(positions), lon_grid.shape)

        # Create heatmap figure
        fig = plt.figure(frameon=True)
        ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.tick_params(which='both', direction='in')
        fig.add_axes(ax)
        ax.imshow(np.rot90(heatmap),cmap='coolwarm', alpha=0.4, extent=[lon_min, lon_max, lat_min, lat_max])
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig('building_heatmap.png', format='png', dpi=300, transparent=True, bbox_inches=extent, pad_inches=0)

        # Overlay on plot
        img_bounds = {}
        img_bounds['west'] = (lon_min - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['east'] = (lon_max - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['north'] = (lat_max - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt
        img_bounds['south'] = (lat_min - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt

        gmap = gmplot.GoogleMapPlotter(lat_center, lon_center, zoom=15)
        gmap.ground_overlay('building_heatmap.png', img_bounds)
        gmap.scatter(lats, lons, '#3B0B39', size=20, marker=False)
        gmap.draw('map.html')