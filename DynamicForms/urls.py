from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("saveform", views.SaveForm.as_view(), name="saveform"),
    path("getStoredForms", views.GetStoredForms.as_view(), name="getFormsDetails"),
    path("addNewForm", views.NewForm.as_view(), name="newForm"),
    path("updateName", views.UpdateName.as_view(), name="updateForm"),
    path("GetBinaryFormData", views.BinaryFormData.as_view(), name="getBinaryFormData"),
    path("AccessForm",views.AccessForm.as_view(),name="AccessForm"),
    path("DeleteForm",views.DeleteForm.as_view(),name="DeleteForm"),

]
