from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.user_app.urls', namespace='user')),
    url(r'^books/', include('apps.book_app.urls', namespace='book')),
]
