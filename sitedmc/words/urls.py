from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('<slug:word>/', views.word_by_slug, name='word_by_slug')
]