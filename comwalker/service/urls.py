from django.urls import path
from . import views
urlpatterns =[
    path('',views.index,name="index"),
    path('sreg',views.service_reg,name='sreg'),
    path('slog',views.service_log,name='slog'),
    path('shome',views.service_home,name='shome'),
    path('about',views.about,name='about'),
    path('sprofile',views.service_profile,name='sprofile'),
    path('sabout',views.service_sabout,name="sabout"),
    path('sbooking',views.service_sbooking,name="sbooking"),
    # path('schat',views.service_schat,name="schat"),
    path('service_order_details',views.service_order_details,name="service_order_details"),
    path('padd',views.product_add,name='padd'),
    path('pview',views.product_view,name='pview'),
    path('pdelete/<int:id>/',views.product_delete,name='pdelete'),
    path('pupdate/<int:uid>',views.product_update,name="pupdate"),
    path('pdetail<int:id>',views.pdetail, name='pdetails'),
    path('userbookingapprove/<str:pk>', views.userbookingapprove, name='userbookingapprove'),
]