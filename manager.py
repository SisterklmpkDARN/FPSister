def compute(data, centroids):
    from scipy.spatial.distance import euclidean
    import numpy as np
    import socket

    minn = 1000000000
    idx = 0
    for j in range(0,len(centroids)):
        dist = euclidean(data, centroids[j])
        if dist < minn:
            minn = dist
            idx = j
            
    data = np.append(data, idx)
    return data

if __name__ == '__main__':
    import dispy
    import pickle
    import numpy as np
    print 'DEBUG: Creating Job Cluster'
    cluster = dispy.JobCluster(compute)
    jobs = np.array([])
    print 'DEBUG: Reading data'
    # load data centroid dengan pickle
    fp = open('centroids_np','r')
    centroids = pickle.load(fp)
    #centroids = np.array(centroids)
    fp.close()
    # load file kddcup-testdata
    fp = open('kddcup-testdata.csv','r')
    #sz = 311028
    n = 0
    print 'DEBUG: Distributing jobs'
    for i,line in enumerate(fp):
        line = line.strip()
        temp = line.split(',')
        lis = np.array([])
        for val in temp:
            lis = np.append(lis, float(val))
        print 'DEBUG: Submit job',n+1
        job = cluster.submit(lis, centroids)
        job.id = n
        jobs = np.append(jobs, job)
        n += 1

    np.set_printoptions(precision=3)
    hasil = np.array([])
    
    for job in jobs:
        res = job()
        if hasil.size == 0:
            hasil = np.append(hasil, res)
        else:
            hasil = np.vstack((hasil,res))
        print '%s executed job %s at %s' % (job.ip_addr, job.id, job.start_time)
        #hasil = np.append(hasil, res)

    print hasil
    print 'DEBUG: Writing to file'
    np.savetxt('test.txt',hasil,fmt='%.2f',delimiter=',',newline=' ')
'''    fp = open('hasil.txt','w')
    for data in hasil:
        fp.write(data)
        fp.write('\n')
    fp.close()'''

cluster.stats()
