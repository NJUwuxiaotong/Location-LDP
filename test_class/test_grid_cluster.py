import time

from data_analysis.grid_cluster import GridCluster, get_max_number_of_matrix
from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator


class TestGridCluster(object):
    def __init__(self, latitude_file, longitude_file, location_range,
                 unit_width, percentage):
        self.latitude_file = latitude_file
        self.longitude_file = longitude_file
        self.location_range = location_range
        self.unit_width = unit_width
        self.percentage = percentage

    def execute_test(self):
        ldp = LocationRandomizedGenerator(
            self.latitude_file, self.longitude_file,
            self.location_range, self.unit_width)
        ldp.get_source_map()
        shape = ldp.source_location_matrix.shape
        threshold = get_max_number_of_matrix(ldp.source_location_matrix,
                                             self.percentage)
        gc = GridCluster(
            ldp.source_location_matrix, shape[0], shape[1], threshold)
        start_t = time.time()
        gc.cluster()
        end_t = time.time()
        gc.get_tabs()

        # show_perturbed_results(gc.cluster_matrix, vmax=1)
        print('-------------- Result --------------\n')
        print("Tab num: %s" % gc.tab_number)
        print("Time: %s" % (end_t - start_t))
        print("Percentage: %s" % gc.get_percentage())
