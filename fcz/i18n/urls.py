from django.urls import path

from i18n import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('hello/', views.hello, name='hello'),
]
