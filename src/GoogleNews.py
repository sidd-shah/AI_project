import urllib2
from xml.dom.minidom import parseString
import sys


def newsSearch(term, count):
    term = "+".join(term.split())
    results = []  # List for storing the URLs

    obj = parseString(urllib2.urlopen(
        'http://news.google.com/news?q=%s&output=rss&num=%s' % (term,
                                                                str(count))).read())
    links = obj.getElementsByTagName('link')[2: count + 2]
    for link in links:
        results.append(link.childNodes[0].data.split('=')[-1])
    return results


if __name__ == '__main__':
    for link in newsSearch("Narendra Modi", 15):
        print link