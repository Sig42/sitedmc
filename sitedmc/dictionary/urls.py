from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('start_not_auth', views.StartNotAuth.as_view(), name='start_not_auth'),
    path('add_words', views.AddWords.as_view(), name='add_words'),
    path('show_words', views.ShowWords.as_view(), name='show_words'),
    path('word/<int:pk>', views.UpdateWord.as_view(), name='update_word'),
    path('check_auth', views.check_auth, name='check_auth'),
    path('delete_word/<int:pk>', views.DeleteWord.as_view(), name='delete_word'),
    path('pre_learn', views.pre_learn, name='pre_learn'),
    path('learn_list', views.learn_list, name='learn_list'),
]
