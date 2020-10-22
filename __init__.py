from data_analysis.location_ldp import LocationLDP

latitude_file = "data/x_"
longitude_file = "data/y_"

left_lat = 39.97
right_lat = 40.02
low_lon = 116.29
high_lon = 116.33

# 0.00004 vmax --> 100/50

unit_width = 0.00012  # 0.00004 0.00008 0.00012 0.00016

ldp = LocationLDP(latitude_file, longitude_file,
                  [left_lat, right_lat, low_lon, high_lon], unit_width)
privacy = 0.1
safe_boundary = 5
# ldp.get_init_statistics()
ldp.perturb_location(privacy, safe_boundary)
ldp.show_perturbed_results()
