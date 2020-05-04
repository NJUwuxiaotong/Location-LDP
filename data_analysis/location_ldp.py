import pandas as pd
import numpy as np
import os
import math
import folium
from folium import plugins
import webbrowser
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import random
import json


class LocationLDP(object):
    def __init__(self, latitude_file_path, longitude_file_path, map_size,
                 unit_width):
        """
        :param latitude_file_path:
        :param longitude_file_path:
        :param map_size: (left_lat, right_lat, low_lon, high_lon))
        :param unit_width:
        """
        self.latitude_file_path = latitude_file_path
        self.longitude_file_path = longitude_file_path
        self.map_size = map_size
        self.latitudes = None
        self.longitudes = None
        self.left_lat = map_size[0]
        self.right_lat = map_size[1]
        self.low_lon = map_size[2]
        self.high_lon = map_size[3]
        self.unit_width = unit_width
        self.number_of_locations = 0
        self.read_data_from_file()
        self.perturbed_location_matrix = None
        self.matrix_x_width = None
        self.matrix_y_width = None
        self.divide_map_to_blocks()

    def read_data_from_file(self):
        # read data
        self.latitudes = []
        with open(self.latitude_file_path, 'r+') as f:
            c = f.readlines()
            for lat in c:
                self.latitudes.append(float(lat))
                self.number_of_locations += 1

        self.longitudes = []
        with open(self.longitude_file_path, 'r+') as f:
            c = f.readlines()
            for lon in c:
                self.longitudes.append(float(lon))

    def get_init_statistics(self):
        self.perturbed_location_matrix = np.zeros(
            [self.matrix_y_width, self.matrix_x_width])
        for i in range(self.number_of_locations):
            lat = self.latitudes[i]
            lon = self.longitudes[i]
            block = self.get_current_block(lat, lon)
            self.perturbed_location_matrix[block[0], block[1]] += 1

    def divide_map_to_blocks(self):
        self.matrix_x_width = int((self.right_lat - self.left_lat) /
                                  self.unit_width) + 1
        self.matrix_y_width = int((self.high_lon - self.low_lon) /
                                  self.unit_width) + 1

    def perturb_location(self, privacy, safe_boundary):
        self.perturbed_location_matrix = np.zeros(
            [self.matrix_y_width, self.matrix_x_width])
        for i in range(self.number_of_locations):
            lat = self.latitudes[i]
            lon = self.longitudes[i]
            block = self.get_current_block(lat, lon)
            x, y = self.random_generator(privacy, safe_boundary, block)
            self.perturbed_location_matrix[y, x] += 1

    def get_current_block(self, c_lat, c_lon):
        x = math.floor((c_lat - self.left_lat) / self.unit_width)
        y = math.floor((c_lon - self.low_lon) / self.unit_width)
        # s_matrix[y_width - y - 1, x - 1] += 1
        return self.matrix_y_width - y - 1, x - 1

    def get_safe_boundary(self, current_block, safe_boundary):
        lon = current_block[0]
        lat = current_block[1]
        number_of_blocks = 0
        safe_blocks = []
        for i in range(safe_boundary+1):
            j = safe_boundary - i
            if 0 <= lat + i < self.matrix_x_width and \
                    0 <= lon + j < self.matrix_y_width:
                if [lat+i, lon+j] not in safe_blocks:
                    number_of_blocks += 1
                    safe_blocks.append([lat+i, lon+j])
            if i != 0 and 0 <= lat - i < self.matrix_x_width and \
                    0 <= lon + j < self.matrix_y_width:
                if [lat-i, lon+j] not in safe_blocks:
                    number_of_blocks += 1
                    safe_blocks.append([lat - i, lon + j])
            if 0 <= lat - i < self.matrix_x_width and \
                    0 <= lon - j < self.matrix_y_width:
                if [lat-i, lon-j] not in safe_blocks:
                    number_of_blocks += 1
                    safe_blocks.append([lat-i, lon-j])
            if j != 0 and 0 <= lat + i < self.matrix_x_width and \
                    0 <= lon - j < self.matrix_y_width:
                if [lat+i, lon-j] not in safe_blocks:
                    number_of_blocks += 1
                    safe_blocks.append([lat+i, lon-j])
        return number_of_blocks, safe_blocks

    def random_generator(self, privacy, safe_boundary, current_block):
        """
        :param privacy:
        :param safe_boundary:
        :param current_location: (lat, lon) --> (x, y)
        :return:
        """
        e_privacy = math.exp(privacy)
        number_of_blocks = 0
        safe_blocks = []
        for i in range(1, safe_boundary+1):
            s_num, s_blocks = self.get_safe_boundary(current_block, i)
            if s_num != 0:
                safe_blocks.extend(s_blocks)
                number_of_blocks += s_num
        print(number_of_blocks)

        p_positive = e_privacy / (e_privacy + number_of_blocks)
        p_negative = 1 / (e_privacy + number_of_blocks)

        p = random.uniform(0, 1)
        if p <= p_positive:
            return current_block[1], current_block[0]
        else:
            num = math.ceil((p - p_positive) / p_negative)
            return safe_blocks[num-1][0], safe_blocks[num-1][1]

    def show_results(self):
        sns.set()
        fig = plt.figure()
        f, ax = plt.subplots(figsize=(6, 5))

        # Reds, OrRd, Blues, BuPu
        sns_plot = sns.heatmap(self.perturbed_location_matrix,
                               cmap='hot',
                               vmax=2000, vmin=0,
                               xticklabels=False,
                               yticklabels=False,
                               cbar=False,
                               robust=True,
                               cbar_kws={"orientation": "horizontal",
                                         "size": 30})
        cb = sns_plot.figure.colorbar(sns_plot.collections[0])
        cb.ax.tick_params(labelsize=18, labelbottom=True)

        # fig.savefig("heatmap.pdf", bbox_inches='tight')
        # ax.set_title('Amounts per kind and region')
        # ax.set_xlabel('latitude')
        # ax.set_xticklabels(x_labels)
        # ax.set_xticks(x_labels)
        # ax.set_ylabel("longitude")
        # ax.set_yticklabels([i*(high_lon - low_lon)/10 for i in range(10)])
        plt.show()
