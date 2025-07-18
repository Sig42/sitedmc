from django.urls import path
from . import views

app_name = 'words'

urlpatterns = [
    path('', views.start, name='start'),
    path('table/', views.table, name='table'),
    path('learn/', views.learn, name='learn'),
    path('add-word/', views.add_word, name='add_word'),
    path('<slug:word>/', views.word_by_slug, name='word_by_slug'),
]
