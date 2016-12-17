import networkx as nx
import numpy as np 
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from HTMLParser import HTMLParser
import nltk
from nltk.corpus import brown
from parser import NPExtractor
class CentroidSummarizer:

	def __init__(self):
		self.documents = []


	def generate_summary(self, sents):

		cv = CountVectorizer()
		bow_matrix = cv.fit_transform(sents)
		
		normalized = TfidfTransformer().fit_transform(bow_matrix)
	
		similarity_graph = normalized * normalized.T

		nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
		# print "graph built"
		scores = nx.pagerank(nx_graph)
		text_rank_graph = sorted(((scores[i],s) for i,s in enumerate(sents)), reverse=True)
		# print text_rank_graph
		number_of_nodes = int(0.3*len(text_rank_graph))
		
		if number_of_nodes < 3:
			number_of_nodes = 3
			
		del text_rank_graph[number_of_nodes:]
		
		summary = ' '.join(word for _,word in text_rank_graph)
		print summary
		return summary

	def add_article(self, document):
		print "ORIGINAL"
		print HTMLParser().unescape(document)
		
		self.documents.append(HTMLParser().unescape(document))

	def tf(self, sentenct):
		return blob.words.count(word) / len(blob.words)

	def summarize(self):
		sents = []
		sentence_tags_dict = {}
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		sentence_tokenizer = PunktSentenceTokenizer()
		for document in self.documents:
			for sent in sent_detector.sentences_from_text(document):
				np_extractor = NPExtractor(sent)
				result = np_extractor.extract()
				index = len(sents)
				for tag in result:
					# print tag
					tag = tag.lower()
					print tag
					if tag in sentence_tags_dict.keys():
						value = sentence_tags_dict[tag]
						print "Found", tag, value
						if value:
							sentence_tags_dict[tag] = value.append(index)
						else:
							print value
					else:
						sentence_tags_dict[tag] = [index,]
						print "Set", tag, sentence_tags_dict[tag]
				# print "This sentence is about: %s" % ", ".join(result)
				sents.append(sent)


		cv = CountVectorizer()
		bow_matrix = cv.fit_transform(sents)
		features = cv.get_feature_names()

		selected_sents = set()
		for feature in features:
			print feature
			if feature in sentence_tags_dict.keys():
				print "FOUND FEATURE"
				if sentence_tags_dict[feature]:
					for index in sentence_tags_dict[feature]:
						selected_sents.add(sents[index])
			# else:
				# print "Feature not a topic"

		print "\n\nAll Sentences Summary\n\n\n"
		self.generate_summary(sents)

		print "\n\nSelected Sentences\n\n\n"
		self.generate_summary(selected_sents)

		# cv = CountVectorizer()
		# count_vec = cv.fit_transform(sents)
		# tf_transformer = TfidfTransformer(use_idf=True)
		# tfidf = tf_transformer.fit_transform(count_vec)
		# tf_scores = {}
		# # print type(cv.get_feature_names()), type(tf_transformer.idf_)
		# # print zip(cv.get_feature_names(),tf_transformer.idf_)
		# # print(tf_transformer.idf_)
		# for index, row in enumerate(cv.get_feature_names()):
		# 	tf_scores[row] = tf_transformer.idf_[index]
		# 	print row, tf_scores[row]


		

 
