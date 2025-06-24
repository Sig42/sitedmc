from multiprocessing.resource_tracker import register

from django.urls import path,  register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "conv_year")

urlpatterns = [
    path('', views.start, name='start'),
    path('add_post', views.add_post, name='add_post'),
    path('blogger/<slug:blogger_name>', views.posts_by_name, name='posts_by_name'),
    path('archive/<conv_year:year>', views.archive, name='archive'),
]

handler404 = views.page_not_found
