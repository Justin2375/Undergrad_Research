from __future__ import print_function
from __future__ import division

import xlwt
import xlrd
import csv

import nltk
from nltk.stem.snowball import SnowballStemmer

import re

from xlwt import Workbook
from xlrd import open_workbook

#Configuration
DEBUG=False
FILE_NAME="sentiment-oracle.xlsx"
COMMENT_COUNT=2000



all_comments=[]
all_ratings=[]
senti_word_dict=[]
contractions_dict=[]
emoticon_dict=[]

# Read in the words with sentiment from the dictionary
with open("EmotionDictionary.txt", "r") as sentidict,\
     open("Contractions.txt","r") as contractions,\
     open("EmoticonLookupTable.txt","r") as emotable:
    dict_reader = csv.reader(sentidict, delimiter='\t')
    contractions_reader=csv.reader(contractions, delimiter='\t')
    emoticon_reader=csv.reader(emotable,delimiter='\t')

    #Hash words from dictionary with their values
    senti_word_dict = {rows[0].strip('*'):rows[1] for rows in dict_reader}
    contractions_dict = {rows[0]:rows[1] for rows in contractions_reader}
    emoticon_dict={rows[0]:rows[1] for rows in emoticon_reader}

    sentidict.close()
    contractions.close()
    emotable.close()


contractions_regex = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

def get_sentiment_class(score):
    if score > 0:
            return 1
    elif score < 0:
            return -1
    else:
            return 0

def replace_all(text, dic):
    #print(text)
    for i, j in dic.iteritems():
        text = text.replace(i,j)
    return text


def expand_contractions(s, contractions_dict=contractions_dict):
     def replace(match):
         return contractions_dict[match.group(0)]
     return contractions_regex.sub(replace, s.lower())

# Tokenize each of the comments 
def tokenize(comment):
    tokens = nltk.word_tokenize(comment)
    return tokens

# Get the stem word from the NLTK
def get_stem(word):
    st = SnowballStemmer("english")
    stemmed_word = st.stem(word)
    return '' if stemmed_word is None else stemmed_word

# Get the overall sentiment score from the comment
def get_comment_sentiment(comment):
    score = 0
    tokens = tokenize(comment)
    #print(tokens)
    for word in tokens:
        current_word = get_stem(word)
        if DEBUG:
                print(current_word,)
        if current_word in senti_word_dict:
            word_score=  int(senti_word_dict.get(current_word))
            if DEBUG:
                    print("[ "+str(word_score)+" ]")
            score += word_score
    return score


#Open oracle
wb = open_workbook(FILE_NAME)
s = wb.sheet_by_index(0)


for cell_num in range(1,COMMENT_COUNT+1):
        comments=replace_all(s.cell(cell_num,9).value,emoticon_dict)
	comments=expand_contractions(comments)
	all_comments.append(comments)
	all_ratings.append(s.cell(cell_num,14).value)


num_cor = 0

neg_cor = 0
neg_inc = 0
neg_total = 0
neg_rated = 0

targ_rating = -1

for sentival, com in zip(all_ratings, all_comments):
    if DEBUG:
            print("----------------------")
            print(com)
            print("Actual:"+str(sentival))

    score_computed = get_comment_sentiment(com)

    score_got=get_sentiment_class(int(score_computed))
    
    if DEBUG:
            print("Got:"+ str(score_got))
            print("----------------------\n\n")

    if int(sentival) == targ_rating:
        neg_total += 1

    if score_got == targ_rating:
        neg_rated += 1
        if int(sentival) == targ_rating:
            neg_cor += 1
        else:
            neg_inc += 1

    if int(sentival) == score_got:
        num_cor += 1

res = num_cor/len(all_comments) * 100
prec = neg_cor/neg_rated
rec = neg_cor/neg_total

print("Target Rating: "+str(targ_rating))
print("Total Comments: "+str(len(all_comments))+" Got Accurate: "+str(num_cor))
print("Accuracy: "+str(res)+"%")
print("Rated: "+str(neg_rated))
print("Correct: "+str(neg_cor))
print("Total: "+str(neg_total))
print("Precision: "+str(prec))
print("Recall: "+str(rec))
