import time
import re
import argparse
import sys
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.corpora.dictionary import Dictionary # process the input of LDA model
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
 
def timer(global_time,local_time):
    gtime=round(time.time() - global_time, 2)
    ltime=round(time.time() - local_time, 2)     
    print("--- "+str(ltime)+" / "+str(gtime)+" sec ---\n")
    return 
    
################################################################################################################
# get the input from the command line - both are required (simplify: file_name=sys.argv[0])
################################################################################################################
global_time = time.time()
root = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("--f", type=str, required=True, help="input csv file")
parser.add_argument('--rf', type=str) # Using default can lose efficacy of "if args.rf is None:"   
parser.add_argument('--delimeter', type=str, default=',',help="CSV delimeter character")
parser.add_argument('--clusterNum', type=int, default=55, help="Number of clusters (default: 3)")
parser.add_argument('--keywordNum', type=int, default=20, help="Number of keywords in each cluster (default: 5)")

args = parser.parse_args()


print('\n\n\n[LDA ANALYSIS]')
print(parser.parse_args())
print('')

file_csv=args.f # For Mac (Jeanine's PC)

if args.rf is None:
   file_results='LDA_'+args.f
else:
   file_results=args.rf+'.csv' # For Mac (Jeanine's PC)

delchar=args.delimeter   
cluster_num=args.clusterNum
keyword_num=args.keywordNum

################################################################################################################
# Read the data from the SEQ file
################################################################################################################
print('Loading data...')
local_time = time.time()
data = pd.read_csv(file_csv)
print('data:', data.shape)

local_time = time.time()
all_content_content_meta = []
print('Generating the all_content sequences (type: list of list words)...')
for tokens in data.values.tolist():
    one_content_content_meta = []
    if type(tokens[-1]) is float:
        content_content_meta = ['']
    else:
        content_content_meta = tokens[-1].strip().split(' ')
    for word_ccm in content_content_meta:
        one_content_content_meta.append(word_ccm)
    all_content_content_meta.append(one_content_content_meta)
lda_input = all_content_content_meta
timer(global_time,local_time)

################################################################################################################
# Data Processor
################################################################################################################
def removeNum(sentence):
    newSentence = ''
    for word in sentence.split():
        if word.isalpha() is True:
            newSentence += word
            newSentence += ' '
    return newSentence.strip()

def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(' ', sentence)

def keepEnglish(sentence):
    global Englist_words
    new_sentence = ' '.join(w for w in nltk.wordpunct_tokenize(sentence) if w.lower() in Englist_words or not w.isalpha())
    return new_sentence

def lemmatisation(sentence):
    lemmSentence = ''
    for word in sentence.split():
        lemm = method.lemmatize(word)
        lemmSentence += lemm
        lemmSentence += ' '
    return lemmSentence.strip()

def removeOneTwoChara(sentence):
    newSentence = ''
    global word_frequency_dict
    for word in sentence.split():
        if len(word) > 2:
            newSentence += word
            newSentence += ' '
    return newSentence.strip()

print('Removing stop words and noise ...')
local_time = time.time()
stop_words = set(stopwords.words('english'))
re_stop_words = re.compile(r'\b(' + '|'.join(stop_words) + ')\\W', re.I)
data['content_content_meta'] = data['content_content_meta'].apply(removeNum)
data['content_content_meta'] = data['content_content_meta'].apply(removeStopWords)
timer(global_time,local_time)

print('Removing one/two characters...')
local_time = time.time()
data['content_content_meta'] = data['content_content_meta'].apply(removeOneTwoChara)
timer(global_time,local_time)

print('Applying Lemmatisation...')
local_time = time.time()
Englist_words = set(nltk.corpus.words.words())
method = WordNetLemmatizer()
data['content_content_meta'] = data['content_content_meta'].apply(lemmatisation)
timer(global_time,local_time)

print('Removing all non-English words...')
local_time = time.time()
data['content_content_meta'] = data['content_content_meta'].apply(keepEnglish)
timer(global_time, local_time)

################################################################################################################
# Learn the LDA model 
################################################################################################################
print('Generating corpus...')
local_time = time.time()
word_dictionary = Dictionary(lda_input)
word_corpus = [word_dictionary.doc2bow(text) for text in lda_input]
word_frequency_map = {}
for sentence in lda_input:
    for word in sentence:
        if word in word_frequency_map.keys():
            word_frequency_map[word] += 1
        else:
            word_frequency_map[word] = 1
timer(global_time,local_time)

print('Training LDA Model...')
local_time = time.time()
lda = LdaModel(word_corpus, num_topics=cluster_num, id2word=word_dictionary, random_state=5, per_word_topics=True)
print('LDA Molde:', lda)
timer(global_time,local_time)

################################################################################################################
# Learn the Coherence Model
################################################################################################################
print('Topic coherence...')
local_time = time.time()
coherence = CoherenceModel(model=lda, corpus=word_corpus, texts=lda_input, dictionary=word_dictionary, coherence='c_v')
print('coherence:', coherence.get_coherence())
timer(global_time,local_time)

################################################################################################################
# Pick keywords in each clusters
################################################################################################################
print('Picking words in each topic...')
local_time = time.time()
keyword_vocab = []
topics_keywords_map = {}
# pick keywords using show_topics function in gensim
for topic in lda.show_topics(num_topics=cluster_num, num_words=1000, formatted=False):
    topic_id = topic[0]
    keywords = topic[1]
    keyword_weight_map = {}
    for keyword, weight in keywords:
        keyword_weight_map[keyword] = weight
        if keyword not in keyword_vocab:
            keyword_vocab.append(keyword)
    topics_keywords_map[topic_id]=keyword_weight_map
timer(global_time,local_time)

################################################################################################################
# Deal with the problem of word overlapping
################################################################################################################
print('Keeping distinct word in each topic ...')
local_time = time.time()
for keyword in keyword_vocab:
    temp_keyword = [None,None,0]
    for topic_id, _ in topics_keywords_map.items():
        if keyword in topics_keywords_map[topic_id].keys():
            weight = topics_keywords_map[topic_id][keyword]
            if weight > temp_keyword[2]:
                if temp_keyword[0] is not None:
                    del topics_keywords_map[temp_keyword[0]][temp_keyword[1]]
                temp_keyword[0] = topic_id
                temp_keyword[1] = keyword
                temp_keyword[2] = weight
            elif weight < temp_keyword[2] and (keyword==temp_keyword[1]):
                del topics_keywords_map[topic_id][keyword]
timer(global_time,local_time)

################################################################################################################
# Keep the number of keywords equal in every cluster
# Use topic score
################################################################################################################
print('Keeping the number of keywords equal in each topic...')
local_time = time.time()
topics_keywords_weight_map_equalnum = {}
for topic_id, keyword_weight_map in topics_keywords_map.items():
    temp_keyword_weight_map = {}
    for idx, (keyword, weight) in enumerate(keyword_weight_map.items()):
        if idx < keyword_num:
            temp_keyword_weight_map[keyword] = weight
    topics_keywords_weight_map_equalnum[topic_id] = temp_keyword_weight_map
topics_words = {}
for topic_id, topic_keywords in topics_keywords_weight_map_equalnum.items():
    topic_words = []
    for keyword, weight in topic_keywords.items():
        topic_words.append(keyword)
    topics_words[topic_id] = topic_words 
timer(global_time,local_time)

################################################################################################################
# Calculate the LDA topic scores
# Match each company to only one cluster using the highest topic score
################################################################################################################
print('Calculating LDA topic scores, and matching each company to one cluster using the highest topic score...')
local_time = time.time()
content_scores = lda.get_document_topics(word_corpus)
contentidx_topicidx_map = {}
contentidx_topicsocre_map = {}
for contentidx, scores in enumerate(content_scores):
    topicid_topicscore_dict = {}
    for topicid, topicscore in scores:
        topicid_topicscore_dict[topicid] = topicscore
    topicid_topicscore_dict_sorted = {k: v for k, v in sorted(topicid_topicscore_dict.items(), key=lambda item: item[1], reverse=True)}
    # print('topicid_topicscore_dict_sorted:', topicid_topicscore_dict_sorted, list(topicid_topicscore_dict_sorted.keys())[0], list(topicid_topicscore_dict_sorted.values())[0])
    contentidx_topicidx_map[contentidx] = list(topicid_topicscore_dict_sorted.keys())[0]
    score = list(topicid_topicscore_dict_sorted.values())[0]
    contentidx_topicsocre_map[contentidx] = score
timer(global_time,local_time)

################################################################################################################
# Store all the results of every corpus as 
# Cluster_ID, Locale, Year, Quarter, Cluster_Keywords, Cluster_Analysis_Result, Cluster_No_Companies, Weight_Cluster_No_Companies
# Save the final results into CSV file
################################################################################################################
print('Saving Results...')
local_time = time.time()
topic_id_list = list({k: v for k, v in sorted(topics_words.items(), key=lambda item: item[0])}.keys())
keywords_list = []
for topic_id, topic_words in topics_words.items():
    topics_words_str = ', '.join(str(word) for word in topic_words)
    keywords_list.append(topics_words_str)
keyword_weight_list = []
for topic_id, keyword_weight_map in topics_keywords_weight_map_equalnum.items():
    weight_keyword_list = []
    for _, original_weight in keyword_weight_map.items():
        # weight = format(original_weight, '.3f')
        weight = format(original_weight, '.6f')
        weight_keyword_str = str(weight)
        weight_keyword_list.append(weight_keyword_str)
        keyword_weight_str = ', '.join(str(i) for i in weight_keyword_list)
    keyword_weight_list.append(keyword_weight_str)

data = pd.read_csv(file_csv)
clusterid_rid_dict = {}
for row, contentidx_topicidx in zip(data.values.tolist(), contentidx_topicidx_map.items()):
    rid = row[1]
    locale = row[2]
    year = row[3]
    quarter = row[4]
    clusterid = contentidx_topicidx[1]
    if clusterid not in clusterid_rid_dict.keys():
        clusterid_rid_dict[clusterid] = [str(rid)]
    clusterid_rid_dict[clusterid].append(str(rid))
clusterid_rid_dict_sorted = {k: v for k, v in sorted(clusterid_rid_dict.items(), key=lambda item: item[0])}
for topic_id, keywords, keyword_weight, rids in zip(topic_id_list, keywords_list, keyword_weight_list, clusterid_rid_dict_sorted.values()):
    topic_id = str(topic_id)
    rids = list(set(rids))
    rids_str = ' '.join(rids)

rid_list = []
locale_list = []
year_list = []
quarter_list = []
clusterid_list = []
keywordslist_list = []
keyword_weightlist_list = []
ridscore_list = []
for row, contentidx_topicidx in zip(data.values.tolist(), contentidx_topicidx_map.items()):
    rid = row[1]
    locale = row[2]
    year = row[3]
    quarter = row[4]
    clusterid = contentidx_topicidx[1]
    contentidx = contentidx_topicidx[0]
    rid_list.append(rid)
    year_list.append(year)
    quarter_list.append(quarter)
    clusterid_list.append(clusterid)
    locale_list.append(locale)
    keywords = keywords_list[int(clusterid)]
    keywords_weight = keyword_weight_list[int(clusterid)]
    ridscore = contentidx_topicsocre_map[contentidx]
    keywordslist_list.append(keywords)
    keyword_weightlist_list.append(keywords_weight)
    ridscore_list.append(ridscore)
result_pd = pd.DataFrame()
result_pd['cluster_id'] = clusterid_list
result_pd['locale'] = locale_list
result_pd['rid'] = rid_list
result_pd['year'] = year_list
result_pd['quarter'] = quarter_list
result_pd['keyword'] = keywordslist_list
result_pd['keyword_weight'] = keyword_weightlist_list
result_pd['company_weight'] = ridscore_list
result_pd.to_csv(file_results, index=False, header=True)
timer(global_time,local_time)
print('EXIT')

