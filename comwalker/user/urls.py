from django.urls import path
from . import views

urlpatterns = [
    path('ureg/', views.user_reg, name="ureg"),
    path('ulog/', views.user_log, name="ulog"),
    path('uhome/', views.user_home, name='uhome'),
    path('uinquire/', views.user_inquire, name='uinquire'),
    path('uorder/', views.user_order, name='uorder'),
    path('uabout/', views.user_about, name='uabout'),
    path('updetail/<int:id>/', views.uproduct_detail, name='updetail'),
    path('usdetails/<int:id>/', views.uservice_details, name='usdetails'),
    path('bookingpay/<int:uid>/', views.bookingpay, name="bookingpay"),
    path('search_results/', views.search_results, name='search_results'),
    path('uproduct_detail_from_dataset/<int:id>/', views.uproduct_detail_from_dataset, name='uproduct_detail_from_dataset'),
    
    path('live_search/', views.live_search, name='live_search'),
    path('updetail/<int:id>/', views.uproduct_detail, name='updetail'),
    # Change the path definition here:
    path('user/uprofile/', views.user_profile, name='uprofile'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('community/', views.community_list, name='community_list'),
    path('community/new/', views.create_post, name='create_post'),
    path('all-reviews/<int:product_id>/', views.all_reviews, name='all_reviews'),
]
