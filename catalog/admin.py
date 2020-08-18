from django.contrib import admin
from catalog.models import (
    Author,
    Genre,
    Book,
    BookInstance,
    User,
    Role,
    BuyerProfile,
    SellerProfile,
)

# adding a custom fields for the admin page
# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name")


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Define a simple list like view
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")

    # Change the layout of "add new"
    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )


admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
