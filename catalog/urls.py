from django.urls import path
from . import views

# name is important to define what URL's in templates should look for
urlpatterns = [
    # path('', views.IndexView, name='index'),
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorDetailView.as_view(), name="authors"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path(
        "book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"
    ),
    path("author/create/", views.AuthorCreate.as_view(), name="author_create"),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author_update"),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author_delete"),
    path("book/create/", views.BookCreate.as_view(), name="book_create"),
]

