import argparse
import numpy as np
import os
import codecs
#import utils
def embedding_coherence_test(vecs, vocab, target_1, target_2, attributes):
  """
  Explicit bias evaluation
  :param vecs: index2vec vector matrix
  :param vocab: term2index dict
  :param target_1: list of t1 terms
  :param target_2: list of t2 terms
  :param attributes: list of attributes
  :return: spearman correlation
  """
  sum_first = np.zeros(300)
  cnt = 0
  for t in target_1:
    if t in vocab:
      sum_first += vecs[vocab[t]]
      cnt += 1
    else:
      print(t + " not in vocab!")
  avg_first = sum_first / float(cnt)

  sum_second = np.zeros(300)
  cnt = 0
  for t in target_2:
    if t in vocab:
      sum_second += vecs[vocab[t]]
      cnt += 1
  avg_second = sum_second / float(cnt)

  sims_first = []
  sims_second = []
  for a in attributes:
    if a in vocab:
      vec_a = vecs[vocab[a]]
      sims_first.append(np.dot(avg_first, vec_a) / (np.linalg.norm(avg_first) * np.linalg.norm(vec_a)))
      sims_second.append(np.dot(avg_second, vec_a) / (np.linalg.norm(avg_second) * np.linalg.norm(vec_a)))
  return stats.spearmanr(sims_first, sims_second)


def eval_k_means(t1_list, t2_list, vecs, vocab):
  '''
  Implicit bias evaluation
  :param t1_list: target terms of T1 (list)
  :param t2_list: target terms of T1 (list)
  :param vocab: word2index dict
  :param vecs: index2vector matrix
  :return: avg score over 50 runs
  '''
  lista = t1_list + t2_list
  word_vecs = []
  for l in lista:
    if l in vocab:
      word_vecs.append(vecs[vocab[l]])
    else:
      print(l + " not in vocab!")
  vecs_to_cluster = word_vecs
  golds1 = [1]*len(t1_list) + [0] * len(t2_list)
  golds2 = [0]*len(t1_list) + [1] * len(t2_list)
  items = list(zip(vecs_to_cluster, golds1, golds2))

  scores = []
  for i in range(50):
    random.shuffle(items)
    kmeans = KMeans(n_clusters=2, random_state=0, init = 'k-means++').fit(np.array([x[0] for x in items]))
    preds = kmeans.labels_

    acc1 = len([i for i in range(len(preds)) if preds[i] == items[i][1]]) / len(preds)
    acc2 = len([i for i in range(len(preds)) if preds[i] == items[i][2]]) / len(preds)
    scores.append(max(acc1, acc2))
  return sum(scores) / len(scores)


def bias_analogy_test(vecs, vocab, target_1, target_2, attributes_1, attributes_2):
    """
    Explicit bias evaluation
    :param vecs: word vector matrix index2vec
    :param vocab: dict term2index
    :param target_1: list of t1 terms
    :param target_2: list of t2 terms
    :param attributes_1: list of a1 terms
    :param attributes_2: list of a2 terms
    :return:
    """
    target_1 = [x for x in target_1 if x in vocab]
    target_2 = [x for x in target_2 if x in vocab]
    attributes_1 = [x for x in attributes_1 if x in vocab]
    attributes_2 = [x for x in attributes_2 if x in vocab]

    to_rmv = [x for x in attributes_1 if x in attributes_2]
    for x in to_rmv:
        attributes_1.remove(x)
        attributes_2.remove(x)

    if len(attributes_1) != len(attributes_2):
        min_len = min(len(attributes_1), len(attributes_2))
        attributes_1 = attributes_1[:min_len]
        attributes_2 = attributes_2[:min_len]
    print(attributes_1)
    print(attributes_2)

    atts_paired = []
    for a1 in attributes_1:
        for a2 in attributes_2:
            atts_paired.append((a1, a2))

    tmp_vocab = list(set(target_1 + target_2 + attributes_1 + attributes_2))
    dicto = []
    matrix = []
    for w in tmp_vocab:
        if w in vocab:
            matrix.append(vecs[vocab[w]])
            dicto.append(w)

    vecs = np.array(matrix)
    vocab = {dicto[i]: i for i in range(len(dicto))}

    eq_pairs = []
    for t1 in target_1:
        for t2 in target_2:
            eq_pairs.append((t1, t2))

    for pair in eq_pairs:
        t1 = pair[0]
        t2 = pair[1]
        vec_t1 = vecs[vocab[t1]]
        vec_t2 = vecs[vocab[t2]]

        biased = []
        totals = []
        for a1, a2 in atts_paired:
            vec_a1 = vecs[vocab[a1]]
            vec_a2 = vecs[vocab[a2]]

            diff_vec = vec_t1 - vec_t2

            query_1 = diff_vec + vec_a2
            query_2 = vec_a1 - diff_vec

            sims_q1 = np.sum(np.square(vecs - query_1), axis=1)
            sorted_q1 = np.argsort(sims_q1)
            ind = np.where(sorted_q1 == vocab[a1])[0][0]
            other_att_2 = [x for x in attributes_2 if x != a2]
            indices_other = [np.where(sorted_q1 == vocab[x])[0][0] for x in other_att_2]
            num_bias = [x for x in indices_other if ind < x]
            biased.append(len(num_bias))
            totals.append(len(indices_other))

            sims_q2 = np.sum(np.square(vecs - query_2), axis=1)
            sorted_q2 = np.argsort(sims_q2)
            ind = np.where(sorted_q2 == vocab[a2])[0][0]
            other_att_1 = [x for x in attributes_1 if x != a1]
            indices_other = [np.where(sorted_q2 == vocab[x])[0][0] for x in other_att_1]
            num_bias = [x for x in indices_other if ind < x]
            biased.append(len(num_bias))
            totals.append(len(indices_other))

    return sum(biased) / sum(totals)

def weat_1(self):
    """
WEAT 1 (universally accepted): Targets 1=Flowers, Targets 2=Insects, Attributes 1=pleasant, Attributes 2=unpleasant
:return: targets_1, targets_2, attributes_1, attributes_2
"""
    targets_1 = ["aster", "clover", "hyacinth", "marigold", "poppy", "azalea", "crocus", "iris", "orchid", "rose",
                 "blue-bell", "daffodil", "lilac", "pansy", "tulip", "buttercup", "daisy", "lily", "peony",
                 "violet",
                 "carnation", "gladiola", "magnolia", "petunia", "zinnia"]
    targets_2 = ["ant", "caterpillar", "flea", "locust", "spider", "bedbug", "centipede", "fly", "maggot",
                 "tarantula",
                 "bee", "cockroach", "gnat", "mosquito", "termite", "beetle", "cricket", "hornet", "moth", "wasp",
                 "blackfly",
                 "dragonfly", "horsefly", "roach", "weevil"]
    attributes_1 = ["caress", "freedom", "health", "love", "peace", "cheer", "friend", "heaven", "loyal",
                    "pleasure",
                    "diamond", "gentle", "honest", "lucky", "rainbow", "diploma", "gift", "honor", "miracle",
                    "sunrise",
                    "family",
                    "happy", "laughter", "paradise", "vacation"]
    attributes_2 = ["abuse", "crash", "filth", "murder", "sickness", "accident", "death", "grief", "poison",
                    "stink",
                    "assault", "disaster", "hatred", "pollute", "tragedy", "divorce", "jail", "poverty", "ugly",
                    "cancer",
                    "kill", "rotten",
                    "vomit", "agony", "prison"]
    return targets_1, targets_2, attributes_1, attributes_2

    # WEAT 2: Target 1=Musical instruments, Target 2= Weapons, Attributes 1: pleasant, Attributes 2=unpleasant
def weat_2(self):
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

    return targets_1, targets_2, attributes_1, attributes_2


    # sex - math
def weat_7(self):
    targets_1 = ["math", "algebra", "geometry", "calculus", "equations", "computation", "numbers", "addition"]
    targets_2 = ["poetry", "art", "dance", "literature", "novel", "symphony", "drama", "sculpture"]
    attributes_1 = ["male", "man", "boy", "brother", "he", "him", "his", "son"]
    attributes_2 = ["female", "woman", "girl", "sister", "she", "her", "hers", "daughter"]
    return targets_1, targets_2, attributes_1, attributes_2

    # sex - science
def weat_8(self):
    targets_1 = ["science", "technology", "physics", "chemistry", "Einstein", "NASA", "experiment", "astronomy"]
    targets_2 = ["poetry", "art", "Shakespeare", "dance", "literature", "novel", "symphony", "drama"]
    attributes_1 = ["brother", "father", "uncle", "grandfather", "son", "he", "his", "him"]
    attributes_2 = ["sister", "mother", "aunt", "grandmother", "daughter", "she", "hers", "her"]
    return targets_1, targets_2, attributes_1, attributes_2

    # desease - uncontrollability
def weat_9(self):
    targets_1 = ["sad", "hopeless", "gloomy", "tearful", "miserable", "depressed"]
    targets_2 = ["sick", "illness", "influenza", "disease", "virus", "cancer"]
    # in w2v experiments, the've replaced short-term with short
    attributes_1 = ["impermanent", "unstable", "variable", "fleeting", "short-term", "brief", "occasional"]
    attributes_2 = ["stable", "always", "constant", "persistent", "chronic", "prolonged", "forever"]

    return targets_1, targets_2, attributes_1, attributes_2


def load_embedding_vocab_vectors(path):
    embbedding_dict = {}
    vocab = {}

    vector = []
    with codecs.open(path, "rb", "utf8", "ignore") as infile:
        for index, line in enumerate(infile):
            try:
                parts = line.split()
                word = parts[0]
                nums = np.array([float(p) for p in parts[1:]])
                vector.append(nums)
                vocab[word] = index
                embbedding_dict[word] = nums

            except Exception as e:
                print(line)
                continue
    vector = np.array(vector)
    return embbedding_dict, vocab, vector #



# def main():
#     def boolean_string(s):
#         if s not in {'False', 'True', 'false', 'true'}:
#             raise ValueError('Not a valid boolean string')
#         return s == 'True' or s == 'true'
#
#
#
#     parser = argparse.ArgumentParser(description="Running XWEAT")
#     parser.add_argument("--test_number", type=int, help="Number of the weat test to run", required=False)
#     parser.add_argument("--permutation_number", type=int, default=None,
#                         help="Number of permutations (otherwise all will be run)", required=False)
#     parser.add_argument("--output_file", type=str, default=None, help="File to store the results)", required=True)
#     parser.add_argument("--lower", type=boolean_string, default=False, help="Whether to lower the vocab", required=True)
#     parser.add_argument("--similarity_type", type=str, default="cosine", help="Which similarity function to use",
#                         required=False)
#     parser.add_argument("--embedding_vocab", type=str, help="Vocab of the embeddings")
#     parser.add_argument("--embedding_vectors", type=str, help="Vectors of the embeddings")
#     parser.add_argument("--use_glove", type=boolean_string, default=False, help="Use glove")
#     parser.add_argument("--postspec", type=boolean_string, default=False, help="Use postspecialized fasttext")
#     parser.add_argument("--is_vec_format", type=boolean_string, default=False,
#                         help="Whether embeddings are in vec format")
#     parser.add_argument("--embeddings", type=str, help="Vectors and vocab of the embeddings")
#     parser.add_argument("--lang", type=str, default="en", help="Language to test")
#     args = parser.parse_args()
#
#


embedding_dict, vocab, vector, = load_embedding_vocab_vectors("data/vec/ara_wikipedia_2012_100K-cbow.vec")