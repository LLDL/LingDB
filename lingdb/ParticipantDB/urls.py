from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adult/<int:adult_id>/', views.adult_detail, name='adult_detail'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('adult/add/', views.add_adult, name='add_adult'),   
]