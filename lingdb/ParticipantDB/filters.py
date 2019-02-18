from .models import Adult
import django_filters
from django.forms import CheckboxSelectMultiple,DateInput
from django_filters.widgets import RangeWidget

GENDERS = Adult.objects.order_by('gender').distinct('gender').values_list('gender', flat=False)
print(GENDERS)

GENDER_CHOICES = ()

for gender_CHOICE in GENDERS:
    GENDER_CHOICES += (gender_CHOICE[0], gender_CHOICE[0].capitalize()),
print(GENDER_CHOICES)
class AdultFilter(django_filters.FilterSet):
    given_name = django_filters.CharFilter(lookup_expr='icontains', label="Given Name")
    surname = django_filters.CharFilter(lookup_expr='icontains', label="Surname")
    preferred_name = django_filters.CharFilter(lookup_expr='icontains', label="Preferred Name")
    # birth_date = django_filters.DateFilter(label='Birth Date', lookup_expr="icontains", widget=DateInput(attrs={'type': 'date'}))
    # birth_date__gt = django_filters.DateFilter(label="Birth Date After", lookup_type='gt', widget=DateInput(attrs={'type': 'date'}))

    # start_birth_date = django_filters.DateFilter(field_name='birth_date', lookup_expr=('gt'),)
    # end_birth_date = django_filters.DateFilter(field_name='birth_date', lookup_expr=('lt'),)
    birth_date = django_filters.DateFromToRangeFilter(label="Birth Date Within", widget=RangeWidget(attrs={'type': 'date'}))
    # birth_date__lt = django_filters.DateFilter(label="Birth Date Before",lookup_expr='birth_date__lt', widget=DateInput(attrs={'type': 'date'}))

    gender = django_filters.MultipleChoiceFilter(choices= GENDER_CHOICES,widget=CheckboxSelectMultiple, lookup_expr='icontains', label="Gender")
    class Meta:
        model = Adult
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender', 'birth_date']