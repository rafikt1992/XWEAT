import  os
import codecs
with codecs.open("data/cc.ar.300(short).vec", "w", "utf8") as f:
    with codecs.open("data/cc.ar.300.vec", "r", "utf8") as file:
        for i, k in enumerate(file):
            f.writelines(k)
            if i == 1000000:
                print('done')
                break

