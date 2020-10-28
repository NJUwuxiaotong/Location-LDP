import numpy as np


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

    def cluster(self):
        pos = 0
        while pos < self._matrix_length * self._matrix_width:
            row_index = int(pos / self._matrix_width)
            column_index = pos % self._matrix_width

            if self._state[row_index, column_index] == 0:
                pos += 1
                continue

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

    def find_neighbor_exceed_threshold(self, center_location):
        cluster = list()
        length = center_location[0]
        width = center_location[1]
        if length - 1 >= 0 and self._state[length - 1, width] != 0:
            self._state[length - 1, width] = 0
            if self._location_matrix[length - 1, width] >= self._threshold:
                cluster.append([length - 1, width])

        if width - 1 >= 0 and self._state[length, width - 1] != 0:
            self._state[length, width - 1] = 0
            if self._location_matrix[length, width - 1] >= self._threshold:
                cluster.append([length, width - 1])

        if length + 1 < self._matrix_length and \
                self._state[length + 1, width] != 0:
            self._state[length+1, width] = 0
            if self._location_matrix[length + 1, width] >= self._threshold:
                cluster.append([length + 1, width])

        if width + 1 < self._matrix_width and \
                self._state[length, width + 1] != 0:
            self._state[length, width + 1] = 0
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
        for i in range(self._tab):
            tab_num, tab_locations = self.get_locations_by_specified_tab(i+1)
            tab_num_list.append(tab_num)
            tab_locations_list.append(tab_locations)
        return tab_num_list, tab_locations_list


class GridClusterComparison(object):
    def get_number_of_clustes_for_comparison(self, src_cluster, dst_cluster):
        """
        function: the number of clusters in source cluster
        src_cluster: a list of locations
        dst_cluster: cluster grid
        """
        number_of_clusters = list()
        for location in src_cluster:
            x = location[0]
            y = location[1]




    def compare_two_grid_clusters(self, src_cluster, dst_cluster):
        pass
