from django.conf.urls import url
from . import views
app_name='book'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^log_out$', views.log_out, name='log_out'),
    url(r'^add$', views.add_book_page, name='add_book_page'),
    url(r'^add_book$', views.add_book, name='add_book'),
    url(r'^(?P<book_id>\d+)$', views.show_book, name='show_book'),
    url(r'^(?P<book_id>\d+)/add_review$', views.add_review, name='add_review'),
    url(r'^(?P<book_id>\d+)/delete_review/(?P<review_id>\d+)$', views.delete_review, name='delete_review'),
    url(r'^(?P<user_id>\d+)/view_user$', views.view_user, name='view_user'),
]
