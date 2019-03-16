from django.urls import path

from fcz_plane import views

urlpatterns = [
    # 成都
    path('cd_plane/', views.cd_plane, name='cd_plane'),
    path('search_info/', views.search_info, name='search_info'),
    path('search/', views.search, name='search'),
]
