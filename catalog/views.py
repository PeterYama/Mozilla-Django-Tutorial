from django.shortcuts import render, get_object_or_404
from django.apps import apps
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from catalog.models import Book, BookInstance, Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import viewsets
from locallibrary.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data["due_back"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {"due_back": ("New renewal date")}
        help_texts = {"due_back": ("Enter a date between now and 4 weeks (default 3).")}


# Create a form that CRUD from a specific model
# Templates should be named following the standard ModelName_From.html
class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("book")


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {"date_of_death": "05/01/2018"}
    success_url = reverse_lazy("authors")


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("authors")


@csrf_protect
@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("index"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        # ugettext_lazy() is imported as _()
        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        # Remember to always return the cleaned data.
        return data


# Class based components use PermissionRequiredMixin from django.contrib.auth.mixins to grant/denie accesss to certain views
# Use @login_required decorator for function based views
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        # Queries are defined in the view
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


# Create your views here.
# Views must return an HttpResponse, with or without template
def IndexView(request):
    return HttpResponse("<h1>Hello</h1>")


@login_required
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
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    # pack the data from the model as context
    context = {
        "website_title": title,
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
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
