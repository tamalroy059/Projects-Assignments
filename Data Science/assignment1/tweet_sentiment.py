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

def printSentiment(score,twitter_data):
	for t in twitter_data:
		total=0
		encoded_t=t.encode('utf-8')
		words=re.findall(r"[\w']+", encoded_t)

		for w in words:
			w=w.lower()
			if w in score.keys():
				total=total+score[w]
		print total
	
		

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    score=afinnfile(lines(sent_file))
    twitter_data=getTweetScore(lines(tweet_file))

    printSentiment(score,twitter_data)



if __name__ == '__main__':
    main()



