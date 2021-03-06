import csv
import json
import os

from django.db.models import Sum, Count
from django.urls import resolve, reverse
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin

from django.contrib import admin
from django import forms
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from PTUT import STATIC_URL, MEDIA_ROOT
from recommandation.tasks import getInfos
from recommandation.tasks import file_processing
from .models import Series, KeyWords, Posting, Rating, SearchCount, Similarity
from admin_auto_filters.filters import AutocompleteFilter


def getInformations(model, request, queryset):
	getInfos(queryset)


getInformations.short_description = "Télécharger les informations complémentaires pour les series selectionnées"


def export_csv(self, request, queryset):
	meta = self.model._meta
	field_names = [field.name for field in meta.fields]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
	writer = csv.writer(response)

	writer.writerow(field_names)
	for obj in queryset:
		row = writer.writerow([getattr(obj, field) for field in field_names])

	return response


export_csv.short_description = "Exporter les selections en CSV"


def handle_uploaded_file(f):
	with open(MEDIA_ROOT[0] + str(f), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return str(f)


class SerieForm(forms.ModelForm):
	file = forms.FileField(required=False)

	class Meta:
		model = Series
		exclude = ['infos', 'max_keyword_nb', 'image_local', 'name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
	list_display = ('real_name', 'infos', 'image', 'max_keyword_nb')
	actions = [getInformations, export_csv]
	search_fields = ['real_name', 'name']
	exclude = ('infos', 'name', 'max_keyword_nb', 'image_local')
	readonly_fields = ('image', 'data_prettified', 'number_of_words')
	form = SerieForm

	class Meta:
		verbose_name_plural = "Series"

	def save_model(self, request, obj, form, change):
		if request.FILES:
			filename = handle_uploaded_file(request.FILES['file'])
			obj.name = os.path.splitext(os.path.basename(filename))[0]
			obj.real_name = request.POST['real_name']
			super(SeriesAdmin, self).save_model(request, obj, form, change)
			file_processing(filename)
		obj.real_name = request.POST['real_name']
		super(SeriesAdmin, self).save_model(request, obj, form, change)

	def similaire(self, instance):
		return Similarity.objects.filter(serie=instance).order_by('-score')[0:10]

	def data_prettified(self, instance):
		response = json.dumps(instance.infos, sort_keys=True, indent=2)
		response = response[:5000]
		formatter = HtmlFormatter(style='colorful')
		response = highlight(response, JsonLexer(), formatter)
		style = "<style>" + formatter.get_style_defs() + "</style><br>"
		return mark_safe(style + response)

	def number_of_words(self, instance):
		return Posting.objects.filter(series=instance).count()

	data_prettified.short_description = 'Informations complémentaires'
	number_of_words.short_description = 'Nombre de mots de la serie'


@admin.register(SearchCount)
class SearchCountAdmin(admin.ModelAdmin):
	list_display = ('search_key', 'count')
	search_fields = ['search_key']
	actions = [export_csv]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	actions = [export_csv]
	list_display = ('serie', 'rating', 'user', 'date_vote')
	autocomplete_fields = ['user']
	list_filter = ('rating', 'serie', 'user')


@admin.register(KeyWords)
class KeyWordsAdmin(admin.ModelAdmin):
	list_display = ('key', 'idf')
	search_fields = ['key']

	actions = [export_csv]


class SeriesFilter(AutocompleteFilter):
	title = 'Serie'  # display title
	field_name = 'series'  # name of the foreign key field


@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
	list_display = ('keywords', 'number', 'tf', 'series')

	search_fields = ['keywords__key']
	autocomplete_fields = ['series']
	list_filter = [SeriesFilter]

	actions = [export_csv]

	class Media:
		pass


class SerieFilter(AutocompleteFilter):
	title = 'Serie'  # display title
	field_name = 'serie'  # name of the foreign key field


@admin.register(Similarity)
class SimilarityAdmin(admin.ModelAdmin):
	search_fields = ['serie__real_name']
	list_display = ('serie', 'similar_to', 'score')
	autocomplete_fields = ['serie']
	# list_filter = ('serie',)
	list_filter = [SerieFilter]

	class Media:
		pass



from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'

admin.site.register(LogEntry, LogEntryAdmin)