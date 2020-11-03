import math
import random

from data_analysis.location_randomized_generator \
    import LocationRandomizedGenerator


class PersonalizedLocationPrivacy(LocationRandomizedGenerator):
    def perturb_location(self, privacy, safe_boundary):
        for i in range(self.number_of_locations):
            lat = self.latitudes[i]
            lon = self.longitudes[i]
            block = self.get_current_block(lat, lon)
            # x: latitude, y: longitude
            x, y = self.random_generator(privacy, safe_boundary, block)
            self.perturbed_location_matrix[y, x] += 1
            self.source_mapping_perturb.append([x, y])

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

        p_positive = e_privacy / (e_privacy + number_of_blocks)
        p_negative = 1 / (e_privacy + number_of_blocks)

        p = random.uniform(0, 1)
        if p <= p_positive:
            return current_block[1], current_block[0]
        else:
            num = math.ceil((p - p_positive) / p_negative)
            return safe_blocks[num-1][0], safe_blocks[num-1][1]
