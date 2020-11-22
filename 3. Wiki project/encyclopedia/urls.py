from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki", views.entry2, name="entry2"),
    path("random", views.random_page, name="random_page"),
    path("create", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit, name="edit")

]
