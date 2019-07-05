import weat
import argparse
import codecs
import logging
'''
ap = argparse.ArgumentParser(description='Convert Hex Files')
ap.add_argument("--name", help="name of the user", type=str, required=True)
ap.add_argument("--second", type=str, required= True)

#args =  vars(ap.parse_args())
args = ap.parse_args()
print(args.name)

print(f"bla bla {args.name} second {args.second}")
'''
'''
loglist= []

listofwords= ["word1","word2","word3","word4","word5", ]

for i in listofwords:

    loglist.append(i)

with codecs.open("temp delet me", "w") as f:
    f.write("\n".join(loglist))
'''
a= "reafik "

logging.warning("not in vocab %s", a)

print(logging.warning)

aaaaaa = XWEAT(obect)

file.writelines(["%s\n" % item  for item in list])

listofwarnings

#with open('./data/embbedding_dict.p', 'rb') as handle:

elif embeddings_path.endswith("p"):  # todo: add load from pickle file
with open('./data/embbedding_dict.p', 'rb') as handle:
    embd_dict = pickle.load(handle)
    return embd_dict