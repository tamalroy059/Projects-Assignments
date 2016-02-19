import sys
import json
import re

def lines(fp):
    all_lines=fp.readlines()
    return all_lines

def afinnfile(lines):
	score=dict()
	for line in lines:
		term, point= line.split("\t")
		score[term]=int(point)
	return score

def getTweetData(lines):
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


def getFreq(twitter_data):
    wordCount=dict()
    totalCount=0
    for t in twitter_data:
        encoded_t=t.encode('utf-8')
        words=re.findall(r"[\w']+", encoded_t)
        for w in words:
            totalCount+=1
            w=w.lower()
            if w in wordCount:
                wordCount[w]=wordCount[w]+1
            else:
                wordCount[w]=1

    for w in wordCount.keys():
        print str(w)+" "+str(float(wordCount[w])/float(totalCount))

def main():
    tweet_file = open(sys.argv[1])
    twitter_data=getTweetData(lines(tweet_file))
    getFreq(twitter_data)

if __name__ == '__main__':
    main()
