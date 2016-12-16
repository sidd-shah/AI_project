# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
access_token = "131085390-nPFrllPaFKWelHZLfUl24gWOWcqjo3evILSYf3Ia"
access_token_secret = "tNfUPZWFrhaJgwrEjOJQl5YNgSj6R39CHdhjWfq1ymwnB"
consumer_key = "ZkEblJjlLUJ79lSSRwuxLPzjc"
consumer_secret = "IVzIr7mi327mvh9BDt5I25aMmk38GdtM7rXA7ojSsdSTSiTXrp"
f = open('trump_14_3.json', 'a')


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        # Called when raw data is received from connection.
        # Override this method if you wish to manually handle
        # the stream data. Return False to stop stream and close connection.
        try:
            print data
            # print data.text
            f.write(data + '\n')
            # print data.text
            return True
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    while True:
        try:
            stream = Stream(auth, l)

            # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(track=['donald trump,trump,#trump2016'])
        # stream.filter(track=['#BiharPolls'])
        except:
            continue
