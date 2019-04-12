from .models import *
from .utils import get_user_groups

import django_filters as filters
from django_filters.widgets import RangeWidget
from django_filters import DateFromToRangeFilter

from django.forms import CheckboxSelectMultiple,DateInput, SelectMultiple
from django_select2.forms import Select2Widget, Select2MultipleWidget

CONTACT_CHOICES = (
    ('P', 'Phone'),
    ('E', 'Email'),
)

PROFICIENCY_L_CHOICES = (
    ('Native', 'Native Like'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)

PROFICIENCY_M_CHOICES = (
    ('Professional', 'Professional'),
    ('Advanced', 'Advanced'),
    ('Intermediate', 'Intermediate'),
    ('Basic','Basic'),
)


# Adult Filters ------------------------


class AdultFilter(filters.FilterSet):
    given_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='given_name', lookup_expr="icontains", label="Given Name")

    surname = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(), field_name='surname', lookup_expr='icontains', label="Surname")

    preferred_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='preferred_name',lookup_expr='icontains', label="Preferred Name")

    birth_date = filters.DateFromToRangeFilter(label="Birth Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    years_of_education = filters.RangeFilter(label="Years of Education Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    contact_pref = filters.MultipleChoiceFilter(choices=CONTACT_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Contact Preference")

    gender = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(), lookup_expr='icontains', label="Gender")


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

def assessments(request):
        groups = get_user_groups(request)
        if request is None:
            return Assessment.objects.none()

        return Assessment.objects.filter(lab__group__name__in=groups)

def assessors(request):
    if request is None:
        return User.objects.none()
    user = getattr(request, 'user', None)

    valid_users = User.objects.filter(groups__in=user.groups.all()).order_by('id').distinct('id')
    return valid_users

class AssessmentRunFilter(filters.FilterSet):
    assessment = filters.ModelMultipleChoiceFilter(queryset=assessments, widget=Select2MultipleWidget(attrs={}),label="Participated In Any Of", field_name="assessment")

    assessment_run_date = filters.DateFromToRangeFilter(field_name="date", label="Within the Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    assessment_run_assessor = filters.ModelMultipleChoiceFilter(queryset=assessors, widget=Select2MultipleWidget(attrs={}),label="Assessed By Any Of", field_name="assessor")

    assessment_run_notes = filters.CharFilter(field_name='notes', lookup_expr='icontains', label="Notes Include")
   

    class Meta:
        model = Assessment_Run
        fields = ['assessment', 'date', 'notes', 'assessor']
    
    @property
    def qs(self):
        parent = super(AssessmentRunFilter, self).qs
        user = getattr(self.request, 'user', None)
        if(self.request):
            return parent.filter(assessment__lab__group__name__in=user.groups.values_list('name', flat=True))
        else:
            return Assessment_Run.objects.none()

def experiment_sections(request):
        groups = get_user_groups(request)
        if request is None:
            return Experiment_Section.objects.none()

        return Experiment_Section.objects.filter(experiment__lab__group__name__in=groups)

class ExperimentSectionRunFilter(filters.FilterSet):
    experiment_section = filters.ModelMultipleChoiceFilter(queryset=experiment_sections, widget=Select2MultipleWidget(attrs={}),label="Participated In Any Of", field_name="experiment_section")

    experiment_section_run_date = filters.DateFromToRangeFilter(field_name="date", label="Within the Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    experiment_section_run_assessor = filters.ModelMultipleChoiceFilter(queryset=assessors, widget=Select2MultipleWidget(attrs={}),label="Assessed By Any Of", field_name="assessor")

    experiment_section_run_notes = filters.CharFilter(field_name='notes', lookup_expr='icontains', label="Notes Include")

    class Meta:
        model = Experiment_Section_Run
        fields = ['experiment_section', 'date', 'notes', 'assessor']

    @property
    def qs(self):
        parent = super(ExperimentSectionRunFilter, self).qs
        user = getattr(self.request, 'user', None)
        if(self.request):
            return parent.filter(experiment_section__experiment__lab__group__name__in=user.groups.values_list('name', flat=True))
        else:
            return Experiment_Section_Run.objects.none()

class MusicalExperienceFilter(filters.FilterSet):
    experience = filters.ModelMultipleChoiceFilter(queryset=MusicalSkill.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Skilled In Any Of", field_name="experience")
    
    m_proficiency = filters.MultipleChoiceFilter(field_name="proficiency", choices=PROFICIENCY_M_CHOICES, widget=Select2MultipleWidget(), lookup_expr='icontains', label="Proficiency Level")
    m_age_learning_started = filters.RangeFilter(field_name="age_learning_started", label="Age Learning Started Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    m_age_learning_ended = filters.RangeFilter(field_name="age_learning_ended", label="Age Learning Ended Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    class Meta:
        model = MusicalExperience
        fields = ['experience', 'proficiency', 'age_learning_started', 'age_learning_ended']


# Child Filters ------------------------


class ChildFilter(filters.FilterSet):
    given_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='given_name', lookup_expr="icontains", label="Given Name")

    surname = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(), field_name='surname', lookup_expr='icontains', label="Surname")

    preferred_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='preferred_name',lookup_expr='icontains', label="Preferred Name")

    gender = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(), lookup_expr='icontains', label="Gender")

    health_notes_inc = filters.CharFilter(field_name='health_notes', lookup_expr='icontains', label="Health Notes Include")

    personal_notes_inc = filters.CharFilter(field_name='personal_notes', lookup_expr='icontains', label="Personal Notes Include")

    has_family = filters.BooleanFilter(field_name='childin', lookup_expr='isnull', exclude=True, label="Family In Database")

    was_full_term = filters.BooleanFilter(label="Was Full Term", field_name="was_full_term")

    hereditary_audio_problems = filters.BooleanFilter(label="Hereditary Audio Problems", field_name="hereditary_audio_problems")

    hereditary_language_pathologies = filters.BooleanFilter(label="Hereditary Language Pathologies", field_name="hereditary_language_pathologies")

    birth_date = filters.DateFromToRangeFilter(label="Birth Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    birth_weight = filters.RangeFilter(label="Birth Weight Range (Grams)", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    birth_height = filters.RangeFilter(label="Birth Height Range (CM)", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    gestation_length_weeks = filters.RangeFilter(label="Gestation Length Range (Weeks)", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))
    #hx ear inf

    hx_repeated_ear_infection = filters.CharFilter(field_name='hx_repeated_ear_infection', lookup_expr='icontains', label="HX Repeated Ear Infection Includes")
    class Meta:
        model = Child
        exclude = ['id']

class ExposureFilter(filters.FilterSet):
    lang = filters.ModelMultipleChoiceFilter(queryset=Language.objects.all(), widget=Select2MultipleWidget(attrs={}),label="Exposed To Any Of", field_name="lang")

    percentage_exposure = filters.RangeFilter(field_name="percentage_exposure", label="Percentage Exposure Range", widget=RangeWidget(attrs={'type': 'number', 'class': 'form-control mb-2'}))

    class Meta:
        model = IsExposedTo
        fields = ['lang', 'percentage_exposure']

# Family

class FamilyFilter(filters.FilterSet):

    parent_given_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='a_family__parent__given_name', lookup_expr='icontains', label="Parental Given Name")
    child_given_name = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='c_family__child__given_name', lookup_expr='icontains', label="Child Given Name")

    parent_surname = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='a_family__parent__surname', lookup_expr='icontains', label="Parental Surname")
    child_surname = filters.AllValuesMultipleFilter(widget=Select2MultipleWidget(),field_name='c_family__child__surname', lookup_expr='icontains', label="Child Surname")

    notes_inc = filters.CharFilter(field_name='notes', lookup_expr='icontains', label="Notes Include")


    class Meta:
        model = Family
        exclude = ['a_family__parent__surname', 'c_family__child__surname', 'a_family__parent__given_name', 'c_family__child__given_name', 'notes']