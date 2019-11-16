import codecs
import re
import  numpy as np
from scipy import spatial
import os
from joblib import Parallel, delayed
import multiprocessing

from sklearn.metrics import r2_score

file_list = os.listdir('data/vec')
#embedding_path = "data/vec/ara_news_2008_1M-sentencesCleaned.txt.vec"

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

def create_gold_standard():
    gold_standard = []

    with open("data/STS.gs.track1.ar-ar.txt" , "r") as sts_results:
        for line in sts_results:
            line= line.strip()
            gold_standard.append(float(line))
    return np.array(gold_standard)


def calculate_correlation(result,output):
    gold_standard = create_gold_standard()
    index_missing_elements = np.argwhere(np.isnan(result))
    gold_standard = np.delete(gold_standard,index_missing_elements)
    result = np.delete(result, index_missing_elements)
    correlation = np.corrcoef(gold_standard, result)

    np.savetxt("eval/" + output + "Eval", correlation, fmt='%.18e', header="")

    return correlation

def semEval(embedding_path,output):

    ''':parameter embedding_path
    :return correlation, print results to a file

    '''

    embedding_dict = load_embedding(embedding_path)
    result = []

    with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8") as input: #load track test
        for index, line in enumerate(input):
            line = line.strip().split("\t") #split into two sentences
            sts_1 = line[0].split(" ") # create array with words from sentence one
            sts_2 = line[1].split(" ") # create array with words from sentence one
            print(index ,"\n",sts_1, "\n" ,sts_2)
            sum_embedding_1 = 0.0
            sum_embedding_2 = 0.0
            number_of_founded_words = 0




            for token in sts_1:
                token = clean_arabic_str(token).replace(" ", "_") #clean the token to match the training format
                token = token.replace(".", "")
                try:
                    embedding_dict[token]
                    word_embedding = np.array(embedding_dict[token])
                    sum_embedding_1 = np.add(sum_embedding_1,word_embedding) # add the word vector to the sentence vector
                    number_of_founded_words +=1
                except KeyError as e:
                    print("not found:" + token)
            if number_of_founded_words > 0:
                sentence_1_representation = np.divide(sum_embedding_1, number_of_founded_words)  # not needed anymore
            elif number_of_founded_words == 0:
                sentence_1_representation = np.divide(sum_embedding_1, 1)

            number_of_founded_words = 0

            for token in sts_2:
                token = clean_arabic_str(token).replace(" ", "_")  # clean the token to match the training format
                token = token.replace(".", "")
                try:
                    embedding_dict[token]
                    word_embedding = np.array(embedding_dict[token])

                    sum_embedding_2 = np.add(sum_embedding_2,word_embedding)
                    number_of_founded_words += 1
                except KeyError as e:
                    print("not found:" + token)
            if number_of_founded_words > 0:
                sentence_2_representation = np.divide(sum_embedding_2, number_of_founded_words)  # normalize
            elif number_of_founded_words == 0:
                sentence_2_representation = np.divide(sum_embedding_2, 1)

            result.append(float(1 - spatial.distance.cosine(sentence_1_representation, sentence_2_representation)))
    result = np.array(result)

    return calculate_correlation(result,output)

#result = semEval(embedding_path, embedding_path)

#correlation = calculate_correlation(result)

num_cores = multiprocessing.cpu_count()

Parallel(n_jobs=num_cores)(delayed(semEval)("data/vec/"+file_name,file_name) for file_name in file_list) #for the server
