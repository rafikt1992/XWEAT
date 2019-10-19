import codecs
import re
import  numpy as np

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


embedding_dict = load_embedding("C:/Users/D071082/PycharmProjects/XWEAT/data/vec/ara_news_2008_1M-sentencesCleaned.txt.vec")
sum_embedding = 0.0
sts_1_score = 0.0
sts_2_score = 0.0
with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8") as input:
    for line in input:
        line = line.strip().split("\t")
        sts_1 = line[0].replace(".","").split(" ")
        sts_2 = line[1].replace(".", "").split(" ")
        print(sts_1, "\n" ,sts_2)

        for token in sts_1:
            token = clean_arabic_str(token).replace(" ", "_")
            try:
                word_embedding = np.array(embedding_dict[token])
                sum_embedding = np.add(sum_embedding,word_embedding)
                sts_1_score = sum_embedding / len(sts_1)
            except Exception as e:
                print("not found:" + token)
        sum_embedding = 0.0
        for token in sts_2:
            token = clean_arabic_str(token).replace(" ", "_")
            try:
                word_embedding = np.array(embedding_dict[token])
                sum_embedding = np.add(sum_embedding, word_embedding)
                sts_2_score = sum_embedding / len(sts_2)
            except Exception as m:
                print("not found:" + token)

        break

print(sum_embedding)
print(sts_1_score)


