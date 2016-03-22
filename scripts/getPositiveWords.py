import nltk, csv, os.path
from nltk import FreqDist, re
from nltk import word_tokenize

TRANING_DATA_SET_PATH = "../data/testdata.manual.2009.06.14.csv"
TEST_DATA_SET_PATH = "../data/training.1600000.processed.noemoticon.csv"
OUTPUT_FILE_POSITIVE = "../output/positive words.txt"
OUTPUT_FILE_NEGATIVE = "../output/negative words.txt"

IDENTIFICATION_THRESHOLD = 3.
MINIMUM_NUMBER_OF_OCCURRENCES = 1.
NUMBER_OF_TWEETS_READ = 100
MINIMUM_SCORE = 1

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

def filterTweets(dataSet):
    filteredTweets = []
    for (sentiment, subject, words, author, datetime) in dataSet:
        tokenized = word_tokenize(words)
        tagged = nltk.pos_tag(tokenized)
        #wordsFiltered = [x.lower() for x in tagged if len(x) >= 3 and not x[0] == '@']
        
        wordsFiltered = []
        for (word, tag) in tagged:
            word = word.lower()
            if len(word) >= 3 and not word[0] == '@' and not tag == 'NN':
                wordsFiltered.append(word)
                
        filteredTweets.append((sentiment, subject, wordsFiltered))
    return filteredTweets

def categorizeTweets(tweets, category):
    categorizedTweets = []
    for tweet in tweets:
        if tweet[0] == category:
            for word in tweet[2]:
                word = reformatWord(word)
                categorizedTweets.append(word)
    return categorizedTweets

def reformatWord(word):
    alphaNumericString = re.sub(r'\W+', '', word) # keep only alphanumeric characters
    stemmer = nltk.stem.snowball.EnglishStemmer()
    stemmedString = stemmer.stem(alphaNumericString)
    return stemmedString

def compareWords(wordList, compareList1, compareList2):
    trainedWords = []
    for word in wordList:
        testWord = word[0]
        compareList1Word = listHasWord(compareList1, testWord)
        compareList2Word = listHasWord(compareList2, testWord)
        # If neither of the other lists has the word it is classified as correct and added to the trained words
        if (compareList1Word == None) and (compareList2Word == None):
            trainedWords.append(word)
            continue
        # Compare numbers of occurrences of word in lists, if it occurs in 
        else:
            list1Ratio = calculateOccurrenceRatio(word,compareList1Word)
            list2Ratio = calculateOccurrenceRatio(word,compareList2Word)
        if (list1Ratio >= IDENTIFICATION_THRESHOLD or list1Ratio == None) and (list2Ratio >= IDENTIFICATION_THRESHOLD or list2Ratio == None):
            trainedWords.append(word)
    return trainedWords

def calculateOccurrenceRatio(firstWord, secondWord):
    if (secondWord != None):
        # Divide number of occurrences of first word by number of occurrences of second word
        ratio = float(firstWord[1]) / float(secondWord[1]) 
        return ratio
    else:
        return None
           
def freqDistToList(freqDist):
    newList = []
    for item in freqDist.viewitems():
        newList.append(item)
    return newList

# Checks presence of testWord in list, returns word and its number of occurrences as a tuple if it is present
def listHasWord(wordList, testWord):
    for word in wordList:
        if word[0] == testWord:
            return word
    return None

def removeInfrequentWords(wordList):
    newList = []
    for (word, numberOfOccurrences) in wordList:
        if numberOfOccurrences > MINIMUM_NUMBER_OF_OCCURRENCES:
            newList.append((word, numberOfOccurrences))
    return newList
 
def showTweets(tweets, wordList):
    positiveWords = wordList[0]
    negativeWords = wordList[1]
    for (sentiment, subject, tweet, author, datetime) in tweets:
        tweet = tweet.split()
        positive = countWordsInCategory(tweet, positiveWords)
        negative = countWordsInCategory(tweet, negativeWords)
        wordScore = positive - negative
        if wordScore >= MINIMUM_SCORE:
            addTweetToFile(tweet, author, datetime, OUTPUT_FILE)
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

def createFile(wordList, filename):
    

def removeExistingOutput(filename):
    if os.path.exists(filename):
        os.remove(filename)
    return
    
#Import training data set
trainingDataSet = importDataSet(TRANING_DATA_SET_PATH)

'''
Filter tweets:
- All words will be turned into lowercase words
- Remove words shorter than 3 characters
- Remove words starting with <@>: word is a user name, likely to not be a real word
'''
filteredTweets = filterTweets(trainingDataSet)

'''
Categorize tweets:
- Create three lists, each containing all tweets belonging to the given category (0, 2 or 4)
- Words are reformatted:
    - Only alphanumeric characters are kept
    - Words are stemmed
'''
negativeWords = categorizeTweets(filteredTweets, '0')
neutralWords = categorizeTweets(filteredTweets, '2')
positiveWords = categorizeTweets(filteredTweets, '4')

'''
- A frequency distribution is made for each category
- The frequency distribution is changed to a list object, to allow modifications to the data
'''
negativeList = freqDistToList(FreqDist(negativeWords))
neutralList = freqDistToList(FreqDist(neutralWords))
positiveList = freqDistToList(FreqDist(positiveWords))

'''
Words occurring NUMBER_OF_OCCURRENCES or less are removed, because they will 
probably not be useful in deciding whether a word is negative, positive or neutral
'''
negativeList = removeInfrequentWords(negativeList)
neutralList = removeInfrequentWords(neutralList)
positiveList = removeInfrequentWords(positiveList)

'''
If a word occurs more than IDENTIFICATION_THRESHOLD times more often in one list 
than in both other lists it is considered to be a decisive word in categorizing a tweet.
The word is then added to the list belonging to its category.
'''
trueNegativeList = compareWords(negativeList, neutralList, positiveList)
trueNeutralList = compareWords(neutralList, negativeList, positiveList)
truePositiveList = compareWords(positiveList, negativeList, neutralList)

# #Add word lists to array
# wordList = [truePositiveList, trueNegativeList]

# #Import test data
# testDataSet = importDataSet(TEST_DATA_SET_PATH, True)

#Remove old output file if it exists
removeExistingOutput(OUTPUT_FILE_POSITIVE)
removeExistingOutput(OUTPUT_FILE_NEGATIVE)

#Export word lists to text files
createFile(truePositiveList, OUTPUT_FILE_POSITIVE)
createFile(trueNegativeList, OUTPUT_FILE_NEGATIVE)
#Add all positive tweets to new text file.
showTweets(testDataSet, wordList)