from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="view-entry"),
    path("search", views.search, name="search"),
    path("new-entry", views.write_entry, name="new-entry"),
    path("edit-entry/<str:title>", views.edit_entry, name="edit-entry"),
    path("rand-entry/", views.get_random_entry, name="rand-entry")
]
