import codecs


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

embeding_dict = {}
sts_1_score = 0.0
sts_2_score = 0.0
with codecs.open('data/STS.input.track1.ar-ar.txt', 'r', "utf-8") as input:
    for line in input:
        line = line.strip().split("\t")
        sts_1 = line[0].replace(".","").split(" ")
        sts_2 = line[1].replace(".", "").split(" ")
        for token in sts_1:

