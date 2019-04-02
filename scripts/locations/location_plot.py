from colour import Color
from scipy import stats
from util import time_util as timeu
from gmplot.color_dicts import html_color_codes

from .trip_visit import Visit
from .building import Building

import datetime as dt
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import gmplot
import numpy as np
import os

class LocationPlot:
    @staticmethod
    def plot_trip(gmap, trip, multi_color=True, scatter=False, marker=True):
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
            if scatter:
                gmap.scatter([start_lat], [start_lon], color.hex_l, size=size, marker=False)
            if marker:
                LocationPlot.add_visits(trip, gmap)
            
        if (multi_color):
            color = colors[last_index]
        else:
            color = Color("#50cefc")
        if scatter:
            gmap.scatter([latitudes[last_index]], [longitudes[last_index]], color.hex_l, size=sizes[last_index], marker=False)
        if marker:
            LocationPlot.add_visits(trip, gmap)
        

    @staticmethod
    def plot_trip_color(gmap, trip, color=Color("#c92318"), scatter=False, marker=True):

        # TODO split visitation as separate class
        sizes = np.linspace(15, 5, len(trip))
        last_index = len(trip) - 1
        building_visits = []
        for position_index in range(last_index):
            start_lat = trip[position_index].lat
            start_lon = trip[position_index].lon
            stop_lat = trip[position_index + 1].lat
            stop_lon = trip[position_index + 1].lon
            lats = [start_lat, stop_lat]
            lons = [start_lon, stop_lon]
            size = sizes[position_index]
            gmap.plot(lats, lons, color.hex_l, edge_width=4, alpha=0.5)
            if scatter:
                gmap.scatter([start_lat], [start_lon], color.hex_l, size=size, marker=False)

        position_index += 1
        if scatter:
            gmap.scatter([trip[last_index].lat], [trip[last_index].lon], color.hex_l, size=sizes[last_index], marker=False)
        if marker:
            LocationPlot.add_visits(trip, gmap)
    
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
    def map_values_with_area(densities, min_r=1, max_r=50):
        radii = []
        for density in densities:
            radius = LocationPlot.get_radius_from_circle_area(density)
            radius = max(radius, min_r)
            radius = min(radius, max_r)
            radii.append(radius)
        radii = np.array(radii)
        max_radii = radii.max()
        scale = math.floor(max_r / max_radii)
        radii *= scale
        return radii

    @staticmethod
    def generate_heatmap(densities, time_start, time_stop, out_dir="output"):
        grid_points = 150
        lats = np.array([visit.lat for visit in densities])
        lons = np.array([visit.lon for visit in densities])
        events = np.array([visit.density for visit in densities])

        lon_range = np.ptp(lons)
        lon_min = lons.min() - lon_range / 3
        lon_max = lons.max() + lon_range / 3
        lon_step = lon_range / grid_points

        lat_range = np.ptp(lats)
        lat_min = lats.min() - lat_range / 3
        lat_max = lats.max() + lat_range / 3
        lat_step = lat_range / grid_points

        # Generate heatmap values
        lon_grid, lat_grid = np.mgrid[lon_min:lon_max:lon_step, lat_min:lat_max:lat_step]
        positions = np.vstack([lon_grid.ravel(), lat_grid.ravel()])
        values = np.vstack([lons, lats])
        kernel = stats.gaussian_kde(values, weights=events)
        heatmap = np.reshape(kernel(positions), lon_grid.shape)

        # Normalize heatmap over all frames
        # Create heatmap figure
        fig = plt.figure(frameon=True)
        ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.tick_params(which='both', direction='in')
        fig.add_axes(ax)
        ax.imshow(np.rot90(heatmap),cmap='coolwarm', alpha=0.4, extent=[lon_min, lon_max, lat_min, lat_max])
        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

        file_name = 'event_heatmap_{0}_{1}.png'.format(time_start, time_stop)
        file_path = os.path.join(out_dir, file_name)
        fig.savefig(file_path, format='png', dpi=300, transparent=True, bbox_inches=extent, pad_inches=0)
        plt.close(fig)
        return file_path

    @staticmethod
    def plot_building_heatmap(densities, start, stop, change_radii=True):
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

        heatmap = LocationPlot.generate_heatmap(densities, start, stop)

        # Overlay on plot
        img_bounds = {}
        img_bounds['west'] = (lon_min - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['east'] = (lon_max - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['north'] = (lat_max - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt
        img_bounds['south'] = (lat_min - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt

        gmap = gmplot.GoogleMapPlotter(lat_center, lon_center, zoom=15)
        gmap.ground_overlay(heatmap, img_bounds)
        if change_radii:
            radii = LocationPlot.map_values_with_area(events)
            for lat, lon, radius in zip(lats, lons, radii):
                gmap.scatter([lat], [lon], '#3B0B39', alpha=0.4, size=radius, marker=False)
        else:
            gmap.scatter(lats, lons, '#3B0B39', alpha=0.4, size=20, marker=False)
            
        file_name = 'map_{0}_{1}.html'.format(start, stop)
        gmap.draw(file_name)

    @staticmethod
    def create_map_overlay(densities, heatmap, title="map"):
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

        # Overlay on plot
        img_bounds = {}
        img_bounds['west'] = (lon_min - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['east'] = (lon_max - lon_midpt) * (grid_points / (grid_points - 1)) + lon_midpt
        img_bounds['north'] = (lat_max - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt
        img_bounds['south'] = (lat_min - lat_midpt) * (grid_points / (grid_points - 1)) + lat_midpt

        gmap = gmplot.GoogleMapPlotter(lat_center, lon_center, zoom=15)
        gmap.ground_overlay(heatmap, img_bounds)
        gmap.scatter(lats, lons, '#3B0B39', alpha=0.5, size=20, marker=False)
        
        file_name = '{0}.html'.format(title)
        gmap.draw(file_name)

    @staticmethod
    def get_radius_from_circle_area(area):
        """
        Computes the radius of a circle given the area
        """
        radius_squared = math.sqrt(area / math.pi)
        radius = math.sqrt(radius_squared)
        return radius

    @staticmethod
    def add_visits(visits, gmap, marker_color=html_color_codes['maroon']):
        # Convert duration from seconds to minutes
        buildings_visited = set()
        for visit in visits:
            building = Building(building=visit.building, lat=visit.lat, lon=visit.lon, density=0)
            buildings_visited.add(building)

        for building in buildings_visited:
            visits_at_building = [i for i, x in enumerate(visits) if x.building == building.building]
            
            title = ""
            for visit_index in visits_at_building:
                visit = visits[visit_index]
                ts = pd.to_datetime(visit.start, unit='s')
                ts = ts.tz_localize('UTC')
                start_time = dt.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second).strftime('%H:%M:%S')
                time_sense_last = 0
                if (visit_index < len(visits) - 1):
                    time_sense_last = visits[visit_index + 1].start - visits[visit_index].start
                title += 'Stop: ' + str(visit_index) + '\\n'
                title += 'Building: ' + visit.building + '\\n'
                title += 'Start: ' + str(start_time) + '\\n'
                title += 'Duration: ' + timeu.display_time(visit.duration) + '\\n'
                title += 'Time Before Next: ' + timeu.display_time(time_sense_last) + '\\n\\n'
            gmap.marker(building.lat, building.lon, color=marker_color, title=title)
