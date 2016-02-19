import sys
import json
import re
import operator

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
    #sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[1])
    tweet_lines=lines(tweet_file)

    htag=dict()

    for line in tweet_lines:
        data=json.loads(line)
        if "entities" in data.keys():
            if data["entities"] !=None:
                fn=data["entities"]
                if "hashtags" in fn.keys():
                    if fn["hashtags"] is not None:
                        if len(fn["hashtags"]) !=0:
                            for hashtag in fn["hashtags"]:
                                h_text= hashtag["text"].encode("UTF-8")
                                if h_text in htag.keys():
                                    htag[h_text]=htag[h_text]+1
                                else:
                                    htag[h_text]=1



    sorted_htag = sorted(htag.items(), key=operator.itemgetter(1))
    count=0
    for i in range (10):
        print str(sorted_htag[i][0])+" "+str(sorted_htag[i][1])


if __name__ == '__main__':
    main()



