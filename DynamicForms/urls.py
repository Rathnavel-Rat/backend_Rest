from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
path("saveform",views.SaveForm.as_view(),name="saveform"),

]
