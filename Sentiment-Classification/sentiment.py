from __future__ import print_function
from __future__ import division

import xlwt
import xlrd
import csv

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.classify import DecisionTreeClassifier
from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier
from nltk.classify import PositiveNaiveBayesClassifier
from nltk.classify import WekaClassifier
from nltk.classify import SklearnClassifier

import random
import re

from xlwt import Workbook
from xlrd import open_workbook
from random import shuffle



import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier

from sklearn.svm import SVC
#from sklearn.ensemble import VotingClassifier

class SentimentData:
	def __init__(self):
		self.data = []
		self.target = []

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

mystop_words=[
'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
'and',  'if', 'or', 'as', 'until', 'while', 'of', 'at', 'by', 'for',   'between', 'into',
'through', 'during', 'to', 'from', 'in', 'out', 'on', 'off', 'then', 'once', 'here',
 'there',  'all', 'any', 'both', 'each', 'few', 'more',
 'other', 'some', 'such',  'than', 'too', 'very', 's', 't', 'can', 'will',  'don', 'should', 'now'
]

emodict={

"%-("	:  "NegativeSentiment",
"%-)"	:  "PositiveSentiment",
"(-:"	:  "PositiveSentiment",
"(:"	:  "PositiveSentiment",
"(^ ^)"	:  "PositiveSentiment",
"(^-^)"	:  "PositiveSentiment",
"(^.^)"	:  "PositiveSentiment",
"(^_^)"	:  "PositiveSentiment",
"(o:"	:  "PositiveSentiment",
"(o;"	:  "NeutralSentiment",
")-:"	:  "NegativeSentiment",
"):"	:  "NegativeSentiment",
")o:"	:  "NegativeSentiment",
"*)"	:  "NeutralSentiment",
"*\o/*"	:  "PositiveSentiment",
"--^--@":  "PositiveSentiment",
"0:)"	:  "PositiveSentiment",
"38*"	:  "NegativeSentiment",
"8)"	:  "PositiveSentiment",
"8-)"	:  "NeutralSentiment",
"8-0"	:  "NegativeSentiment",
"8/"	:  "NegativeSentiment",
#"8\"	:  "NegativeSentiment",
"8c"	:  "NegativeSentiment",
":#"	:  "NegativeSentiment",
":'("	:  "NegativeSentiment",
":'-("	:  "NegativeSentiment",
":("	:  "NegativeSentiment",
":)"	:  "PositiveSentiment",
":*("	:  "NegativeSentiment",
":,("	:  "NegativeSentiment",
":-&"	:  "NegativeSentiment",
":-("	:  "NegativeSentiment",
":-(o)"	:  "NegativeSentiment",
":-)"	:  "PositiveSentiment",
":-*"	:  "PositiveSentiment",
":-*"	:  "PositiveSentiment",
":-/"	:  "NegativeSentiment",
":-/"	:  "NeutralSentiment",
":-D"	:  "PositiveSentiment",
":-O"	:  "NeutralSentiment",
":-P"	:  "PositiveSentiment",
":-S"	:  "NegativeSentiment",
#":-\"	:  "NegativeSentiment",
#":-\"	:  "NeutralSentiment",
":-|"	:  "NegativeSentiment",
":-}"	:  "PositiveSentiment",
":/"	:  "NegativeSentiment",
":0->-<|:"	:  "NeutralSentiment",
":3"	:  "PositiveSentiment",
":9"	:  "PositiveSentiment",
":D"	:  "PositiveSentiment",
":E"	:  "NegativeSentiment",
":F"	:  "NegativeSentiment",
":O"	:  "NegativeSentiment",
":P"	:  "PositiveSentiment",
":P"	:  "PositiveSentiment",
":S"	:  "NegativeSentiment",
":X"	:  "PositiveSentiment",
":["	:  "NegativeSentiment",
":["	:  "NegativeSentiment",
#":\"	:  "NegativeSentiment",
":]"	:  "PositiveSentiment",
":_("	:  "NegativeSentiment",
":b)"	:  "PositiveSentiment",
":l"	:  "NeutralSentiment",
":o("	:  "NegativeSentiment",
":o)"	:  "PositiveSentiment",
":p"	:  "PositiveSentiment",
":s"	:  "NegativeSentiment",
"0:|"	:  "NegativeSentiment",
":|"	:  "NeutralSentiment",
":p"	:  "PositiveSentiment",
":("	:  "NegativeSentiment",
";)"	:  "NeutralSentiment",
";^)"	:  "PositiveSentiment",
";o)"	:  "NeutralSentiment",
"</3-1"	:  "NegativeSentiment",
"<3"	:  "PositiveSentiment",
"<:}"	:  "NeutralSentiment",
"<o<"	:  "NegativeSentiment",
">/"	:  "NegativeSentiment",
">:("	:  "NegativeSentiment",
">:)"	:  "PositiveSentiment",
">:D"	:  "PositiveSentiment",
">:L"	:  "NegativeSentiment",
">:O"	:  "NegativeSentiment",
">=D"	:  "PositiveSentiment",
">["	:  "NegativeSentiment",
#">\"	:  "NegativeSentiment",
">o>"	:  "NegativeSentiment",
"@}->--":  "PositiveSentiment",
"B("	:  "NegativeSentiment",
"Bc"	:  "NegativeSentiment",
"D:"	:  "NegativeSentiment",
"X("	:  "NegativeSentiment",
"X("	:  "NegativeSentiment",
"X-("	:  "NegativeSentiment",
"XD"	:  "PositiveSentiment",
"XD"	:  "PositiveSentiment",
"XO"	:  "NegativeSentiment",
"XP"	:  "NegativeSentiment",
"XP"	:  "PositiveSentiment",
"^_^"	:  "PositiveSentiment",
"^o)"	:  "NegativeSentiment",
"x3?"	:  "PositiveSentiment",
"xD"	:  "PositiveSentiment",
"xP"	:  "NegativeSentiment",
"|8C"	:  "NegativeSentiment",
"|8c"	:  "NegativeSentiment",
"|D"	:  "PositiveSentiment",
"}:)"	:  "PositiveSentiment"
}

contractions_dict = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she has",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}


contractions_regex = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

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
    for word in tokens:
        current_word = get_stem(word)
        if current_word in senti_word_dict:
            score += int(senti_word_dict.get(current_word))
    return score

wb = open_workbook("sentiment-oracle.xlsx")
s = wb.sheet_by_index(0)

data_train=SentimentData()
data_test=SentimentData()


data_train.target=[i for i in range(750)]
data_train.data=[i for i in range(750)]

data_test.target=[i for i in range(75)]
data_test.data=[i for i in range(75)]

all_comments=[]
all_ratings=[]
senti_word_dict=[]

# Read in the words with sentiment from the dictionary
with open("EmotionDictionary.txt", "r") as sentidict, open("Sentiment-comments.csv", "r") as codedvals:
    dict_reader = csv.reader(sentidict, delimiter='\t')
    coded_reader = csv.reader(codedvals, delimiter=',')

    #Hash words from dictionary with their values
    senti_word_dict = {rows[0].strip('*'):rows[1] for rows in dict_reader}
    coded_sentiment_vals = list(zip(*coded_reader))[2]

    sentidict.close()
    codedvals.close()


for cell_num in range(1,2001):
	comments=expand_contractions(s.cell(cell_num,9).value)
        comments=replace_all(comments,emodict)
	all_comments.append(comments)
	all_ratings.append(s.cell(cell_num,14).value)
        com = tokenize(comments)

count = 0

for sentival, com in zip(coded_sentiment_vals, all_comments):
    score_got = get_comment_sentiment(com)
    if int(sentival) == score_got:
        count += 1
res = count/len(all_comments) * 100

print("Accuracy: "+str(res)+"%")

