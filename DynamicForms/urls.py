from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("saveform", views.SaveForm.as_view(), name="saveform"),
    path("getStoredForms", views.GetStoredForms.as_view(), name="getFormsDetails"),
    path("addNewForm", views.NewForm.as_view(), name="newForm"),
    path("updateName", views.UpdateName.as_view(), name="updateForm"),
    path("GetBinaryFormData", views.BinaryFormData.as_view(), name="getBinaryFormData"),
    path("AccessForm", views.AccessForm.as_view(), name="AccessForm"),
    path("DeleteForm", views.DeleteForm.as_view(), name="DeleteForm"),
    path("SubmitResponse", views.SaveResponses.as_view(), name="SubmitResponses"),
    path("GetResponse",views.GetResponses.as_view(),name="GetFormResponses"),
    path("saveFile",views.FileSave.as_view(),name="saveFile"),
    path("MakeFormVisible",views.MakeFormVisible.as_view(),name="MakeFormVisible"),

]
