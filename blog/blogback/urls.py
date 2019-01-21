
from django.urls import path

from blogback import views

urlpatterns = [
    path('article/', views.article, name='article'),
    path('category/', views.category, name='category'),
    path('add-article/', views.add_article, name='add_article'),
    path('index/', views.index, name='index'),
    path('register/<int:id>', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('update-article/<int:id>', views.update_article, name='update_article'),
    path('delete-article/<int:id>', views.delete_article, name='delete_article'),
]
