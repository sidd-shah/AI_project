import sys
import urllib2

import fetch_url
from CentroidSummarizer import CentroidSummarizer
from GoogleNews import newsSearch
from Summary import textRank
from bsReadability import readable
from classify_tweets import clean, predict, vader
from cursor import get_tweets
from summ import FrequencySummarizer

DEFAULT_ENCODING = 'latin-1'


def print_usage():
    print "USAGE:"
    print "%s <SEARCH TERM>" % sys.argv[0]


def dump_all(l):
    for i in l:
        print i


def dump_tweets(tweets):
    for tweet_set in tweets:
        for tweet in tweet_set:
            print tweet.text


def get_only_text(url):
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text


def sentiment_analyze(link):
    print "Scanning tweets for link %s" % link
    tweets = get_tweets(link)
    texts = []
    for tweet in tweets:
        texts.append(tweet.text)
    texts = clean(texts)
    analysis = predict(texts)
    vader_analysis = vader(texts)

    positive_tweets = []
    negative_tweets = []

    for i in range(len(texts)):
        score = 0.25 * analysis[i] + 0.75 * vader_analysis[i]
        if score > 0.8:
            positive_tweets.append(texts[i])
        elif score < -0.8:
            negative_tweets.append()

    print "*******************************************************"
    print "++++++++++++++++++++++POSITIVE+++++++++++++++++++++++++"
    print "*******************************************************"
    print positive_tweets
    print "*******************************************************"
    print "                      NEGATIVE                         "
    print "*******************************************************"
    print negative_tweets

    return positive_tweets, negative_tweets


def main(search_term):
    result_count = 15
    result_links = newsSearch(search_term, result_count)

    dump_all(result_links)

    article_list = []
    summary_list = []
    sentiment_list = []
    summary_new = []
    if not result_links:
        print "No links found"
    else:
        result = fetch_url.fetch_parallel(result_links)
        fs = FrequencySummarizer()
        cs = CentroidSummarizer()
        while not result.empty():
            try:
                url_entry = result.get()
                article = readable(url_entry[0], url_entry[1], DEFAULT_ENCODING)
                # title, text = get_only_text(url_entry[1])
                print '----------------------------------'
                # print title
                # summary = textRank(article).encode('ascii', 'ignore')
                # article_list.append(article)
                # summary_list.append(summary + "\n******************************************\n")
                # for s in fs.summarize(article, 3):
                #     print '*', s
                #     summary_new.append(s)
                # summary_new.append("\n******************************************\n")
                cs.add_article(article)
                # twittersearch(url_entry[0])
                # twittersearch('Manchester United')
                #  print url_entry[0]
                # try:
                # url_entry = result.get()
                link = url_entry[0]
                article = readable(url_entry[0], url_entry[1], DEFAULT_ENCODING)
                # title, text = get_only_text(url_entry[1])
                summary = textRank(article).encode('ascii', 'ignore')
                article_list.append(article)
                summary_list.append(summary)
                sentiment_list.append(sentiment_analyze(link))
                # except error as e:
                #     print "EXCEPT %s" % e
                #     pass

            except Exception as ex:
                print ex
        print "Calling summarize"
        cs.summarize()
    outfile1 = open("summary1", "w")
    outfile2 = open("summary2", "w")
    # dump_all(article_list)
    # dump_all(summary_list)
    outfile1.write(str(summary_new))
    outfile2.write(str(summary_list))
    outfile1.close()
    outfile2.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        exit(-1)
    search_term = '+'.join(sys.argv[1:])

    main(search_term)
