from django.urls import path
from . import views

app_name = 'words'

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('show_list/', views.ShowList.as_view(), name='show_list'),
    path('create_list/', views.CreateList.as_view(), name='create_list'),
    path('my_lists/', views.MyLists.as_view(), name='my_lists'),
    path('add_words/', views.AddWords.as_view(), name='add_words'),
    path('learn_words/', views.LearnWords.as_view(), name='learn_words'),
]
