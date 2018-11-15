# Django Imports ----------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from itertools import chain
# Project Imports ---------------------------------------------------------------
from .forms import *
from .models import *
from .utils import make_unique_id, get_user_groups

# Index Views -------------------------------------------------------------------

@login_required
def index(request):
    if (request.method == 'GET') and (request.GET.get('searchPeopleField', None)):
        # Open by ID Handling
        person = request.GET.get('searchPeopleField', None)
        # If adult exists, open that adult's details
        try:
            Adult.objects.get(pk=person)
            return redirect(reverse('adult_detail', kwargs={'adult_id': person}))
        # Adult doesn't exist, try with child
        except Adult.DoesNotExist:
            try: 
                Child.objects.get(pk=person)
                return redirect(reverse('child_detail', kwargs={'child_id': person}))
            #Child doesn't exist, try with family
            except Child.DoesNotExist:
                try:
                    Family.objects.get(pk=person)
                    return redirect(reverse('family_detail', kwargs={'family_id': person}))
                #Family doesn't exist, invalid pk
                except Family.DoesNotExist:
                    raise Http404("No Adult, Child, or Family matches ID#" + person)
    else:
        # Standard Visit to Index
        return render(request, 'ParticipantDB/index.html')

# Family Views -----------------------------------------------------------------

@login_required
def add_family(request):
    child_forms = ChildInFamilyInlineFormSet(
        queryset = IsChildIn.objects.none(),
        prefix = 'children'
    )
    parent_forms = ParentInlineFormSet(
        queryset = IsParentIn.objects.none(),
        prefix = 'parents'
    )
    if request.method == "POST":
        family_form = FamilyForm(request.POST)
        child_forms = ChildInFamilyInlineFormSet(request.POST, prefix='children')
        parent_forms = ParentInlineFormSet(request.POST, prefix='parents')
        if family_form.is_valid() and child_forms.is_valid() and parent_forms.is_valid():
            family = family_form.save(commit=False)
            family.save()
            
            for parent_form in parent_forms:
                if parent_form.cleaned_data.get('parent'):
                    inst = parent_form.save(commit=False)
                    inst.family = family
                    inst.save()
            
            for child_form in child_forms:
                if child_form.cleaned_data.get('child'):
                    inst = child_form.save(commit=False)
                    inst.family = family
                    inst.save()

            return redirect(reverse('family_detail', kwargs={'family_id': family.id}))

    else:
        family_form = FamilyForm(initial={'id': make_unique_id()})

    return render(request, "ParticipantDB/family_form.html", {'family_form': family_form, 'child_forms': child_forms, 'parent_forms': parent_forms})

@login_required
def family_detail(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    parents = IsParentIn.objects.filter(family = family)
    children = IsChildIn.objects.filter(family = family)
    return render(request, 'ParticipantDB/family_detail.html', {'family': family, 'parents': parents, 'children': children})

@login_required
def delete_family(request, family_id):
    try:
        Family.objects.get(pk=family_id).delete()
        return redirect(reverse('index'))
    except Family.DoesNotExist:
        raise Http404("No family with id" + family_id)
    
@login_required
def update_family(request, family_id):
    try:
        family_inst = Family.objects.get(pk=family_id)
    except Family.DoesNotExist:
        Http404("No Family with id " + family_id)

    child_forms = ChildInFamilyInlineFormSet(
        queryset = IsChildIn.objects.filter(family=family_inst),
        prefix = 'children'
    )
    parent_forms = ParentInlineFormSet(
        queryset = IsParentIn.objects.filter(family=family_inst),
        prefix = 'parents'
    )
    if request.method == "POST":
        family_form = FamilyForm(request.POST, instance = family_inst)
        child_forms = ChildInFamilyInlineFormSet(request.POST, request.FILES, prefix='children')
        parent_forms = ParentInlineFormSet(request.POST, request.FILES, prefix='parents')
        
        if family_form.is_valid() and parent_forms.is_valid() and child_forms.is_valid():
            family = family_form.save(commit=False)
            family.save()

            for parent_form in parent_forms:                    
                if parent_form.cleaned_data.get('DELETE'):
                    toDelete = parent_form.cleaned_data.get('parent')
                    print(toDelete)
                    IsParentIn.objects.filter(parent=toDelete, family=family_inst).delete()
                elif parent_form.cleaned_data.get('parent'):
                    inst = parent_form.save(commit=False)
                    inst.family = family
                    inst.save()
            
            for child_form in child_forms:
                if child_form.cleaned_data.get('DELETE'):
                    toDelete = child_form.cleaned_data.get('child')
                    print(toDelete)
                    IsChildIn.objects.filter(child=toDelete, family=family_inst).delete()
                elif child_form.cleaned_data.get('child'):
                    inst = child_form.save(commit=False)
                    inst.family = family
                    inst.save()

            return redirect(reverse('family_detail', kwargs={'family_id': family.id}))

    else:
        family_form = FamilyForm(instance = family_inst)

    return render(request, "ParticipantDB/family_form_update.html", {'family_id': family_id, 'family_form': family_form, 'child_forms': child_forms, 'parent_forms': parent_forms})

# Adult Views ------------------------------------------------------------------

@login_required
def add_adult(request):
    musical_experience_forms = MusicalExperienceInlineFormSet(
        queryset = MusicalExperience.objects.none(), 
        prefix = 'musical_experiences'
    )
    speaks_forms = SpeaksInlineFormSet(
        queryset = Speaks.objects.none(), 
        prefix = 'speaks_forms'
    )
    if request.method == "POST":
        adult_form = AdultForm(request.POST)
        speaks_forms = SpeaksInlineFormSet(request.POST, prefix = 'speaks_forms')
        musical_experience_forms = MusicalExperienceInlineFormSet(request.POST, prefix = 'musical_experiences')
        
        if adult_form.is_valid() and speaks_forms.is_valid() and musical_experience_forms.is_valid():   
            adult = adult_form.save(commit=False)
            adult.save()
            
            for speaks_form in speaks_forms:
                if speaks_form.is_valid() and speaks_form.cleaned_data.get('lang'):
                    inst = speaks_form.save(commit=False)
                    inst.person = adult
                    inst.save()

            for musical_experience_form in musical_experience_forms:
                if musical_experience_form.is_valid() and musical_experience_form.cleaned_data.get('experience'):
                    inst = musical_experience_form.save(commit=False)
                    inst.person = adult
                    inst.save()

            return redirect(reverse('adult_detail', kwargs={'adult_id': adult.id}))
        
    else:
        adult_form = AdultForm(initial={'id': make_unique_id()})

    return render(request, "ParticipantDB/adult_form.html", {'adult_form': adult_form, 'speaks_formset': speaks_forms, 'musical_experience_formset': musical_experience_forms})


@login_required
def update_adult(request, adult_id):
    try:
        adult_inst = Adult.objects.get(pk=adult_id)
    except Adult.DoesNotExist:
        Http404("No Adult with id " + adult_id)

    speaks_forms = SpeaksInlineFormSet(
        prefix = 'speaks_forms',
        queryset = Speaks.objects.filter(person=adult_inst),
    )
    
    musical_experience_forms = MusicalExperienceInlineFormSet(
        prefix = 'musical_experiences',
        queryset = MusicalExperience.objects.filter(person=adult_inst),
    )
   
    if request.method == "POST":
        adult_form = AdultForm(request.POST, request.FILES, instance=adult_inst)
        
        speaks_forms = SpeaksInlineFormSet(request.POST, request.FILES, prefix = 'speaks_forms')
        musical_experience_forms = MusicalExperienceInlineFormSet(request.POST, request.FILES, prefix = 'musical_experiences')
        
        if adult_form.is_valid():   
            adult = adult_form.save(commit=False)
            adult.save()
            if speaks_forms.is_valid():
                for speaks_form in speaks_forms:
                    if speaks_form.cleaned_data.get('DELETE'):
                        toDelete = speaks_form.cleaned_data.get('lang')
                        Speaks.objects.filter(person=adult_inst, lang=toDelete).delete()
                        # delete
                    elif speaks_form.cleaned_data.get('lang'):
                        inst = speaks_form.save(commit=False)
                        inst.person = adult
                        inst.save()
                    
            if musical_experience_forms.is_valid():  
                for musical_experience_form in musical_experience_forms:
                    if musical_experience_form.cleaned_data.get('DELETE'):
                        toDelete = musical_experience_form.cleaned_data.get('experience')
                        MusicalExperience.objects.filter(person=adult_inst, experience=toDelete).delete()
                    elif musical_experience_form.cleaned_data.get('experience'):
                        inst = musical_experience_form.save(commit=False)
                        inst.person = adult
                        inst.save()
            
            return redirect(reverse('adult_detail', kwargs={'adult_id': adult_id}))
        

    else:
        adult_form = AdultForm(instance = adult_inst)

    return render(request, "ParticipantDB/adult_form_update.html", {'adult_id': adult_id, 'adult_form': adult_form, 'speaks_formset': speaks_forms, 'musical_experience_formset': musical_experience_forms})

@login_required
def adult_detail(request, adult_id):
    adult = get_object_or_404(Adult, pk=adult_id)
    speaks = Speaks.objects.filter(person = adult)
    musical_exps = MusicalExperience.objects.filter(person = adult)
    assessment_participations = Assessment_Run.objects.filter(participantAdult = adult)

    # all_scores = {}
    # for assessment_participation in assessment_participations:
    #     assessment_scores = {}
    #     score_query = Assessment_Run_Field_Score.objects.filter(assessment_run =  assessment_participation)
    #     for score in score_query:
    #         assessment_scores[score.assessment_field] = score
    #     all_scores[assessment_participation] = assessment_scores
    all_scores = {}
    for assessment_participation in assessment_participations:
        assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = assessment_participation)
        all_scores[assessment_participation.id] = assessment_run_fields
    try:
        parent_in = IsParentIn.objects.get(parent = adult)
        family = Family.objects.get(pk=parent_in.family.id)
        all_parents = IsParentIn.objects.filter(family = family)
        all_children = IsChildIn.objects.filter(family = family)
        return render(request, 'ParticipantDB/adult_detail.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps, 'family': family, 'parents': all_parents, 'children': all_children, 'assessment_participations': assessment_participations, 'all_scores': all_scores})
    except IsParentIn.DoesNotExist:
         return render(request, 'ParticipantDB/adult_detail.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps, 'assessment_participations': assessment_participations, 'all_scores': all_scores})   

@login_required
def delete_adult(request, adult_id):
    try:
        Adult.objects.get(pk=adult_id).delete()
        return redirect(reverse('index'))
    except Adult.DoesNotExist:
        raise Http404("No adult with id" + adult_id)
    

# Child Views ------------------------------------------------------------------

@login_required
def add_child(request):
    exposure_forms = ExposureInlineFormSet(
        queryset = IsExposedTo.objects.none()
    )
    if request.method == "POST":
        child_form = ChildForm(request.POST)
        exposure_forms = ExposureInlineFormSet(request.POST)
        if child_form.is_valid() and exposure_forms.is_valid():
            child = child_form.save(commit=False)
            child.save()
            for exposure_form in exposure_forms:
                if exposure_form.cleaned_data.get('lang'):
                    inst = exposure_form.save(commit=False)
                    inst.child = child
                    inst.save()
            
            return redirect(reverse('child_detail', kwargs={'child_id': child.id}))
    else:
        child_form = ChildForm(initial={'id': make_unique_id()})
    return render(request, "ParticipantDB/child_form.html", {'child_form': child_form, 'exposure_forms': exposure_forms})

@login_required
def update_child(request, child_id):
    try:
        child_inst = Child.objects.get(pk=child_id)
    except Child.DoesNotExist:
        Http404("No Child with id " + child_id)

    exposure_forms = ExposureInlineFormSet(
        queryset = IsExposedTo.objects.filter(child=child_inst)
    )
    
    if request.method == "POST":
        child_form = ChildForm(request.POST, instance = child_inst)
        exposure_forms = ExposureInlineFormSet(request.POST)
        if child_form.is_valid():
            child = child_form.save(commit=False)
            child.save()

            if exposure_forms.is_valid():
                for exposure_form in exposure_forms:
                    if exposure_form.cleaned_data.get('DELETE'):
                        toDelete = exposure_form.cleaned_data.get('lang')
                        IsExposedTo.objects.filter(child=child_inst, lang=toDelete).delete()
                    elif exposure_form.cleaned_data.get('lang'):
                        inst = exposure_form.save(commit=False)
                        inst.child = child
                        inst.save()
            return redirect(reverse('child_detail', kwargs={'child_id': child.id}))
    else:
        child_form = ChildForm(instance = child_inst)

    return render(request, "ParticipantDB/child_form_update.html", {'child_id': child_id, 'child_form': child_form, 'exposure_forms': exposure_forms})

@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    languages_exposed_to = IsExposedTo.objects.filter(child = child)
    child_in = IsChildIn.objects.get(child = child)
    family = Family.objects.get(pk=child_in.family.id)
    all_parents = IsParentIn.objects.filter(family = family)
    all_children = IsChildIn.objects.filter(family = family)
    return render(request, 'ParticipantDB/child_detail.html', {'child': child, 'languages_exposed_to': languages_exposed_to, 'family': family, 'parents': all_parents, 'children': all_children})


@login_required
def delete_child(request, child_id):
    try:
        Child.objects.get(pk=child_id).delete()
        return redirect(reverse('index'))
    except Child.DoesNotExist:
        raise Http404("No child with id" + child_id)


# Language Views ------------------------------------------------------------------

@login_required
def add_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = LanguageForm()
        return render(request, "ParticipantDB/language_form.html", {'form': form})

# Musical Views ------------------------------------------------------------------
@login_required
def add_musical_skill(request):
    if request.method == "POST":
        form = MusicalSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = MusicalSkillForm()
        return render(request, "ParticipantDB/musical_skill_form.html", {'form': form})

# Assessment Views --------------------------------------------------------------
@login_required
def add_assessment(request):
    assessment_field_forms = AssessmentFieldInlineFormSet(
        queryset = Assessment_Field.objects.none(),
        prefix = 'assessment_fields'
    )

    if request.method == "POST":
        assessment_form = AssessmentForm(request.POST)
        assessment_field_forms = AssessmentFieldInlineFormSet(request.POST, prefix = 'assessment_fields') 
        if assessment_form.is_valid() and assessment_field_forms.is_valid():
            assessment = assessment_form.save(commit=False)
            assessment.save()

            for assessment_field_form in assessment_field_forms:
                if assessment_field_form.is_valid() and assessment_field_form.cleaned_data.get('field_name'):
                    inst = assessment_field_form.save(commit=False)
                    inst.field_of = assessment
                    inst.save()

            return redirect(reverse('index'))
    else:
        assessment_form = AssessmentForm()
    
    return render(request, "ParticipantDB/assessment_form.html", {'assessment_form': assessment_form, 'assessment_field_formset': assessment_field_forms})


@login_required
def assessment_detail(request, assessment_name):
    assessment = get_object_or_404(Assessment, pk=assessment_name)
    assessment_fields = Assessment_Field.objects.filter(field_of = assessment)

    return render(request, 'ParticipantDB/assessment_detail.html', {'assessment': assessment, 'assessment_fields': assessment_fields})

@login_required
def delete_assessment(request, assessment_name):
    try:
        Assessment.objects.get(pk=assessment_name).delete()
        return redirect(reverse('index'))
    except Assessment.DoesNotExist:
        raise Http404("No assessment named " + assessment_name)

@login_required
def update_assessment(request, assessment_name):
    try:
        assessment_inst = Assessment.objects.get(pk=assessment_name)
    except Assessment.DoesNotExist:
        raise Http404("No assessment named " + assessment_name)

    assessment_field_forms = AssessmentFieldInlineFormSet(
        prefix = 'assessment_fields',
        queryset = Assessment_Field.objects.filter(field_of=assessment_inst),
    )

    if request.method == "POST":
        assessment_form = AssessmentForm(request.POST, request.FILES, instance=assessment_inst)
        assessment_field_forms = AssessmentFieldInlineFormSet(request.POST, request.FILES, prefix = 'assessment_fields')
        if assessment_form.is_valid():
            assessment = assessment_form.save(commit=False)
            assessment.save()
            if assessment_field_forms.is_valid():
                for field_form in assessment_field_forms:
                    if field_form.cleaned_data.get('DELETE'):
                        toDelete = field_form.cleaned_data.get('field_name')
                        Assessment_Field.objects.filter(field_of=assessment_inst, field_name=toDelete).delete()
                        # delete
                    elif field_form.cleaned_data.get('field_name'):
                        inst = field_form.save(commit=False)
                        inst.field_of = assessment
                        inst.save()
            if(assessment_form.cleaned_data.get('assessment_name') != assessment_name):
                print('{} != {}'.format(assessment_form.cleaned_data.get('assessment_name'), assessment_name))
                Assessment.objects.get(pk=assessment_name).delete()

            return redirect(reverse('assessment_detail', kwargs={'assessment_name': assessment.assessment_name}))
    else:
        assessment_form = AssessmentForm(instance = assessment_inst)
    
    return render(request, "ParticipantDB/assessment_form_update.html", {'assessment_name': assessment_name,'assessment_form': assessment_form, 'assessment_field_formset': assessment_field_forms})


# Assessment Run Views --------------------------------
@login_required
def choose_assessment(request):
    if (request.method == 'GET') and (request.GET.get('chooseAssessmentField', None)) and (request.GET.get('chooseParticipantField', None)):
        assessment_name = request.GET.get('chooseAssessmentField', None)
        participant_type = request.GET.get('chooseParticipantField', None)
        try:
            Assessment.objects.get(pk=assessment_name)
            return redirect(reverse('add_assessment_run', kwargs={'assessment_name': assessment_name, 'participant_type': participant_type}))
        except Assessment.DoesNotExist:
            raise Http404("No Assessment with name " + assessment_name)
    else:
        user_groups = get_user_groups(request)  
        assessments = []
        assessments_all = Assessment.objects.all()
        for assessment in assessments_all:
            print(assessment)
            for user_group in user_groups:
                print(user_group)
                if assessment.lab.group.id == user_group:
                    assessments.append(assessment)
            
        # if user_groups.count() > 1:
        #     for user_group in user_groups:
        #         print("Group: ", (user_group))
        #         assessment_querysets.append(Assessment.objects.filter(lab__group__id = user_group))
        #     assessments = list(chain([assessment_queryset for assessment_queryset in assessment_querysets]))
        # else:
        #     assessments = assessment_querysets
    return render(request, 'ParticipantDB/choose_assessment.html', {'assessments': assessments})


@login_required 
def add_assessment_run(request, assessment_name, participant_type):
    assessment = Assessment.objects.get(pk=assessment_name)
    assessment_run_field_score_forms = AssessmentRunFieldScoreInlineFormSet(
        queryset = Assessment_Run_Field_Score.objects.none(),
        prefix = 'assessment_field_scores'
    )
    assessment_fields = Assessment_Field.objects.filter(field_of=assessment)
    if request.method == "POST":
        assessment_run_form = AssessmentRunForm(request.POST)
        assessment_run_field_score_forms = AssessmentRunFieldScoreInlineFormSet(
            request.POST,
            prefix = 'assessment_field_scores'
        )
        if assessment_run_form.is_valid() and assessment_run_field_score_forms.is_valid():
            assessment_run = assessment_run_form.save(commit=False)
            assessment_run.assessment = assessment
            print(assessment_run.participantAdult)
            print(assessment_run.participantChild)
            assessment_run.save()
            for field, form in zip(assessment_fields, assessment_run_field_score_forms):
                inst = form.save(commit=False)
                inst.assessment_run = assessment_run
                inst.assessment_field = field
                inst.save()
            
            return redirect(reverse('assessment_run_detail', kwargs={'assessment_run_id': assessment_run.id}))
            
    
    else:
        assessment_run_form = AssessmentRunForm(initial = {'assessment': assessment})
    
    field_score_pairs = zip(assessment_fields, assessment_run_field_score_forms)
    return render(request, "ParticipantDB/assessment_run_form.html", {'assessment_name': assessment_name, 'field_score_pairs': field_score_pairs ,'assessment_run_form': assessment_run_form, 'assessment_run_field_score_formset': assessment_run_field_score_forms, 'participant_type': participant_type})


@login_required
def assessment_run_detail(request, assessment_run_id):
    assessment_run = get_object_or_404(Assessment_Run, pk=assessment_run_id)
    assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = assessment_run)
    return render(request, 'ParticipantDB/assessment_run_detail.html', {'assessment_run': assessment_run, 'assessment_run_fields': assessment_run_fields})

@login_required
def delete_assessment_run(request, assessment_run_id):
    try:
        Assessment_Run.objects.get(pk=assessment_run_id).delete()
        return redirect(reverse('index'))
    except Assessment_Run.DoesNotExist:
        raise Http404("No assessment_run with id " + assessment_run_id)