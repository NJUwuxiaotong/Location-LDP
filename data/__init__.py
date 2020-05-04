import pandas as pd
import numpy as np
import os
import math
import folium
from folium import plugins
import webbrowser
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import random
import json


exit(1)

num = len(latitudes)
lat_mean = sum(latitudes)/num
lon_mean = sum(longitudes)/num

schools_map = folium.Map(location=[lat_mean, lon_mean], zoom_start=10)
# marker_cluster = plugins.MarkerCluster().add_to(schools_map)

s_data = dict()
route = []
for i in range(100):
#    folium.Circle((latitudes[i], longitudes[i]), 1, color='red',
#                  fill_color='red', fillOpacity=0.2).add_to(marker_cluster)
    if (str(latitudes[i]) + "," + str(longitudes[i])) not in s_data:
        s_data[str(latitudes[i]) + "," + str(longitudes[i])] = 1
    else:
        s_data[str(latitudes[i]) + "," + str(longitudes[i])] += 1
    route.append([latitudes[i], longitudes[i]])

d_data = []
for keys, values in s_data.items():
    z = keys.split(',')
    d_data.append([float(z[0]), float(z[1]), values])

print(d_data)
HeatMap(d_data).add_to(schools_map)

#folium.PolyLine(route,
#                weight=15,  # 粗细
#                opacity=1,  # 透明度
#                color='green').add_to(marker_cluster)

schools_map.save('wxt.html')
webbrowser.open('F:\\busyfish\paper\paper\privacy preservation\locat'
                'ion under LDP\experiment spde\Location-LDP\data\wxt.html')

# San Francisco latitude and longitude values
# latitude = 37.77
# longitude = -122.42

# Create map and display it
# san_map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Display the map of San Francisco
# san_map.save('wxt.html')
# webbrowser.open('F:\\busyfish\paper\paper\privacy preservation\location under LDP\experiment spde\Location-LDP\data\wxt.html')
