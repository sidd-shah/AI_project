import networkx as nx
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from HTMLParser import HTMLParser
import nltk
from nltk.corpus import brown
from parser import NPExtractor
from sklearn.feature_extraction.text import TfidfVectorizer
import re


class CentroidSummarizer:	

    def __init__(self):
        self.documents = []

    def document_summaries(self, summaries):
        result = ""
        for index in range(len(self.documents)):
            if index in summaries:
                # print "\n\n\nDocument ", index
                result += ". ".join(re.sub('[\t|\n]+', '', summary.strip()) for summary in summaries[index])
            else:
                print "Index not found"
        return result

    def cosine_similarity(self, sentences):
        vect = TfidfVectorizer(min_df=1)
        tfidf = vect.fit_transform(sentences)
        cosine = (tfidf * tfidf.T).A
        print cosine

    def set_documents(self,documents):
		parsedDocuments = []
		
		for document in documents:
			if len(document) > 500:
				parsedDocuments.append(HTMLParser().unescape(document))
		self.documents = parsedDocuments
		

    def generate_summary(self, sents):

        cv = CountVectorizer(ngram_range=(2, 2))
        bow_matrix = cv.fit_transform(sents)

        normalized = TfidfTransformer().fit_transform(bow_matrix)

        similarity_graph = normalized * normalized.T

        nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
        # print "graph built"
        scores = nx.pagerank(nx_graph)
        text_rank_graph = sorted(((scores[i], s) for i, s in enumerate(sents)), reverse=False)
        # print text_rank_graph
        number_of_nodes = int(0.3 * len(text_rank_graph))

        if number_of_nodes < 3:
            number_of_nodes = 3

        del text_rank_graph[number_of_nodes:]
        summaries = {}
        removed_sentences = []
        for _, sentence in text_rank_graph:

            for index, document in enumerate(self.documents):
                if sentence in document:
                    found = True
                    if index in summaries:
                        sentences = summaries[index]
                        sentences.append(sentence.strip())
                        summaries[index] = sentences
                    else:
                        summaries[index] = [sentence.strip()]

        # summary = ' '.join(sentence.strip() for _,sentence in text_rank_graph)
        # print summary
        return summaries, removed_sentences

    def add_article(self, document):
        # print "Adding document", len(self.documents)
        # print "ORIGINAL"
        # print HTMLParser().unescape(document)
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
                    # print tag
                    if tag in sentence_tags_dict.keys():
                        value = sentence_tags_dict[tag]
                        # print "Found", tag, value
                        value.append(index)
                        sentence_tags_dict[tag] = value
                    # else:
                    # print value
                    else:
                        sentence_tags_dict[tag] = [index, ]
                    # print "Set", tag, sentence_tags_dict[tag]
                # print "This sentence is about: %s" % ", ".join(result)
                sents.append(sent)

        cv = CountVectorizer()
        bow_matrix = cv.fit_transform(sents)
        features = cv.get_feature_names()

        selected_sents = set()
        for feature in features:
            # print feature
            if feature in sentence_tags_dict.keys():
                # print "FOUND FEATURE"
                # print feature
                if sentence_tags_dict[feature]:
                    for index in sentence_tags_dict[feature]:
                        selected_sents.add(sents[index])
            else:
                pass

        # print len(sents)
        # print len(selected_sents)
        # print "Documents", len(self.documents)
        # print "Cosine Similarity"
        # self.cosine_similarity(sents)

        # print "\n\nAll Sentences Summary\n\n"
        # self.generate_summary(sents)

        # print "\n\nSelected Sentences\n"
        summaries, removed_sentences = self.generate_summary(sents)

        # self.document_summaries(summaries)
        # print removed_sentences

        return self.document_summaries(summaries)

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
