from GoogleNews import newsSearch
from bsReadability import readable
import urllib2
from bs4 import BeautifulSoup
from twitter import twittersearch
import fetch_url
from Summary import textRank
from summ import FrequencySummarizer
import sys
import re
from CentroidSummarizer import CentroidSummarizer

DEFAULT_ENCODING = 'latin-1'


def print_usage():
    print "USAGE:"
    print "%s <SEARCH TERM>" % sys.argv[0]


def dump_all(l):
    for i in l:
        print i


def get_only_text(url):
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text


def main(search_term):
    result_count = 2
    result_links = newsSearch(search_term, result_count)

    dump_all(result_links)

    article_list = []
    summary_list = []
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
