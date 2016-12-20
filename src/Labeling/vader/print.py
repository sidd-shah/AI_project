import csv

with open('tedCruz_43k_7th.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        # print row[1]
	# label=raw_input("Enter label\nTrump=t\tCruz=c\tHillary=h\tsanders=s\tneutral=n\n")
	# result.append([row[1],label])
	# pickle.dump(result,open("labllled.txt","wb"))
	try:
		print row[1]		
		#result.append(row[1])		
	except IndexError:
		pass
