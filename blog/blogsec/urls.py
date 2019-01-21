from django.urls import path

from blogsec import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('share/', views.share, name='share'),
    path('list/', views.my_list, name='list'),
    path('about/', views.about, name='about'),
    path('gbook/', views.gbook, name='gbook'),
    path('info/<int:id>', views.info, name='info'),
    path('infopic/', views.infopic, name='infopic'),
    path('time/', views.time, name='time'),
    path('life/', views.life, name='life'),
]
