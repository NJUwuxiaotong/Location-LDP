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
        perturb_start_t = time.time()
        ldp.perturb_location(privacy, safe_boundary)
        perturb_end_t = time.time()
        # show_perturbed_results(ldp.perturbed_location_matrix)
        ldp.get_privacy_preservation_effect()
        privacy_effect = ldp.preservation_effect
        privacy_grid_distance = ldp.distance_of_perturbed_grids

        shape = ldp.perturbed_location_matrix.shape
        threshold = get_max_number_of_matrix(
            ldp.perturbed_location_matrix, percentage)
        gc = GridCluster(ldp.perturbed_location_matrix, shape[0], shape[1],
                         threshold)
        cluster_start_t = time.time()
        gc.cluster()
        cluster_end_t = time.time()
        gc.get_tabs()

        print('-------------- Result --------------\n')
        print("Tab num: %s" % gc.tab_number)
        print("Percentage: %s" % gc.get_percentage())
        print('------------------------------------')
        print("Preservation effect [distance]: %s" % privacy_effect)
        print("[Privacy Preservation] grid distance --> %s\n" %
              privacy_grid_distance)
        print('------------------------------------')
        perturb_time = perturb_end_t - perturb_start_t
        cluster_time = cluster_end_t - cluster_start_t
        print("Perturb Time: %s\n" % perturb_time)
        print('Grid Time: %s\n'% cluster_time)
        print('Total time: %s\n' % (perturb_time + cluster_time))
        print('------------------------------------')
