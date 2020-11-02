import numpy as np

from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator, show_perturbed_results


class TestSourceMap(object):
    def __init__(self, latitude_file, longitude_file, location_range,
                 unit_width):
        self.latitude_file = latitude_file
        self.longitude_file = longitude_file
        self.location_range = location_range
        self.unit_width = unit_width

    def execute_test(self):
        ldp = LocationRandomizedGenerator(
            self.latitude_file, self.longitude_file, self.location_range,
            self.unit_width)

        ldp.get_source_map()
        ldp.perturbed_location_matrix = ldp.source_location_matrix
        show_perturbed_results(ldp.perturbed_location_matrix, vmax=4000)

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
        print(x[int(shape[0]*shape[1]*0.1)])
