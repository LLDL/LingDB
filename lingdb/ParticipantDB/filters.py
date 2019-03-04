from .models import *
import django_filters
from django.forms import CheckboxSelectMultiple,DateInput, SelectMultiple
from django_filters.widgets import RangeWidget

from django_select2.forms import Select2Widget, Select2MultipleWidget

genders = Adult.objects.order_by('gender').distinct('gender').values_list('gender', flat=False)

GENDER_CHOICES = ()


for gender_choice in genders:
    GENDER_CHOICES += (gender_choice[0], gender_choice[0]),


CONTACT_CHOICES = (
    ('P', 'Phone'),
    ('E', 'Email'),
)



class AdultFilter(django_filters.FilterSet):
    given_name = django_filters.CharFilter(lookup_expr='icontains', label="Given Name")
    surname = django_filters.CharFilter(lookup_expr='icontains', label="Surname")
    preferred_name = django_filters.CharFilter(lookup_expr='icontains', label="Preferred Name")
    birth_date = django_filters.DateFromToRangeFilter(label="Birth Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))
    years_of_education = django_filters.RangeFilter(label="Years of Education Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))


    contact_pref = django_filters.MultipleChoiceFilter(choices=CONTACT_CHOICES, widget=CheckboxSelectMultiple(), lookup_expr='icontains', label="Contact Preference")
    gender = django_filters.MultipleChoiceFilter(choices= GENDER_CHOICES,widget=CheckboxSelectMultiple(), lookup_expr='icontains', label="Gender")


    class Meta:
        model = Adult
        # exclude = []
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender', 'birth_date', 'contact_pref', 'years_of_education']

PROFICIENCY_L_CHOICES = (
    ('Native', 'Native'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)

class SpeaksFilter(django_filters.FilterSet):
    lang = django_filters.ModelMultipleChoiceFilter(queryset=Language.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Speaks Any Of", field_name="lang")

    is_native = django_filters.BooleanFilter(label="Native")

    
    proficiency = django_filters.MultipleChoiceFilter(choices=PROFICIENCY_L_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    age_learning_started = django_filters.RangeFilter(label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    age_learning_ended = django_filters.RangeFilter(label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    class Meta:
        model = Speaks
        fields = ['lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended']


PROFICIENCY_M_CHOICES = (
    ('Professional', 'Professional'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)

# class MusicalExperienceFilter(django_filters.FilterSet):
    # experience = django_filters.ModelMultipleChoiceFilter(queryset=MusicalSkill.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Skilled In Any Of", field_name="experience")

    
    # proficiency = django_filters.MultipleChoiceFilter(choices=PROFICIENCY_M_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    # age_learning_started = django_filters.RangeFilter(label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    # age_learning_ended = django_filters.RangeFilter(label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    # no_musical = django_filters.BooleanFilter(field_name='experience', lookup_expr='isnull', label="People without musical skills listed")
    # class Meta:
    #     model = MusicalExperience
    #     fields = ['experience']