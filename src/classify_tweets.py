import pickle
from ttp import ttp
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
import os


def load_classifier(classifier):
    classifier_list = pickle.load(open(classifier, "rb"))
    vectorizer = classifier_list[0]
    classifier_svm = classifier_list[1]
    classifier_nb = classifier_list[2]
    return vectorizer, classifier_svm, classifier_nb


def load_unlabelled_dataset(filename):
    dataset = pickle.load(open(filename, 'rb'))
    # tweets = pickle.load(open('cruz_list_combined.p', 'rb'))
    result = set()

    for tweet in dataset:
        result.add(tweet)

    total_tweet_count = len(result)
    print("Dataset count: \t\t%s" % total_tweet_count)

    return list(result)


def main():
    classifier_root = "classifiers/"
    hillary_vectorizer, hillary_svm, hillary_nb = load_classifier(classifier_root + "hillary.p")
    trump_vectorizer, trump_svm, trump_nb = load_classifier(classifier_root + "trump.p")
    entity_vectorizer, entity_svm, entity_nb = load_classifier(classifier_root + "entity.p")

    filename = "all_tweets.p"
    dataset = load_unlabelled_dataset(filename)
    entity_vectors = entity_vectorizer.transform(dataset)
    entity_svm_predictions = entity_svm.predict(entity_vectors)

    hillary_dataset = []
    trump_dataset = []

    hillary_positive_count = 0
    hillary_negative_count = 0

    trump_positive_count = 0
    trump_negative_count = 0

    for i in range(len(entity_svm_predictions)):
        if entity_svm_predictions[i] == "hillary":
            hillary_dataset.append(dataset[i])
        else:
            trump_dataset.append(dataset[i])

    hillary_count = len(hillary_dataset)
    trump_count = len(trump_dataset)

    hillary_vectors = hillary_vectorizer.transform(hillary_dataset)
    trump_vectors = trump_vectorizer.transform(trump_dataset)

    hillary_predictions = hillary_svm.predict(hillary_vectors)
    trump_predictions = trump_svm.predict(trump_vectors)

    for i in hillary_predictions:
        if i == "positive":
            hillary_positive_count += 1
        else:
            hillary_negative_count += 1

    for i in trump_predictions:
        if i == "positive":
            trump_positive_count += 1
        else:
            trump_negative_count += 1

    print("Total:")
    print("Hillary:\t%s\t-\t%s :Trump\n" % (hillary_count, trump_count))
    print("Positive:")
    print("Hillary:\t%s\t-\t%s :Trump\n" % (hillary_positive_count, trump_positive_count))
    print("Negative:")
    print("Hillary:\t%s\t-\t%s :Trump\n" % (hillary_negative_count, trump_negative_count))

    if hillary_positive_count + trump_negative_count > hillary_negative_count + trump_positive_count:
        print("Hillary wins!")
        print("Make Donald Drumpf again!")
    else:
        print("Trump triumphs!")
        print("Make America Great again!")

    sentence = raw_input("Enter sentence to classify:")
    while sentence != "break":
        sentence_vector = entity_vectorizer.transform([sentence])
        sentence_entity = entity_svm.predict(sentence_vector)
        # print(sentence_entity)
        if sentence_entity[0] == "hillary":
            sentence_vector = hillary_vectorizer.transform([sentence])
            sentence_prediction = hillary_svm.predict(sentence_vector)
            print("Prediction for hillary: %s" % sentence_prediction)
        else:
            sentence_vector = trump_vectorizer.transform([sentence])
            sentence_prediction = trump_svm.predict(sentence_vector)
            print("Prediction for trump: %s" % sentence_prediction)
        sentence = raw_input("Enter sentence to classify:")


def clean(list_of_tweets_texts):
    p = ttp.Parser(include_spans=True)
    dataset = list_of_tweets_texts
    result_set = []
    for mystring in dataset:
        try:
            mystring.encode('utf8', 'ignore')
            sentence = mystring
            result = p.parse(mystring)
            try:
                start = result.urls[0][1][0]
                end = result.urls[0][1][1]
                sentence = mystring[:start] + mystring[end:]
            except:
                pass
            result_set.append(sentence)
        except (IndexError, UnicodeDecodeError) as e:
            pass
    return result_set


def predict(list_of_tweet_texts):
    dataset = list_of_tweet_texts
    classifier_path = "%s/classifier/pol.p" % os.path.join(os.path.dirname(__file__))
    # print classifier_path
    vectorizer, svm, nb = load_classifier(classifier_path)
    data_vectors = vectorizer.transform(dataset)
    svm_predict = svm.predict(data_vectors)
    nb_predict = nb.predict(data_vectors)

    # positive_tweets = []
    # negative_tweets = []

    result = []

    for i, prediction in enumerate(svm_predict):
        if prediction == "positive":
            result.append(1)
        else:
            result.append(-1)

    # result = dict()
    # result['positive'] = positive_tweets
    # result['negative'] = negative_tweets
    # result['pos_count'] = len(positive_tweets)
    # result['neg_count'] = len(negative_tweets)
    # result['total_count'] = len(dataset)

    return result


def vader(list_of_tweet_texts):
    sid = SentimentIntensityAnalyzer()
    result = []
    for tweet in list_of_tweet_texts:
        ss = sid.polarity_scores(tweet)
        classification = ss['compound']
        if abs(classification) > 0.5:
            result.append(classification / abs(classification))
        else:
            result.append(0)
    return result


if __name__ == "__main__":
    print predict(["Donald Trump is awesomeadasd ", ])
