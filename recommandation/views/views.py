import csv
import datetime
import json
import pickle
import time
from _operator import itemgetter
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from recommandation.tfidf.searchTFIDF4 import search
from recommandation.models import Series, KeyWords, Posting, Rating, Similarity
from rest_framework.views import APIView
from PTUT.settings import REACT_URL, POSTER_URL
from recommandation.views.utils import afficheVoteFn, recherche_history


def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response

def index(request):
    if request.user.is_anonymous:
        return render(request, 'index.html', {'base_url':REACT_URL})
    else:
        user = User.objects.get(pk=request.user.pk)
        token, created = Token.objects.get_or_create(user=user)
        return render(request, 'index.html', {'token': token, 'base_url':REACT_URL})


class rechercheView(APIView):

    def get(self, *args, **kwargs):
        """
           :param request:
           :return: utiliser pour la recherche
           """
        keywords = self.request.query_params.get('keywords')
        resultat_json = []
        recherche_history(keywords)
        #Si l'on est authentifié
        if self.request.user.is_authenticated:
            #On lance la recherche
            res = search(keywords)

            for serie in res[0:4]:
                serie = Series.objects.get(name=serie[0])
                serie.infos['Poster'] = str(POSTER_URL + str(serie.image_local))
                afficheVote = afficheVoteFn(user=self.request.user, serie=serie) # On regarde si on affiche le vote au cas ou l'utilisateur aurait déjà voté

                resultat_json.append(
                    {'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))

        #Si l'on n'est pas authentifié
        else:
            res = search(keywords)
            for serie in res[0:4]:
                serie = Series.objects.get(name=serie[0])
                serie.infos['Poster'] = str(POSTER_URL + str(serie.image_local))
                resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
            return HttpResponse(json.dumps(resultat_json))




class similarItemsView(APIView):

    def get(self, *args, **kwargs):
        # Si on est authentifié
        if self.request.user.is_authenticated:

            id = self.request.query_params.get('id')
            #resultat = Similarity.objects.filter(serie=id).order_by('-score')
            resultat = Similarity.objects.filter(serie=id).order_by('-score')
            resultat_json = []
            for similar in resultat[0:3]:


                serie = Series.objects.get(id=similar.similar_to.id)
                afficheVote = afficheVoteFn(user=self.request.user, serie=serie.id)
                serie.infos['Poster'] = str(POSTER_URL + str(serie.image_local))

                resultat_json.append(
                    {'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))

        else:
            id = self.request.query_params.get('id')
            resultat = Similarity.objects.filter(serie=id).order_by('-score')
            resultat_json = []
            for similar in resultat[0:3]:
                serie = Series.objects.get(id=similar.similar_to.id)
                serie.infos['Poster'] = str(POSTER_URL + str(serie.image_local))
                resultat_json.append({'pk': serie.pk, 'name': serie.real_name, 'infos': serie.infos})
            return HttpResponse(json.dumps(resultat_json))



class lastRecentView(APIView):
    # permission_classes = (permissions.IsAuthenticated)
    #authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            series = Series.objects.all()
            serieToOrder = dict()
            for serie in series:
                try:
                    serieToOrder[serie] = datetime.datetime.strptime(serie.infos.get('Released', None), "%d %b %Y")
                except:
                    pass
            resultat_json = []
            for serie in sorted(serieToOrder.items(), key=itemgetter(1), reverse=True):
                serie[0].infos['Poster'] = str(POSTER_URL + str(serie[0].image_local))
                afficheVote = afficheVoteFn(user=self.request.user, serie=serie[0])
                resultat_json.append({'pk': serie[0].pk, 'name': serie[0].real_name, 'infos': serie[0].infos, 'afficheVote': afficheVote})
            return HttpResponse(json.dumps(resultat_json))
        else:

            series = Series.objects.all()
            serieToOrder = dict()
            for serie in series:
                try:
                    serieToOrder[serie] = datetime.datetime.strptime(serie.infos.get('Released', None), "%d %b %Y")
                except:
                    pass
            resultat_json = []
            for serie in sorted(serieToOrder.items(), key=itemgetter(1), reverse=True):
                serie[0].infos['Poster'] = str(POSTER_URL + str(serie[0].image_local))
                resultat_json.append({'pk': serie[0].pk, 'name': serie[0].real_name, 'infos': serie[0].infos,'afficheVote': True })
            return HttpResponse(json.dumps(resultat_json))





