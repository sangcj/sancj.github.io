from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # 个人中心
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    # 我的订单
    path('user_center_order/', views.user_center_order, name='user_center_order'),
    # 收货地址
    path('user_center_site/', views.user_center_site, name='user_center_site'),
    # 浏览记录
    # path('user_cookies/', views.user_cookies, name='user_cookies'),
]
