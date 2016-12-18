import sys
import nltk
import re
import fetch_url
from GoogleNews import newsSearch
from bsReadability import readable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation

stemmer = SnowballStemmer("english")


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


DEFAULT_ENCODING = 'latin-1'


def print_usage():
    print "USAGE:"
    print "%s <SEARCH TERM>" % sys.argv[0]


def dump_all(l):
    for i in l:
        print i


def makeClusters(article_list):
    tfidf = TfidfVectorizer(stop_words='english',
                            use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 2)).fit_transform(article_list)
    dist = cosine_similarity(tfidf)
    # print dist
    num_clusters = 5

    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf)
    clusters = km.labels_.tolist()
    return clusters



