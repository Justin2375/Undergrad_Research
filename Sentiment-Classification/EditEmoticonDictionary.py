
import xlwt
import xlrd
import csv

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

all_comments=[]
all_ratings=[]
senti_word_dict=[]
contractions_dict=[]
emoticon_dict=[]

# Read in the words with sentiment from the dictionary
with open("EmotionDictionary.txt", "r") as sentidict:
    dict_reader = csv.reader(sentidict, delimiter='\t')

    #Hash words from dictionary with their values
    senti_word_dict = {rows[0].strip('*'):rows[1] for rows in dict_reader}

    sentidict.close()

# Get the stem word from the NLTK
def get_stem(word):
    st = SnowballStemmer("english")
    stemmed_word = st.stem(word)
    return '' if stemmed_word is None else stemmed_word

file = open('EmotionDictionaryLemma.csv', 'w')
wordnet_lemmatizer = WordNetLemmatizer()


for word,value in senti_word_dict.iteritems():
    #word_stem=get_stem(word)
    word_lemma=wordnet_lemmatizer.lemmatize(word,pos="v")
    file.write(word_lemma+","+value+"\n")

file.close()

