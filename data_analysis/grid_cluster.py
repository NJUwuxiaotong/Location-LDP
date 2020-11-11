import copy
import numpy as np


def get_max_number_of_matrix(matrix_data, percentage):
    shape = matrix_data.shape
    row = shape[0]
    column = shape[1]

    x = list()
    for i in range(row):
        for j in range(column):
            x.append(matrix_data[i, j])
    x.sort()
    x.reverse()
    return x[int(row*column*percentage)]


class GridCluster(object):
    def __init__(self, location_matrix, matrix_length, matrix_width, threshold):
        """
        location_matrix: a matrix
        threshold:
        """
        self._location_matrix = location_matrix
        self._matrix_length = matrix_length
        self._matrix_width = matrix_width
        self._threshold = threshold
        self._state = np.ones([matrix_length, matrix_width])
        self._tab = 0
        self.cluster_matrix = np.zeros([matrix_length, matrix_width])
        self.tab_number = 0
        self.point_num = 0

    def cluster(self):
        pos = 0
        while pos < self._matrix_length * self._matrix_width:
            row_index = int(pos / self._matrix_width)
            column_index = pos % self._matrix_width

            if self._state[row_index, column_index] == 0:
                pos += 1
                continue

            self.point_num += self._location_matrix[row_index, column_index]
            if self._location_matrix[row_index, column_index] < self._threshold:
                pos += 1
                self._state[row_index, column_index] = 0
                continue

            self._state[row_index, column_index] = 0
            self._tab += 1
            new_cluster = [[row_index, column_index]]
            while new_cluster:
                first_entry = new_cluster.pop(0)
                self.cluster_matrix[first_entry[0], first_entry[1]] = self._tab
                self._state[first_entry[0], first_entry[1]] = 0
                sub_cluster = self.find_neighbor_exceed_threshold(first_entry)
                new_cluster.extend(sub_cluster)
            pos += 1

    def get_tabs(self):
        self.tab_number = self._tab
        return self.tab_number

    def find_neighbor_exceed_threshold(self, center_location):
        cluster = list()
        length = center_location[0]
        width = center_location[1]
        if length - 1 >= 0 and self._state[length - 1, width] != 0:
            self._state[length - 1, width] = 0
            self.point_num += self._location_matrix[length - 1, width]
            if self._location_matrix[length - 1, width] >= self._threshold:
                cluster.append([length - 1, width])

        if width - 1 >= 0 and self._state[length, width - 1] != 0:
            self._state[length, width - 1] = 0
            self.point_num += self._location_matrix[length, width - 1]
            if self._location_matrix[length, width - 1] >= self._threshold:
                cluster.append([length, width - 1])

        if length + 1 < self._matrix_length and \
                self._state[length + 1, width] != 0:
            self._state[length+1, width] = 0
            self.point_num += self._location_matrix[length + 1, width]
            if self._location_matrix[length + 1, width] >= self._threshold:
                cluster.append([length + 1, width])

        if width + 1 < self._matrix_width and \
                self._state[length, width + 1] != 0:
            self._state[length, width + 1] = 0
            self.point_num += self._location_matrix[length, width + 1]
            if self._location_matrix[length, width + 1] >= self._threshold:
                cluster.append([length, width + 1])
        return cluster

    def get_locations_by_specified_tab(self, tab):
        num = 0
        location_list = list()
        for i in range(self._matrix_length):
            for j in range(self._matrix_width):
                if self.cluster_matrix[i, j] == tab:
                    num += 1
                    location_list.append([i, j])
        return num, location_list

    def get_clusters(self):
        tab_num_list = list()
        tab_locations_list = list()
        for i in range(1, self._tab + 1):
            tab_num, tab_locations = self.get_locations_by_specified_tab(i+1)
            tab_num_list.append(tab_num)
            tab_locations_list.append(tab_locations)
        return tab_num_list, tab_locations_list

    def get_clusters_with_most_grids(self, top_k):
        tab_num_list, tab_locations_list = self.get_clusters()
        grid_num_of_tab = list()
        for tab_locations in tab_locations_list:
            grid_num = len(tab_locations)
            grid_num_of_tab.append(grid_num)

        if top_k > len(grid_num_of_tab):
            print("Error: Top k(i.e., %s) exceeds the number of tabs %s" %
                  (top_k, len(grid_num_of_tab)))
            exit(1)

        grid_num_list_bak = copy.deepcopy(grid_num_of_tab)
        grid_num_list_bak.sort()
        grid_num_list_bak.reverse()
        top_k_grid_list = grid_num_list_bak[:top_k]
        top_k_index = list()
        for i in range(top_k):
            value = top_k_grid_list[i]
            if i == 0:
                pos = tab_num_list.index(value)
                top_k_index.append(pos)
            elif top_k_grid_list[i] == top_k_grid_list[i-1]:
                pos = tab_num_list.index(value, top_k_index[i-1] + 1)
                top_k_index.append(pos)
            else:
                pos = tab_num_list.index(value)
                top_k_index.append(pos)

        clusters = list()
        for i in range(top_k):
            clusters.append(tab_locations_list[top_k_index[i]])
        return clusters

    def get_percentage(self):
        num = 0
        for i in range(self._matrix_length):
            for j in range(self._matrix_width):
                if self.cluster_matrix[i, j] > 0:
                    num += 1
        return num/(self._matrix_length * self._matrix_width)


class GridClusterComparison(object):
    def get_number_of_clusters_for_comparison(self, src_cluster, dst_cluster):
        """
        function: the number of clusters in source cluster
        src_cluster: a list of locations [[l1, ..., ln], ..., [l1, ..., lm]]
        dst_cluster: cluster grid --- matrix [][]
        return:
        """
        cluster_results = 0
        grid_results = 0
        total_grid_num = 0
        for locations in src_cluster:
            clusters = dict()
            grid_num = 0
            total_grid_num += len(locations)
            for location in locations:
                lon = location[0]
                lat = location[1]
                tab = dst_cluster[lon, lat]
                if tab != 0:
                    grid_num += 1
                    tab = int(tab)
                    if tab not in clusters:
                        clusters[tab] = [[lon, lat]]
                    else:
                        clusters[tab].append([lon, lat])
            cluster_results += len(clusters)
            grid_results += grid_num
        return cluster_results, grid_results/total_grid_num
