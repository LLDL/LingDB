from .models import Adult
import django_filters

class AdultFilter(django_filters.FilterSet):
    given_name = django_filters.CharFilter(lookup_expr='icontains', label="Given Name")
    surname = django_filters.CharFilter(lookup_expr='icontains', label="Surname")
    preferred_name = django_filters.CharFilter(lookup_expr='icontains', label="Preferred Name")
    birth_date = django_filters.DateFilter()
    birth_date__gte = django_filters.DateFilter(field_name='birth_date', lookup_expr='gte')
    birth_date__lte = django_filters.DateFilter(field_name='birth_date', lookup_expr='lte')
    gender = django_filters.CharFilter(lookup_expr="iexact", label="Gender")
    class Meta:
        model = Adult
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender', 'birth_date']