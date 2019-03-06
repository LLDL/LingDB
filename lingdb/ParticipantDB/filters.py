from .models import *

# import rest_framework_filters
# from django_filters.rest_framework import FilterSet, filters
# import rest_framework_filters as filters

import django_filters as filters
from django_filters.widgets import RangeWidget
from django_filters import DateFromToRangeFilter

from django.forms import CheckboxSelectMultiple,DateInput, SelectMultiple
from django_select2.forms import Select2Widget, Select2MultipleWidget


genders = Adult.objects.order_by('gender').distinct('gender').values_list('gender', flat=False)
GENDER_CHOICES = ()
for gender_choice in genders:
    GENDER_CHOICES += (gender_choice[0], gender_choice[0]),


CONTACT_CHOICES = (
    ('P', 'Phone'),
    ('E', 'Email'),
)

PROFICIENCY_L_CHOICES = (
    ('Native', 'Native'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)


class AdultFilter(filters.FilterSet):
    given_name = filters.CharFilter(field_name='given_name', lookup_expr="icontains", label="Given Name")
    surname = filters.CharFilter(field_name='surname', lookup_expr='icontains', label="Surname")
    preferred_name = filters.CharFilter(field_name='preferred_name',lookup_expr='icontains', label="Preferred Name")

    birth_date = filters.DateFromToRangeFilter(label="Birth Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))
    years_of_education = filters.RangeFilter(label="Years of Education Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    contact_pref = filters.MultipleChoiceFilter(choices=CONTACT_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Contact Preference")
    gender = filters.MultipleChoiceFilter(choices= GENDER_CHOICES,widget=Select2MultipleWidget(), lookup_expr='icontains', label="Gender")

    class Meta:
        model = Adult
        # exclude = ['id',]
        fields = ['given_name', 'surname', 'preferred_name', 'birth_date', 'contact_pref', 'gender']



class SpeaksFilter(filters.FilterSet):
    lang = filters.ModelMultipleChoiceFilter(queryset=Language.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Speaks Any Of", field_name="lang")

    is_native = filters.BooleanFilter(label="Native", field_name="is_native")

#     
    age_learning_started = filters.RangeFilter(label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    age_learning_ended = filters.RangeFilter(label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    class Meta:
        model = Speaks
        fields = ['lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended']


# PROFICIENCY_M_CHOICES = (
#     ('Professional', 'Professional'),
#     ('Advanced', 'Advanced'),
#     ('Intermediate', 'Intermediate'),
#     ('Basic','Basic'),
# )

# class MusicalExperienceFilter(filters.FilterSet):
    # experience = df.ModelMultipleChoiceFilter(queryset=MusicalSkill.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Skilled In Any Of", field_name="experience")

    
    # proficiency = df.MultipleChoiceFilter(choices=PROFICIENCY_M_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    # age_learning_started = df.RangeFilter(label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    # age_learning_ended = df.RangeFilter(label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    # no_musical = df.BooleanFilter(field_name='experience', lookup_expr='isnull', label="People without musical skills listed")
    # class Meta:
    #     model = MusicalExperience
    #     fields = ['experience']