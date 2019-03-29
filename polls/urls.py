from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
     # ex: /polls/
    path('', views.short_index, name='index'),
    path('home/', views.index, name='index-login'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='details'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.user_logout, name='logout'),
    path('filter/', views.question_filter, name='question_filter')
]