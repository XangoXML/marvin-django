from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse
from frontpage.models import VulnerabilityResult, App_comments
from frontpage.forms import CommentForm 

def addComment(request,pk):
	myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
	if request.method == "POST":
		myForm = CommentForm(request.POST)
		#myVuln = get_object_or_404 (VulnerabilityResult, pk=pk)
		if myForm.is_valid():
			comment = myForm.cleaned_data['text']
			user = request.user
			new_comment = App_comments(author = request.user,
									   contents = comment,
									   vuln = myVuln,
									   app = myVuln.app)
			new_comment.save()
		context = {'object':myVuln, 'form':myForm}
		return render(request, 'frontpage/vulnerabilityresult_detail.html', context)
	else:
		myForm = CommentForm()
		context = {'object':myVuln, 'form':myForm}
		return render(request, 'frontpage/vulnerabilityresult_detail.html', context)

def deleteComment(request,pk):
	myComment = get_object_or_404 (App_comments, pk=pk)
	myVuln = myComment.vuln
	myComment.delete()
	myForm = CommentForm(request.POST)
	context = {'object':myVuln, 'form':myForm}
	return render(request, 'frontpage/vulnerabilityresult_detail.html', context)
