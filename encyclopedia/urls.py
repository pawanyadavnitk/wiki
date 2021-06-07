from django.urls import path

from . import views

app_name = "encyclopedia" # for adding namespace
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.display_entry_page, name="display_entry_page")
]
