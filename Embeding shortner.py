import  os
import codecs
with codecs.open("data/Aravec_cbow_300_twitter(short).txt", "w", "utf8") as f:
    with codecs.open("data/Aravec_cbow_300_twitter.txt", "r", "utf8") as file:
        for i, k in enumerate(file):
            f.writelines(k)
            if i == 1000000:
                break