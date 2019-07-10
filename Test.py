import weat
import argparse
import codecs
import logging
import pickle
import regex as re
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

a= "reafik "

logging.warning("not in vocab %s", a)

print(logging.warning)

aaaaaa = XWEAT(obect)

file.writelines(["%s\n" % item  for item in list])

listofwarnings

#with open('./data/embbedding_dict.p', 'rb') as handle:

elif embeddings_path.endswith("p"):
with open('./data/embbedding_dict.p', 'rb') as handle:
    embd_dict = pickle.load(handle)
    return embd_dict
    
'''
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
def load_vocab_goran(path):  #load pickle files
    return pickle.load(open(path, "rb"))
def translate(translation_dict, terms):
    translation = []
    for t in terms:
        if t in translation_dict or t.lower() in translation_dict:
            if t.lower() in translation_dict:
                male, female = translation_dict[t.lower()]
            elif t in translation_dict:
                male, female = translation_dict[t]
            if female is None or female is '':
                translation.append(male)
            else:
                translation.append(male)
                translation.append(female)
        else:
            translation.append(t)
    translation = list(set(translation))
    return translation
path = "./data/vocab_dict_en_ar.p"

targets_1 = ["bagpipe", "cello", "guitar", "lute", "trombone", "banjo", "clarinet", "harmonica", "mandolin",
                     "trumpet", "bassoon", "drum", "harp", "oboe", "tuba", "bell", "fiddle", "harpsichord", "piano",
                     "viola", "bongo",
                     "flute", "horn", "saxophone", "violin"]
targets_2 = ["arrow", "club", "gun", "missile", "spear", "axe", "dagger", "harpoon", "pistol", "sword", "blade",
             "dynamite", "hatchet", "rifle", "tank", "bomb", "firearm", "knife", "shotgun", "teargas", "cannon",
             "grenade",
             "mace", "slingshot", "whip"]
attributes_1 = ["caress", "freedom", "health", "love", "peace", "cheer", "friend", "heaven", "loyal",
                "pleasure",
                "diamond", "gentle", "honest", "lucky", "rainbow", "diploma", "gift", "honor", "miracle",
                "sunrise",
                "family", "happy", "laughter", "paradise", "vacation"]
attributes_2 = ["abuse", "crash", "filth", "murder", "sickness", "accident", "death", "grief", "poison",
                "stink",
                "assault", "disaster", "hatred", "pollute", "tragedy", "divorce", "jail", "poverty", "ugly",
                "cancer",
                        "kill", "rotten",
                        "vomit", "agony", "prison"]

translation_dict = load_vocab_goran(path)
targets_1 = translate(translation_dict, targets_1)
targets_2 = translate(translation_dict, targets_2)
attributes_1 = translate(translation_dict, attributes_1)
attributes_2 = translate(translation_dict, attributes_2)



for key, arabictuple in translation_dict.items():
    listofwords = list(arabictuple)
    print(listofwords)
    for i in range(0, len(listofwords)):
        if listofwords[i]== None:
            print(listofwords[i])
        else:
            print(listofwords[i])