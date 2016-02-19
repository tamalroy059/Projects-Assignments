import sys
import json
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    all_lines=fp.readlines()
    #return all_lines
    return all_lines


def afinnfile(lines):

	score=dict()
	for line in lines:
		term, point= line.split("\t")
		score[term]=int(point)
	#print score.items()
	return score

	#score[term]=int(point)
	#print score.items()

def getTweetScore(lines):
	count=0
	twitter_data=[]
	for line in lines:
		count=count+1
		if count==200:
			break
		dic=json.loads(line)
		if "text" in dic.keys():
			if dic["text"] is not None:
				twitter_data.append (dic["text"])
	return twitter_data

def countPositiveSentiment(score,words):
    count=0
    total=0
    for w in words:
        w=w.lower()
        if w in score.keys():
            total=total+1
            if score[w]>0:
                count=score[w]+1
    return count

def countNegativeSentiment(score,words):
    count=0
    for w in words:
        w=w.lower()
        if w in score.keys():
            if score[w]<0:
                count=score[w]+1
    return count


def getSentiment(score,twitter_data):
    nonSentimentedPositive=dict()
    nonSentimentedNegative=dict()
    for t in twitter_data:
        total=0
        encoded_t=t.encode('utf-8')
        words=re.findall(r"[\w']+", encoded_t)
        pCount=countPositiveSentiment(score,words)
        nCount=countNegativeSentiment(score,words)
        for w in words:
            w=w.lower()
            if w not in score.keys():
                if w in nonSentimentedPositive.keys():
                    nonSentimentedPositive[w]=nonSentimentedPositive[w]+pCount
                else:
                    nonSentimentedPositive[w]=pCount

                if w in nonSentimentedNegative.keys():
                    nonSentimentedNegative[w]=nonSentimentedNegative[w]+nCount
                else:
                    nonSentimentedNegative[w]=nCount

    for word in nonSentimentedNegative.keys():
        if nonSentimentedNegative[word]==0 | nonSentimentedPositive[word]==0:
            print str(word) + " "+str(0)
        elif nonSentimentedNegative[word]==0:
            print str(word) +" " + str(float(nonSentimentedPositive[word]))
        elif nonSentimentedPositive[word]==0:
            print str(word) +" " + str(float(nonSentimentedNegative[word]))
        else:
            print str(word) +" " + str(float(nonSentimentedPositive[word])+float(nonSentimentedPositive[word]))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    score=afinnfile(lines(sent_file))
    twitter_data=getTweetScore(lines(tweet_file))
    getSentiment(score,twitter_data)



if __name__ == '__main__':
    main()
