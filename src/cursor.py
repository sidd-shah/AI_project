def get_tweets(keyword, limit=1000, debug=False):
    import tweepy
    result = set()
    auth = tweepy.AppAuthHandler('NVHNnaLGqNimBCNPl20nXD7bw', 'cmqdCIuUAlOqdGaExEarMbTcn68Qly65GnTj665COpj5NH2wjb')
<<<<<<< HEAD
    auth = tweepy.AppAuthHandler('GebRqhJNATDN5C4DgHSlJiDKm', '1tkgK3ic3mJollNwU6CrQIncFslC34T1hVg2EmxfBnZKNvLaS9')

    api = tweepy.API(auth,
                     wait_on_rate_limit=False,
                     wait_on_rate_limit_notify=False)
=======
    # auth = tweepy.AppAuthHandler('GebRqhJNATDN5C4DgHSlJiDKm', '1tkgK3ic3mJollNwU6CrQIncFslC34T1hVg2EmxfBnZKNvLaS9')

    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
>>>>>>> 8a7a6030fb9a78b5eba17a287e1729faeef816f5

    for tweet in tweepy.Cursor(api.search,
                               q=keyword,
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items(limit=limit):
        # print tweet.created_at, tweet.text
        if debug:
            print tweet.text
        result.add(tweet)

    return result


if __name__ == '__main__':
    get_tweets(
        "http://indianexpress.com/article/india/pm-narendra-modi-sits-through-hamid-ansari-critique-interacts-only-"
        "with-bjp-mps-4431239/")
