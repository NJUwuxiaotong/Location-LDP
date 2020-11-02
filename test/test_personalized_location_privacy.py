from test_class.test_personalized_location_privacy \
    import TestPersonalizedLocationPrivacy


latitude_file = "D:\\workspace\\paper\\location under LDP\\experim" \
                "ent spde\\Location-LDP\\data\\x_"
longitude_file = "D:\\workspace\\paper\\location under LDP\\exp" \
                 "eriment spde\\Location-LDP\\data\\y_"

left_lat = 39.97
right_lat = 40.02
low_lon = 116.29
high_lon = 116.33

# 0.00008, 0.00016, 0.00032
unit_width = 0.00032
privacy = 1
safe_boundary = 2
percentage = 0.1

test_plp = TestPersonalizedLocationPrivacy(
    latitude_file, longitude_file, [left_lat, right_lat, low_lon, high_lon],
    unit_width)
test_plp.execute_instance(privacy, safe_boundary, percentage)
