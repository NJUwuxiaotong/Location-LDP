import math
import numpy as np
import random

from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator
from pub_lic.pub_functions import generate_random_value_from_Laplace


class PersonalizedLocationPrivacyHE(LocationRandomizedGenerator):
    def perturb_location(self, privacy, safe_boundary):
        """
        use self.perturbed_location_matrix to get perturbed results
        """
        for i in range(self.number_of_locations):
            lat = self.latitudes[i]
            lon = self.longitudes[i]
            block = self.get_current_block(lat, lon)
            column = self.random_generator(
                privacy, safe_boundary, block)
            self.perturbed_location_matrix[block[0], column] += 1
            self.source_mapping_perturb.append([column, block[0]])
            if i % 100 == 0:
                print("Having processed %s" % i)

    def random_generator(self, privacy, safe_boundary, current_block):
        """
        :param privacy:
        :param safe_boundary:
        :param current_location: (lat, lon) --> (x, y)
        :return:
        """
        value = generate_random_value_from_Laplace(
            -1*safe_boundary, safe_boundary, privacy/2)
        value = math.floor(value)
        perturbed_value = value + current_block[1]
        if perturbed_value < 0:
            return 0
        if perturbed_value >= self.matrix_x_width:
            return self.matrix_x_width - 1
        return perturbed_value
