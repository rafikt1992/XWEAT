import codecs
import os
import pickle
import  re
import json

'''
THIS SCRIPT CREATE ARABIC VOCAB FROM CSV TO PICKLE WITH TEST CLEANING TO FIT THE ARAVEC MODEL
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

is_russian = False
with codecs.open('data/vocab_en_ar.csv', "r", "utf8") as f:
  translation_dict = {}
  for line in f.readlines():
    parts = line.split(",")
    en = parts[0]
    if en == "" or en[0].isupper():
      continue
    else:
      if is_russian and parts[3] != "\n" and parts[3] != "\r\n" and parts[3] != "\r":
          other_m = parts[2]
          other_m = clean_arabic_str(other_m).replace(" ", "_")
          other_f = parts[3].strip()
          other_f = clean_arabic_str(other_f).replace(" ", "_") # clean text
          translation_dict[en] = (other_m, other_f)
      else:
        other_m = parts[1].strip()
        other_m = clean_arabic_str(other_m).replace(" ", "_")
        other_f = None
        if len(parts) > 2 and parts[2] != "\n" and parts[2] != "\r\n" and parts[2] != "\r" and parts[2] != '':
            other_f = parts[2].strip()
            other_f = clean_arabic_str(other_f).replace(" ", "_")
        translation_dict[en] = (other_m, other_f)
  pickle.dump(translation_dict, open("data/vocab_dict_en_ar.p", "wb"))
