from .models import Adult
from django.forms import ModelForm

class AdultForm(ModelForm):
    class Meta:
        model = Adult
        fields = ['id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','health_notes','languages','musical_background']

