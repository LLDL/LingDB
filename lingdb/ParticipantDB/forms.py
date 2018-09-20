from .models import Adult, Language, Family, Child, Musical_Skill, Speaks, IsExposedTo, Musical_Experience
from django.forms import *


class AdultForm(ModelForm):
    class Meta:
        model = Adult
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','health_notes')
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
        }

class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','gestation_length_weeks','was_full_term','birth_weight','birth_height','personal_notes','hx_repeated_ear_infection','last_ear_infection','hereditary_audio_problems','hereditary_language_pathologies','health_notes','exposed_to')
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'})
        }

class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ('language_name',)

class MusicalSkillForm(ModelForm):
    class Meta:
        model = Musical_Skill
        fields = ('skill',)

class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ('parents', 'children', )

class SpeaksForm(ModelForm):
    class Meta:
        model = Speaks
        fields = ('language', 'is_native', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')

class MusicalExperienceForm(ModelForm):
    class Meta:
        model = Musical_Experience
        fields = ('experience', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')

class ExposureForm(ModelForm):
    class Meta:
        model = IsExposedTo
        fields = ('language', 'percentage_exposure')

SpeaksFormSet = modelformset_factory(
    Speaks,
    form = SpeaksForm,
    extra = 0
)

MusicalExperienceFormSet = modelformset_factory(
    Musical_Experience,
    form = MusicalExperienceForm,
    extra = 0
)

ExposureFormSet = modelformset_factory(
    IsExposedTo,
    form = ExposureForm,
    extra = 0
)

SpeaksInlineFormSet = inlineformset_factory(
    Adult,
    Speaks,
    extra = 4,
    fields = ('language', 'is_native', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended'),
    formset = SpeaksFormSet,
    min_num = 1,
)

ExposureInlineFormSet = inlineformset_factory(
    Child,
    IsExposedTo,
    extra = 4,
    fields = ('language', 'percentage_exposure'),
    formset = ExposureFormSet,
    min_num = 1,
)

MusicalExperienceInlineFormSet = inlineformset_factory(
    Adult,
    Musical_Experience,
    extra = 4,
    fields = ('experience', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended'),
    formset = MusicalExperienceFormSet,
    min_num = 0,
)