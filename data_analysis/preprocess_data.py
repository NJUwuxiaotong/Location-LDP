input_file_path = "F:\\busyfish\paper\paper\privacy preservation\location u" \
                  "nder LDP\data\Geolife Trajectories 1.3\Data\\000\Tra" \
                  "jectory\\20090403011657.plt"
output_file_path = "F:\\busyfish\paper\paper\privacy preservation\location u" \
                   "nder LDP\experiment spde\Location-LDP\data\\r.txt"

with open(input_file_path, 'r') as f:
    c = f.readlines()

with open(output_file_path, 'w+') as f:
    for l in c[6:5000]:
        x = l.split(',')
        f.write(x[1]+','+x[0]+'\n')
