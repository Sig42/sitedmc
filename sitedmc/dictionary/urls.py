from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('start_not_auth', views.StartNotAuth.as_view(), name='start_not_auth'),
    path('learn_words/<int:pk>', views.LearnWords.as_view(), name='learn_words'),
    path('choose_words/', views.ChooseWords.as_view(), name='choose_words'),
    path('add_words', views.AddWords.as_view(), name='add_words'),
    path('show_words', views.ShowWords.as_view(), name='show_words'),
    path('word/<slug:slug>', views.UpdateWord.as_view(), name='update_word'),
    path('check_auth', views.check_auth, name='check_auth'),
]
