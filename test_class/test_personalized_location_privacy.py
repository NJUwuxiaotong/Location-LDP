import time

from data_analysis.location_randomized_generator import show_perturbed_results
from data_analysis.grid_cluster \
    import GridCluster, GridClusterComparison, get_max_number_of_matrix


class TestPersonalizedLocationPrivacy(object):
    def __init__(self, latitude_file, longitude_file, location_range,
                 unit_width, perturbation_class):
        self.latitude_file = latitude_file
        self.longitude_file = longitude_file
        self.location_range = location_range
        self.unit_width = unit_width
        self.perturbation_class = perturbation_class

    def execute_instance(self, privacy, safe_boundary, percentage, top_k):
        ldp = self.perturbation_class(
            self.latitude_file, self.longitude_file, self.location_range,
            self.unit_width)

        ldp.get_source_map()
        threshold = get_max_number_of_matrix(
            ldp.source_location_matrix, percentage)
        shape = ldp.source_location_matrix.shape
        src_gc = GridCluster(ldp.source_location_matrix, shape[0],
                             shape[1], threshold)
        src_cluster_start_t = time.time()
        src_gc.cluster()
        src_cluster_end_t = time.time()
        src_tab_num = src_gc.get_tabs()
        src_clusters = src_gc.get_clusters_with_most_grids(top_k)

        perturb_start_t = time.time()
        ldp.perturb_location(privacy, safe_boundary)
        perturb_end_t = time.time()
        show_perturbed_results(ldp.perturbed_location_matrix)
        ldp.get_privacy_preservation_effect()
        privacy_effect = ldp.preservation_effect
        privacy_grid_distance = ldp.distance_of_perturbed_grids

        dst_gc = GridCluster(
            ldp.perturbed_location_matrix, shape[0], shape[1], threshold)
        dst_cluster_start_t = time.time()
        dst_gc.cluster()
        dst_cluster_end_t = time.time()
        dst_tab_num = dst_gc.get_tabs()

        gcc = GridClusterComparison()
        cluster_num, grid_percentage = \
            gcc.get_number_of_clusters_for_comparison(
                src_clusters, dst_gc.cluster_matrix)

        print("==================== Results ====================\n")
        print("Source cluster number: %s\n" % src_tab_num)
        print("Source grid percentage: %s\n" % src_gc.get_percentage())
        print("Source cluster time: %s\n" %
              (src_cluster_end_t - src_cluster_start_t))
        print("-------------------------------------------------\n")
        print("Perturb grid difference: %s\n" % privacy_grid_distance)
        print("Perturb location distance: %s\n" % privacy_effect)
        print("Perturb process time: %s\n" % (perturb_end_t - perturb_start_t))
        print("-------------------------------------------------\n")
        print("Perturb cluster number: %s\n" % dst_tab_num)
        print("Perturb grid percenatage: %s\n" % dst_gc.get_percentage())
        print("Perturb cluster time: %s\n" %
              (dst_cluster_end_t - dst_cluster_start_t))
        print("-------------------------------------------------\n")
        print("Comparison cluster number: %s\n" % cluster_num)
        print("Comparison grid percentage: %s\n" % grid_percentage)
        print("-------------------------------------------------\n")
