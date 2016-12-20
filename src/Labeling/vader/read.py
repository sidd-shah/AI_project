import pickle
def read_file(filename):
	labelled = pickle.load(open(filename, "rb"))
	for line in labelled:
		print line

read_file("tedCruz_43k_7th_vader.p")
#read_file("trump_list.p")
