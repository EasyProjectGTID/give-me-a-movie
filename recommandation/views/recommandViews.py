import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

from recommandation.tfidf.searchTFIDF2 import search
from recommandation.models import Series, KeyWords, Posting, Rating
from django.core.cache import cache
import redis
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions
from recommandation.tfidf.recommandationCompute import compute
from PTUT.settings import REACT_URL
from recommandation.views import afficheVoteFn


@login_required(login_url='/login')
def recommandTemplate(request):
    user = User.objects.get(pk=request.user.pk)
    token, created = Token.objects.get_or_create(user=user)
    return render(
        request, "recommand.html", {"user": user, "token": token, "base_url": REACT_URL}
    )


class recommandView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @method_decorator(login_required(login_url='/login'))
    def get(self, *args, **kwargs):
        """

		:param args:
		:param kwargs:
		:return:
		"""

        series = Series.objects.all()
        resultat_json = []
        for serie in series:
            resultat_json.append(
                {"pk": serie.pk, "name": serie.real_name, "infos": serie.infos}
            )
        return HttpResponse(json.dumps(resultat_json))

    @method_decorator(login_required(login_url='/login'))
    def post(self, *args, **kwargs):
        """
		:param args:
		:param kwargs:
		:return: Donne le résultat des recommandations compute dans l'onglet recommandez moi
		"""

        resultat = compute(
            like=self.request.data["like"], dislike=self.request.data["dislike"]
        )
        resultat_json = []

        for res in resultat[0:3]:

            serie = Series.objects.get(id=res[0])
            afficheVote = afficheVoteFn(user=self.request.user, serie=serie)
            resultat_json.append(
                {
                    "pk": serie.pk,
                    "name": serie.real_name,
                    "infos": serie.infos,
                    "afficheVote": afficheVote,
                }
            )

        return HttpResponse(json.dumps(resultat_json))
