from .models import Adult
import django_filters
from django.forms import CheckboxSelectMultiple

GENDERS = Adult.objects.order_by('gender').distinct('gender').values_list('gender', flat=False)
print(GENDERS)

GENDER_CHOICES = ()

for gender_CHOICE in GENDERS:
    GENDER_CHOICES += (gender_CHOICE[0], gender_CHOICE[0]),
print(GENDER_CHOICES)
class AdultFilter(django_filters.FilterSet):
    given_name = django_filters.CharFilter(lookup_expr='icontains', label="Given Name")
    surname = django_filters.CharFilter(lookup_expr='icontains', label="Surname")
    preferred_name = django_filters.CharFilter(lookup_expr='icontains', label="Preferred Name")
    # birth_date = django_filters.DateFromToRangeFilter()
    # birth_date__gte = django_filters.DateFilter(field_name='birth_date', lookup_expr='gte')
    # birth_date__lte = django_filters.DateFilter(field_name='birth_date', lookup_expr='lte')
    gender = django_filters.MultipleChoiceFilter(choices= GENDER_CHOICES,widget=CheckboxSelectMultiple)
    class Meta:
        model = Adult
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender', 'birth_date']