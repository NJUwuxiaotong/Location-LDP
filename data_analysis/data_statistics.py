import json
import numpy as np
import pandas as pd
import os

root_path = "F:\\busyfish\paper\paper\privacy preservation\location under L" \
            "DP\data\Geolife Trajectories 1.3\Data"
output_parent_path = "F:\\busyfish\paper\paper\privacy preservation\locat" \
                     "ion under LDP\experiment spde\Location-LDP\data"
first_parent_path = os.listdir(root_path)
sub_dir = "\\Trajectory"

num = 0
statistical_info = dict()
x_atitude = []
y_atitude = []
for f_pp in first_parent_path:
    abs_path = root_path + "\\" + f_pp + sub_dir
    leaf_path = os.listdir(abs_path)
    for l_path in leaf_path:
        print("%s: Process %s" % (num, l_path))
        num += 1
        abs_leaf_path = abs_path + "\\" + l_path
        with open(abs_leaf_path, "r+") as f:
            c = f.readlines()
            for l in c[6:]:
                x = l.split(',')
                if (39.97 <= float(x[0]) <= 40.02) and \
                        (116.29 <= float(x[1]) <= 116.33):
                    x_atitude.append(x[0])
                    y_atitude.append(x[1])

                # if x[0]+x[1] not in statistical_info:
                #     statistical_info[x[0] + ',' + x[1]] = 1
                # else:
                #     statistical_info[x[0] + ',' + x[1]] += 1


# with open(output_parent_path+"\statistical", "w+") as f:
#     json.dump(statistical_info, f)

with open(output_parent_path+"\\x_", "w+") as f:
    for x in x_atitude:
        f.write(x+"\n")

with open(output_parent_path+"\\y_", "w+") as f:
    for y in y_atitude:
        f.write(y+"\n")
