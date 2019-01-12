import time
import os
from multiprocessing import pool, Process, Manager
from multiprocessing.pool import Pool
import asyncio
import psycopg2
import pysrt
import re

from nltk import PorterStemmer
from nltk.corpus import stopwords
import operator
from collections import Counter
import time

cachedStopWords = stopwords.words("french") + stopwords.words("english")
conn = psycopg2.connect("dbname='django123' user='postgres' host='localhost' password=''")
def getWords(text):
    return re.compile('\w+').findall(text)

def getKey(item):
    return item[1]

def analyseFile(liste_episode, serie):
    list = []
    string = ''

    for episode in liste_episode:
        subs = pysrt.open(episode, encoding='iso-8859-1')

        for i in range(len(subs)):
            for j in getWords(subs[i].text):
                list.append(j.lower())
                string = string + ' ' + j

    filtered_words = [word for word in list if word not in cachedStopWords]
    d = Counter(' '.join(filtered_words).split())

    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    cur = conn.cursor()

    list = set()
    for x in sorted_d:
        list.add(x)
    list_sorted = sorted(list, key=getKey)
    for word in list_sorted:
        if len(word[0]) > 2:
            try:
                    cur.execute(
                        "INSERT INTO recommandation_keywords (key) VALUES ('{}') returning id".format(word[0]))
                    key_id = cur.fetchone()[0]
                    conn.commit()
            except Exception as e:
                conn.rollback()
                cur.execute("SELECT k.id from recommandation_keywords as k where k.key='{}'".format(word[0]))
                key_id = cur.fetchone()[0]

            cur.execute("INSERT INTO recommandation_posting (number, keywords_id, series_id) VALUES ('{0}','{1}','{2}')".format(word[1], key_id, serie))
            conn.commit()

def walk_sub():
    for root in os.scandir("/home/hadrien/Bureau/sous-titres"):
        start = time.time()
        cur = conn.cursor()
        cur.execute("INSERT INTO recommandation_series (name) VALUES ('{}') returning id".format(root.name))
        conn.commit()
        serie_id = cur.fetchone()[0]
        liste_episode = []
        for files in os.scandir(root):
            if str(files.name)[-4:] == '.zip':
                pass
            else:
                liste_episode.append("/home/hadrien/Bureau/sous-titres/" + root.name + '/' + files.name,)
        analyseFile(liste_episode, serie=serie_id)
        end = time.time()
        print('walk ', end - start)
    conn.close()







import nltk
start = time.time()
#nltk.download('stopwords')
walk_sub()

end = time.time()
print('total ',end - start)




