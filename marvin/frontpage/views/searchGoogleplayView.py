from frontpage.settings import gp_server, gp_authenticated
from gpApi import utils
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render
from frontpage.forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

def dirtybastard(numDownloadsString):
	# print numDownloadsString, (re.search(r'\d+', numDownloadsString.replace(',', '')).group())
	return int(re.search(r'\d+', numDownloadsString.replace(',', '')).group())+10*len(numDownloadsString)

def search_googleplay(request):
	myToken = csrf(request)
	if request.method == 'POST':
		form = SearchForm(request.POST)
		import pdb;pdb.set_trace()
		if form.is_valid() & gp_authenticated:
			searchterms = request.POST['terms']
			appsFound = gp_server.search(searchterms, 34, None)
			appsFound.sort(key=lambda app: dirtybastard(app['numDownloads']), reverse=True)
			paginator = Paginator(appsFound, 20)
			page = request.GET.get('page')
			try:
				last_packages = paginator.page(page)
			except PageNotAnInteger:
				last_packages = paginator.page(1)
			except EmptyPage:
				last_packages = paginator.page(paginator.num_pages)
			context = {'packages':last_packages, 'terms':searchterms}
			return render(request, 'frontpage/gpresults.html', context)
		# else:
			# return HttpResponseRedirect('frontpage/search_source.html/',myDict)
	else:
		myToken = csrf(request)
		form = SearchForm()
		myDict = {'form':form, 'title':"Buscar en Google Play"}
		myDict.update(myToken)
		return render(request, 'frontpage/search_source.html/',myDict)