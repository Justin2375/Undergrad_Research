from __future__ import print_function
from __future__ import division

import xlwt
import xlrd
import csv

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

import re

from xlwt import Workbook
from xlrd import open_workbook

#Configuration
DEBUG=True
FILE_NAME="test-dataset.xlsx"
COMMENT_COUNT=20

B_INCR = 0.293
B_DECR = -0.293

mystop_words=[
'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
'have', 'has', 'had', 'having',  'does', 'did', 'doing', 'a', 'an', 'the',
'and',   'or', 'as', 'until',  'of', 'at', 'by', 'for',   'between', 'into',
'through', 'during', 'to', 'from',  'on', 'off', 'then', 'once', 'here',
 'there',  'all', 'any', 'both',  'few', 'more',
 'other', 'some', 'such',   'too', 'very', 's', 't', 'can', 'will',  'don', 'should', 'now',
#keywords
'while','case','switch','if', 'do','while','each','than','catch', 'class', 'double','float','int',
'long','super','import','short','default','catch','try','new','final','extends','implements',
'public','protected','static','this','return','char','const','break','boolean','bool','package',
'byte','assert', 'raise','global','with','or','yield','in', 'out','except','and','enum','signed',
'void','virtual','union','goto','var','function','require','print','echo','foreach','elseif','namespace',
'delegate','event','override','struct','readonly','explicit','interface','get','set'
]

negation_words =['not', 'never', 'none', 'nobody', 'nowhere', 'neither', 'barely', 'hardly',
                     'nothing', 'rarely', 'seldom', 'despite' ]

# # Still needs to be populated with more terms
but_clause_words = ['but', 'except']

# Still needs to be populated with more terms
too_words = ['too']

sentiment_intensifiers = \
{"absolutely": B_INCR, "amazingly": B_INCR, "awfully": B_INCR, "completely": B_INCR, "considerably": B_INCR,
 "decidedly": B_INCR, "deeply": B_INCR, "effing": B_INCR, "enormously": B_INCR,
 "entirely": B_INCR, "especially": B_INCR, "exceptionally": B_INCR, "extremely": B_INCR,
 "fabulously": B_INCR, "flipping": B_INCR, "flippin": B_INCR,
 "fricking": B_INCR, "frickin": B_INCR, "frigging": B_INCR, "friggin": B_INCR, "fully": B_INCR, "fucking": B_INCR,
 "greatly": B_INCR, "hella": B_INCR, "highly": B_INCR, "hugely": B_INCR, "incredibly": B_INCR,
 "intensely": B_INCR, "majorly": B_INCR, "more": B_INCR, "most": B_INCR, "particularly": B_INCR,
 "purely": B_INCR, "quite": B_INCR, "really": B_INCR, "remarkably": B_INCR,
 "so": B_INCR, "substantially": B_INCR,
 "thoroughly": B_INCR, "totally": B_INCR, "tremendously": B_INCR,
 "uber": B_INCR, "unbelievably": B_INCR, "unusually": B_INCR, "utterly": B_INCR,
 "very": B_INCR,
 "almost": B_DECR, "barely": B_DECR, "hardly": B_DECR, "just enough": B_DECR,
 "kind of": B_DECR, "kinda": B_DECR, "kindof": B_DECR, "kind-of": B_DECR,
 "less": B_DECR, "little": B_DECR, "marginally": B_DECR, "occasionally": B_DECR, "partly": B_DECR,
 "scarcely": B_DECR, "slightly": B_DECR, "somewhat": B_DECR,
 "sort of": B_DECR, "sorta": B_DECR, "sortof": B_DECR, "sort-of": B_DECR}


senti_word_dict=[]
emoticon_dict=[]
wordnet_lemmatizer = WordNetLemmatizer()
contractions_dict=[]

# Read in the words with sentiment from the dictionary
with open("EmotionDictionaryLemma.csv", "r") as sentidict,\
     open("Contractions.txt","r") as contractions,\
     open("EmoticonLookupTable.txt","r") as emotable:
    dict_reader = csv.reader(sentidict, delimiter=',')
    contractions_reader=csv.reader(contractions, delimiter='\t')
    emoticon_reader=csv.reader(emotable,delimiter='\t')

    #Hash words from dictionary with their values
    senti_word_dict = {rows[0]:rows[1] for rows in dict_reader}
    contractions_dict = {rows[0]:rows[1] for rows in contractions_reader}
    emoticon_dict={rows[0]:rows[1] for rows in emoticon_reader}

    sentidict.close()
    contractions.close()
    emotable.close()

# Get the lemma word from the NLTK
def get_lemma(word):
    lemma_word = wordnet_lemmatizer.lemmatize(word, pos="v")
    return '' if lemma_word is None else lemma_word

contractions_regex = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

def expand_contractions(s, contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_regex.sub(replace, s.lower())


def replace_all(text, dic):
    #print(text)
    for i, j in dic.iteritems():
        text = text.replace(i,j)
    return text


# Text represents the entire text to scored. A Text is a collection of sentences
class SentiText(object):
    def __init__(self, text):
        if not isinstance(text, str):
            text = str(text.encode('utf-8'))
        text = replace_all(text, emoticon_dict)
        self.text = expand_contractions(text)
        self.sentences = self._parse_sentences()
    def _parse_sentences(self):
        sententce_list=[]
        sentences =nltk.sent_tokenize(self.text)

        for st in sentences:
            sententce_list.append(SentiSentence(st))
        return sententce_list

    def get_total_score(self):
        total_score=0.0
        for sentence in self.sentences:
            total_score +=sentence.get_sentence_score()
        return total_score

# Sentence represents individual sentences. A sentence is a collection of words
class SentiSentence(object):
    def __init__(self, sentence):
        self.sentence=sentence
        self.words = self._parse_words()
        self.word_scores=self._compute_sentiscores()

    def _parse_words(self):
        allwords = dict()
        allwords = nltk.word_tokenize(self.sentence)
        allwords = [word for word in allwords if len(word) > 1]
        allwords = [get_lemma(word) for word in allwords]
        print(allwords)
        return allwords

    def _compute_sentiscores(self):
        scores = []
        #Tag the different parts of speech for classification
        part_of_speech = nltk.tag.pos_tag(self.words, tagset='universal')
        for word in self.words:
            word_score = 0
            if but_word(word):
                scores.append(int(senti_word_dict.get('but')))
                for clause_word in self.words[self.words.index(word)+1:len(self.words)]:
                    if clause_word in senti_word_dict:
                        word_score = int(senti_word_dict.get(clause_word))
                        if word_score > 0:
                            word_score = -1
                        else:
                            if word_score < 0:
                                word_score = 1 
                            else: 
                                word_score = 0
                    else:
                        word_score = 0
                    scores.append(word_score)
                    if DEBUG:
                        print(clause_word)
                        print("BUT: [ " + str(word_score) + " ]")
                return scores
            
            if negated(word):
                scores.append(int(senti_word_dict.get(word)))
                for clause_word in self.words[self.words.index(word)+1:len(self.words)]:
                    if clause_word in senti_word_dict:
                        word_score = int(senti_word_dict.get(clause_word))
                        if word_score > 0:
                            word_score = -1
                        else:  
                            if word_score < 0:
                                word_score = 1
                            else:
                                word_score = 0
                    else:
                        word_score = 0
                    scores.append(word_score)
                    if DEBUG:
                        print(clause_word)
                        print("NOT: [ " + str(word_score) + " ]")
                return scores

            if word in senti_word_dict:
                word_score = int(senti_word_dict.get(word))
                if word_score > 0:
                    word_score = 1
                else:
                    if word_score < 0:
                        word_score = -1
                    else:
                        word_score = 0
            else:
                word_score = 0

            if DEBUG:
                print(word)
                # print(part_of_speech)
            if word in senti_word_dict:
                word_score = int(senti_word_dict.get(word))
                if DEBUG:
                    print("[ " + str(word_score) + " ]")
                scores.append(word_score)
        return scores

    def get_sentence_score(self):
        sentence_score=0
        for score in self.word_scores:
            sentence_score += score
        return sentence_score

def but_word(input_words):
    """
    Determine if the sentence contains any but words
    """
    but_words = []
    but_words.extend(but_clause_words)
    for word in but_clause_words:
        if word in input_words:
            return True
    return False
    

# Check to see if the sentence cotains any negation words 
def negated(input_words):
    """
    Determine if input contains negation words
    """
    neg_words = []
    neg_words.extend(negation_words)
    for word in neg_words:
        if word in input_words:
            return True
    if "least" in input_words:
        i = input_words.index("least")
        if i > 0 and input_words[i-1] != "at":
            return True
    return False

all_comments=[]
all_ratings=[]

def get_sentiment_class(score):
    if score > 0:
            return 1
    elif score < 0:
            return -1
    else:
            return 0


def write_most_frequent_words(comment_list,file_name):
    allWords = nltk.word_tokenize(', '.join(str(x) for x in comment_list))

    allWords = [word for word in allWords if len(word) > 1]

    # Remove numbers
    allWords = [word for word in allWords if not word.isdigit()]

    allWords = [word for word in allWords if word.isalpha()]

    # Lowercase all words (default_stopwords are lowercase too)
    allWords = [word.lower() for word in allWords]

   # Remove stopwords
    allWords = [word for word in allWords if word not in mystop_words]

    # Lowercase all words (default_stopwords are lowercase too)
    allWords = [get_lemma(word) for word in allWords]

    allWordDist = nltk.FreqDist(w.lower() for w in allWords)

    file = open(file_name, 'w')
    file.write("Word,Frequency\n")

    for word, frequency in allWordDist.most_common(200):
        file.write(word + "," + str(frequency) + "\n")

    file.close()


#Open oracle
wb = open_workbook(FILE_NAME)
s = wb.sheet_by_index(0)

for cell_num in range(1,COMMENT_COUNT+1):

    comments=s.cell(cell_num, 9).value
    all_comments.append(comments.encode('ascii','ignore'))
    all_ratings.append(s.cell(cell_num,14).value)

#print(allWordDist)

num_cor = 0

num_total = 0
num_rated = 0

targ_rating = -1
num_fn=0
num_fp=0
num_tp =0
num_tn =0

false_positives= []
false_nagatives=[]
true_positives=[]
true_negatives=[]

for sentival, com in zip(all_ratings, all_comments):
    if DEBUG:
            print("----------------------")
            print(com)
            print("Actual:"+str(sentival))
    sentitext =SentiText(com)
    score_computed = sentitext.get_total_score()

    score_got=get_sentiment_class(int(score_computed))
    
    if DEBUG:
            print("Got:"+ str(score_got))
            print("----------------------\n\n")

    if int(sentival) == targ_rating:
        num_total += 1
        if score_got != int(sentival):
            num_fn +=1
            false_nagatives.append(com)


    if score_got == targ_rating:
        num_rated += 1
        if int(sentival) == score_got:
            num_tp += 1
            true_positives.append(com)
        else:
            false_positives.append(com)
            num_fp +=1

    if int(sentival) == score_got:
        num_cor += 1

res = num_cor/len(all_comments) * 100
prec = num_tp / num_rated
rec = num_tp / num_total

print("Target Rating: "+str(targ_rating))
print("Total Comments: "+str(len(all_comments))+" Got Accurate: "+str(num_cor))
print("Accuracy: "+str(res)+"%")
print("Rated: " + str(num_rated))
print("Correct: "+str(num_tp))
print("Total: " + str(num_total))
print("Precision: "+str(prec))
print("Recall: "+str(rec))

print("Writing frequent false positives...")
write_most_frequent_words(false_positives,"frequent_fp.csv")
print("Writing frequent false negatives...")
write_most_frequent_words(false_nagatives,"frequent_fn.csv")



