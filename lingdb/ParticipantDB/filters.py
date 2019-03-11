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


    health_notes_inc = filters.CharFilter(field_name='health_notes', lookup_expr='icontains', label="Health Notes Include")
    personal_notes_inc = filters.CharFilter(field_name='personal_notes', lookup_expr='icontains', label="Personal Notes Include")

    has_family = filters.BooleanFilter(field_name='parent', lookup_expr='isnull', exclude=True, label="Family In Database")
    class Meta:
        model = Adult
        exclude = ['id', 'address', 'phone', 'email']


class SpeaksFilter(filters.FilterSet):
    lang = filters.ModelMultipleChoiceFilter(queryset=Language.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Speaks Any Of", field_name="lang")

    is_native = filters.BooleanFilter(label="Native", field_name="is_native")

    s_proficiency = filters.MultipleChoiceFilter(field_name="proficiency", choices=PROFICIENCY_L_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    s_age_learning_started = filters.RangeFilter(field_name="age_learning_started", label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    s_age_learning_ended = filters.RangeFilter(field_name="age_learning_ended", label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    class Meta:
        model = Speaks
        fields = ['lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended']


class AssessmentRunFilter(filters.FilterSet):
    assessment = filters.ModelMultipleChoiceFilter(queryset=Assessment.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Participated In Any Of", field_name="assessment")

    assessment_run_date = filters.DateFromToRangeFilter(field_name="date", label="Within the Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    assessment_run_assessor = filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Assessed By Any Of", field_name="assessor")

    assessment_run_notes = filters.CharFilter(field_name='notes', lookup_expr='icontains', label="Notes Include")

    class Meta:
        model = Assessment_Run
        fields = ['assessment', 'date', 'notes', 'assessor']


class ExperimentSectionRunFilter(filters.FilterSet):
    experiment_section = filters.ModelMultipleChoiceFilter(queryset=Experiment_Section.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Participated In Any Of", field_name="experiment_section")

    experiment_section_run_date = filters.DateFromToRangeFilter(field_name="date", label="Within the Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    experiment_section_run_assessor = filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Assessed By Any Of", field_name="assessor")

    experiment_section_run_notes = filters.CharFilter(field_name='notes', lookup_expr='icontains', label="Notes Include")

    class Meta:
        model = Assessment_Run
        fields = ['experiment_section', 'date', 'notes', 'assessor']

PROFICIENCY_M_CHOICES = (
    ('Professional', 'Professional'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)

class MusicalExperienceFilter(filters.FilterSet):
    experience = filters.ModelMultipleChoiceFilter(queryset=MusicalSkill.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Skilled In Any Of", field_name="experience")

    
    m_proficiency = filters.MultipleChoiceFilter(field_name="proficiency", choices=PROFICIENCY_M_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    m_age_learning_started = filters.RangeFilter(field_name="age_learning_started", label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    m_age_learning_ended = filters.RangeFilter(field_name="age_learning_ended", label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    class Meta:
        model = MusicalExperience
        fields = ['experience', 'proficiency', 'age_learning_started', 'age_learning_ended']
