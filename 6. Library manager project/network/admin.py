from django.contrib import admin
from .models import User, Author, Loan, Genre, Books


# Register your models here.
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Loan)
admin.site.register(Genre)
admin.site.register(Books)
