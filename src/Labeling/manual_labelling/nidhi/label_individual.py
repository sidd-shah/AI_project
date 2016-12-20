import csv
import pickle
import random
result=[]


reader=pickle.load(open("list1.p","rb"))
global_counter = 0

try:
	global_counter = pickle.load(open("counter.p", "rb"))
except:
	pass

labelled_list = []
try:
	labelled_list = pickle.load(open("labelled_list.p","rb"))
	reader = reader - set(labelled_list)
except:
	labelled_list = []

trump_list, hillary_list, garbage_list = [], [], []
try:
	trump_list = pickle.load(open("trump_list.p","rb"))
except:
	trump_list = []

try:
	hillary_list = pickle.load(open("hillary_list.p","rb"))
except:
	hillary_list = []

try:
	garbage_list = pickle.load(open("garbage_list.p","rb"))
except:
	garbage_list = []

reader = list(reader)
random.shuffle(reader)

counter = 0
for row in reader:
	print("\n%s:%s" % (counter, row)) 
	pickle.dump(counter, open("counter.p", "wb"))
	counter += 1
	label = "none"
	label=raw_input("Enter label\nTrump +ve=t\t-ve=n\thillary +ve=c\t-ve=p\tneutral=0\tshow=s\tremove=r\n")		
	if label == "t":
		trump_list.append([row, 'positive'])
	elif label == "n":
		trump_list.append([row, 'negative'])
	if label == "c":
		hillary_list.append([row, 'positive'])
	if label == "p":
		hillary_list.append([row, 'negative'])
	if label == "break":
		break
	if label == "r":
		garbage_list.append([row, 'garbage'])
	
	pickle.dump(garbage_list,open("garbage_list.p","wb"))			
	pickle.dump(trump_list,open("trump_list.p","wb"))
	pickle.dump(hillary_list,open("hillary_list.p","wb"))

pickle.dump(garbage_list,open("garbage_list.p","wb"))
pickle.dump(trump_list,open("trump_list.p","wb"))
pickle.dump(hillary_list,open("hillary_list.p","wb"))

