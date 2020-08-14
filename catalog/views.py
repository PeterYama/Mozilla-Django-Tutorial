from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from catalog.models import Book, BookInstance, Author

# Create your views here.
# Views must return an HttpResponse, with or without template
def IndexView(request):
    return HttpResponse("<h1>Hello</h1>")


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    title = "Library"
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # pack the data from the model as context
    context = {
        "website_title": title,
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(ListView):
    model = Book
    # adding a pagination to allow the listview break data into pages
    paginate_by = 10
    # Default method for generic views
    # Generic views matches name patterns, in this case book_list
    # Therefore there is no need to specify the template path.
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context["some_data"] = "This is just some data"
        return context


class BookDetailView(DetailView):
    model = Book


class AuthorDetailView(ListView):
    model = Author
    # adding a pagination to allow the listview break data into pages
    paginate_by = 10
    # Default method for generic views
    # Generic views matches name patterns, in this case book_list
    # Therefore there is no need to specify the template path.
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context["some_data"] = "This is just some data"
        return context
