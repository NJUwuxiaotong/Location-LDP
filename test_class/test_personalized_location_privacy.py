import time

from data_analysis.location_randomized_generator import show_perturbed_results
from data_analysis.personalized_location_privacy \
    import PersonalizedLocationPrivacy
from data_analysis.grid_cluster \
    import GridCluster, GridClusterComparison, get_max_number_of_matrix


class TestPersonalizedLocationPrivacy(object):
    def __init__(self, latitude_file, longitude_file, location_range,
                 unit_width):
        self.latitude_file = latitude_file
        self.longitude_file = longitude_file
        self.location_range = location_range
        self.unit_width = unit_width

    def execute_instance(self, privacy, safe_boundary, percentage):
        ldp = PersonalizedLocationPrivacy(
            self.latitude_file, self.longitude_file, self.location_range,
            self.unit_width)

        ldp.get_source_map()
        start_t = time.time()
        ldp.perturb_location(privacy, safe_boundary)
        end_t = time.time()
        show_perturbed_results(ldp.perturbed_location_matrix)
        ldp.get_privacy_preservation_effect()
        privacy_effect = ldp.preservation_effect

        shape = ldp.perturbed_location_matrix.shape
        percentage = 0.1
        threshold = get_max_number_of_matrix(ldp.perturbed_location_matrix,
                                             percentage)
        gc = GridCluster(ldp.perturbed_location_matrix, shape[0], shape[1],
                         threshold)
        gc.cluster()
        gc.get_tabs()

        print('-------------- Result --------------\n')
        print("Tab num: %s" % gc.tab_number)
        print("Time: %s" % (end_t - start_t))
        print("Percentage: %s" % gc.get_percentage())
