import os
import codecs
import pandas as pd

# version: 1.6
# todo: replate .log with ""

report = {
    "id": [],
    "year": [],
    "corpus_size": [],
    'test_number': [],
    "data_set_source": [],
    "language/dialect": [],
    "embedding_method": [],
    "tocken_type": [],
    "vector_size": [],
    "pretrained/trained": [],
    "d": [],
    "e": [],
    "p": [],
    "number_of_permutation": [],
    "number_of_words": [],
    "percent": [],
    "list_of_missing_words": [],

}
data_set_source = "liptiz_news"
tocken_type = "bigram"
vector_size = "300"
language = "MSA"
embedding_method = "cbow"
trained = "myself"
result_tuple = []

file_list = os.listdir('./results')  # change this directory


def get_list_of_missing_words(file_name):
    '''return list of words'''
    with codecs.open("./results/" + file_name, "r", "utf-8") as f:
        log_list = []
        for i in f:
            log_list.append(i.strip())
    return log_list[1:-3]


def get_result_values(file_name):
    '''returns a list with d, e, p, score'''

    with codecs.open("results/" + file_name, "r", "utf-8") as f:
        log_list = []
        for i in f:
            log_list.append(i.strip())

        log_list = log_list[-2]

        log_list = log_list.split(" ")
        log_list = (log_list[1:])
        d = log_list[0].replace("(", "").replace(",", "")
        e = log_list[1].replace(",", "")
        p = log_list[2].replace(")", "")

    return d, e, p


def get_test_number(file_name):
    ''' return test number from file name'''

    file_name = file_name.strip().split("_")
    test_number = file_name[4]
    test_number = test_number[0]

    return test_number


def percent_of_missing_words(file_name):
    dictionary = {
        "1": 100,
        "2": 100,
        "7": 32,
        "8": 32,
        "9": 26,
    }

    test_number = get_test_number(file_name)
    number_of_words = len(get_list_of_missing_words(file_name))

    precent = number_of_words / dictionary[test_number]
    print(number_of_words, dictionary[test_number])
    return precent


def get_year(file_name):
    '''return the year name using the file name as an input'''
    file_name = file_name.strip().split("_")
    year = file_name[2]
    return year


def get_corpus_size(file_name):
    ''' return the corpus size from the file name'''
    file_name = file_name.strip().split("_")
    size = file_name[3]
    size = size.split("-")
    size = size[0]
    return size


def get_permutation_number(file_name):
    with codecs.open("./results/" + file_name, "r", "utf-8") as f:
        log_list = []
        for i in f:
            log_list.append(i.strip())
    return log_list[-3]


for file_name in file_list:
    report['id'].append(file_name.replace(".log", ""))
    report["test_number"].append(get_test_number(file_name))
    report["data_set_source"].append(data_set_source)
    report['language/dialect'].append(language)
    report['embedding_method'].append(embedding_method)
    report['tocken_type'].append(tocken_type)
    report['vector_size'].append(vector_size)
    report['pretrained/trained'].append(trained)
    d, e, p = (get_result_values(file_name))
    report['d'].append(str(d))
    report["e"].append(str(e))
    report["p"].append(str(p))
    report['number_of_words'].append(len(get_list_of_missing_words(file_name)))
    report['percent'].append(percent_of_missing_words(file_name))
    report['list_of_missing_words'].append(get_list_of_missing_words(file_name))
    report['year'].append(get_year(file_name))
    report["corpus_size"].append(get_corpus_size(file_name))
    report["number_of_permutation"].append(get_permutation_number(file_name))

df = pd.DataFrame.from_dict(report)
df.to_csv("reprot_with_permutation.csv", sep=",", index=False)

print(df)