import os
import codecs
import pandas as pd

# version: 1.7.1

report = {
    "id": [],
    "year": [],
    "corpus_size": [],
    'test_number': [],
    "data_set_source": [],
    "language/dialect": [],
    "embedding_method": [],
    "token_type": [],
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
#tocken_type = "bigram" todo method
#language = "MSA" #:todo: method
trained = "aravec"
result_tuple = []
corpus_size = ""
file_list = os.listdir('./results')  # change this directory
year = ""

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

def get_embedding_method(file_name):
    file_name = file_name.strip().split("_")
    embeddin_method = file_name[2]
    return embeddin_method

def get_data_source(file_name):
    file_name = file_name.strip().split("_")
    embeddin_method = file_name[4]
    return embeddin_method

def get_vector_size(file_name):
    file_name = file_name.strip().split("_")
    vector_size = file_name[3]
    return vector_size

def get_token_type(file_name):
    file_name = file_name.strip().split("_")
    token_type = file_name[1]
    return token_type

def get_language(file_name):
    file_name = file_name.strip().split("_")
    file_name = file_name[4].replace(".p", "")
    if file_name == "twitter":
        language = "mixed"
    elif file_name == "wiki":
        language = "MSA"
    else:
        language = "web"
    return language

for file_name in file_list:
    report['id'].append(file_name.replace(".log", ""))
    report["test_number"].append(get_test_number(file_name))
    report["data_set_source"].append(get_data_source(file_name).replace(".p", ""))
    report['vector_size'].append(get_vector_size(file_name))
    report['pretrained/trained'].append(trained)
    d, e, p = (get_result_values(file_name))
    report['d'].append(str(d))
    report["e"].append(str(e))
    report["p"].append(str(p))
    report['number_of_words'].append(len(get_list_of_missing_words(file_name)))
    report['percent'].append(percent_of_missing_words(file_name))
    report['list_of_missing_words'].append(get_list_of_missing_words(file_name))
    report['year'].append(year)
    report["corpus_size"].append(corpus_size)
    report["number_of_permutation"].append(get_permutation_number(file_name))
    report["embedding_method"].append(get_embedding_method(file_name))
    report["token_type"].append(get_token_type(file_name))
    report["language/dialect"].append((get_language(file_name)))


df = pd.DataFrame.from_dict(report)
df.to_csv("reprot_with_permutation.csv", sep=",", index=False)

print(df)