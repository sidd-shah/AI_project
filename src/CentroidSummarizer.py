import networkx as nx
import numpy as np 

from nltk.tokenize import sent_tokenize,word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

class CentroidSummarizer:

	def __init__(self):
		self.documents = []

	def add_article(self, document):
		self.documents.append(document)

	def tf(self, sentenct):
		return blob.words.count(word) / len(blob.words)

	def summarize(self):
		sents = []
		sentence_tokenizer = PunktSentenceTokenizer()
		for document in self.documents:
			for sent in sentence_tokenizer.tokenize(document):
				sents.append(sent)
		print len(sents)

		bow_matrix = CountVectorizer().fit_transform(sents)
		normalized = TfidfTransformer().fit_transform(bow_matrix)
	
		similarity_graph = normalized * normalized.T

		nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
		print "graph built"
		scores = nx.pagerank(nx_graph)
		text_rank_graph = sorted(((scores[i],s) for i,s in enumerate(sents)), reverse=True)
		number_of_nodes = int(0.3*len(text_rank_graph))
		
		if number_of_nodes < 3:
			number_of_nodes = 3
			
		del text_rank_graph[number_of_nodes:]
		
		summary = ' '.join(word for _,word in text_rank_graph)
		print summary
		return summary

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


		

 
