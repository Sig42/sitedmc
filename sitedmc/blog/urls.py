from multiprocessing.resource_tracker import register

from django.urls import path,  register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "conv_year")

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('add_post', views.AddPost.as_view(), name='add_post'),
    path('blogger/<slug:blogger_name>', views.PostsByName.as_view(), name='posts_by_name'),
    path('archive/<conv_year:year>', views.archive, name='archive'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='show_post'),
    path('tag/<slug:tag_slug>', views.PostsByTag.as_view(), name='posts_by_tag'),
]

handler404 = views.page_not_found
