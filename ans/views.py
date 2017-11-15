from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
# redirect - redirects the user to a pre-defined url.
# HttpResponse - used to return a simple html response to the user upon request.
# Http404 - custom 404 error.
# to return JsonResponse
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse
# Calling the models/tables of the database defined in models.py.
from .models import CustomUser, Question
#authenticate, login - support inbuilt functions for building the authentication and login system.
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.views.generic import View
from django.views import generic
#importing user model
from django.contrib.auth.models import User
import json
# serializers are used to serialize data, here return in the json format
from django.core import serializers
from django.dispatch import receiver
# getting extended user model
from django.contrib.auth import get_user_model
User = get_user_model()

#in answers_given 1 means attempted, 2 means correctly answered and 3 means skipped
# view that returns all the details to be displayed
def main(request):
	# If user is already authenticated by the django admin, else redirect to login page
	if (request.user.is_authenticated()):
		leaderboard = User.objects.order_by('score').reverse()
		user=request.user
		i = 0
		# update rank
		for player in leaderboard:
			if user.score == player.score:
				user.rank = i + 1
				user.save()
			else:
				i += 1
		
		return render(request,'index.html/',{'user':user.username,'score':user.score,'rank':user.rank,'leaderboard':leaderboard})
	else:
		return render(request,'front.html/')






# view to logout the user
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://127.0.0.1:8000')
	


# checks answer and updates marks and rank
def answer(request, number):
	# If user is already authenticated by the django admin, else redirect to login page
	if request.user.is_authenticated():
		user = request.user
		user.save()
		#checks which type of question attempted and makes a list of that tupe of question and initialises variables accordingly
		if number=='1':
			product=Question.objects.get(question_type='football',question_no=user.question_no1)
			qsno=user.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=user.question_no2)
			qsno=user.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=user.question_no3)
			qsno=user.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=user.question_no4)
			qsno=user.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=user.question_no5)
			qsno=user.question_no5
			no=5
		
		answerof = request.GET.get('answerof')

		# update answer_given and question_no
		if answerof == product.solution:
			list1 = list(user.answers_given)
			list1[30*(no-1) +qsno] = '1'
			user.answers_given = ''.join(list1)
			user.score+=100
			if number=='1':
				user.question_no1+=1
			elif number=='2':
				user.question_no2+=1
			elif number=='3':
				user.question_no3+=1
			elif number=='4':
				user.question_no4+=1
			elif number=='5':
				user.question_no5+=1
			user.save()
			error = False
		else:
			list1 = list(user.answers_given)
			list1[30*(no-1)+qsno] = '3'
			user.answers_given = ''.join(list1)
			user.save()
			return HttpResponseRedirect('/accounts/profile/%s/' % number)

		
		
		leaderboard = User.objects.order_by('score').reverse()
		i = 0
		# updates rank
		for player in leaderboard:
			if user.score == player.score:
				user.rank = i + 1
				user.save()
			else:
				i += 1

		user.save()
		return HttpResponseRedirect('/accounts/profile/%s/' % number)
	else:
		return HttpResponseRedirect('/')



# returns details to be displayed in question popup
def detail(request, number):
	# If user is already authenticated by the django admin, else redirect to login page
	if request.user.is_authenticated():
		error = False
		u = request.user
		#checks which type of question attempted and makes a list of that tupe of question and initialises variables accordingly
		if number=='1':
			product=Question.objects.get(question_type="football",question_no=u.question_no1)
			qsno=u.question_no1
			no=1
			left=5
		elif number=='2':
			product=Question.objects.get(question_type="cricket",question_no=u.question_no2)
			qsno=u.question_no2
			no=2
			left=5
		elif number=='3':
			product=Question.objects.get(question_type="miscellaneous",question_no=u.question_no3)
			qsno=u.question_no3
			no=3
			left=5
		elif number=='4':
			product=Question.objects.get(question_type="track&field",question_no=u.question_no4)
			qsno=u.question_no
			no=4
			left=5
		elif number=='5':
			product=Question.objects.get(question_type="extras",question_no=u.question_no5)
			qsno=u.question_no5
			no=5
			left=5
		s = 3-u.answers_given.count('2')
		u.save()
		qsleft=left-product.question_no+1
		resp={'score':u.score,'hinttext':product.question,'skip':s,'djangoNoofQuestionsLeft':qsleft,'qsno':qsno,'djangoImage':product.question_img.url}
		
		return JsonResponse(resp)
	else:
		return HttpResponseRedirect('/')


# Updates no of skips left, rank and marks after a question is skipped
def skip(request, number):
	# If user is already authenticated by the django admin, else redirect to login page
	if request.user.is_authenticated():
		u=request.user
		u.score-=25
		#checks which type of question attempted and makes a list of that tupe of question and initialises variables accordingly
		if number=='1':
			product=Question.objects.get(question_type='football',question_no=u.question_no1)
			qsno=u.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=u.question_no2)
			qsno=u.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=u.question_no3)
			qsno=u.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=u.question_no4)
			qsno=u.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=u.question_no5)
			qsno=u.question_no5
			no=5
		
		s = u.answers_given.count('2')
		# updates answer_given and question_no
		if s < 3:
			list1 = list(u.answers_given)
			list1[30*(no-1)+qsno] = '2'
			u.answers_given = ''.join(list1)
			if number=='1':
				u.question_no1+=1
			elif number=='2':
				u.question_no2+=1
			elif number=='3':
				u.question_no3+=1
			elif number=='4':
				u.question_no4+=1
			elif number=='5':
				u.question_no5+=1
			u.save()

			leaderboard = User.objects.order_by('score').reverse()
			i = 0
			# updates rank
			for player in leaderboard:
				if u.score == player.score:
					u.rank = i + 1
					u.save()
				else:
					i += 1

			u.save()
			return HttpResponseRedirect('/accounts/profile/%s/' % number)

		else:
			return HttpResponseRedirect('/accounts/profile/%s/' % number)
	else:
		return HttpResponseRedirect('/')



# updates marks and ranks after player leaves a stadium
def leave(request, number):
	# If user is already authenticated by the django admin, else redirect to login page
	if request.user.is_authenticated():
		#checks which type of question attempted and makes a list of that tupe of question and initialises variables accordingly
		u = request.user
		if number=='1':
			product=Question.objects.get(question_type='football',question_no=u.question_no1)
			qsno=u.question_no1
			no=1
		elif number=='2':
			product=Question.objects.get(question_type='cricket',question_no=u.question_no2)
			qsno=u.question_no2
			no=2
		elif number=='3':
			product=Question.objects.get(question_type='miscellaneous',question_no=u.question_no3)
			qsno=u.question_no3
			no=3
		elif number=='4':
			product=Question.objects.get(question_type='track&field',question_no=u.question_no4)
			qsno=u.question_no
			no=4
		elif number=='5':
			product=Question.objects.get(question_type='extras',question_no=u.question_no5)
			qsno=u.question_no5
			no=5
		score=u.score-50
		u.score=score
		leaderboard = User.objects.order_by('score').reverse()
		i = 0
		# updating rank
		for player in leaderboard:
			if u.score == player.score:
				u.rank = i + 1
				u.save()
			else:
				i += 1
		u.save()
		resp={'score':u.score}
		
		return HttpResponse(json.dumps(resp),content_type='application/json')
	else:
		return HttpResponseRedirect('/')



# for displaying leaderboard
def leaderboard(request):
	if request.user.is_authenticated():
		leaderboard = User.objects.order_by('score').reverse()
		username = ["" for x in range(10)]
		score = [0 for i in range(10)]
		# get top 10 players
		for i in range(10):
			username[i]=leaderboard[i].username
			score[i]=leaderboard[i].score
		resp={'username':username,'rank':request.user.rank, 'score':score}
		
		return HttpResponse(json.dumps(resp),content_type='application/json')
	else:
		return HttpResponseRedirect('/')