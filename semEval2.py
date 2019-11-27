import codecs
import re
import  numpy as np
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity

import os
#from joblib import Parallel, delayed
#import multiprocessing

from sklearn.metrics import r2_score


def load_embedding(path):
    embbedding_dict = {}
    with codecs.open(path, "rb", "utf8", "ignore") as infile:
        for line in infile:
            try:
                parts = line.split()
                word = parts[0]
                nums = [float(p) for p in parts[1:]]
                embbedding_dict[word] = nums
            except Exception as e:
                print(line)
                continue
    return embbedding_dict #

def clean_arabic_str(text):
    '''
    this method clean strings of arabic, remove tashkeel, and replace double letters and unify ta2 marbuta and ha2
    :param text: text: an arabic word
    :type text str
    :return:text
    '''
    search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
              '&quot;', '?', '؟', '!']
    replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',
               ' ! ']

    # remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)

    # remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # trim
    text = text.strip()

    return text

def refactor():
    ''':returns  sts_1 list of sentences 1
        :return sts_2 list of senteces 2
        :return list of gold standard

    '''
    gold_standard = []
    sts_1 = []
    sts_2 = []

    with open("data/STS.gs.track1.ar-ar.txt" , "r") as sts_results:
        for line in sts_results:
            line= line.strip()
            gold_standard.append(float(line))
    with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8-sig", ) as input:
        for line in input:
            line = line.strip().split("\t")
            sts_1.append(line[0].split(" "))
            sts_2.append(line[1].split(" "))


        for i,  sentence in enumerate(sts_1):
            for k, word in enumerate(sentence):
                word = clean_arabic_str(word).replace(" ", "_")  # clean the token to match the training format
                word = word.replace(".", "")
                sts_1[i][k] = word.strip()
        for i, sentence in enumerate(sts_2):
            for k, word in enumerate(sentence):
                word = clean_arabic_str(word).replace(" ", "_")  # clean the token to match the training format
                word = word.replace(".", "")
                sts_2[i][k] = word.strip()

    return  sts_1,sts_2,gold_standard

def build_mattrix(sts_1, sts_2, embedding_dict): #:todo: figure out how to delete empty lists

    ''' :input: sts_1 sts_2 are two list of sentences from the similarity evaluation task1
                embedding_dic: a dictionary of word vector representation (loaded)

        :output sts_1_embedding, sts_2_embedding: lists contains converted sentences to embeddings where every element
                        is a list of founded word embeddings.
                        sentence 66 was deleted as there is no representation of it

    '''
    sts_1_embeddings = []
    sts_2_embeddings = []
    sentence_embedding_1 = []
    sentence_embedding_2 = []

    for i, sentence in enumerate(sts_1):
        for k, word in enumerate(sentence):
            try:
                sentence_embedding_1.append(list(embedding_dict[word]))
            except KeyError:
                print("not found:" + word)
        sts_1_embeddings.append(sentence_embedding_1)
        sentence_embedding_1 = []

    for i, sentence in enumerate(sts_2):
        for k, word in enumerate(sentence):
            try:
                sentence_embedding_2.append(list(embedding_dict[word]))
            except KeyError:
                print("not found:" + word)

        sts_2_embeddings.append(sentence_embedding_2)
        sentence_embedding_2 = []

    sts_1_embeddings = np.array(sts_1_embeddings)
    sts_1_embeddings = np.delete(sts_1_embeddings,66)
    sts_2_embeddings = np.array(sts_2_embeddings)
    sts_2_embeddings = np.delete(sts_2_embeddings,66)


    return averaged_sentence_representaion (sts_1_embeddings, sts_2_embeddings)



def averaged_sentence_representaion(sts_1_embeddings, sts_2_embeddings):

    '''
    creates one embedding per sentence
    :returns sts_1_embeddings list of embeddings representation of all the sentences 1 normalized by the average
                                    length of the founded words
                sts_2_embeddings: same as above except for the second part of the sentence
    '''
    sentence_1_rep = []
    sentence_2_rep = []
    sum = 0.0
    for sentencelist in sts_1_embeddings:  #get the sentence
        for word_embd in sentencelist:  #get the word embedding of every word in the senentece
            word_embd = np.array(word_embd)
            word_embd = np.divide(word_embd, len(sentencelist))  #normalize by the length of the sentece (founded words)
            sum = np.add(sum,word_embd)  #aggrigate with the previouse
        sentence_1_rep.append(sum)       #append a representation of the sentence
    sum = 0.0
    for sentencelist in sts_2_embeddings:
        for word_embd in sentencelist:
            word_embd = np.array(word_embd)
            word_embd = np.divide(word_embd, len(sentencelist))
            sum = np.add(sum,word_embd)
        sentence_2_rep.append(sum)

    sentence_1_rep = np.array(sentence_1_rep)
    sentence_2_rep = np.array(sentence_2_rep)

    return ( sentence_1_rep,sentence_2_rep)

def compute_cosine(sentence_reprentation_1, sentence_representation_2):
    result =[]
    ''' :return result: list of cosine similarity between two sentence representaion'''

    for i in zip(sentence_reprentation_1, sentence_representation_2):
        result.append((1 - spatial.distance.cosine(i[0], i[1])))


    return result

def compute_correlation(result, gold_standard):
    gold_standard = np.delete(gold_standard, 66)
    correlation = np.corrcoef(gold_standard, result)  #
    #np.savetxt("eval/" + output + "Eval", correlation, fmt='%.18e', header="")
    return correlation






#
# def semEval(embedding_path,output):
#
#     ''':parameter embedding_path
#     :return correlation, print results to a file
#
#     '''
#
#
#
#     embedding_dict = load_embedding(embedding_path)
#     result = []
#     gold_standard = []
#
#     with open("data/STS.gs.track1.ar-ar.txt" , "r") as sts_results:
#         for line in sts_results:
#             line= line.strip()
#             gold_standard.append(float(line))
#
#     with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8-sig",) as input: #load track test
#         for index, line in enumerate(input):
#             line = line.strip().split("\t") #split into two sentences
#             #sts_1 = line[0].replace(".","").split(" ")
#             #sts_2 = line[1].replace(".", "").split(" ")
#             sts_1 = line[0].split(" ") # create array with words from sentence one
#             sts_2 = line[1].split(" ") # create array with words from sentence one
#             sum_embedding_1 = 0.0
#             sum_embedding_2 = 0.0
#             length_found = 0
#
#
#
#
#             for m, token in enumerate(sts_1):
#                 try:
#                     embedding_dict[token]
#                     word_embedding = np.array(embedding_dict[token])
#                     word_embedding = np.divide(word_embedding, length_found) #normalizing the word embedding by the length of the sentence
#                     sum_embedding_1 = np.add(sum_embedding_1,word_embedding) # add the word vector to the sentence vector
#                 except KeyError as e:
#                     print("not found:" + token)
#                     #sts_1_score = np.divide(sum_embedding_2, len(sts_2))  # not needed anymore
#             length_found = 0
#             for token in sts_2:
#                 if token in embedding_dict:
#                     length_found += 1
#             if length_found == 0:
#                 length_found = 1
#
#             for token in sts_2:
#                 try:
#                     embedding_dict[token]
#                     word_embedding = np.array(embedding_dict[token])
#                     word_embedding = np.divide(word_embedding,length_found)
#                     sum_embedding_2 = np.add(sum_embedding_2, word_embedding)  # same as above
#                 except KeyError as e:
#                     print("not found:" + token)
#                     #sts_2_score = np.divide(sum_embedding_2, len(sts_2)) #not needed anymore
#             result.append(float(1 - spatial.distance.cosine(sum_embedding_1, sum_embedding_2)))
#             #result = [result.append(float(i)) for i in result]
#         index_missing_elements = np.argwhere(np.isnan(result))
#         print(index_missing_elements)
#         for a in index_missing_elements:
#             print(int(a))
#             del result[int(a)]  # there is a sentance causing nan value, so i deleted it
#             del gold_standard[int(a)]  #delete the missing from the gold standard
#
#     result = np.array(result)
#     print(result)
#     gold_standard = np.array(gold_standard)
#     print(np.argwhere(np.isnan(result)))
#
#     #print(r2_score(gold_standard, result))
#     correlation = np.corrcoef(gold_standard, result)
#     print(correlation)#
#
#     np.savetxt("eval/"+output+"Eval",correlation,fmt='%.18e',header="")
#     return correlation
#

#semEval("data/vec/"+"ara_news_2010_300K-sentencesCleaned.txt.vec","55ara_news_2008_1M-sentencesCleaned.txt.vec")
#num_cores = multiprocessing.cpu_count()

#Parallel(n_jobs=num_cores)(delayed(semEval)("data/vec/"+file_name,file_name) for file_name in file_list) #for the server

# file_list = os.listdir('data/vec')

def run(embedding_path):
    path_prefix = "data/vec/"
    embedding_dict = load_embedding()
    pass


#listofembedidngs = ["ara_news_2008_1M-sentencesCleaned.txt.vec"]
embedding_path = "data/vec/years_concatinated.vec"
embedding_dict = load_embedding(embedding_path)


sts_1, sts_2, gold_standard = refactor()

sts_1_embeddings, sts_2_embeddings = build_mattrix(sts_1, sts_2, embedding_dict)

result = compute_cosine( sts_1_embeddings, sts_2_embeddings)

result = compute_correlation(result, gold_standard)






