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

    def execute_instance(self, privacy, safe_boundary, percentage, top_k):
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

        threshold = get_max_number_of_matrix(
            ldp.source_location_matrix, percentage)
        shape = ldp.source_location_matrix.shape
        source_gc = GridCluster(ldp.source_location_matrix, shape[0],
                                shape[1], threshold)
        source_gc.cluster()

        source_tab_num = source_gc.get_tabs()
        source_clusters = source_gc.get_clusters_with_most_grids(top_k)

        dst_gc = GridCluster(
            ldp.perturbed_location_matrix, shape[0], shape[1], threshold)
        dst_gc.cluster()
        dst_tab_num = dst_gc.get_tabs()

        gcc = GridClusterComparison()
        cluster_num, grid_percentage = \
            gcc.get_number_of_clusters_for_comparison(
                source_clusters, dst_gc.cluster_matrix)

        print('-------------- Result --------------\n')
        print("Tab num: %s" % dst_gc.tab_number)
        print("Percentage: %s" % dst_gc.get_percentage())
        print('------------------------------------')
        print("Preservation effect [distance]: %s" % privacy_effect)
        print("[Privacy Preservation] grid distance --> %s\n" %
              privacy_grid_distance)
        print('------------------------------------')
