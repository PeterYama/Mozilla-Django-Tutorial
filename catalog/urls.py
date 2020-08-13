from django.urls import path
from . import views
# name is important to define what URL's in templates should look for
urlpatterns = [
    # path('', views.IndexView, name='index'),
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(), name="books"),
    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail')
    # path('catalog/', HttpResponse("<h1>Welcome to my website</h1>"), name="HttpResponse")
] 