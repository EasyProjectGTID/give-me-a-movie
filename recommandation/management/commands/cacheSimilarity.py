import math
import operator
import time
from collections import Counter

import numpy
import psycopg2
from django.core.management import BaseCommand

from PTUT import settings

conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(settings.DATABASES['default']['NAME'],
																						   settings.DATABASES['default']['USER'],
																						   settings.DATABASES['default']['HOST'],
																						   settings.DATABASES['default']['PASSWORD']))
cur = conn.cursor()

class Command(BaseCommand):
	help = 'Cache IDF'

	def handle(self, *args, **options):
		cur.execute(
			"select s.id from recommandation_series s")
		series = cur.fetchall()
		for serie in series:
			# print(serie[0])
			construct(serie[0])

def cosine_distance(serie_id, u, v):
	"""
	Returns the cosine of the angle between vectors v and u. This is equal to
	u.v / |u||v|.
	"""
	return serie_id, 100 * (numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))))

def buildVector(seriename, serie1, serie2):
	counter1 = serie1
	counter2 = serie2

	counter1_c = Counter()
	counter2_c = Counter()

	for k in counter1:
		counter1_c[k[0]] = k[1]
	for k in counter2:
		counter2_c[k[0]] = k[1]

	all_items = set(counter1_c.keys()).union(set(counter2_c.keys()))
	vector1 = [round(counter1_c[k], 3) for k in all_items]
	vector2 = [round(counter2_c[k], 3) for k in all_items]
	return seriename, vector1, vector2

def construct(serie_pk):
	cur.execute(
		"select s.id from recommandation_series s where s.id='{}'".format(serie_pk))
	serie_id = cur.fetchall()[0][0]

	cur.execute(
		"select * from mv_{}".format(serie_id))
	serie_comparer = cur.fetchall()

	cur.execute("select s.id from recommandation_series s where s.id <> '{}'".format(serie_id))
	others = cur.fetchall()
	resultat = []

	for other in others:
		cur.execute("select s.id from recommandation_series s where s.id='{}'".format(other[0]))
		serieid = cur.fetchall()[0][0]

		cur.execute("select * from mv_{}".format(other[0]))
		other_words = cur.fetchall()
		seriename, v1, v2 = buildVector(serieid, serie_comparer, other_words)
		resultat.append(cosine_distance(serieid, v1, v2))

	resultat_trier = sorted(resultat, key=operator.itemgetter(1), reverse=True)

	for res in resultat_trier:
		cur.execute(
			"INSERT INTO recommandation_similarity (serie_id, similar_to_id, score) VALUES ('{0}', '{1}', '{2}')".format(serie_pk, res[0],
																														 res[1]))

	conn.commit()



