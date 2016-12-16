import pickle
import time

import nltk
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


def train_classifier_obsolete(tweets, training_tweets, testing_tweets):
    """
    Uses svm and naivebayes from nltk to classify tweets as positive and negative

    :param tweets: a list of labelled tweets in the tuple format - [(tweet, sentiment), ...]
    :param training_tweets: the partition of tweets used for training
    :param testing_tweets: the partition of tweets used for testing
    :return: correct result count of svm, nb, and both together
    """

    def get_words_in_tweets(tweets_get):
        all_words = []
        for (words, sentiment) in tweets_get:
            all_words.extend(words)
        return all_words

    def get_word_features(wordlist_get):
        wordlist_get = nltk.FreqDist(wordlist_get)
        word_features = wordlist_get.keys()
        return word_features

    word_features = get_word_features(get_words_in_tweets(training_tweets))

    def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    training_set = nltk.classify.apply_features(extract_features, training_tweets)
    nb_classifier = nltk.NaiveBayesClassifier.train(training_set)

    svm_classifier = nltk.classify.SklearnClassifier(LinearSVC())
    svm_classifier.train(training_set)

    svm_results = []
    nb_results = []
    results = []

    for tweet in testing_tweets:
        test_line = tweet[0]
        tweet_words = test_line.split()
        svm_result = svm_classifier.classify(extract_features(tweet_words))
        nb_result = nb_classifier.classify(extract_features(tweet_words))
        result = tweet[1]
        svm_results.append(svm_result)
        nb_results.append(nb_result)
        results.append(result)
        # print("%s:%s:%s" % (svm_result, nb_result, result))

    return svm_results, nb_results, results


def train_classifier_sklearn(training_tweets, testing_tweets, training_labels, testing_labels):
    """
    Uses svm and naivebayes from sklearn to classify tweets as positive and negative

    :param training_tweets:
    :param testing_tweets:
    :param training_labels:
    :param testing_labels:
    :return:
    """

    # Read the data
    train_data = training_tweets
    train_labels = training_labels
    test_data = testing_tweets
    test_labels = testing_labels

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

    # """
    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    t0 = time.time()
    classifier_rbf.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_rbf = classifier_rbf.predict(test_vectors)
    t2 = time.time()
    time_rbf_train = t1 - t0
    time_rbf_predict = t2 - t1
    # """

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1 - t0
    time_linear_predict = t2 - t1

    # """
    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    t0 = time.time()
    classifier_liblinear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_liblinear = classifier_liblinear.predict(test_vectors)
    t2 = time.time()
    time_liblinear_train = t1 - t0
    time_liblinear_predict = t2 - t1
    # """

    # Print results in a nice table
    print("Results for SVC(kernel=rbf)")
    print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
    print(classification_report(test_labels, prediction_rbf))
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction_linear))
    print("Results for LinearSVC()")
    print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    print(classification_report(test_labels, prediction_liblinear))


    # Naive Bayes Classifier
    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, and the existing classifications in the training set.
    # nb = MultinomialNB()
    nb = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    t0 = time.time()
    nb.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_nb = nb.predict(test_vectors)
    t2 = time.time()
    time_nb_train = t1 - t0
    time_nb_predict = t2 - t1

    print("Results for Naive Bayes (MultinomialNB)")
    print("Training time: %fs; Prediction time: %fs" % (time_nb_train, time_nb_predict))
    print(classification_report(test_labels, prediction_nb))
    return vectorizer, classifier_linear, nb


def load_dataset_sklearn(filename):
    dataset = pickle.load(open(filename, 'rb'))
    # tweets = pickle.load(open('cruz_list_combined.p', 'rb'))
    data = []
    target = []

    for (tweet, sentiment) in dataset:
        data.append(tweet)
        target.append(sentiment)

    total_tweet_count = len(data)

    # print("Dataset count: \t\t%s" % total_tweet_count)

    return data, target


def load_and_partition_dataset_sklearn(filename):
    dataset = pickle.load(open(filename, "rb"))
    # tweets = pickle.load(open('cruz_list_combined.p', 'rb'))
    data = []
    target = []
    for (tweet, sentiment) in dataset:
        data.append(tweet)
        target.append(sentiment)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=1810)
    total_tweet_count = len(data)
    training_tweet_count = len(X_train)
    testing_tweet_count = len(X_test)
    print("Total count: \t\t%s" % total_tweet_count)
    print("Testing count: \t\t%s" % testing_tweet_count)
    print("Training count: \t%s" % training_tweet_count)
    return X_train, X_test, y_train, y_test



def load_and_label_and_dump(filename, label, dumpname=""):
    dataset = pickle.load(open(filename, 'rb'))
    # tweets = pickle.load(open('cruz_list_combined.p', 'rb'))
    data = []
    resultset = []
    target = []

    for (tweet, sentiment) in dataset:
        data.append(tweet)
        target.append(sentiment)

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=1810)

    total_tweet_count = len(data)
    training_tweet_count = len(X_train)
    testing_tweet_count = len(X_test)

    for i in range(total_tweet_count):
        resultset.append((data[i], label))

    # print("Total count: \t\t%s" % total_tweet_count)
    # print("Testing count: \t\t%s" % testing_tweet_count)
    # print("Training count: \t%s" % training_tweet_count)

    pickle.dump(resultset, open(dumpname, "wb"))


def load_dataset_nltk(filename):
    X_train, X_test, y_train, y_test = load_and_partition_dataset_sklearn(filename)
    training_labelled_tweets = []
    for x, y in zip(X_train, y_train):
        training_labelled_tweets.append((x, y))
    testing_labelled_tweets = []
    for x, y in zip(X_test, y_test):
        testing_labelled_tweets.append((x, y))
    all_labelled_tweets = training_labelled_tweets + testing_labelled_tweets
    return all_labelled_tweets, training_labelled_tweets, testing_labelled_tweets


def accuracy_three(svm_results, nb_results, results, total_tweet_count):
    both_correct = 0
    svm_correct = 0
    nb_correct = 0

    testing_tweet_count = len(results)
    training_tweet_count = total_tweet_count - testing_tweet_count
    print
    testing_tweet_count

    for svm_result_a, nb_result_a, result_a in zip(svm_results, nb_results, results):
        if svm_result_a == nb_result_a and nb_result_a == result_a:
            both_correct += 1
            svm_correct += 1
            nb_correct += 1
        elif svm_result_a == result_a:
            svm_correct += 1
        elif nb_result_a == result_a:
            nb_correct += 1

    print("SVM:\t\t %s :: %s" % (svm_correct, svm_correct * 1.0 / testing_tweet_count * 100.0))
    print("Naive Bayes: %s :: %s" % (nb_correct, nb_correct * 1.0 / testing_tweet_count * 100.0))
    print("Both:\t\t %s :: %s" % (both_correct, both_correct * 1.0 / testing_tweet_count * 100.0))


def predict_and_dump_list(training_tweets, testing_tweets, training_labels, testing_labels):
    """
    Uses svm and naivebayes from sklearn to classify tweets as positive and negative

    :param training_tweets:
    :param testing_tweets:
    :param training_labels:
    :param testing_labels:
    :return:
    """

    # Read the data
    train_data = training_tweets
    train_labels = training_labels
    test_data = testing_tweets
    test_labels = testing_labels

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

    # """
    # Perform classification with SVM, kernel=rbf
    classifier_rbf = svm.SVC()
    t0 = time.time()
    classifier_rbf.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_rbf = classifier_rbf.predict(test_vectors)
    t2 = time.time()
    time_rbf_train = t1 - t0
    time_rbf_predict = t2 - t1
    # """

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1 - t0
    time_linear_predict = t2 - t1

    # """
    # Perform classification with SVM, kernel=linear
    classifier_liblinear = svm.LinearSVC()
    t0 = time.time()
    classifier_liblinear.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_liblinear = classifier_liblinear.predict(test_vectors)
    t2 = time.time()
    time_liblinear_train = t1 - t0
    time_liblinear_predict = t2 - t1
    # """

    # Print results in a nice table
    # print("Results for SVC(kernel=rbf)")
    # print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
    # print(classification_report(test_labels, prediction_rbf))
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction_linear))
    # print("Results for LinearSVC()")
    # print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    # print(classification_report(test_labels, prediction_liblinear))


    # Naive Bayes Classifier
    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, and the existing classifications in the training set.
    # nb = MultinomialNB()
    nb = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    t0 = time.time()
    nb.fit(train_vectors, train_labels)
    t1 = time.time()
    prediction_nb = nb.predict(test_vectors)
    t2 = time.time()
    time_nb_train = t1 - t0
    time_nb_predict = t2 - t1

    print("Results for Naive Bayes (MultinomialNB)")
    print("Training time: %fs; Prediction time: %fs" % (time_nb_train, time_nb_predict))
    print(classification_report(test_labels, prediction_nb))


def sklearn_train_and_dump(training_tweets, training_labels):
    """
    Uses svm and naivebayes from sklearn to classify tweets as positive and negative

    :param training_tweets:
    :param testing_tweets:
    :param training_labels:
    :param testing_labels:
    :return:
    """

    # Read the data
    train_data = training_tweets
    train_labels = training_labels

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    # test_vectors = vectorizer.transform(test_data)

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')

    # Naive Bayes Classifier
    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, and the existing classifications in the training set.
    nb = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    pickle.dump(nb, open("sklearn_nb.p", "w"))
    pickle.dump(classifier_linear, open("sklearn_svm.p", "w"))


def sklearndata_to_ntlkdata(data, target):
    length = len(data)
    result = []
    for i in range(length):
        result.append((data[i], target[i]))
    return result


def sklearn_load_and_test(testing_tweets, testing_labels):
    # Read the data
    test_data = testing_tweets
    test_labels = testing_labels

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    test_vectors = vectorizer.transform(test_data)

    # Perform classification with SVM, kernel=linear
    classifier_linear = pickle.load(open("sklearn_svm.p", "rb"))
    prediction_linear = classifier_linear.predict(test_vectors)

    # Naive Bayes Classifier
    # Fit a naive bayes model to the training data.
    # This will train the model using the word counts we computer, and the existing classifications in the training set.
    nb = pickle.load(open("sklearn_nb.p", "w"))
    prediction_nb = nb.predict(test_vectors)

    print("Results for SVC(kernel=linear)")
    print(classification_report(test_labels, prediction_linear))

    print("Results for Naive Bayes (MultinomialNB)")
    print(classification_report(test_labels, prediction_nb))


def generate_word_list(data, label):
    length = len(data)
    positive_words = []
    negative_words = []
    for i in range(length):
        if label[i] == "positive":
            print(data[i].upper())
            positive_words.append(data[i].split())
        else:
            print(data[i].lower())
            negative_words.append(data[i].split())


def load_dataset_multi_cat(filename1, filename2):
    data1, target1 = load_dataset_sklearn(filename1)
    data2, target2 = load_dataset_sklearn(filename2)
    for i in range(len(data1)):
        target1[i] = "p1-" + target1[i]
    for i in range(len(data2)):
        target2[i] = "p2-" + target2[i]
    return data1 + data2, target1 + target2


def load_partition_multi_cat(filename1, filename2):
    return train_test_split(load_dataset_multi_cat(filename1, filename2))


def combine(file1, file2, result_file):
    result = []
    data1, target1 = load_dataset_sklearn(file1)
    data2, target2 = load_dataset_sklearn(file2)

    for i, z in zip(data1, target1):
        result.append((i, z))

    for i, z in zip(data2, target2):
        result.append((i, z))

    pickle.dump(result, open(result_file, "wb"))


if __name__ == "__main__":
    # filename = 'cruz_list_combined.p'
    # filename = 'tedCruz_43k_7th_vader.p'
    # filename = 'trump_43k_9th_vader.p'
    # filename = 'trump_list_combined.p'

    # train_filename = input("Training file:")
    # test_filename = input("Testing file:")
    #
    # print("******************** Training dataset **********************")
    # tweets_train, labels_train = load_dataset_sklearn(train_filename)
    # print("**************** End of Training dataset *******************\n\n")
    #
    # print("********************* Testing dataset **********************")
    # tweets_test, labels_test = load_dataset_sklearn(test_filename)
    # print("***************** End of Testing dataset *******************\n\n")
    #
    # nltk_training = sklearndata_to_ntlkdata(tweets_train, labels_train)
    # nltk_testing = sklearndata_to_ntlkdata(tweets_test, labels_test)
    # nltk_all = nltk_training + nltk_testing

    # train_classifier_sklearn(tweets_train, tweets_test, labels_train, labels_test)
    ### all_tweets, labelled_training_tweets, labelled_testing_tweets = load_dataset_nltk(train_filename)
    # svm_result, nb_result, result = train_classifier_obsolete(nltk_all, nltk_training, nltk_testing)
    # accuracy_three(svm_result, nb_result, result, len(nltk_all))
    datasets_home = "../Datasets/"

    hillary_file = "hillary-agg-17-3-0.8.p"
    # trump_file = "trump_list_combined.p"
    trump_file = "trump-agg.p"
    hillary_entity_file = "hillary-entity.p"
    trump_entity_file = "trump-entity.p"
    combined_entity_file = "combined-entity.p"

    # print("test!")
    # hillary_train, hillary_test, hillary_train_labels, hillary_test_labels = load_and_partition_dataset_sklearn(
    #     "list.p")
    # hillary_vectorizer, hillary_svm, hillary_nb = train_classifier_sklearn(hillary_train, hillary_test,
    #                                                                        hillary_train_labels, hillary_test_labels)

    print("Hillary!")
    hillary_train, hillary_test, hillary_train_labels, hillary_test_labels = load_and_partition_dataset_sklearn(
        datasets_home + hillary_file)
    hillary_vectorizer, hillary_svm, hillary_nb = train_classifier_sklearn(hillary_train, hillary_test,
                                                                           hillary_train_labels, hillary_test_labels)

    print("Trump!")
    trump_train, trump_test, trump_train_labels, trump_test_labels = load_and_partition_dataset_sklearn(datasets_home + trump_file)
    trump_vectorizer, trump_svm, trump_nb = train_classifier_sklearn(trump_train, trump_test, trump_train_labels,
                                                                     trump_test_labels)

    load_and_label_and_dump(datasets_home + hillary_file, "hillary", hillary_entity_file)
    load_and_label_and_dump(datasets_home + trump_file, "trump", trump_entity_file)

    combine(hillary_entity_file, trump_entity_file, combined_entity_file)

    print("Entity!")
    entity_train, entity_test, e_train_labels, e_test_labels = load_and_partition_dataset_sklearn(combined_entity_file)
    entity_vectorizer, entity_svm, entity_nb = train_classifier_sklearn(entity_train, entity_test, e_train_labels,
                                                                        e_test_labels)

    pickle.dump([entity_vectorizer, entity_svm, entity_nb], open("classifiers/entity.p", "wb"))
    pickle.dump([hillary_vectorizer, hillary_svm, hillary_nb], open("classifiers/hillary.p", "wb"))
    pickle.dump([trump_vectorizer, trump_svm, trump_nb], open("classifiers/trump.p", "wb"))
