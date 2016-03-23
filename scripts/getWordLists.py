import nltk, csv, os.path
from nltk import FreqDist, re
from nltk import word_tokenize

TRAINING_DATA_SET_PATH = "data/testdata.manual.2009.06.14.csv"
OUTPUT_FILE_POSITIVE = "output/positive words.txt"
OUTPUT_FILE_NEGATIVE = "output/negative words.txt"

IDENTIFICATION_THRESHOLD = 3.
MINIMUM_NUMBER_OF_OCCURRENCES = 2
MINIMUM_WORD_LENGTH = 4
EXCLUDED_TAGS = ['IN', 'VB', 'NN', 'NNP', 'NNS', 'PRP', 'PRP$']
counter = 1
def importDataSet(path):
    dataSet = []
    with open(path, "rb") as data:
        reader = csv.reader(data)
        for row in reader:
            tweetData = (row[0], row[3], row[5], row[4], row[2]) #(sentiment, subject, tweet, author, date and time)
            dataSet.append(tweetData)
    return dataSet

def filterTweets(dataSet):
    global counter
    filteredTweets = []
    for (sentiment, subject, words, author, datetime) in dataSet:
        tokenized = word_tokenize(words)
        wordsFiltered = []
        for word in tokenized:
            word = word.lower()
            if len(word) >= MINIMUM_WORD_LENGTH and not word[0] == '@':
                wordsFiltered.append(word)
        wordsTagged = nltk.pos_tag(wordsFiltered)
        filteredAndTagged = []
        for (word, tag) in wordsTagged:
            if tag not in EXCLUDED_TAGS:
                filteredAndTagged.append((word, tag))
        filteredTweets.append((sentiment, subject, filteredAndTagged))
        print counter
        counter += 1
    return filteredTweets

def categorizeTweets(tweets, category):
    categorizedTweets = []
    for tweet in tweets:
        if tweet[0] == category:
            for (word, tag) in tweet[2]:
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
        if numberOfOccurrences >= MINIMUM_NUMBER_OF_OCCURRENCES:
            newList.append((word, numberOfOccurrences))
    return newList

def createFile(wordList, filename):
    textFile = open(filename, "w")
    if len(wordList) >= 1:
        textFile.write(wordList[0][0])
        textFile.write("\n")
        if len(wordList) >= 2:
            textFile = open(filename, "a")
            for word in wordList[1:]:
                textFile.write(word[0])
                textFile.write("\n")
    return

def removeExistingOutput(filename):
    if os.path.exists(filename):
        os.remove(filename)
    return
    
#Import training data set
trainingDataSet = importDataSet(TRAINING_DATA_SET_PATH)
print "Data set of %i tweets imported" % len(trainingDataSet)

'''
Filter tweets:
- All words will be turned into lowercase words
- Remove words shorter than 3 characters
- Remove words starting with <@>: word is a user name, likely to not be a real word
'''
filteredTweets = filterTweets(trainingDataSet)
print "Tweets filtered"

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
print "Word lists created"

'''
- A frequency distribution is made for each category
- The frequency distribution is changed to a list object, to allow modifications to the data
'''
negativeList = freqDistToList(FreqDist(negativeWords))
neutralList = freqDistToList(FreqDist(neutralWords))
positiveList = freqDistToList(FreqDist(positiveWords))
print "Frequency distributions created"

'''
Words occurring NUMBER_OF_OCCURRENCES or less are removed, because they will 
probably not be useful in deciding whether a word is negative, positive or neutral
'''
negativeList = removeInfrequentWords(negativeList)
neutralList = removeInfrequentWords(neutralList)
positiveList = removeInfrequentWords(positiveList)
print "Infrequent words removed"

'''
If a word occurs more than IDENTIFICATION_THRESHOLD times more often in one list 
than in both other lists it is considered to be a decisive word in categorizing a tweet.
The word is then added to the list belonging to its category.
'''
truePositiveList = compareWords(positiveList, negativeList, neutralList)
print "Positive word list created"
trueNegativeList = compareWords(negativeList, neutralList, positiveList)
print "Negative word list created"

#Remove old output files if they exist
removeExistingOutput(OUTPUT_FILE_POSITIVE)
removeExistingOutput(OUTPUT_FILE_NEGATIVE)
print "Old output deleted"

#Export word lists to text files
createFile(truePositiveList, OUTPUT_FILE_POSITIVE)
createFile(trueNegativeList, OUTPUT_FILE_NEGATIVE)
print "Output created"
print "\nProgram finished"