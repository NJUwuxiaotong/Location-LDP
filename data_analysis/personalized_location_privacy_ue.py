import math
import numpy as np
import random

from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator


class PersonalizedLocationPrivacyUE(LocationRandomizedGenerator):
    def __init__(self, latitude_file_path, longitude_file_path, map_size,
                 unit_width):
        super(PersonalizedLocationPrivacyUE, self).__init__(
            latitude_file_path, longitude_file_path, map_size, unit_width)

        if self.matrix_x_width >= self.matrix_y_width:
            self.perturb_side = "column"
            self.perturb_side_length = self.matrix_y_width
        else:
            self.perturb_side = "row"
            self.perturb_side_length = self.matrix_x_width

    def perturb_location(self, privacy, safe_boundary):
        """
        use self.perturbed_location_matrix to get perturbed results
        """
        for i in range(self.number_of_locations):
            lat = self.latitudes[i]
            lon = self.longitudes[i]
            block = self.get_current_block(lat, lon)
            perturbed_array = self.random_generator(
                privacy, safe_boundary, block)

            if self.perturb_side == "row":
                self.perturbed_location_matrix[block[0], :] += perturbed_array
            else:
                self.perturbed_location_matrix[:, block[1]] += perturbed_array

    def random_generator(self, privacy, safe_boundary, current_block):
        """
        :param privacy:
        :param safe_boundary:
        :param current_location: (lat, lon) --> (x, y)
        :return:
        """
        perturb_vector = np.array([-1] * self.perturb_side_length)
        if self.perturb_side == "row":
            perturb_vector[current_block[1]] = 1
        else:
            perturb_vector[current_block[0]] = 1

        for i in range(self.perturb_side_length):
            perturb_vector[i] *= self.generate_binary(privacy)
        return perturb_vector

    def generate_binary(self, privacy):
        e_privacy = math.exp(privacy / 2)
        p1 = e_privacy / (e_privacy + 1)
        p = random.uniform(0, 1)
        if p <= p1:
            result = 1
        else:
            result = -1
        return result
