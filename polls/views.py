from django.views.generic import CreateView

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice, UserInfo
# Library to load HTML content
from django.template import loader
from django.shortcuts import get_object_or_404,render
# Library to handle errors
from django.http import Http404

from polls.forms import CUserLoginForm, CUserRegisterForm, CUserChangeForm, ProductForm, CategoryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

#Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')
        page_number = request.GET.get('page', 1)

        paginate_result = do_paginate(latest_question_list, page_number)
        latest_question_list = paginate_result[0]
        paginator = paginate_result[1]
        base_url = '?'
        return render(request, 'polls/quiz.html',
                        {'latest_question_list': latest_question_list, 'paginator' : paginator, 'base_url': base_url})

def short_index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list}
        return render(request, 'polls/index.html', context)

def index2(request):
        return HttpResponse("Buenos días")

def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            chioces = question.choice_set.get(pk=question_id)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'error_message': "You didn't select a choice.",
            })
        else:
            return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#Login section
@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

def register_user(request):
    registered = False
    if request.method == 'POST':
        profile_form = CUserChangeForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            if 'username' in request.FILES:
                print('found it')
                profile.username = request.FILES['username']
            profile.save()
            registered = True
        else:
            print(profile_form.errors)
    else:
        profile_form = CUserChangeForm()
    return render(request,'polls/registration.html',
                          {'profile_form':profile_form,
                           'registered':registered})

def register_product(request):
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
        else:
            print(product_form.errors)
    else:
        product_form = ProductForm()
    return render(request,'polls/product.html',
                          {'product_form':product_form})

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(email=email)
            print(user)
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('polls:index-login'))
        except:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'polls/login.html', {})

@login_required
def question_filter(request):
    question = request.POST.get('question_text', '').strip()
    question_date = request.POST.get('question_date', '').strip()
    print(question_date)
    if len(question) == 0:
        question = request.GET.get('question_text', '').strip()
    if len(question_date) == 0:
        question_date = datetime.now()
    question_list = Question.objects.filter(question_text__contains=question, pub_date__date=question_date).order_by('-pub_date')
    page_number = request.GET.get('page', 1)
    paginate_result = do_paginate(question_list, page_number)
    question_list = paginate_result[0]
    paginator = paginate_result[1]
    base_url = '/polls/filter/?question_text=' + question + "&question_date=" + question_date + '&'
    return render(request, 'polls/quiz.html',
                      {'latest_question_list': question_list, 'paginator' : paginator, 'base_url': base_url, 'search_question': question, 'search_date': question_date})

def do_paginate(data_list, page_number):
    ret_data_list = data_list
    # suppose we display at most 2 records in each page.
    result_per_page = 2
    # build the paginator object.
    paginator = Paginator(data_list, result_per_page)
    try:
        # get data list for the specified page_number.
        ret_data_list = paginator.page(page_number)
    except EmptyPage:
        # get the lat page data if the page_number is bigger than last page number.
        ret_data_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if the page_number is not an integer then return the first page data.
        ret_data_list = paginator.page(1)
    return [ret_data_list, paginator]