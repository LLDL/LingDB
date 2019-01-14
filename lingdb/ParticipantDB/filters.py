from models import Adult, Child, Family
import django_filters

class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Adult
        fields = ['birth_date', 'gender', 'years_of_education']