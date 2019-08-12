import  os
import gensim
import codecs
import pickle

with codecs.open("C:/Users/D071082/Corpus/MSA/playground/WikipediaW2Vec.model(shortened).txt", "w", "utf8") as f:
    with codecs.open("C:/Users/D071082/Corpus/MSA/playground/WikipediaW2Vec.model.txt", "r", "utf8") as file:
        for i, k in enumerate(file):
            f.writelines(k)
            if i == 1000000:
                print('done')
                break

# returns a dictionary of embeddings
def load_embeddings(path, word2vec=False, rdf2vec=False):
    embbedding_dict = {}
    if word2vec == False and rdf2vec == False:
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
    elif word2vec == True:
        #Load Google's pre-trained Word2Vec model.
        if os.name != 'nt':
            model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        else:
            model = gensim.models.Word2Vec.load_word2vec_format(path, binary=True)
        return model
    elif rdf2vec == True:
        #Load Petars model.
        model = gensim.models.Word2Vec.load(path)
        return model


embeding_dict = load_embeddings("C:/Users/D071082/Corpus/MSA/playground/WikipediaW2Vec.model(shortened).txt",word2vec=False, rdf2vec=False) #change the path here
with open('WikipediaW2Vec.model(shortened).p', 'wb') as handle:
    pickle.dump(embeding_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('WikipediaW2Vec.model(shortened).p', 'rb') as handle:
    b = pickle.load(handle)

print(embeding_dict == b)
