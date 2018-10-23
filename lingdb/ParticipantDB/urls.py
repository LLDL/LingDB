from django.urls import path

from . import views

urlpatterns = [
    # index
    path('', views.index, name='index'),

    # family
    path('family/add/', views.add_family, name='add_family'),   
    path('family/<int:family_id>/', views.family_detail, name='family_detail'),
    path('family/<int:family_id>/update/', views.update_family, name='update_family'),
    path('family/<int:family_id>/delete/', views.delete_family, name='delete_family'),

    # adult
    path('adult/add/', views.add_adult, name='add_adult'),  
    path('adult/<int:adult_id>/', views.adult_detail, name='adult_detail'),
    path('adult/<int:adult_id>/update/', views.update_adult, name='update_adult'),
    path('adult/<int:adult_id>/delete/', views.delete_adult, name='delete_adult'),

    # child
    path('child/add/', views.add_child, name='add_child'),  
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('child/<int:child_id>/update/', views.update_child, name='update_child'),
    path('child/<int:child_id>/delete/', views.delete_child, name='delete_child'),
    
    # languages
    path('language/add/', views.add_language, name='add_language'),   
    path('adult/<int:adult_id>/speaks/', views.add_speaks, name='add_speaks'),

    # music
    path('musical_skill/add/', views.add_musical_skill, name='add_musical_skill'),   
    path('adult/<int:adult_id>/musical_experience/', views.add_musical_experience, name='add_musical_experience'),

    # assessments
    path('assessment/add', views.add_assessment, name='add_assessment'),
    path('adult/<int:assessment_name>/field/', views.add_assessment_flex_field, name='add_assessment_flex_field'),
    # path('assessments/<int:assessment_name', views.assessment_detail, name='assessment_detail'),
    # path('assessments/<int:assessment_name/update/', views.update_assessment, name='update_assessment'),
    # path('assessments/<int:assessment_name/delete/', views.delete_assessment, name='delete_assessment'),

]

    