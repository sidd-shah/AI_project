import Queue
import httplib
import threading
import urllib2

DEFAULT_ENCODING = 'latin-1'


def read_url(url, queue):
    data = ""
    try:
        data = urllib2.urlopen(url).read().decode(DEFAULT_ENCODING)
    except urllib2.HTTPError, e:
        # print('%s: HTTPError = ' % url + str(e.code))
        pass
    except urllib2.URLError, e:
        # print('%s: URLError = ' % url + str(e.reason))
        pass
    except httplib.HTTPException, e:
        # print('HTTPException')
        pass
    except Exception:
        import traceback
        pass
        # print('generic exception: ' + traceback.format_exc())

    # print('Fetched %s from %s' % (len(data), url))
    queue.put([url, data])


def fetch_parallel(list_of_urls):
    result = Queue.Queue()
    threads = [threading.Thread(target=read_url, args=(url, result)) for url in list_of_urls]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result
