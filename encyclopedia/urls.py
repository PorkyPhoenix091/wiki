from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry,name="entry"),
    path("random", views.entry, name="random"),
    path("newpage", views.entry, name="newpage")
]
