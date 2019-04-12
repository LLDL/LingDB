# Django Imports ----------------------------------------------------------------
from django.forms import ModelForm, DateInput, inlineformset_factory, modelformset_factory, ValidationError, TextInput, RadioSelect, EmailInput, Textarea, CheckboxInput

from django_select2.forms import Select2Widget, Select2MultipleWidget

import datetime
import dateutil.relativedelta as relativedelta

# Project Imports ---------------------------------------------------------------
from .models import *

# Family Forms ------------------------------------------------------------------
class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ('id', 'notes') 
        widgets = {
            'id': TextInput(attrs={'readonly': 'readonly', 'class': 'form-control-plaintext'}),
        }

class ParentForm(ModelForm):
    class Meta:
        model = IsParentIn
        fields = ('parent',)
    # def clean(self):
    #     flag = True
    #     for form in self.forms:
    #         if form.cleaned_data['isPrimary']:
    #             flag = False
    #     if flag:
    #         raise ValidationError('Ensure a primary parent is selected')
    #     else:
    #         return self
        

ParentFormSet = modelformset_factory(
    IsParentIn,
    form = ParentForm,
    can_delete = True
)

ParentInlineFormSet = inlineformset_factory(
    Adult,
    IsParentIn,
    formset = ParentFormSet,
    form = ParentForm,
    fields = ('parent', 'isPrimary'),
    extra = 1,
    max_num = 2,
    min_num = 1,
    validate_min = True,
    widgets = {
        'parent': Select2Widget(),
        'isPrimary': CheckboxInput(attrs={'class': 'primaryContact'})
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

class AddChildForm(ModelForm):
    class Meta:
        model = IsChildIn
        fields = ('family',)
        widgets = {
            'family': Select2Widget(attrs={'required': False})
        }
    def clean_family(self):
        family = self.cleaned_data['family']
        if family:
            children = IsChildIn.objects.filter(family=family)
            if len(children)>9:
                raise ValidationError('This family already has ten children.')
        return self.cleaned_data['family']


class AddParentForm(ModelForm):
    class Meta:
        model = IsParentIn
        fields = ('family',)
        widgets = {
            'family': Select2Widget(attrs={'required': False})
        }
    def clean_family(self):
        family = self.cleaned_data['family']
        if family:
            parents = IsParentIn.objects.filter(family=family)
            if len(parents)>1:
                print('too many parents')
                raise ValidationError('This family already has two parents.')
        return self.cleaned_data['family']


# Adult Forms -------------------------------------------------------------------

class AdultForm(ModelForm):
    class Meta:
        model = Adult
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','personal_notes','health_notes')
        widgets = {
            'id': TextInput(attrs={'readonly': 'readonly'}),
            'birth_date': DateInput(attrs={'type': 'date', 'min': '1900-01-01'}),
            'gender': TextInput(attrs={'list':'auto-genders'}),
            'sfu_id': TextInput(attrs={'min': 100000000, 'max': 999999999, 'type': 'number', }),
            'address': TextInput(attrs={}),
            'years_of_education': TextInput(attrs={'min': 0, 'max': 50, 'type': 'number', }),
            'phone': TextInput(attrs={'type': 'tel'}),
            'email': EmailInput(attrs={}),
            'contact_pref': Select2Widget(attrs={}),
            'pref_phone_time': Select2Widget(attrs={}),   
        }
    def clean_email(self):
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email']
        # contact_pref = self.cleaned_data['contact_pref']
        if phone == None and email == None:
            raise ValidationError('Enter at least one of email or phone')
        # if (contact_pref == 'phone' and phone == None) or (contact_pref == 'email' and email == None):
        #     raise ValidationError('Enter the preferred contact method')
        else:
            return self.cleaned_data['email']

    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        min_birth = datetime.date.today() - relativedelta.relativedelta(years=18)
        if birth_date >= min_birth:
            raise ValidationError('Birthdate must be before or on {} to add this person as an adult'.format(min_birth))
        else:
            return birth_date
    
    def clean_gender(self):
        return self.cleaned_data['gender'].lower()

# Child Forms -------------------------------------------------------------------

class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ('id','given_name','preferred_name','surname','birth_date','gender','gestation_length_weeks','was_full_term','birth_weight','birth_height','personal_notes','hx_repeated_ear_infection','hereditary_audio_problems','hereditary_language_pathologies','health_notes')
        widgets = {
            'id': TextInput(attrs={'readonly': 'readonly'}),
            'birth_date': DateInput(attrs={'type': 'date', 'min': '2000-01-01'}),
            'gestation_length_weeks': TextInput(attrs={'min': 0, 'max': 50, 'type': 'number'}),
            'birth_weight': TextInput(attrs={'min': 0, 'max': 10000, 'type': 'number'}),
            'birth_height': TextInput(attrs={'min': 0, 'max': 100, 'type': 'number'}),
            'gender': TextInput(attrs={'list':'auto-genders'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        max_birth = datetime.date.today() - relativedelta.relativedelta(years=18)
        if birth_date <= max_birth:
            raise ValidationError('Birthdate must be after or on {} to add this person as a child'.format(max_birth))
        else:
            return birth_date
    
    def clean_gender(self):
        return self.cleaned_data['gender'].lower()
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
        fields = ('lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended')

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
    can_delete = True,
)

SpeaksInlineFormSet = inlineformset_factory(
    Adult,
    Speaks,
    fields = ('lang', 'is_native', 'proficiency', 'age_learning_started', 'age_learning_ended'),
    formset = SpeaksFormSet,
    extra = 5,
    max_num = 5,
    min_num = 1,
    validate_min = True,
    widgets = {
        'age_learning_started': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number', 'class': 'age_learning_started'}),
        'is_native': CheckboxInput(attrs={'class': 'centered-checkbox-child position-static isNative'}),
        'age_learning_ended': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number', 'class': 'age_learning_ended'}),
        'proficiency': Select2Widget(),
        'lang': Select2Widget(),
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
        fields = ('experience', 'proficiency', 'age_learning_started', 'age_learning_ended')
    

MusicalExperienceFormSet = modelformset_factory(
    MusicalExperience,
    form = MusicalExperienceForm,
    can_delete = True,
)

MusicalExperienceInlineFormSet = inlineformset_factory(
    Adult,
    MusicalExperience,
    fields = ('experience', 'proficiency', 'age_learning_started', 'age_learning_ended'),
    formset = MusicalExperienceFormSet,
    extra = 5,
    max_num = 5,
    min_num = 0,
    validate_min = True,
    widgets = {
        'age_learning_started': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number', 'class': 'age_learning_started'}),
        'age_learning_ended': TextInput(attrs={'min': 0, 'max': 120, 'type': 'number', 'class': 'age_learning_ended'}),
        'proficiency': Select2Widget(),
        'experience': Select2Widget()
    }
)

# Assessment Forms

class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = ('assessment_name', 'lab',)
        widgets = {
            'lab': Select2Widget()
        }
    
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
    validate_min = True,
    widgets = {
        'type': Select2Widget()
    }
)

# Experiment Forms 
class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ('experiment_name', 'lab', 'status',)
        widgets = {
            'lab': Select2Widget(),
            'status': Select2Widget(),
        }

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
    validate_min = True,
    widgets = {
        'section_status': Select2Widget(),
    }
) 

class ExperimentSectionFieldForm(ModelForm):
    class Meta:
        model = Experiment_Section_Field
        fields = ('field_name', 'type', )
        widgets = {
            'type': Select2Widget(),
        }

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
    validate_min = True,
    widgets = {
        'type': Select2Widget(),
    },
) 


# Assessment Run Forms

class ChooseAssessmentForm(ModelForm):
    class Meta: 
        model = Assessment
        fields = ('assessment_name',)

class AdultAssessmentRunForm(ModelForm):
    class Meta: 
        model = Assessment_Run
        fields = ('participantAdult', 'date', 'notes', 'assessor',)

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'participantAdult': Select2Widget(),
            'assessor': Select2Widget(),
        }
    def clean_participantAdult(self):
        adult = self.cleaned_data['participantAdult']
        if adult == None:
            raise ValidationError("Specify a participant")
        return adult

class ChildAssessmentRunForm(ModelForm):
    class Meta: 
        model = Assessment_Run
        fields = ('participantChild', 'date', 'notes', 'assessor',)

        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'participantChild': Select2Widget(),
            'assessor': Select2Widget(),
        }
    
    def clean_participantChild(self):
        child = self.cleaned_data['participantChild']
        if child == None:
            raise ValidationError("Specify a participant")
        return child
    
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
    form = AssessmentRunFieldScoreForm,
    formset = AssessmentRunFieldScoreFormSet,
    extra = 5,
)
AssessmentRunFieldScoreInlineFormSet = inlineformset_factory(
    Assessment_Run,
    Assessment_Run_Field_Score,
    fields = ('score',),
    form = AssessmentRunFieldScoreForm,
    formset = AssessmentRunFieldScoreFormSet,
    extra = 5,
)

# Experiment Section Run Forms

class ChooseExperimentSectionForm(ModelForm):
    class Meta:
        model = Experiment_Section
        fields = ('experiment_section_name',)

class AdultExperimentSectionRunForm(ModelForm):
    class Meta:
        model = Experiment_Section_Run
        fields = ('participantAdult', 'date', 'notes', 'assessor', )
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'participantAdult': Select2Widget(),
            'assessor': Select2Widget(),
        }
    def clean_participantAdult(self):
        adult = self.cleaned_data['participantAdult']
        if adult == None:
            raise ValidationError("Specify a participant")
        return adult

class ChildExperimentSectionRunForm(ModelForm):
    class Meta:
        model = Experiment_Section_Run
        fields = ('participantChild', 'date', 'notes', 'assessor', )
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'participantChild': Select2Widget(),
            'assessor': Select2Widget(),
        }
    
    def clean_participantChild(self):
        child = self.cleaned_data['participantChild']
        if child == None:
            raise ValidationError("Specify a participant")
        return child


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
