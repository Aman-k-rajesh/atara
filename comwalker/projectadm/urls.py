from django.urls import path
from . import views 

urlpatterns = [
    path('alog/', views.adm_log, name='alog'),
    # path('ahome/', views.adm_home, name='ahome'),
    path('aindex/', views.aindex, name="aindex"),
    path('shopdetails/', views.shopdetails, name="shopdetails"),
    path('services/', views.services, name="services"),
    path('userdetails/', views.userdetails, name="userdetails"),
    path('bookingdetails/', views.bookingdetails, name="bookingdetails"),
    path('datasetbookingdetails/', views.datasetbookingdetails, name="datasetbookingdetails"),
    path('feedbacks/', views.feedbacks, name="feedbacks"),
    path('astock/', views.stock, name="astock"),
    path('delete/<int:id>/', views.adm_delete, name='delete'),
    path('adelete/<int:id>/', views.ad_delete, name='adelete'),
    path('shopapprove/<int:pk>/', views.shopapprove, name='shopapprove'),
    path('bookingapprove/<int:pk>/', views.bookingapprove, name='bookingapprove'),
    path('create_admin_post/', views.create_admin_post, name='create_admin_post'),
    path('admin_post_list', views.admin_post_list, name='admin_post_list'),
]
