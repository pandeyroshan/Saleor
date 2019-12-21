#saleor >> dashboard >> University >> urls

from django.urls import path,include

from . import views

urlpatterns = [
    path("",views.home,name="university-list"),
    path("payment-approval/",views.payment_approval,name="payment_approval"),
    path("add-university/",views.create_view,name="add-university"),
    path("delete-university/<int:pk>/",views.delete_view,name="delete-university"),
    path("edit-university/<int:pk>/",views.edit_view,name="edit-university"),
    path("detail-page/<int:pk>/",views.detail_view,name="detail-page"),
    path("add-consignment/<int:uk>/<int:rk>",views.add_consignment,name="add-consignment"),
    path("delete-consignment/<int:pk>/<int:rk>/",views.delete_consignment,name="delete-consignment"),
    path("edit-consignment/<int:pk>/<int:uk>/<int:rk>",views.edit_consignment,name='edit_consignment'),
    path("my-consignment/",views.my_consignment,name='my_consignment'),
    path("my-consignment/<int:pk>/",views.my_consignment_detail,name='my_consignment_detail'),
    path("add-money/<int:ck>/",views.add_money,name='add-money'),
    path("approve/<int:pk>/",views.toggle,name='toggle'),
    path("cancel/<int:pk>/",views.retoggle,name='cancel'),


    path('add-repr/<int:uk>/', views.add_repr, name='add-repr'),
    path('edit-repr/<int:rk>/<int:uk>',views.edit_repr,name='edit_repr'),
    path('del-repr/<int:rk>/<int:uk>',views.delete_repr,name='del_repr'),
    path('open-repr/<int:rk>/',views.open_repr,name='open_repr')
]