from django.urls import path

from . import views

app_name = "sparevolumecalculator"
urlpatterns = [
    path("", views.index, name="index"),
    path("results", views.results, name="results"),
    path("documentation", views.documentation, name="documentation")
]