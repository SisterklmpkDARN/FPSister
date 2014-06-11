def compute(start, stop):
    import pickle
    from scipy.spatial.distance import euclidean
    # load data centroid dengan pickle
    fp = open('centroids','r')
    centroids = pickle.load(fp)
    fp.close()

    # proses test data yang berada pada rentang [start,stop)
    fp = open('kddcup-testdata.csv','r')
    res = []
    for i, line in enumerate(fp):
        if i >= start:
            line = line.strip()
            values = line.split(',')
            temp = []
            for val in values: # konversi dari array of string ke array of float
                temp.append(float(val))
            idx = 0
            minn = 1000000000
            for cent in centroids: # untuk setiap centroid
                dist = euclidean(temp, cent) # hitung euclidean distance dengan data ini
                if dist < minn: # TODO: hasil akhirnya seperti apa.. tanya bapaknya lagi
                    minn = dist
                    cluster_no = idx
                idx += 1
            temp.append(float(idx)) # asumsinya hasil akhirnya data + nomor kluster sbg variabel terakhir
            res.append(temp)
        if i == stop:
	    break
    fp.close()
    return res

if __name__ == '__main__':
    import dispy
    # nodes = alamat ip yg jalanin dispynode, depends = persyaratan yg harus ada di setiap yg jalanin dispynode, ip_addr = ip address yg dipake buat cluster
    # filenya harus satu folder sama dispynode.py
    cluster = dispy.JobCluster(compute, nodes=['192.168.1.4', '127.0.0.1'], depends=['kddcup-testdata.csv','centroids'], ip_addr='192.168.1.2')
    jobs = []
    start = 0
    stop = 51838
    end = 311028 # banyaknya baris di file kddcup-testdata.csv -1 (311029-1)
    for n in range(6): # looping 6 job
        job = cluster.submit(start, stop) # jalankan
        job.id = n
        jobs.append(job)
        start = stop
	stop += stop
	if stop == end
            stop = end+1
    for job in jobs:
        res = job()
        # TODO: hasil akhirnya seperti apa..
    cluster.stats()
