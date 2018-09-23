from .models import Adult, Language, Family, Child, MusicalSkill, Speaks, IsExposedTo, MusicalExperience
# from .models import Adult, Language, Family, Child, Speaks, IsExposedTo
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
        model = MusicalSkill
        fields = ('skill',)

class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ('parents', 'children', )

class SpeaksForm(ModelForm):
    class Meta:
        model = Speaks
        fields = ('lang', 'is_native', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')

class MusicalExperienceForm(ModelForm):
    class Meta:
        model = MusicalExperience
        fields = ('experience', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')

class ExposureForm(ModelForm):
    class Meta:
        model = IsExposedTo
        fields = ('lang', 'percentage_exposure')

SpeaksFormSet = modelformset_factory(
    Speaks,
    form = SpeaksForm
)

MusicalExperienceFormSet = modelformset_factory(
    MusicalExperience,
    form = MusicalExperienceForm,
)

ExposureFormSet = modelformset_factory(
    IsExposedTo,
    form = ExposureForm,
)

SpeaksInlineFormSet = inlineformset_factory(
    Adult,
    Speaks,
    fields = ('lang', 'is_native', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended'),
    formset = SpeaksFormSet,
    extra = 5,
    max_num = 5,
    min_num = 1,
    validate_min = True,

)

ExposureInlineFormSet = inlineformset_factory(
    Child,
    IsExposedTo,
    fields = ('lang', 'percentage_exposure'),
    formset = ExposureFormSet,
    extra = 5,
    max_num = 5,
    min_num = 1,
    validate_min = True,
)

MusicalExperienceInlineFormSet = inlineformset_factory(
    Adult,
    MusicalExperience,
    fields = ('experience', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended'),
    formset = MusicalExperienceFormSet,
    extra = 5,
    max_num = 5,
    min_num = 0,
    validate_min = False,
)