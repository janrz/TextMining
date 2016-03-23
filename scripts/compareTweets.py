import csv, os.path
import nltk
from nltk import word_tokenize, re

TEST_DATA_SET_PATH = "data/training.1600000.processed.noemoticon.csv"
TWEETS_OUTPUT_FILE = "output/positive tweets.txt"
POSITIVE_WORD_LIST = "output/positive words.txt"
NEGATIVE_WORD_LIST = "output/negative words.txt"

NUMBER_OF_TWEETS_READ = 100
MINIMUM_POSITIVE_TWEET_SCORE = 1

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

def getWordList(filepath):
    with open(filepath) as file:
        wordList = file.readlines()
    return wordList

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

def stripLastCharacters(wordList):
    strippedList = []
    for word in wordList:
        word = word[:-1]
        strippedList.append(word)
    return strippedList

def rateTweets(tweets, positiveWords, negativeWords):
    tweetList = []
    for (sentiment, subject, tweet, author, datetime) in tweets:
        tokenized = word_tokenize(tweet)
        tweetScore = 0
        for word in tokenized:
            if reformatWord(word) in positiveWords:
                tweetScore += 1
            elif reformatWord(word) in negativeWords:
                tweetScore -= 1
        tweetList.append((tweetScore, tweet, author, datetime))
    return tweetList

def reformatWord(word):
    alphaNumericString = re.sub(r'\W+', '', word) # keep only alphanumeric characters
    stemmer = nltk.stem.snowball.EnglishStemmer()
    stemmedString = stemmer.stem(alphaNumericString)
    return stemmedString
    
def addTweetToFile(tweet, author, datetime, filename):
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
    
def removeExistingOutput(filename):
    if os.path.exists(filename):
        os.remove(filename)
    return  
    
# Import test data
testDataSet = importDataSet(TEST_DATA_SET_PATH, True)

# Get lists for positive and negative words from output files
positiveWordList = stripLastCharacters(getWordList(POSITIVE_WORD_LIST))
negativeWordList = stripLastCharacters(getWordList(NEGATIVE_WORD_LIST))

# Rate tweets
tweetList = rateTweets(testDataSet, positiveWordList, negativeWordList)

# Remove old output
removeExistingOutput(TWEETS_OUTPUT_FILE)

# Export positive tweets
for (score, tweet, author, datetime) in tweetList:
    if score >= MINIMUM_POSITIVE_TWEET_SCORE:
        addTweetToFile(tweet, author, datetime, TWEETS_OUTPUT_FILE)