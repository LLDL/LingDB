# Django Imports ----------------------------------------------------------------
from django.forms import ModelForm, DateInput, inlineformset_factory, modelformset_factory, ValidationError, TextInput, RadioSelect

from django_select2.forms import Select2Widget, Select2MultipleWidget


# Project Imports ---------------------------------------------------------------
from .models import *

# Family Forms ------------------------------------------------------------------
class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ('id',) 

class ParentForm(ModelForm):
    class Meta:
        model = IsParentIn
        fields = ('parent',)

ParentFormSet = modelformset_factory(
    IsParentIn,
    form = ParentForm,
    can_delete = True
)

ParentInlineFormSet = inlineformset_factory(
    Adult,
    IsParentIn,
    formset = ParentFormSet,
    fields = ('parent',),
    extra = 1,
    max_num = 2,
    min_num = 1,
    validate_min = True,
    widgets = {
        'parent': Select2Widget()
    }
)

class ChildInFamilyForm(ModelForm):
    class Meta:
        model = IsChildIn
        fields = ('child',)

ChildInFamilyFormSet = modelformset_factory(
    IsChildIn,
    form = ChildInFamilyForm,
    can_delete = True
)

ChildInFamilyInlineFormSet = inlineformset_factory(
    Child,
    IsChildIn,
    formset = ChildInFamilyFormSet,
    fields = ('child',),
    extra = 9,
    max_num = 10,
    min_num = 1,
    validate_min = True,
    widgets = {
        'child': Select2Widget()
    }
)


# Adult Forms -------------------------------------------------------------------

class AdultForm(ModelForm):
    class Meta:
        model = Adult
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','personal_notes','health_notes')
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'pref_phone_time': Select2Widget(),
            'contact_pref': Select2Widget(),
        }

# Child Forms -------------------------------------------------------------------

class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','gestation_length_weeks','was_full_term','birth_weight','birth_height','personal_notes','hx_repeated_ear_infection','hereditary_audio_problems','hereditary_language_pathologies','health_notes')
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'gestation_length_weeks': TextInput(attrs={'min': 0, 'max': 50, 'type': 'number'}),
            'birth_weight': TextInput(attrs={'min': 0, 'max': 10000, 'type': 'number'}),
            'birth_height': TextInput(attrs={'min': 0, 'max': 100, 'type': 'number'}),
        }

# Language Forms ----------------------------------------------------------------

class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ('language_name',)
    def clean(self):
        if Language.objects.filter(language_name=self.cleaned_data['language_name'].capitalize()).count() != 0:
            raise ValidationError('This language already exists.')
    def clean_language_name(self):
        return self.cleaned_data['language_name'].capitalize()
        

class SpeaksForm(ModelForm):
    class Meta:
        model = Speaks
        fields = ('lang', 'is_native', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')
        

class ExposureForm(ModelForm):
    class Meta:
        model = IsExposedTo
        fields = ('lang', 'percentage_exposure')

SpeaksFormSet = modelformset_factory(
    Speaks,
    form = SpeaksForm,
    can_delete = True,
)

ExposureFormSet = modelformset_factory(
    IsExposedTo,
    form = ExposureForm,
    can_delete = True
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
    widgets = {
        'age_learning_started': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number'}),
        'age_learning_ended': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number'}),
        'nth_most_dominant': TextInput(attrs={'min': 1, 'max': 10, 'type': 'number'}),
        'lang': Select2Widget()
    }
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
    widgets = {
        'percentage_exposure': TextInput(attrs={'min': 1, 'max': 100, 'type': 'number'}),
        'lang': Select2Widget()
    }
)

# Musical Forms -----------------------------------------------------------------

class MusicalSkillForm(ModelForm):
    class Meta:
        model = MusicalSkill
        fields = ('skill',)
    def clean(self):
        if MusicalSkill.objects.filter(skill=self.cleaned_data['skill'].capitalize()).count() != 0:
            raise ValidationError('This skill already exists.')
    def clean_skill(self):
        return self.cleaned_data['skill'].capitalize()
        
class MusicalExperienceForm(ModelForm):
    class Meta:
        model = MusicalExperience
        fields = ('experience', 'nth_most_dominant', 'age_learning_started', 'age_learning_ended')

MusicalExperienceFormSet = modelformset_factory(
    MusicalExperience,
    form = MusicalExperienceForm,
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
    widgets = {
        'age_learning_started': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number'}),
        'age_learning_ended': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number'}),
        'nth_most_dominant': TextInput(attrs={'min': 1, 'max': 10, 'type': 'number'}),
        'experience': Select2Widget()
    }
)

# Assessment Forms

class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = ('assessment_name', 'lab',)
    
class AssessmentFieldForm(ModelForm):
    class Meta:
        model = Assessment_Field
        fields = ('field_name', 'type',)

AssessmentFieldFormSet = modelformset_factory(
    Assessment_Field,
    form = AssessmentFieldForm,
    can_delete = True
)

AssessmentFieldInlineFormSet = inlineformset_factory(
    Assessment,
    Assessment_Field,
    fields = ('field_name', 'type'),
    formset = AssessmentFieldFormSet,
    extra = 5,
    max_num = 10,
    min_num = 1,
    validate_min = True
)

# Experiment Forms 
class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ('experiment_name', 'lab', 'status',)

class ExperimentSectionForm(ModelForm):
    class Meta:
        model = Experiment_Section
        fields = ('experiment_section_name', 'section_status',)


ExperimentSectionFormSet = modelformset_factory(
    Experiment_Section,
    form = ExperimentSectionForm,
    can_delete = True
)

ExperimentSectionInlineFormSet = inlineformset_factory(
    Experiment,
    Experiment_Section,
    fields = ('experiment_section_name', 'section_status'),
    formset = ExperimentSectionFormSet,
    extra = 5,
    max_num = 5,
    min_num = 1,
    validate_min = True
) 

class ExperimentSectionFieldForm(ModelForm):
    class Meta:
        model = Experiment_Section_Field
        fields = ('field_name', 'type', )

ExperimentSectionFieldFormSet = modelformset_factory(
    Experiment_Section_Field,
    form = ExperimentSectionFieldForm,
    can_delete = True
)

ExperimentSectionFieldInlineFormSet = inlineformset_factory(
    Experiment_Section,
    Experiment_Section_Field,
    fields = ('field_name', 'type'),
    formset = ExperimentSectionFieldFormSet,
    extra = 5,
    max_num = 10,
    min_num = 1,
    validate_min = True
) 


# Assessment Run Forms

class ChooseAssessmentForm(ModelForm):
    class Meta: 
        model = Assessment
        fields = ('assessment_name',)

class AssessmentRunForm(ModelForm):
    class Meta: 
        model = Assessment_Run
        fields = ('participantAdult', 'participantChild', 'date', 'notes', 'assessor',)
        # fields = ('participantAdult', 'participantChild', 'date', 'notes',)

        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }
    
class AssessmentRunFieldScoreForm(ModelForm):
    class Meta:
        model = Assessment_Run_Field_Score
        fields = ('score',)
        
AssessmentRunFieldScoreFormSet = modelformset_factory(
    Assessment_Run_Field_Score,
    form = AssessmentRunFieldScoreForm,
    can_delete = True
)
AssessmentRunFieldScoreInlineFormSet = inlineformset_factory(
    Assessment_Run,
    Assessment_Run_Field_Score,
    fields = ('score',),
    formset = AssessmentRunFieldScoreFormSet,
    extra = 5,
)

# Experiment Section Run Forms

class ChooseExperimentSectionForm(ModelForm):
    class Meta:
        model = Experiment_Section
        fields = ('experiment_section_name',)

class ExperimentSectionRunForm(ModelForm):
    class Meta:
        model = Experiment_Section_Run
        fields = ('participantAdult', 'participantChild', 'date', 'notes', )
        # fields = ('participantAdult', 'participantChild', 'date', 'notes', 'assessor', )
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }

class ExperimentSectionRunFieldScoreForm(ModelForm):
    class Meta:
        model: Experiment_Section_Run_Field_Score
        fields = ('score',)

ExperimentSectionRunFieldScoreFormSet = modelformset_factory(
    Experiment_Section_Run_Field_Score,
    form = ExperimentSectionRunFieldScoreForm,
    can_delete = True
)

ExperimentSectionRunFieldScoreInlineFormSet = inlineformset_factory(
    Experiment_Section_Run,
    Experiment_Section_Run_Field_Score,
    fields = ('score',),
    formset = ExperimentSectionRunFieldScoreFormSet,
    extra = 5,
)
