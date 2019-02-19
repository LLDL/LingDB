from .models import Adult, Speaks, Language
import django_filters
from django.forms import CheckboxSelectMultiple,DateInput
from django_filters.widgets import RangeWidget

genders = Adult.objects.order_by('gender').distinct('gender').values_list('gender', flat=False)

GENDER_CHOICES = ()


for gender_choice in genders:
    GENDER_CHOICES += (gender_choice[0], gender_choice[0].capitalize()),

CONTACT_CHOICES = (
    ('P', 'Phone'),
    ('E', 'Email'),
)

class AdultFilter(django_filters.FilterSet):
    given_name = django_filters.CharFilter(lookup_expr='icontains', label="Given Name")
    surname = django_filters.CharFilter(lookup_expr='icontains', label="Surname")
    preferred_name = django_filters.CharFilter(lookup_expr='icontains', label="Preferred Name")
    birth_date = django_filters.DateFromToRangeFilter(label="Birth Date Range", widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control mb-2'}))

    contact_pref = django_filters.MultipleChoiceFilter(choices=CONTACT_CHOICES, widget=CheckboxSelectMultiple(), lookup_expr='icontains', label="Contact Preference")
    gender = django_filters.MultipleChoiceFilter(choices= GENDER_CHOICES,widget=CheckboxSelectMultiple(), lookup_expr='icontains', label="Gender")
    class Meta:
        model = Adult
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender', 'birth_date', 'contact_pref']


# languages = Language.objects.all()

# LANG_CHOICES = ()


# for lang_choice in languages:
#     LANG_CHOICES += (lang_choice.language_name, lang_choice.language_name.capitalize()),




# class SpeaksFilter(django_filters.FilterSet):
#     lang = django_filters.MultipleChoiceFilter(choices=LANG_CHOICES, widget=CheckboxSelectMultiple(), lookup_expr='icontains', label="Language")
#     class Meta:
#         model = Speaks
#         fields = ['lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended']