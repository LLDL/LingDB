# Django Imports ----------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

# Project Imports ---------------------------------------------------------------
from .forms import AdultForm, ChildForm, ExposureForm, ExposureInlineFormSet, FamilyForm, LanguageForm, MusicalExperienceForm, MusicalExperienceFormSet, MusicalExperienceInlineFormSet, MusicalSkillForm, SpeaksForm, SpeaksFormSet, SpeaksInlineFormSet
from .models import *
from .utils import make_unique_id

# Index Views -------------------------------------------------------------------

@login_required
def index(request):
    
    if (request.method == 'GET') and (request.GET.get('searchPeopleField', None)):
        # Open by ID Handling
        person = request.GET.get('searchPeopleField', None)
        try:
            Adult.objects.get(pk=person)
            return redirect(reverse('adult_detail', kwargs={'adult_id': person}))
        except Adult.DoesNotExist:
            try: 
                Child.objects.get(pk=person)
                return redirect(reverse('child_detail', kwargs={'child_id': person}))
            except Child.DoesNotExist:
                raise Http404("No Adult or Child matches id " + person)
    else:
        # Standard Visit to Index
        return render(request, 'ParticipantDB/index.html')

# Family Views -----------------------------------------------------------------

@login_required
def add_family(request):
    if request.method == "POST":
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = FamilyForm()
        return render(request, "ParticipantDB/family_form.html", {'form': form})


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
            print(speaks_forms)
            if speaks_forms.is_valid():
                for speaks_form in speaks_forms:
                    if speaks_form.cleaned_data.get('DELETE'):
                        print('Delete:')
                        print(speaks_form.cleaned_data.get('lang'))
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
                        print('Delete:')
                        print(musical_experience_form.cleaned_data.get('experience'))
                        print(musical_experience_form.cleaned_data.get('experience'))
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
    return render(request, 'ParticipantDB/adult_detail.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps})

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
                oldExposures = IsExposedTo.objects.filter(child=child_inst)
                if oldExposures.exists():
                    oldExposures.delete()
                for exposure_form in exposure_forms:
                    if exposure_form.cleaned_data.get('lang'):
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
    return render(request, 'ParticipantDB/child_detail.html', {'child': child, 'languages_exposed_to': languages_exposed_to})

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

@login_required
def add_speaks(request, adult_id):
    adult = Adult.objects.get(pk=adult_id)
    if request.method == "POST":
        form = SpeaksForm(request.POST, instance = adult)
        if form.is_valid():
            adult_mod = form.save(commit=False)
            adult_mod.save()
            speaksLanguage = Speaks()
            speaksLanguage.person = adult
            speaksLanguage.lang = form.cleaned_data['lang']
            speaksLanguage.is_native = form.cleaned_data['is_native']
            speaksLanguage.nth_most_dominant = form.cleaned_data['nth_most_dominant']
            speaksLanguage.age_learning_started = form.cleaned_data['age_learning_started']
            speaksLanguage.age_learning_ended = form.cleaned_data['age_learning_ended']
            speaksLanguage.save()
            return redirect(reverse('adult_detail', kwargs={'adult_id': adult_id}))
            # return redirect('/adult/' + str(adult_id))
    else:
        form = SpeaksForm(initial = {'person': adult})
    return render(request, "ParticipantDB/speaks_form.html", {'form': form})

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
  
@login_required
def add_musical_experience(request, adult_id):
    adult = Adult.objects.get(pk=adult_id)
    if request.method == "POST":
        form = MusicalExperienceForm(request.POST, instance = adult)
        if form.is_valid():
            adult_mod = form.save(commit=False)
            adult_mod.save()
            hasMusicalExperience = MusicalExperience()
            hasMusicalExperience.person = adult
            hasMusicalExperience.experience = form.cleaned_data['experience']
            hasMusicalExperience.nth_most_dominant = form.cleaned_data['nth_most_dominant']
            hasMusicalExperience.age_learning_started = form.cleaned_data['age_learning_started']
            hasMusicalExperience.age_learning_ended = form.cleaned_data['age_learning_ended']
            hasMusicalExperience.save()
            return redirect(reverse('adult_detail', kwargs={'adult_id': adult_id}))
            # return redirect('/adult/' + str(adult_id))
    else:
        form = MusicalExperienceForm(initial = {'person': adult})
    return render(request, "ParticipantDB/musical_experience_form.html", {'form': form})
    