import numpy as np

from data_analysis.grid_cluster import GridCluster


row = 100
column = 30
data = np.random.rand(row, column)
gc= GridCluster(data, row, column, 0.5)
gc.cluster()
print(gc.cluster_matrix)
