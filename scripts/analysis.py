from dhcp import dhcp_activity as dhcp
from util import time_util as timeu
from locations import locations_analysis as loc

if __name__ == "__main__":  
    dhcp_file = "data/dhcp/outputwireless-logs-20120407.DHCP_ANON.csv"
    location_file = "data/prefix_lat_lon_name_category.csv"
    analysis = dhcp.DHCPAnalysis(dhcp_file, location_file)

    buildings = analysis.get_buildings(1)
    categories = analysis.get_categories(1)
    fav_building = loc.LocationsAnalysis.get_favorite(buildings)
    fav_category = loc.LocationsAnalysis.get_favorite(categories)    
    trip = analysis.get_trip(1)
    for location in trip:
        print(location)
        print()