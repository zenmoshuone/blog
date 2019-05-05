from django.urls import path
from blog.views import blog_detail, blog_type, blog_list, blog_date, send, search

urlpatterns = [
    path('', blog_list, name='list'),
    path('<int:id>', blog_detail, name='detail'),
    path('type/<int:type_id>', blog_type, name='type'),
    path('date/<int:year>/<int:month>', blog_date, name='blog_date'),
    path('index/', send, name='send'),



]
