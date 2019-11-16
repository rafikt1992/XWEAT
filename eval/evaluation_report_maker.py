import os
import codecs
import pandas as pd

"""copy to eval directory"""

report = {
    "id": [],
    "value": [],

}
teststring = "years_concatinated.vecEval"
file_list = os.listdir('/home/rtakiedd/projects/XWEAT/eval')  # turn off
#  file_list = [
# "ara_news_2007_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2007_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2007_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2007_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2008_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2008_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2008_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2008_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2008_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2009_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2009_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2009_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2009_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2009_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2010_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2010_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2010_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2010_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2010_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2011_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2011_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2011_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2011_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2011_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2015_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2015_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2015_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2015_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2015_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2016_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2016_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2016_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2016_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2016_300K-sentencesCleaned.txt.vecEval",
# "ara_news_2017_1M-sentencesCleaned.txt.vecEval",
# "ara_news_2017_10K-sentencesCleaned.txt.vecEval",
# "ara_news_2017_30K-sentencesCleaned.txt.vecEval",
# "ara_news_2017_100K-sentencesCleaned.txt.vecEval",
# "ara_news_2017_300K-sentencesCleaned.txt.vecEval",
# "ara_wikipedia_2016_1M-cbow.vecEval",
# "years_concatinated.vecEval"
# ]

def get_result(file_name):
    with codecs.open(file_name, "r", "utf-8") as f:
        log_list = []
        for i in f:
            log_list.append(i.strip())
        log_list = str(log_list[1])
        log_list = log_list.split(" ")
    return log_list[0]


for file_name in file_list:
    if file_name.endswith("Eval"):

        report["id"].append(file_name)
        report["value"].append(get_result(file_name))

df = pd.DataFrame.from_dict(report)
df.to_csv("model_evaluation_new.csv", sep=",", index=False)

print(df)