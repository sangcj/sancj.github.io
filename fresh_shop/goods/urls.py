from django.urls import path

from goods import views

urlpatterns = [
    # 首页
    path('index/', views.index, name='index'),
    # 详情
    path('detail/<int:id>/', views.detail, name='detail'),
    # 商品列表
    path('goods_list/<int:id>/', views.goods_list, name='goods_list'),
    # 查询商品
    path('search/', views.search, name='search'),
]
