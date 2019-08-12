import  os
import codecs
with codecs.open("C:/Users/D071082/Corpus/MSA/playground/WikipediaW2Vec.model(shortened).txt", "w", "utf8") as f:
    with codecs.open("C:/Users/D071082/Corpus/MSA/playground/WikipediaW2Vec.model.txt", "r", "utf8") as file:
        for i, k in enumerate(file):
            f.writelines(k)
            if i == 2000000:
                print('done')
                break

