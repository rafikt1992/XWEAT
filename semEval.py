import codecs
import re
import  numpy as np
from scipy import spatial
from scipy.stats.stats import pearsonr

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
    return embbedding_dict
''
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

def semEval(embedding_path, output_path):
    pass

embedding_dict = load_embedding("C:/Users/D071082/PycharmProjects/XWEAT/data/vec/ara_news_2008_1M-sentencesCleaned.txt.vec")
result = []
gold_standard = []

with open ("data/STS.gs.track1.ar-ar.txt" , "r") as sts_results:
    for line in sts_results:
        result.append(line)

with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8") as input:
    for line in input:
        line = line.strip().split("\t")
        sts_1 = line[0].replace(".","").split(" ")
        sts_2 = line[1].replace(".", "").split(" ")
        print(sts_1, "\n" ,sts_2)
        sum_embedding_1 = 0.0
        sum_embedding_2 = 0.0
        sts_1_score = 0.0
        sts_2_score = 0.0

        for token in sts_1:
            token = clean_arabic_str(token).replace(" ", "_")
            try:
                embedding_dict[token]
                word_embedding = np.array(embedding_dict[token])
                sum_embedding_1 = np.add(sum_embedding_1,word_embedding)
            except KeyError as e:
                print("not found:" + token)
        sts_1_score = np.divide(sum_embedding_1,len(sts_1))
        for token in sts_2:
            token = clean_arabic_str(token).replace(" ", "_")
            try:
                embedding_dict[token]
                word_embedding = np.array(embedding_dict[token])
                sum_embedding_2 = np.add(sum_embedding_2, word_embedding)
            except KeyError as e:
                print("not found:" + token)
        sts_2_score = np.divide(sum_embedding_2, len(sts_2))
        result.append(1 - spatial.distance.cosine(sts_1_score,sts_2_score))


print(result)
print(len(result))
print(pearsonr(gold_standard,result))


