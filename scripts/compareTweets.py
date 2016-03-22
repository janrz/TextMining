import csv, os.path

TEST_DATA_SET_PATH = "../data/training.1600000.processed.noemoticon.csv"
TWEETS_OUTPUT_FILE = "../output/positive tweets.txt"
POSITIVE_WORD_LIST = "../output/positive words.txt"
NEGATIVE_WORD_LIST = "../output/negative words.txt"

NUMBER_OF_TWEETS_READ = 100
MINIMUM_TWEET_SCORE = 1

def importDataSet(path, limitNumberOfTweetsRead = False):
    dataSet = []
    numberOfTweets = 0
    with open(path, "rb") as data:
        reader = csv.reader(data)
        for row in reader:
            if numberOfTweets < NUMBER_OF_TWEETS_READ:
                tweetData = (row[0], row[3], row[5], row[4], row[2]) # (sentiment, subject, tweet, author, date and time)
                dataSet.append(tweetData)
                if limitNumberOfTweetsRead:
                    numberOfTweets += 1
    return dataSet

def showTweets(tweets, wordList):
    positiveWords = wordList[0]
    negativeWords = wordList[1]
    for (sentiment, subject, tweet, author, datetime) in tweets:
        tweet = tweet.split()
        positive = countWordsInCategory(tweet, positiveWords)
        negative = countWordsInCategory(tweet, negativeWords)
        wordScore = positive - negative
        if wordScore >= MINIMUM_TWEET_SCORE:
            addTweetToFile(tweet, author, datetime, TWEETS_OUTPUT_FILE)
    return

def countWordsInCategory(tweet, category):
    counter = 0
    for tweetWord in tweet:
        for categoryWord in category:
            if tweetWord == categoryWord[0]:
                counter += 1
    return counter

def addTweetToFile(tweet, author, datetime, filename):
    tweet = " ".join(tweet)
    tweetData = []
    tweetData.append(author)
    tweetData.append(datetime)
    tweetData.append(tweet)
    if not os.path.isfile(filename):
        textFile = open(filename, "w")
    else:
        textFile = open(filename, "a")
    for element in tweetData:
        textFile.write(element)
        textFile.write("\n")
    return

testDataSet = importDataSet(TEST_DATA_SET_PATH, True)