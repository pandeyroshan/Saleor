#saleor >> dashboard >> University >> urls

from django.urls import path,include

from . import views

urlpatterns = [
    path("",views.home,name="university-list"),
    path("add-university/",views.create_view,name="add-university"),
    path("delete-university/<int:pk>/",views.delete_view,name="delete-university"),
    path("edit-university/<int:pk>/",views.edit_view,name="edit-university"),
]