import codecs
import re
import  numpy as np
from scipy import spatial
import os
from joblib import Parallel, delayed
import multiprocessing

from sklearn.metrics import r2_score

file_list = os.listdir('data/vec')
embedding_path = "data/vec/ara_news_2008_1M-sentencesCleaned.txt.vec"

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

def semEval(embedding_path,output):

    ''':parameter embedding_path
    :return correlation, print results to a file

    '''


    embedding_dict = load_embedding(embedding_path)
    result = []
    gold_standard = []

    with open("data/STS.gs.track1.ar-ar.txt" , "r") as sts_results:
        for line in sts_results:
            line= line.strip()
            gold_standard.append(float(line))

    with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8") as input: #load track test
        for index, line in enumerate(input):
            line = line.strip().split("\t") #split into two sentences
            #sts_1 = line[0].replace(".","").split(" ")
            #sts_2 = line[1].replace(".", "").split(" ")
            sts_1 = line[0].split(" ") # create array with words from sentence one
            sts_2 = line[1].split(" ") # create array with words from sentence one
            print(index ,"\n",sts_1, "\n" ,sts_2)
            sum_embedding_1 = 0.0
            sum_embedding_2 = 0.0
            sts_1_score = 0.0
            sts_2_score = 0.0



            for token in sts_1:
                token = clean_arabic_str(token).replace(" ", "_") #clean the token to match the training format
                token = token.replace(".", "")
                try:
                    embedding_dict[token]
                    word_embedding = np.array(embedding_dict[token])
                    word_embedding = np.divide(word_embedding, len(sts_1)) #normalizing the word embedding by the length of the sentence
                    sum_embedding_1 = np.add(sum_embedding_1,word_embedding) # add the word vector to the sentence vector
                except KeyError as e:
                    print("not found:" + token)
                    #sts_1_score = np.divide(sum_embedding_2, len(sts_2))  # not needed anymore
            for token in sts_2:
                token = clean_arabic_str(token).replace(" ", "_")
                token = token.replace(".", "")
                try:
                    embedding_dict[token]
                    word_embedding = np.array(embedding_dict[token])
                    word_embedding = np.divide(word_embedding,len(sts_2))
                    sum_embedding_2 = np.add(sum_embedding_2, word_embedding)  # same as above
                except KeyError as e:
                    print("not found:" + token)
                    #sts_2_score = np.divide(sum_embedding_2, len(sts_2)) #not needed anymore
            result.append(float(1 - spatial.distance.cosine(sum_embedding_1, sum_embedding_2)))
            #result = [result.append(float(i)) for i in result]
        index_missing_elements = np.argwhere(np.isnan(result))
        for a in index_missing_elements:
            print(int(a))
            del result[int(a)]  # there is a sentance causing nan value, so i deleted it
            del gold_standard[int(a)]  #delete the missing from the gold standard

    # print(gold_standard)
    # print(result)
    # print(len(result))
    # print(len(gold_standard))
    result = np.array(result)
    gold_standard = np.array(gold_standard)
    print(np.argwhere(np.isnan(result)))

    #print(r2_score(gold_standard, result))
    correlation = np.corrcoef(gold_standard, result)  #
    #print(correlation)

    #np.savetxt("eval/"+embedding_path+"Eval",correlation)
    np.savetxt("eval/"+output+"Eval",correlation,fmt='%.18e',header="")
    return correlation
#for file_name in file_list:
 #   semEval("data/vec/"+file_name,file_name)
num_cores = multiprocessing.cpu_count()

Parallel(n_jobs=num_cores)(delayed(semEval)("data/vec/"+file_name,file_name) for file_name in file_list) #for the server
