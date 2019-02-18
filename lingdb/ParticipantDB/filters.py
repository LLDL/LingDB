from .models import Adult
import django_filters

class AdultFilter(django_filters.FilterSet):
    class Meta:
        model = Adult
        fields = ['given_name', 'surname', 'preferred_name', 'sfu_id', 'gender']