from dhcp import dhcp_activity as dhcp
from dhcp import dhcp_filters as dhcpf
from locations import locations_analysis as loc
from locations import location_plot as locp
from locations import location_writer as locw
from util import image_util as imageu
from util import time_util as timeu

from colour import Color

import gmplot
import numpy as np

# TODO look into density modular
# TODO construct densitiy information for paths at specific times
# TODO get distance between paths (for now use WGS84 reference elipsoid, but later explain how this can be modified for google map routes)
# TODO construct weighted routes between notes based upon density, and map routes
# TODO difficulty in determining whether a trip is the start of a new day, or if the user just
# stayed at the last location for a long time. For this, we can just assume that this is a trip,
# since the user will take a trip if it is the next day.
if __name__ == "__main__":
    dhcp_file = "data/dhcp/20120407_buildings.csv"
    # dhcp_file = "data/dhcp/20120409_buildings.csv"
    location_file = "data/prefix_lat_lon_name_category_main_campus.csv"
    # dhcp_file = "D:/Development/data/dhcp/DHCP_April_2012_ANON_MAC.csv"

    analysis = dhcp.DHCPAnalysis(dhcp_file, location_file)
    # minutes = 60
    # analysis.get_in_trips(minutes)