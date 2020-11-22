
from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("author/<str:first_name>/<str:last_name>", views.author_profile, name="author_profile"),
    path("book/<str:book_title>", views.book_profile, name="book_profile"),
    path("genre/<str:genre_name>", views.genre_profile, name="genre_profile"),

    path("loan/<str:book>", views.new_loan, name="new_loan"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("delete_loan/<int:loan_id>", views.delete_loan, name="delete_loan")
]

