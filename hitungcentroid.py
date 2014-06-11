import time
import pickle
import numpy as np
from scipy.cluster.vq import kmeans, whiten

start = time.time()
# baca file
f = open('kddcup-newtestdata.csv', 'r')
data = []
for line in f:
	line = line.strip('\n')	
	temp = []
	for d in (line.split(',')):
		temp.append(float(d))
	data.append(temp)
data = np.array(data)	
result = kmeans(data, 23) # generate centroid untuk 23 cluster

# dump ke file
f.close()
f = open('centroids', 'w')
pickle.dump(result[0],f)
f.close()
print "Execution time:", time.time()-start, "seconds"