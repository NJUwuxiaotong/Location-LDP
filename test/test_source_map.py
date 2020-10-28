import numpy as np

from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator

latitude_file = "D:\\workspace\\paper\\location under LDP\\experim" \
                "ent spde\\Location-LDP\\data\\x_"
longitude_file = "D:\\workspace\\paper\\location under LDP\\exp" \
                 "eriment spde\\Location-LDP\\data\\y_"

left_lat = 39.97
right_lat = 40.02
low_lon = 116.29
high_lon = 116.33

# 0.00004 vmax --> 100/50
# unit_width = 0.0002  # 0.00004 0.00008 0.00012 0.00016 0.0002
unit_width = 0.00032  # 0.00008  0.00016 0.00032
ldp = LocationRandomizedGenerator(
    latitude_file, longitude_file,
    [left_lat, right_lat, low_lon, high_lon], unit_width)

ldp.get_source_map()
ldp.perturbed_location_matrix = ldp.source_location_matrix
ldp.show_perturbed_results(vmax=4000)

print(ldp.source_location_matrix.max())
print(ldp.source_location_matrix.min())

print(ldp.source_location_matrix.shape)
print(np.median(ldp.source_location_matrix))

shape = ldp.source_location_matrix.shape
x = list()
for i in range(shape[0]):
    for j in range(shape[1]):
        x.append(ldp.source_location_matrix[i, j])

x.sort()
x.reverse()
print(x[:10])
