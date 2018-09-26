from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adult/<int:adult_id>/', views.adult_detail, name='adult_detail'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('adult/<int:adult_id>/delete/', views.delete_adult, name='delete_adult'),
    path('child/<int:child_id>/delete/', views.delete_child, name='delete_child'),
    path('adult/add/', views.add_adult, name='add_adult'),  
    path('child/add/', views.add_child, name='add_child'),  
    path('language/add/', views.add_language, name='add_language'),   
    path('musical_skill/add/', views.add_musical_skill, name='add_musical_skill'),   
    path('family/add/', views.add_family, name='add_family'),   
    path('adult/<int:adult_id>/speaks/', views.add_speaks, name='add_speaks'),
    path('adult/<int:adult_id>/musical_experience/', views.add_musical_experience, name='add_musical_experience')
]