from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
path("saveform",views.saveform.as_view(),name="saveform")

]
