# DHCP_static_analysis
Some scripts used to analyze and visualize DHCP logs and pedestrian traffic on a university campus. Additional scripts are added to present expiremental measurements of bluetoosh RSSI. The plots are created using Matplotlib. 

## Sample Plots
The following contains a subset of generated plots.

### DHCP Analysis
![DHCP Events](/img/Monday_2012-04-09_1min.png)

DHCP events grouped in 1 minute bins. If a timestamp intersects the bin time, then an event is added to the corresponding bin. Moreover, if an event’s start to end timestamps span multiple bins, then an event is added to each of the overlapping bins. The time with the most events is indicated by a yellow annotation and the time with the least events indicated using a pink annotation. 

![DHCP Events With Class Periods](/img/Monday, 2012-04-09_1min_periods.png)

DHCP events grouped in 1 minute bins. The beginning and ending timestamps of class periods is illustrated with an orange and green line.

### Bluetooth RSSI Analysis
![RSSI Analysis](/img/rssi_s1.png)

Bluetooth RSSI compared to the log shadowing model. The advertiser device was a Pocophone F1, and the scanning device was a Pixel 2 XL. The experiment was conducted in a open, empty room. The stationary device was advertising, while the other device was scanning. The advertiser broadcasted at four settings: ultra-low, low, medium, and high. The scanning device was placed at the following distances: 0.5m, 1m, 5m, 10m, 20m, 25m, and 30m. The scanning device was set to record for approximately 8 seconds at each distance, and the measurements were repeated for each power setting. 

![RSSI vs_Distance](/img/galaxy-s8_versus_pocophone_distance.png)

RSSI versus distance in a mobility scenario. The advertiser started at a set at a distance of approximately 10 meters, walked past the advertiser (coming into contact at a minimum of around 1 meter), and stopped at approximately 10 meters in the opposite direction of the sender. This procedure was conducted for classic Bluetooth and each of the transmission power settings. 
