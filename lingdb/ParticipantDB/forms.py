from .models import Adult, Language, Musical_Skill
from django.forms import *

class AdultForm(ModelForm):
    class Meta:
        model = Adult
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','health_notes','languages','musical_background')
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
        }

class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ('language_name',)

class Musical_Skill_Form(ModelForm):
    class Meta:
        model = Musical_Skill
        fields = ('skill',)