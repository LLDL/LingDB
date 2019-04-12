from django.urls import path

from . import views

urlpatterns = [
    # search
    path('search/', views.search, name='search'),
    # index
    path('', views.index, name='index'),
    # family
    path('family/add/', views.add_family, name='add_family'),   
    path('family/<int:family_id>/', views.family_detail, name='family_detail'),
    path('family/<int:family_id>/update/', views.update_family, name='update_family'),
    path('family/<int:family_id>/delete/', views.delete_family, name='delete_family'),
    path('family/', views.family_query, name='family_query'),
    # adult
    path('adult/add/', views.add_adult, name='add_adult'),  
    path('adult/<int:adult_id>/', views.adult_detail, name='adult_detail'),
    path('adult/<int:adult_id>/update/', views.update_adult, name='update_adult'),
    path('adult/<int:adult_id>/delete/', views.delete_adult, name='delete_adult'),
    path('adult/', views.adult_query, name='adult_query'),

    # child
    path('child/add/', views.add_child, name='add_child'),  
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('child/<int:child_id>/update/', views.update_child, name='update_child'),
    path('child/<int:child_id>/delete/', views.delete_child, name='delete_child'),
    path('child/', views.child_query, name='child_query'),
    
    # languages
    path('language/add/', views.add_language, name='add_language'),   

    # music
    path('musical_skill/add/', views.add_musical_skill, name='add_musical_skill'),   

    # assessments

    ## add assessment
    path('assessment/', views.assessment_list, name='assessment_list'),
    path('assessment/add/', views.add_assessment, name='add_assessment'),
    ## view assessment
    path('assessment/<str:assessment_name>/', views.assessment_detail, name='assessment_detail'),
    ## update assessment
    path('assessment/<str:assessment_name>/update/', views.update_assessment, name='update_assessment'),
    ## delete assessment
    path('assessment/<str:assessment_name>/delete/', views.delete_assessment, name='delete_assessment'),
    ## choose assessment to run
    path('assessment_run/add/', views.choose_assessment, name='choose_assessment'),
    ## add assessment run w/ preselected person
    path('assessment_run/add/<str:assessment_name>/<str:participant_type>/<int:participant>', views.add_assessment_run, name='add_assessment_run'),
    ## add assessment run
    path('assessment_run/add/<str:assessment_name>/<str:participant_type>/', views.add_assessment_run, name='add_assessment_run'),
    ## view assessment run detail
    path('assessment_run/<int:assessment_run_id>/', views.assessment_run_detail, name='assessment_run_detail'),
    ## delete assessment run
    path('assessment_run/<str:assessment_run_id>/delete/', views.delete_assessment_run, name='delete_assessment_run'),
    ## update assessment run
    path('assessment_run/<str:assessment_run_id>/update/', views.update_assessment_run, name='update_assessment_run'),

    # experiments
    path('experiment/', views.experiment_list, name='experiment_list'),
    path('experiment/add/', views.add_experiment, name='add_experiment'),
    path('experiment/<str:experiment_name>/', views.experiment_detail, name='experiment_detail'),
    path('experiment/<str:experiment_name>/sections/add/', views.add_experiment_section_fields, name='add_experiment_section_fields'),
    path('experiment/<str:experiment_name>/sections/update/', views.update_experiment_section_fields, name='update_experiment_section_fields'),

    path('experiment/<str:experiment_name>/update/', views.update_experiment, name='update_experiment'),
    path('experiment/<str:experiment_name>/delete/', views.delete_experiment, name='delete_experiment'),


    path('experiment/<str:experiment_name>/experiment_section/<str:experiment_section_name>/', views.experiment_section_detail, name='experiment_section_detail'),
    # path('experiment/<str:experiment_name>/experiment_section/<str:experiment_section_name>/update/', views.update_experiment_section, name='update_experiment_section'),
    path('experiment/<str:experiment_name>/experiment_section/<str:experiment_section_name>/delete/', views.delete_experiment_section, name='delete_experiment_section'),


    path('experiment_section_run/add/', views.choose_experiment_section, name='choose_experiment_section'),
    path('experiment_section_run/add/<str:experiment_name>/<str:experiment_section_name>/<str:participant_type>/<int:participant>', views.add_experiment_section_run, name='add_experiment_section_run'),
    path('experiment_section_run/add/<str:experiment_name>/<str:experiment_section_name>/<str:participant_type>/', views.add_experiment_section_run, name='add_experiment_section_run'),
    path('experiment_section_run/<int:experiment_section_run_id>/', views.experiment_section_run_detail, name='experiment_section_run_detail'),

    path('experiment_section_run/<int:experiment_section_run_id>/delete/', views.delete_experiment_section_run, name='delete_experiment_section_run'),
    path('experiment_section_run/<int:experiment_section_run_id>/update/', views.update_experiment_section_run, name='update_experiment_section_run'),
]

    