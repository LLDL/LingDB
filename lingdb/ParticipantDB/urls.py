from django.urls import path

from . import views
from ParticipantDB.views import AdultCreate

urlpatterns = [
    path('', views.index, name='index'),
    path('adult/<int:adult_id>/', views.adult_detail, name='adult_detail'),
    path('child/<int:child_id>/', views.child_detail, name='child_detail'),
    path('adult/add/',  AdultCreate.as_view(), name='adult_add'),   
]