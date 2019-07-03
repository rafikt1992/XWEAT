import  os
import codecs
with codecs.open("data/crawl-300d-2M.-smallvec", "w", "utf8") as f:
    with codecs.open("data/crawl-300d-2M.vec", "r", "utf8") as file:
        for i, k in enumerate(file):
            f.writelines(k)
            if i == 600000:
                break