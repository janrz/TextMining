import csv, os.path

TWEET_DATA_PATH = "data/training.1600000.processed.noemoticon.csv"
TWEETS_OUTPUT_FILE = "output/all tweets.txt"
NUMBER_OF_TWEETS_READ = 100

def importDataSet(path, limitNumberOfTweetsRead = True):
    dataSet = []
    numberOfTweets = 0
    with open(path, "rb") as data:
        reader = csv.reader(data)
        for row in reader:
            if numberOfTweets < NUMBER_OF_TWEETS_READ:
                tweetData = (row[5], row[4], row[2]) # (tweet, author, date and time)
                dataSet.append(tweetData)
                if limitNumberOfTweetsRead:
                    numberOfTweets += 1
    return dataSet
	
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
    
dataSet = importDataSet(TWEET_DATA_PATH)
removeExistingOutput(TWEETS_OUTPUT_FILE)
for (tweet, author, datetime) in dataSet:
	addTweetToFile(tweet, author, datetime, TWEETS_OUTPUT_FILE)