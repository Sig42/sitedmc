from django.urls import path,  register_converter
from . import views, converters

app_name = 'blog'
register_converter(converters.FourDigitYearConverter, "conv_year")

urlpatterns = [
    path('', views.Start.as_view(), name='start'),
    path('add_post', views.AddPost.as_view(), name='add_post'),
    path('update_post/<int:pk>', views.UpdatePost.as_view(), name='update_post'),
    path('delete_post/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path('blogger/<slug:blogger_name>', views.PostsByName.as_view(), name='posts_by_name'),
    path('archive/<conv_year:year>', views.archive, name='archive'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='show_post'),
    path('tag/<slug:tag_slug>', views.PostsByTag.as_view(), name='posts_by_tag'),
    path('authors', views.AuthorsList.as_view(), name='authors'),
    path('tags', views.TagsList.as_view(), name='tags'),
    path('my_posts', views.MyPosts.as_view(), name='my_posts'),
    # path('get_some/<int:pk>', views.get_some, name='get_some'),
]

handler404 = views.page_not_found
