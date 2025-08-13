from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('learn_words/<int:pk>', views.LearnWords.as_view(), name='learn_words'),
    path('add_words', views.AddWords.as_view(), name='add_words'),
    path('show_words', views.ShowWords.as_view(), name='show_words'),
]
