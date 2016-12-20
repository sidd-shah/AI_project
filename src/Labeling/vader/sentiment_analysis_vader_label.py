# http://www.nltk.org/howto/sentiment.html
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sentences = []


def clean(sentence):
    mystring = sentence
    try:
        mystring.encode('utf8', 'ignore')
        result = p.parse(mystring)
        start = result.urls[0][1][0]
        end = result.urls[0][1][1]
        sentence = mystring[:start] + mystring[end:]
    except (IndexError, UnicodeDecodeError) as e:
        pass
    return sentence


labelled_list = []

import pickle


def read_file(filename):
    labelled = pickle.load(open(filename, "rb"))
    for line in labelled:
        labelled_list.append(line[0])
        # print line[0]


read_file("trump_list.p")
read_file("cruz_list.p")
hashset_labelled = set(labelled_list)

# import pickle
# positive_list = pickle.load(open("positive_list.p", "rb"))
# negative_list = pickle.load(open("negative_list.p", "rb"))
result = []

with open('tedCruz_43k_7th.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        # print row[1]
        # label=raw_input("Enter label\nTrump=t\tCruz=c\tHillary=h\tsanders=s\tneutral=n\n")
        # result.append([row[1],label])
        # pickle.dump(result,open("labllled.txt","wb"))
        try:
            result.append(row[1])
        except IndexError:
            pass

hashset_total = set(result)

differenceSet = hashset_total.difference(hashset_labelled)
differenceList = list(differenceSet)

from ttp import ttp

p = ttp.Parser(include_spans=True)
# mystring = "@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/ yasha asdas asdasdas"
# result = p.parse(mystring)
counterOut = 0
counterP = 0
sid = SentimentIntensityAnalyzer()
cruzList = []
for sentence in differenceList:
    counterP += 1
    sentence = clean(sentence)
    # print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        # print k
        if k == 'compound' and (ss[k] >= 0.8 or ss[k] <= -0.8):
            print(sentence)
            print "%s %s, \t" % (k, ss[k]),
            print
            counterOut += 1
            if ss[k] >= 0.8:
                print 'positive'
                cruzList.append([sentence, 'positive'])
            else:
                cruzList.append([sentence, 'negative'])
                # print('{0}: {1}, '.format(k, ss[k]), end ='')
                # print

pickle.dump(cruzList, open("tedCruz_43k_7th.csv_vader.p", "wb"))

counterN = 0
# print counterP
print len(differenceSet)
print counterP + counterN
print 'Output:', counterOut
