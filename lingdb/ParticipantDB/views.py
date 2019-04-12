# Imports ---------------------------------------------------------------
# Django
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from watson import search as watson

# Python
from itertools import chain
import operator
from datetime import date, timedelta

# Project
from .forms import *
from .models import *
from .utils import make_unique_id, get_user_groups, get_user_authed_list, check_user_groups
from .filters import *



# Singular -----------------------------------------------------------------
@login_required
def search(request):
    if request.method == 'GET':
        query = request.GET.get('search_box', None)
    # search_results = watson.search(query)
    # for result in search_results:
    #     print(result.title, result.url)
    try:
        Adult.objects.get(pk=query)
        return redirect(reverse('adult_detail', kwargs={'adult_id': query}))
    # Adult doesn't exist, try with child
    except Adult.DoesNotExist:
        try: 
            Child.objects.get(pk=query)
            return redirect(reverse('child_detail', kwargs={'child_id': query}))
        #Child doesn't exist, try with family
        except Child.DoesNotExist:
            try:
                Family.objects.get(pk=query)
                return redirect(reverse('family_detail', kwargs={'family_id': query}))
            #Family doesn't exist, invalid pk
            except Family.DoesNotExist:
                raise Http404("No Adult, Child, or Family matches ID#" + query)
    #Query refers either to an assessment, experiment, or experiment_section
    except ValueError:
        try: 
            Assessment.objects.get(assessment_name=query)
            return redirect(reverse('assessment_detail', kwargs={'assessment_name': query}))
        except Assessment.DoesNotExist:
            try:
                Experiment.objects.get(experiment_name=query)
                return redirect(reverse('experiment_detail', kwargs={'experiment_name': query}))
            except Experiment.DoesNotExist:
                    raise Http404("No Assessment, Experiment, Adult, Child, or Family matches " + query)
        except ValueError:
            raise Http404("Invalid query " + query)

@login_required
def index(request):
    return render(request, 'ParticipantDB/index.html')

@login_required
def add_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Language was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_language'))
            else:
                return redirect(reverse('index'))
    else:
        form = LanguageForm()
    return render(request, "ParticipantDB/Language/new.html", {'form': form})

@login_required
def add_musical_skill(request):
    if request.method == "POST":
        form = MusicalSkillForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Musical skill was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_musical_skill'))
            else:
                return redirect(reverse('index'))
    else:
        form = MusicalSkillForm()
    return render(request, "ParticipantDB/MusicalSkill/new.html", {'form': form})


# People -------------------------------------------------------------------------



# Adult
@login_required
def adult_query(request):
    # querysets
    adults = Adult.objects.all()
    speaks = Speaks.objects.all()
    music = MusicalExperience.objects.all()
    groups = get_user_groups(request)
    assessment_run = Assessment_Run.objects.all()
    
    # assessment_run = Assessment_Run.objects.all()
    experiment_section_run = Experiment_Section_Run.objects.filter(experiment_section__experiment__lab__group__name__in=groups)
    # filter init
    adultFilter = AdultFilter(request.GET, queryset=adults, request=request)
    
    speaksFilter = SpeaksFilter(request.GET, queryset=speaks, request=request)
    speakers = speaksFilter.qs.order_by('person__id').distinct('person__id').values_list('person__id', flat=True)
    
    musicalExperienceFilter = MusicalExperienceFilter(request.GET, queryset=music, request=request)
    musicians = musicalExperienceFilter.qs.order_by('person__id').distinct('person__id').values_list('person__id', flat=True)

    musicians = musicalExperienceFilter.qs.order_by('person__id').distinct('person__id').values_list('person__id', flat=True)


    assessmentRunFilter = AssessmentRunFilter(request.GET, queryset=assessment_run, request=request)
    assessment_participants = assessmentRunFilter.qs.order_by('participantAdult__id').distinct('participantAdult__id').values_list('participantAdult__id', flat=True)

    experimentSectionRunFilter = ExperimentSectionRunFilter(request.GET, queryset=experiment_section_run, request=request)
    experiment_section_participants = experimentSectionRunFilter.qs.order_by('participantAdult__id').distinct('participantAdult__id').values_list('participantAdult__id', flat=True)



    # filter by language skill
    combined = adultFilter.qs.filter(id__in=speakers).distinct('id')
    
    # potentially filter by musical skill
    musical_field_filled = request.GET.get('experience', '') or request.GET.get('m_proficiency', '') or  request.GET.get('m_age_learning_started', '') or  request.GET.get('m_age_learning_ended', '')
    if musical_field_filled:
        combined = combined.filter(id__in=musicians).distinct('id')
    

     # potentially filter by assessment run
    assessment_field_filled = request.GET.get('assessment', '') or request.GET.get('assessment_run_date_min', '') or request.GET.get('assessment_run_date_max', '') or request.GET.get('assessment_run_assessor', '') or request.GET.get('assessment_run_notes')
    if assessment_field_filled:
        combined = combined.filter(id__in=assessment_participants).distinct('id')
    
     # potentially filter by experiment section run
    experiment_run_field_filled = request.GET.get('experiment_section', '') or request.GET.get('experiment_section_run_date_min', '') or request.GET.get('experiment_section_run_date_max', '') or request.GET.get('experiment_section_run_assessor', '') or request.GET.get('experiment_section_run_notes')
    if experiment_run_field_filled:
        combined = combined.filter(id__in=experiment_section_participants).distinct('id')
    

    return render(request, 'ParticipantDB/Adult/list.html', {'adultFilter': adultFilter, 'speaksFilter': speaksFilter, 'musicalExperienceFilter': musicalExperienceFilter, 'assessmentRunFilter': assessmentRunFilter, 'experimentSectionRunFilter': experimentSectionRunFilter, 'combined': combined})



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
        adult_form = AdultForm(request.POST, prefix="adult")
        add_parent_form = AddParentForm(request.POST, prefix = "parent")
        speaks_forms = SpeaksInlineFormSet(request.POST, prefix = 'speaks_forms')
        musical_experience_forms = MusicalExperienceInlineFormSet(request.POST, prefix = 'musical_experiences')

        if adult_form.is_valid() and speaks_forms.is_valid() and musical_experience_forms.is_valid() and add_parent_form.is_valid():   
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
            if add_parent_form.cleaned_data.get('family'):
                inst = add_parent_form.save(commit=False)
                inst.parent = adult
                inst.save()

            print(add_parent_form.cleaned_data.get('family'))
            messages.success(request, 'Adult was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_adult'))
            else:
                return redirect(reverse('adult_detail', kwargs={'adult_id': adult.id}))
        
    else:
        adult_form = AdultForm(initial={'id': make_unique_id()}, prefix="adult")
        add_parent_form = AddParentForm(prefix="parent")
    return render(request, "ParticipantDB/Adult/new.html", {'adult_form': adult_form, 'speaks_formset': speaks_forms, 'musical_experience_formset': musical_experience_forms, 'addParentForm': add_parent_form})

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
        adult_form = AdultForm(request.POST, instance=adult_inst)
        
        speaks_forms = SpeaksInlineFormSet(request.POST, prefix = 'speaks_forms')
        musical_experience_forms = MusicalExperienceInlineFormSet(request.POST, prefix = 'musical_experiences')
        
        if adult_form.is_valid() and speaks_forms.is_valid() and musical_experience_forms.is_valid(): 
            adult = adult_form.save(commit=False)
            adult.save()
            for speaks_form in speaks_forms:
                if speaks_form.cleaned_data.get('DELETE'):
                    toDelete = speaks_form.cleaned_data.get('lang')
                    Speaks.objects.filter(person=adult_inst, lang=toDelete).delete()
                    # delete
                elif speaks_form.cleaned_data.get('lang'):
                    inst = speaks_form.save(commit=False)
                    inst.person = adult
                    inst.save()
                    
            for musical_experience_form in musical_experience_forms:
                if musical_experience_form.is_valid():
                    if musical_experience_form.cleaned_data.get('DELETE'):
                        toDelete = musical_experience_form.cleaned_data.get('experience')
                        MusicalExperience.objects.filter(person=adult_inst, experience=toDelete).delete()
                    elif musical_experience_form.cleaned_data.get('experience') and musical_experience_form.is_valid():
                        inst = musical_experience_form.save(commit=False)
                        inst.person = adult
                        inst.save()          
            messages.success(request, 'Adult was successfully updated')
            return redirect(reverse('adult_detail', kwargs={'adult_id': adult_id}))
        

    else:
        adult_form = AdultForm(instance = adult_inst)

    return render(request, "ParticipantDB/Adult/update.html", {'adult_id': adult_id, 'adult_form': adult_form, 'speaks_formset': speaks_forms, 'musical_experience_formset': musical_experience_forms})

@login_required
def adult_detail(request, adult_id):
    adult = get_object_or_404(Adult, pk=adult_id)
    speaks = Speaks.objects.filter(person = adult)
    musical_exps = MusicalExperience.objects.filter(person = adult)

    all_assessment_participations = Assessment_Run.objects.filter(participantAdult = adult)
    assessment_participations = get_user_authed_list(request, all_assessment_participations, "assessment")
    all_assessments = Assessment.objects.all()
    eligible_assessments = get_user_authed_list(request, all_assessments)
    all_scores = {}
    for assessment_participation in assessment_participations:
        assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = assessment_participation)
        all_scores[assessment_participation.id] = assessment_run_fields

    all_experiment_section_participations = Experiment_Section_Run.objects.filter(participantAdult = adult)
    experiment_participations = get_user_authed_list(request, all_experiment_section_participations, "experiment_section.experiment")
    all_experiment_sections = Experiment_Section.objects.all()
    eligible_experiment_sections = get_user_authed_list(request, all_experiment_sections, "experiment")
    all_experiment_scores = {}
    for experiment_participation in experiment_participations:
        experiment_section_run_fields = Experiment_Section_Run_Field_Score.objects.filter(experiment_section_run = experiment_participation)
        all_experiment_scores[experiment_participation.id] = experiment_section_run_fields
    if adult.health_notes != "" or adult.personal_notes != "":
        messages.info(request, 'Please see health/personal notes')

    try:
        parent_in_families = IsParentIn.objects.filter(parent = adult)
        families = []
        all_parents = {}
        all_children = {}
        for parent_in in parent_in_families:
            family = Family.objects.get(pk=parent_in.family.id)
            families.append(family)
            all_parents[family.id] =IsParentIn.objects.filter(family = family)
            all_children[family.id] =IsChildIn.objects.filter(family = family)

        return render(request, 'ParticipantDB/Adult/view.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps, 'families': families, 'all_parents': all_parents, 'all_children': all_children, 'assessment_participations': assessment_participations, 'all_scores': all_scores, 'eligible_assessments': eligible_assessments, 'experiment_section_participations': experiment_participations, 'eligible_experiment_sections': eligible_experiment_sections, 'all_experiment_scores': all_experiment_scores})
    except IsParentIn.DoesNotExist:
        return render(request, 'ParticipantDB/Adult/view.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps, 'assessment_participations': assessment_participations, 'all_scores': all_scores, 'eligible_assessments': eligible_assessments, 'experiment_section_participations': experiment_participations, 'eligible_experiment_sections': eligible_experiment_sections, 'all_experiment_scores': all_experiment_scores})

@login_required
def delete_adult(request, adult_id):
    try:
        Adult.objects.get(pk=adult_id).delete()
        
        messages.success(request, 'Adult was successfully deleted')
        return redirect(reverse('index'))
    except Adult.DoesNotExist:
        raise Http404("No adult with id" + adult_id)

# Child
@login_required
def child_query(request):
    # querysets
    children = Child.objects.all()
    lang_exposure = IsExposedTo.objects.all()
    groups = get_user_groups(request)
    assessment_run = Assessment_Run.objects.filter(assessment__lab__group__name__in=groups)
    experiment_section_run = Experiment_Section_Run.objects.filter(experiment_section__experiment__lab__group__name__in=groups)

    childFilter = ChildFilter(request.GET, queryset=children, request=request)

    exposureFilter = ExposureFilter(request.GET, queryset=lang_exposure, request=request)
    exposed_to_lang = exposureFilter.qs.order_by('child__id').distinct('child__id').values_list('child__id', flat=True)
    
    assessmentRunFilter = AssessmentRunFilter(request.GET, queryset=assessment_run, request=request)
    assessment_participants = assessmentRunFilter.qs.order_by('participantChild__id').distinct('participantChild__id').values_list('participantChild__id', flat=True)

    experimentSectionRunFilter = ExperimentSectionRunFilter(request.GET, queryset=experiment_section_run, request=request)
    experiment_section_participants = experimentSectionRunFilter.qs.order_by('participantChild__id').distinct('participantChild__id').values_list('participantChild__id', flat=True)

    # filter by exposure
    combined = childFilter.qs.filter(id__in=exposed_to_lang).distinct('id')

     # potentially filter by assessment run
    assessment_field_filled = request.GET.get('assessment', '') or request.GET.get('assessment_run_date_min', '') or request.GET.get('assessment_run_date_max', '') or request.GET.get('assessment_run_assessor', '') or request.GET.get('assessment_run_notes')
    if assessment_field_filled:
        combined = combined.filter(id__in=assessment_participants).distinct('id')
    
     # potentially filter by experiment section run
    experiment_run_field_filled = request.GET.get('experiment_section', '') or request.GET.get('experiment_section_run_date_min', '') or request.GET.get('experiment_section_run_date_max', '') or request.GET.get('experiment_section_run_assessor', '') or request.GET.get('experiment_section_run_notes')
    if experiment_run_field_filled:
        combined = combined.filter(id__in=experiment_section_participants).distinct('id')



    return render(request, 'ParticipantDB/Child/list.html', {'childFilter': childFilter,'exposureFilter': exposureFilter, 'assessmentRunFilter': assessmentRunFilter, 'experimentSectionRunFilter': experimentSectionRunFilter, 'combined': combined})


@login_required
def add_child(request):
    exposure_forms = ExposureInlineFormSet(
        queryset = IsExposedTo.objects.none()
    )
    if request.method == "POST":
        child_form = ChildForm(request.POST, prefix="child")
        exposure_forms = ExposureInlineFormSet(request.POST)
        add_child_form = AddChildForm(request.POST, prefix = "childin")

        if request.POST.get('sumExposure', '') != '0':
            messages.error(request, 'Ensure Language Exposure Percentages add to 100')
        elif child_form.is_valid() and exposure_forms.is_valid() and add_child_form.is_valid():
            child = child_form.save(commit=False)
            child.save()
            for exposure_form in exposure_forms:
                if exposure_form.cleaned_data.get('lang'):
                    inst = exposure_form.save(commit=False)
                    inst.child = child
                    inst.save()
            
            if add_child_form.cleaned_data.get('family'):
                inst = add_child_form.save(commit=False)
                inst.child = child
                inst.save()
            
            messages.success(request, 'Child was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_child'))
            else:
                return redirect(reverse('child_detail', kwargs={'child_id': child.id}))

    else:
        child_form = ChildForm(initial={'id': make_unique_id()}, prefix="child")
        add_child_form = AddChildForm(prefix="childin")
    return render(request, "ParticipantDB/Child/new.html", {'child_form': child_form, 'exposure_forms': exposure_forms, 'addChildForm': add_child_form})

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
        if request.POST.get('sumExposure', '') != '0':
            messages.error(request, 'Ensure Language Exposure Percentages add to 100')
        elif child_form.is_valid() and exposure_forms.is_valid():
            child = child_form.save(commit=False)
            child.save()
            for exposure_form in exposure_forms:
                if exposure_form.cleaned_data.get('DELETE'):
                    toDelete = exposure_form.cleaned_data.get('lang')
                    IsExposedTo.objects.filter(child=child_inst, lang=toDelete).delete()
                elif exposure_form.cleaned_data.get('lang'):
                    inst = exposure_form.save(commit=False)
                    inst.child = child
                    inst.save()
                        
            messages.success(request, 'Child was successfully updated')
            return redirect(reverse('child_detail', kwargs={'child_id': child.id}))
    else:
        child_form = ChildForm(instance = child_inst)

    return render(request, "ParticipantDB/Child/update.html", {'child_id': child_id, 'child_form': child_form, 'exposure_forms': exposure_forms})

@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    languages_exposed_to = IsExposedTo.objects.filter(child = child)

    all_assessment_participations = Assessment_Run.objects.filter(participantChild = child)
    assessment_participations = get_user_authed_list(request, all_assessment_participations, "assessment")
    all_assessments = Assessment.objects.all()
    eligible_assessments = get_user_authed_list(request, all_assessments)
    all_scores = {}
    for assessment_participation in assessment_participations:
        assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = assessment_participation)
        all_scores[assessment_participation.id] = assessment_run_fields

    all_experiment_section_participations = Experiment_Section_Run.objects.filter(participantChild = child)
    experiment_participations = get_user_authed_list(request, all_experiment_section_participations, "experiment_section.experiment")
    all_experiment_sections = Experiment_Section.objects.all()
    eligible_experiment_sections = get_user_authed_list(request, all_experiment_sections, "experiment")
    all_experiment_scores = {}
    for experiment_participation in experiment_participations:
        experiment_section_run_fields = Experiment_Section_Run_Field_Score.objects.filter(experiment_section_run = experiment_participation)
        all_experiment_scores[experiment_participation.id] = experiment_section_run_fields
    if child.health_notes != "" or child.personal_notes != "":
        messages.info(request, 'Please see health/personal notes')
    if child.hereditary_audio_problems == True:
        messages.info(request, 'Please see hereditary audio/language problems')

    try:
        child_in = IsChildIn.objects.get(child = child)
        family = Family.objects.get(pk=child_in.family.id)
        all_parents = IsParentIn.objects.filter(family = family)
        all_children = IsChildIn.objects.filter(family = family)
        return render(request, 'ParticipantDB/Child/view.html', {'child': child, 'languages_exposed_to': languages_exposed_to, 'family': family, 'parents': all_parents, 'siblings': all_children, 'assessment_participations': assessment_participations, 'all_scores': all_scores, 'eligible_assessments': eligible_assessments, 'experiment_section_participations': experiment_participations, 'eligible_experiment_sections': eligible_experiment_sections, 'all_experiment_scores': all_experiment_scores})
    except IsChildIn.DoesNotExist:
        messages.warning(request, 'Family not in database')
        return render(request, 'ParticipantDB/Child/view.html', {'child': child, 'languages_exposed_to': languages_exposed_to, 'assessment_participations': assessment_participations, 'all_scores': all_scores, 'eligible_assessments': eligible_assessments, 'experiment_section_participations': experiment_participations, 'eligible_experiment_sections': eligible_experiment_sections, 'all_experiment_scores': all_experiment_scores})

@login_required
def delete_child(request, child_id):
    try:
        Child.objects.get(pk=child_id).delete()
        
        messages.success(request, 'Child was successfully deleted')
        return redirect(reverse('index'))
    except Child.DoesNotExist:
        raise Http404("No child with id" + child_id)

# Family

@login_required
def family_query(request):
    families = Family.objects.all()
    familyFilter = FamilyFilter(request.GET, queryset=families, request=request)
    return render(request, 'ParticipantDB/Family/list.html', {'familyFilter': familyFilter})
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


            messages.success(request, 'Family was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_family'))
            else:
                return redirect(reverse('family_detail', kwargs={'family_id': family.id}))

    else:
        family_form = FamilyForm(initial={'id': make_unique_id()})

    return render(request, "ParticipantDB/Family/new.html", {'family_form': family_form, 'child_forms': child_forms, 'parent_forms': parent_forms})

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

            messages.success(request, 'Family was successfully updated')
            return redirect(reverse('family_detail', kwargs={'family_id': family.id}))

    else:
        family_form = FamilyForm(instance = family_inst)

    return render(request, "ParticipantDB/Family/update.html", {'family_id': family_id, 'family_form': family_form, 'child_forms': child_forms, 'parent_forms': parent_forms})

@login_required
def family_detail(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    parents = IsParentIn.objects.filter(family = family)
    children = IsChildIn.objects.filter(family = family)
    parentsSpeak = {}
    parentsMusic = {}
    parentNotes = False
    childNotes = False
    childHered = False
    for parent in parents:
        parentsSpeak[parent.parent.id] = Speaks.objects.filter(person = parent.parent)
        parentsMusic[parent.parent.id] = MusicalExperience.objects.filter(person = parent.parent)
        if parent.parent.health_notes != "" or parent.parent.personal_notes != "":
            parentNotes = True
    childrenLangExposure = {}
    for child in children:
        childrenLangExposure[child.child.id] = IsExposedTo.objects.filter(child = child.child)
        if child.child.health_notes != "" or child.child.personal_notes != "":
            childNotes = True
        if child.child.hereditary_audio_problems == True or child.child.hereditary_language_pathologies:
            childHered = True
    
    notes = ""
    

    if parentNotes:    
        messages.info(request, 'At least one parent has health or personal notes')
    if childNotes:    
        messages.info(request, 'At least one child has health or personal notes')
    if childHered:    
        messages.info(request, 'At least one child has hereditary audio problems or language pathologies')




    return render(request, 'ParticipantDB/Family/view.html', {'family': family, 'parents': parents, 'children': children, 'parentsSpeak': parentsSpeak, 'parentsMusic': parentsMusic, 'childrenLangExposure': childrenLangExposure})
    
@login_required
def delete_family(request, family_id):
    try:
        Family.objects.get(pk=family_id).delete()
        
        messages.success(request, 'Family was successfully deleted')
        return redirect(reverse('index'))
    except Family.DoesNotExist:
        raise Http404("No family with id" + family_id)




# Assessment --------------------------------------------------------------
@login_required
def assessment_list(request):
    all_assessments = Assessment.objects.all()
    eligible_assessments = get_user_authed_list(request, all_assessments)  
    all_counts = {}
    all_fields = {}
    for assessment in eligible_assessments:
        all_counts[assessment.assessment_name] = Assessment_Run.objects.filter(assessment = assessment).count()
        all_fields[assessment.assessment_name] = Assessment_Field.objects.filter(field_of = assessment)
    
    return render(request, 'ParticipantDB/Assessment/list.html', {'assessments': eligible_assessments, 'assessment_run_counts': all_counts, 'assessment_fields': all_fields})




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
            authed_groups = get_user_groups(request)
            nameOverload = Experiment.objects.filter(experiment_name=assessment.assessment_name).exists()
            if(assessment.lab.group.name in authed_groups and not nameOverload):
                assessment.save()

                for assessment_field_form in assessment_field_forms:
                    if assessment_field_form.is_valid() and assessment_field_form.cleaned_data.get('field_name'):
                        inst = assessment_field_form.save(commit=False)
                        inst.field_of = assessment
                        inst.save()

        
                messages.success(request, 'Assessment was successfully added')
                if 'save_add_another' in request.POST:
                    return redirect(reverse('add_assessment'))
                else:
                    return redirect(reverse('assessment_detail', kwargs={'assessment_name': assessment.assessment_name}))
            else:
                if(nameOverload):
                    messages.error(request, "An experiment already exists with this name, please choose another name")
                else:
                    messages.error(request, "You are not authorized to add assessments to {} lab ".format(assessment.lab))
    else:
        assessment_form = AssessmentForm()
    
        assessment_form.fields["lab"].queryset = Lab.objects.filter(group__name__in=get_user_groups(request))
    return render(request, "ParticipantDB/Assessment/new.html", {'assessment_form': assessment_form, 'assessment_field_formset': assessment_field_forms})

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
    authed_groups = get_user_groups(request)
    canAccess = assessment_inst.lab.group.name in authed_groups

    if request.method == "POST":
        assessment_form = AssessmentForm(request.POST, request.FILES, instance=assessment_inst)
        assessment_field_forms = AssessmentFieldInlineFormSet(request.POST, request.FILES, prefix = 'assessment_fields')
        if assessment_form.is_valid():
            assessment = assessment_form.save(commit=False)
            authed_groups = get_user_groups(request)
            nameOverload = Experiment.objects.filter(experiment_name=assessment.assessment_name).exists()
            if(assessment.lab.group.name in authed_groups and not nameOverload):
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

                
                messages.success(request, 'Assessment was successfully updated')
                return redirect(reverse('assessment_detail', kwargs={'assessment_name': assessment.assessment_name}))
            else:
                if(nameOverload):
                    messages.error(request, "An experiment already exists with this name, please choose another name")
                else:
                    messages.error(request, "You are not authorized to edit {} lab's assessments ".format(assessment.lab))
    else:
        assessment_form = AssessmentForm(instance = assessment_inst)
    
        assessment_form.fields["lab"].queryset = Lab.objects.filter(group__name__in=get_user_groups(request))
    return render(request, "ParticipantDB/Assessment/update.html", {'assessment_name': assessment_name,'assessment_form': assessment_form, 'assessment_field_formset': assessment_field_forms, 'canAccess': canAccess})

@login_required
def assessment_detail(request, assessment_name):
    assessment = get_object_or_404(Assessment, pk=assessment_name)
    assessment_fields = Assessment_Field.objects.filter(field_of = assessment)
    assessment_runs = Assessment_Run.objects.filter(assessment = assessment)
    authed_groups = get_user_groups(request)
    
    all_scores = {}
    for run in assessment_runs:
        assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = run)
        all_scores[run.id] = assessment_run_fields


    canAccess = assessment.lab.group.name in authed_groups
    return render(request, 'ParticipantDB/Assessment/view.html', {'canAccess': canAccess, 'assessment': assessment, 'assessment_fields': assessment_fields, 'assessment_runs': assessment_runs, 'all_scores': all_scores})

@login_required
def delete_assessment(request, assessment_name):
    try:
        assessment = Assessment.objects.get(pk=assessment_name)
        authed_groups = get_user_groups(request)
        canAccess = assessment.lab.group.name in authed_groups
        if canAccess:
            assessment.delete()
            messages.success(request, 'Assessment was successfully deleted')
        else:
            messages.error(request, 'Assessment was not deleted as you do not have authorization to access it')
        return redirect(reverse('index'))
    except Assessment.DoesNotExist:
        raise Http404("No assessment named " + assessment_name)





# Assessment Run -----------------------------------------------------------
@login_required
def choose_assessment(request):
    if (request.method == 'GET') and (request.GET.get('chooseAssessmentField', None)) and (request.GET.get('chooseParticipantField', None)):
        assessment_name = request.GET.get('chooseAssessmentField', None)
        participant_type = request.GET.get('chooseParticipantField', None)
        participant = request.GET.get('participantID', None)
        try:
            Assessment.objects.get(pk=assessment_name)
            if participant:
                return redirect(reverse('add_assessment_run', kwargs={'assessment_name': assessment_name, 'participant_type': participant_type, 'participant': participant}))
            else:
                return redirect(reverse('add_assessment_run', kwargs={'assessment_name': assessment_name, 'participant_type': participant_type}))
        except Assessment.DoesNotExist:
            raise Http404("No Assessment with name " + assessment_name)
    else:
        assessments_all = Assessment.objects.all()
        assessments = get_user_authed_list(request, assessments_all)
        
    return render(request, 'ParticipantDB/AssessmentRun/new1.html', {'assessments': assessments})

@login_required 
def add_assessment_run(request, assessment_name, participant_type, participant=None):
    assessment = Assessment.objects.get(pk=assessment_name)
    user_can_add = check_user_groups(request, assessment)
    if not user_can_add:
        return HttpResponseForbidden()
    assessment_run_field_score_forms = AssessmentRunFieldScoreInlineFormSet(
        queryset = Assessment_Run_Field_Score.objects.none(),
        prefix = 'assessment_field_scores',
    )
    assessment_fields = Assessment_Field.objects.filter(field_of=assessment)
    if request.method == "POST":
        if participant_type == "adult":
            assessment_run_form = AdultAssessmentRunForm(request.POST, prefix = 'assessment_run_form')
        else:
            assessment_run_form = ChildAssessmentRunForm(request.POST, prefix = 'assessment_run_form')
        assessment_run_field_score_forms = AssessmentRunFieldScoreInlineFormSet(
            request.POST,
            prefix = 'assessment_field_scores'
        )
        if assessment_run_form.is_valid() and assessment_run_field_score_forms.is_valid():
            assessment_run = assessment_run_form.save(commit=False)
            assessment_run.assessment = assessment
            assessment_run.save()
            for field, form in zip(assessment_fields, assessment_run_field_score_forms):
                inst = form.save(commit=False)
                inst.assessment_run = assessment_run
                inst.assessment_field = field
                inst.save()
            

            messages.success(request, 'Assessment run was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_assessment_run', kwargs={'assessment_name': assessment_name, 'participant_type': participant_type}))
            else:
                return redirect(reverse('assessment_run_detail', kwargs={'assessment_run_id': assessment_run.id}))
            
    
    else:
        if participant_type == "adult" and participant:
            adult = Adult.objects.get(pk=participant)
            assessment_run_form = AdultAssessmentRunForm(initial = {'assessment': assessment, 'participantAdult': adult}, prefix = 'assessment_run_form')
        elif participant_type == "adult":
            assessment_run_form = AdultAssessmentRunForm(initial = {'assessment': assessment}, prefix = 'assessment_run_form')
        elif participant_type == "child" and participant:
            child = Child.objects.get(pk=participant)
            assessment_run_form = ChildAssessmentRunForm(initial = {'assessment': assessment, 'participantChild': child}, prefix = 'assessment_run_form')
        else:
            assessment_run_form = ChildAssessmentRunForm(initial = {'assessment': assessment}, prefix = 'assessment_run_form')
        assessment_run_form.fields["assessor"].queryset = User.objects.filter(groups=assessment.lab.group)
    field_score_pairs = zip(assessment_fields, assessment_run_field_score_forms)
    return render(request, "ParticipantDB/AssessmentRun/new2.html", {'assessment_name': assessment_name, 'field_score_pairs': field_score_pairs ,'assessment_run_form': assessment_run_form, 'assessment_run_field_score_formset': assessment_run_field_score_forms, 'participant_type': participant_type})

@login_required
def assessment_run_detail(request, assessment_run_id):
    assessment_run = get_object_or_404(Assessment_Run, pk=assessment_run_id)
    assessment_run_fields = Assessment_Run_Field_Score.objects.filter(assessment_run = assessment_run)
    return render(request, 'ParticipantDB/AssessmentRun/view.html', {'assessment_run': assessment_run, 'assessment_run_fields': assessment_run_fields})

@login_required
def delete_assessment_run(request, assessment_run_id):
    try:
        Assessment_Run.objects.get(pk=assessment_run_id).delete()
        messages.success(request, 'Assessment run was successfully deleted')
        return redirect(reverse('index'))
    except Assessment_Run.DoesNotExist:
        raise Http404("No assessment_run with id " + assessment_run_id)

@login_required
def update_assessment_run(request, assessment_run_id):
    pass




# Experiment --------------------------------------------------------------
@login_required
def experiment_list(request):
    all_experiments = Experiment.objects.all()
    eligible_experiments = get_user_authed_list(request, all_experiments)  
    all_experiment_sections = {}
    
    all_counts = {}
    # all_fields = {}
    for experiment in eligible_experiments:
        all_experiment_sections[experiment.experiment_name] = Experiment_Section.objects.filter(experiment = experiment)
        all_counts[experiment.experiment_name] = 0
        for section in all_experiment_sections[experiment.experiment_name]:
            all_counts[experiment.experiment_name] += Experiment_Section_Run.objects.filter(experiment_section = section).count()
    
    return render(request, 'ParticipantDB/Experiment/list.html', {'experiments': eligible_experiments, 'experiment_run_counts': all_counts, 'experiment_sections': all_experiment_sections})


@login_required
def add_experiment(request):
    experiment_section_forms = ExperimentSectionInlineFormSet(
        queryset = Experiment_Section.objects.none(),
        prefix = 'experiment_sections'
    )
    all_labs = Lab.objects.all()
    auth_groups = get_user_groups(request)
    auth_labs = []
    for lab in all_labs:
        flag = False
        for group in auth_groups:
            if lab.group.name == group:
                flag = True
        if flag:
            auth_labs.append(lab)
    if request.method == "POST":
        experiment_form = ExperimentForm(request.POST)
        experiment_section_forms = ExperimentSectionInlineFormSet(request.POST, prefix = 'experiment_sections') 
        if experiment_form.is_valid() and experiment_section_forms.is_valid():
            experiment = experiment_form.save(commit=False)
            authed_groups = get_user_groups(request)
            nameOverload = Assessment.objects.filter(assessment_name=experiment.experiment_name).exists()
            if(experiment.lab.group.name in authed_groups and not nameOverload):
                experiment.save()

                for experiment_section_form in experiment_section_forms:
                    if experiment_section_form.is_valid() and experiment_section_form.cleaned_data.get('experiment_section_name'):
                        inst = experiment_section_form.save(commit=False)
                        inst.experiment = experiment
                        inst.save()
                
                messages.success(request, 'Experiment was successfully added')
                return redirect(reverse('add_experiment_section_fields', kwargs={'experiment_name': experiment.experiment_name}))
            else:
                if(nameOverload):
                    messages.error(request, "An assessment already exists with this name, please choose another name")
                else:
                    messages.error(request, "You are not authorized to add experiments to {} lab ".format(experiment.lab))
    else:
        experiment_form = ExperimentForm()
    
    
        experiment_form.fields["lab"].queryset = Lab.objects.filter(group__name__in=get_user_groups(request))
    return render(request, "ParticipantDB/Experiment/new.html", {'experiment_form': experiment_form, 'experiment_section_formset': experiment_section_forms})

@login_required
def update_experiment(request, experiment_name):
    try:
        experiment_inst = Experiment.objects.get(pk=experiment_name)
    except Experiment.DoesNotExist:
        Http404("No experiment with name " + experiment_name)
    
    experiment_section_forms = ExperimentSectionInlineFormSet(
        queryset = Experiment_Section.objects.filter(experiment = experiment_inst),
        prefix = 'experiment_sections'
    )
    
    authed_groups = get_user_groups(request)
    canAccess = experiment_inst.lab.group.name in authed_groups
    if request.method == "POST":
        experiment_form = ExperimentForm(request.POST, instance=experiment_inst)
        experiment_section_forms = ExperimentSectionInlineFormSet(request.POST, prefix = 'experiment_sections') 
        if experiment_form.is_valid():
            experiment = experiment_form.save(commit=False)
            nameOverload = Assessment.objects.filter(assessment_name=experiment.experiment_name).exists()
            if(experiment.lab.group.name in authed_groups and not nameOverload):
                if experiment_section_forms.is_valid():
                    experiment.save()
                    for form in experiment_section_forms:
                        if form.cleaned_data.get('DELETE'):
                            toDelete = form.cleaned_data.get('experiment_section_name')
                            Experiment_Section.objects.filter(experiment = experiment_inst, experiment_section_name=toDelete).delete()
                        elif form.cleaned_data.get('experiment_section_name'):
                            inst = form.save(commit=False)
                            inst.experiment = experiment
                            inst.save()
               
                    messages.success(request, 'Experiment was successfully updated')
                    return redirect(reverse('update_experiment_section_fields', kwargs={'experiment_name': experiment.experiment_name}))       
            else:
                if(nameOverload):
                    messages.error(request, "An assessment already exists with this name, please choose another name")
                else:
                    messages.error(request, "You are not authorized to update this experiment")
    else:
        experiment_form = ExperimentForm(instance = experiment_inst)

        experiment_form.fields["lab"].queryset = Lab.objects.filter(group__name__in=get_user_groups(request))
    return render(request, "ParticipantDB/Experiment/update.html", {'experiment_form': experiment_form, 'experiment_section_formset': experiment_section_forms, 'experiment_name': experiment_name, 'canAccess': canAccess})

@login_required
def experiment_detail(request, experiment_name):
    experiment = get_object_or_404(Experiment, pk=experiment_name)
    experiment_sections = Experiment_Section.objects.filter(experiment=experiment)
    all_fields = {}
    for section in experiment_sections:
        all_fields[section.experiment_section_name] = Experiment_Section_Field.objects.filter(field_of = section)
    authed_groups = get_user_groups(request)  
    canAccess = experiment.lab.group.name in authed_groups
    return render(request, 'ParticipantDB/Experiment/view.html', {'canAccess': canAccess, 'experiment': experiment, 'experiment_sections': experiment_sections, 'all_fields': all_fields})

@login_required
def delete_experiment(request, experiment_name):
    try:
        Experiment.objects.get(pk=experiment_name).delete()
        messages.success(request, 'Experiment was successfully deleted')
        return redirect(reverse('index'))
    except Experiment.DoesNotExist:
        raise Http404("No experiment named " + experiment_name)




# Experiment Section ----------------------------------------------------

@login_required
def experiment_section_detail(request, experiment_name, experiment_section_name):
    try:
        experiment = Experiment.objects.get(experiment_name = experiment_name)
        try:
            experiment_section = Experiment_Section.objects.get(experiment_section_name=experiment_section_name, experiment=experiment)
        except Experiment_Section.DoesNotExist:
            raise Http404("No Experiment Section '{}' in Experiment '{}'".format(experiment_name, experiment_section_name))
    except Experiment.DoesNotExist:
        raise Http404("No Experiment '{}'".format(experiment_name))
    experiment_section_fields = Experiment_Section_Field.objects.filter(field_of = experiment_section)
    experiment_section_runs = Experiment_Section_Run.objects.filter(experiment_section = experiment_section)

    authed_groups = get_user_groups(request)
    all_scores = {}
    for run in experiment_section_runs:
        all_scores[run.id] = Experiment_Section_Run_Field_Score.objects.filter(experiment_section_run = run)
    
    canAccess = experiment.lab.group.name in authed_groups
    return render(request, 'ParticipantDB/ExperimentSection/view.html', {'canAccess': canAccess, 'experiment': experiment, 'experiment_section': experiment_section, 'experiment_section_fields': experiment_section_fields, 'experiment_section_runs':experiment_section_runs, 'all_scores': all_scores})

@login_required
def delete_experiment_section(request, experiment_name, experiment_section_name):
    try:
        experiment = Experiment.objects.get(experiment_name = experiment_name)
        try:
            Experiment_Section.objects.get(experiment_section_name=experiment_section_name, experiment=experiment).delete()
            messages.success(request, 'Experiment section was successfully deleted')
            return redirect(reverse('index'))
        except Experiment_Section.DoesNotExist:
            raise Http404("Experiment '{}' does not have an experiment section '{}' ".format(experiment_name, experiment_section_name))
    except Experiment.DoesNotExist:
        raise Http404("No Experiment '{}'".format(experiment_name))


@login_required
def add_experiment_section_fields(request, experiment_name):
    try:
        experiment = Experiment.objects.get(pk=experiment_name)
    except Experiment.DoesNotExist:
        Http404("No experiment with name " + experiment_name)
    experiment_sections = Experiment_Section.objects.filter(experiment=experiment)
    fields = {}
    for section in experiment_sections:
        section_prefix = 'experiment_section_fields_' + section.experiment_section_name
        section_fields = ExperimentSectionFieldInlineFormSet(
            queryset = Experiment_Section_Field.objects.none(),
            prefix = section_prefix
        )
        fields[section.id] = section_fields
    if request.method == "POST":
        for section in experiment_sections:
            section_prefix = 'experiment_section_fields_' + section.experiment_section_name
            section_fields = ExperimentSectionFieldInlineFormSet(
                request.POST,
                prefix = section_prefix,
            )
            for section_field in section_fields:
                if section_field.is_valid() and section_field.cleaned_data.get('field_name'):
                    inst = section_field.save(commit = False)
                    inst.field_of = section
                    inst.save()
        
        messages.success(request, 'Experiment Section Fields were successfully added')
        return redirect(reverse('experiment_detail', kwargs={'experiment_name': experiment.experiment_name}))       
    return render(request, "ParticipantDB/ExperimentSection/new.html", {'experiment': experiment, 'experiment_sections': experiment_sections, 'fields': fields})
    
@login_required
def update_experiment_section_fields(request, experiment_name): 
    try:
        experiment_inst = Experiment.objects.get(pk=experiment_name)
    except Experiment.DoesNotExist:
        Http404("No experiment with name " + experiment_name)
    experiment_sections = Experiment_Section.objects.filter(experiment=experiment_inst)
    fields = {}
    for section in experiment_sections:
        section_prefix = 'experiment_section_fields_' + section.experiment_section_name
        section_fields = ExperimentSectionFieldInlineFormSet(
            queryset = Experiment_Section_Field.objects.filter(field_of = section),
            prefix = section_prefix
        )
        fields[section.id] = section_fields
    
    if request.method == "POST":
        for section in experiment_sections:
            section_prefix = 'experiment_section_fields_' + section.experiment_section_name
            section_fields = ExperimentSectionFieldInlineFormSet(
                request.POST,
                prefix = section_prefix,
            )
            for section_field in section_fields:
                if section_field.is_valid():
                    if section_field.cleaned_data.get('DELETE'):
                        toDelete = section_field.cleaned_data.get('field_name')
                        Experiment_Section_Field.objects.filter(field_of=section, field_name=toDelete).delete()
                    elif section_field.cleaned_data.get('field_name'):
                        inst = section_field.save(commit = False)
                        inst.field_of = section
                        inst.save()
        
        messages.success(request, 'Experiment Section Fields were successfully updated')
        return redirect(reverse('experiment_detail', kwargs={'experiment_name': experiment_name}))       
    return render(request, "ParticipantDB/ExperimentSection/update.html", {'experiment': experiment_inst, 'experiment_sections': experiment_sections, 'fields': fields})


# Experiment Section Run Views -----------------------------------------------------
@login_required
def choose_experiment_section(request):
    if (request.method == 'GET') and (request.GET.get('chooseExperimentSectionField', None)) and (request.GET.get('chooseParticipantField', None)):
        experiment_pair = request.GET.get('chooseExperimentSectionField', None).split("|")
        print(experiment_pair)
        
        experiment_name = experiment_pair[0]
        experiment_section_name = experiment_pair[1]
        participant_type = request.GET.get('chooseParticipantField', None)
        participant = request.GET.get('participantID', None)
        try:
            experiment = Experiment.objects.get(experiment_name = experiment_name)
            experiment_section = Experiment_Section.objects.get(experiment_section_name = experiment_section_name, experiment = experiment)
            if participant:
                return redirect(reverse('add_experiment_section_run', kwargs={'experiment_section_name': experiment_section_name, 'experiment_name': experiment_name, 'participant_type': participant_type, 'participant': participant}))
            else:
                return redirect(reverse('add_experiment_section_run', kwargs={'experiment_section_name': experiment_section_name, 'experiment_name': experiment_name, 'participant_type': participant_type}))
        except Experiment_Section.DoesNotExist:
            raise Http404("No Experiment Section '{}' of Experiment '{}' ".format(experiment_section_name, experiment_name))
        except Experiment.DoesNotExist:
            raise Http404("No Experiment '{}'".format(experiment_name))
    else:
        experiment_sections_all = Experiment_Section.objects.all().order_by('experiment', 'experiment_section_name')
        experiment_sections = get_user_authed_list(request, experiment_sections_all, "experiment")
        
    return render(request, 'ParticipantDB/ExperimentSectionRun/new1.html', {'experiment_sections': experiment_sections})

@login_required
def add_experiment_section_run(request, experiment_section_name, experiment_name, participant_type, participant=None):
    experiment = Experiment.objects.get(experiment_name=experiment_name)
    experiment_section = Experiment_Section.objects.get(experiment=experiment, experiment_section_name=experiment_section_name)
    user_can_add = check_user_groups(request, experiment_section, "experiment")
    if not user_can_add:
        return HttpResponseForbidden()
    experiment_section_run_field_score_forms = ExperimentSectionRunFieldScoreInlineFormSet(
        queryset = Experiment_Section_Run_Field_Score.objects.none(),
        prefix = 'experiment_section_field_scores'
    )
    experiment_section_fields = Experiment_Section_Field.objects.filter(field_of=experiment_section)
    if request.method == "POST":
        
        if participant_type == "adult":
            experiment_section_run_form = AdultExperimentSectionRunForm(request.POST, prefix = 'experiment_run_form')
        else:
            experiment_section_run_form = ChildExperimentSectionRunForm(request.POST, prefix = 'experiment_run_form')
        experiment_section_run_field_score_forms = ExperimentSectionRunFieldScoreInlineFormSet(
            request.POST,
            prefix = 'experiment_section_field_scores'
        )
        if experiment_section_run_form.is_valid() and experiment_section_run_field_score_forms.is_valid():
            experiment_section_run = experiment_section_run_form.save(commit=False)
            experiment_section_run.experiment_section = experiment_section
            experiment_section_run.save()
            for field, form in zip(experiment_section_fields, experiment_section_run_field_score_forms):
                inst = form.save(commit=False)
                inst.experiment_section_run = experiment_section_run
                inst.experiment_section_field = field
                inst.save()
            


            messages.success(request, 'Experiment section run was successfully added')
            if 'save_add_another' in request.POST:
                return redirect(reverse('add_experiment_section_run', kwargs={'experiment_section_name': experiment_section_name, 'experiment_name': experiment_name ,'participant_type': participant_type}))
            else:
                return redirect(reverse('experiment_section_run_detail', kwargs={'experiment_section_run_id': experiment_section_run.id}))
            
    
    else:
        if participant_type == "adult" and participant:
            adult = Adult.objects.get(pk=participant)
            experiment_section_run_form = AdultExperimentSectionRunForm(initial = {'experiment_section': experiment_section, 'participantAdult': adult}, prefix = 'experiment_run_form')
        elif participant_type == "adult":
            experiment_section_run_form = AdultExperimentSectionRunForm(initial = {'experiment_section': experiment_section}, prefix = 'experiment_run_form')
        elif participant_type == "child" and participant:
            child = Child.objects.get(pk=participant)
            experiment_section_run_form = ChildExperimentSectionRunForm(initial = {'experiment_section': experiment_section, 'participantChild': child}, prefix = 'experiment_run_form')
        else:
            experiment_section_run_form = ChildExperimentSectionRunForm(initial = {'experiment_section': experiment_section}, prefix = 'experiment_run_form')

        experiment_section_run_form.fields["assessor"].queryset = User.objects.filter(groups=experiment.lab.group)
    
    field_score_pairs = zip(experiment_section_fields, experiment_section_run_field_score_forms)
    return render(request, "ParticipantDB/ExperimentSectionRun/new2.html", {'experiment_section_name': experiment_section_name,'experiment_name': experiment_name, 'field_score_pairs': field_score_pairs ,'experiment_section_run_form': experiment_section_run_form, 'experiment_section_run_field_score_formset': experiment_section_run_field_score_forms, 'participant_type': participant_type})

@login_required
def experiment_section_run_detail(request, experiment_section_run_id):
    experiment_section_run = get_object_or_404(Experiment_Section_Run, pk=experiment_section_run_id)
    experiment_section_run_fields = Experiment_Section_Run_Field_Score.objects.filter(experiment_section_run = experiment_section_run)
    return render(request, 'ParticipantDB/ExperimentSectionRun/view.html', {'experiment_section_run': experiment_section_run, 'experiment_section_run_fields': experiment_section_run_fields})

@login_required
def delete_experiment_section_run(request, experiment_section_run_id):
    try:
        Experiment_Section_Run.objects.get(pk=experiment_section_run_id).delete()
        messages.success(request, 'Experiment Section run was successfully deleted')
        return redirect(reverse('index'))
    except Experiment_Section_Run.DoesNotExist:
        raise Http404("No experiment section run with id " + experiment_section_run_id)

@login_required
def update_experiment_section_run(request, experiment_section_run_id):
    pass