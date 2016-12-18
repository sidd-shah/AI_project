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
from cluster_articles import makeClusters
import json
import pprint

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
    # print "Scanning tweets for link %s" % link
    tweets = get_tweets(link)
    texts = []
    for tweet in tweets:
        texts.append([tweet.text, tweet.user.name])

    texts, authors = clean(texts)
    analysis = predict(texts)
    vader_analysis = vader(texts)

    positive_tweets = []
    negative_tweets = []

    for i in range(len(texts)):
        score = 0.25 * analysis[i] + 0.75 * vader_analysis[i]
        if score > 0.8:
            positive_tweets.append([texts[i], authors[i]])
        elif score < -0.8:
            negative_tweets.append([texts[i], authors[i]])

    # print "*******************************************************"
    # print "++++++++++++++++++++++POSITIVE+++++++++++++++++++++++++"
    # print "*******************************************************"
    # print positive_tweets
    # print "*******************************************************"
    # print " ---------------------NEGATIVE--------------------------"
    # print "*******************************************************"
    # print negative_tweets

    return positive_tweets, negative_tweets


def main(search_term):
    result_count = 15
    result_links = newsSearch(search_term, result_count)

    # dump_all(result_links)

    article_list = []
    summary_list = []
    sentiment_list = []
    pt_list = []
    nt_list = []
    p_users = []
    n_users = []
    url_list = []
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
                # print '----------------------------------'
                # print title
                # summary = textRank(article).encode('ascii', 'ignore')
                # article_list.append(article)
                # summary_list.append(summary + "\n******************************************\n")
                # sum = ""
                # for s in fs.summarize(article, 3):
                #     print '*', s
                #     sum += s+"."
                # summary_new.append(sum)
                # summary_new.append("\n******************************************\n")
                cs.add_article(article)
                # twittersearch(url_entry[0])
                link = url_entry[0]
                url_list.append(link)
                article = readable(url_entry[0], url_entry[1], DEFAULT_ENCODING)
                # title, text = get_only_text(url_entry[1])
                # summary = textRank(article).encode('ascii', 'ignore')
                article_list.append(article)
                # summary_list.append(summary)
                sentiment_list.append(sentiment_analyze(link))

                pt, nt = sentiment_analyze(link)
                for x in pt:
                    pt_list.append(x[0])
                    p_users.append(x[1])
                for y in nt:
                    nt_list.append(y[0])
                    n_users.append(y[1])
            except Exception as ex:
                # print ex
                pass
        # print "Calling summarize"
        # cs.summarize()
    clusters = makeClusters(article_list)
    clust_dict = [[], [], [], [], []]
    article_dict = [[], [], [], [], []]
    summaries = []
    cs = CentroidSummarizer()

    for index, cluster in enumerate(clusters):
        clust_dict[cluster].append(url_list[index])
        article_dict[cluster].append(article_list[index])

    for artic in article_dict:
        cs.set_documents(artic)
        summaries.append(cs.summarize())

    outfile  = open('summary_' + search_term,'w')
    for index, summary in  enumerate(summaries):
        outfile.write("\n============================================\
            LINKS: "+ str(clust_dict[index]) +"\n\n" + summary.encode('ascii','ignore'))
    outfile.close()

    outfile = open('summary1_' + search_term,'w')
    # print(len(url_list), len(summary_new))
    for index, summary in enumerate(summary_new):
        outfile.write("\n============================================\
            LINKS: "+url_list[index]+"\n\n"+ summary.encode('ascii','ignore'))
    outfile.close()
    

    pnr = "+ "+ str(len(pt_list)) +"/ - " + str(len(nt_list))
    # for clus in clust_dict:
        # print clus
    result = {'status': clust_dict, 'articles': summaries, 'positive': pt_list, 'neg': nt_list,
              'p_users': p_users, 'n_users': n_users, 'no_stories': len(article_list), 'no_tweets': (len(pt)+len(nt)),
              'pnr': pnr}
    # print result
    print json.dumps(result)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        exit(-1)
    search_term = '+'.join(sys.argv[1:])

    main(search_term)
