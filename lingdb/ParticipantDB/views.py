from django.http import HttpResponse
from .models import Adult, Child, Family, Speaks, MusicalExperience, MusicalSkill, Language
# from .models import Adult, Child, Family, Speaks, Language
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.urls import reverse
from .utils import make_unique_id
from django.forms import inlineformset_factory

@login_required
def index(request):
    if request.method == 'GET' and request.GET.get('searchPeopleField', None):
        person = request.GET.get('searchPeopleField', None)
        try:
            adult = Adult.objects.get(pk=person)
            return redirect(reverse('adult_detail', kwargs={'adult_id': person}))
        except Adult.DoesNotExist:
            try: 
                child  = Child.objects.get(pk=person)
                return redirect(reverse('child_detail', kwargs={'child_id': person}))
            except Child.DoesNotExist:
                raise Http404("No Adult or Child matches id " + person)
    else:
        return render(request, 'ParticipantDB/index.html', {})


@login_required
def adult_detail(request, adult_id):
    adult = get_object_or_404(Adult, pk=adult_id)
    speaks = Speaks.objects.filter(person = adult)
    musical_exps = MusicalExperience.objects.filter(person = adult)
    return render(request, 'ParticipantDB/adult_detail.html', {'adult': adult, 'speaksLanguages': speaks, 'musical_exps': musical_exps})

@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'ParticipantDB/child_detail.html', {'child': child})

@login_required
def delete_adult(request, adult_id):
    try:
        Adult.objects.get(pk=adult_id).delete()
        return redirect(reverse('index'))
    except Adult.DoesNotExist:
        raise Http404("No adult with id" + adult_id)
    
@login_required
def delete_child(request, child_id):
    try:
        Child.objects.get(pk=child_id).delete()
        return redirect(reverse('index'))
    except Child.DoesNotExist:
        raise Http404("No child with id" + child_id)

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

            # return redirect('/')
            return redirect(reverse('adult_detail', kwargs={'adult_id': adult.id}))
        
    else:
        adult_form = AdultForm(initial={'id': make_unique_id()})

    return render(request, "ParticipantDB/adult_form.html", {'adult_form': adult_form, 'speaks_formset': speaks_forms, 'musical_experience_formset': musical_experience_forms})
    # return render(request, "ParticipantDB/adult_form.html", {'adult_form': adult_form, 'speaks_formset': speaks_forms})


@login_required
def add_child(request):
    exposure_forms = ExposureInlineFormSet(
        queryset = IsExposedTo.objects.none()
    )
    if request.method == "POST":
        form = ChildForm(request.POST)
        exposure_forms = ExposureInlineFormSet(request.POST, queryset = IsExposedTo.objects.none())
        if form.is_valid() and exposure_forms.is_valid():
            child = form.save(commit=False)
            child.save()
            exposedToLangs = exposure_forms.save(commit=False)
            for exposedToLang in exposedToLangs:
                exposedToLang.child = child
                exposedToLang.save()
                        
            return redirect('/')
    else:
        form = ChildForm(initial={'id': make_unique_id()})
        return render(request, "ParticipantDB/child_form.html", {'form': form, 'formset': exposure_forms})



@login_required
def add_language(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = LanguageForm()
        return render(request, "ParticipantDB/language_form.html", {'form': form})

@login_required
def add_musical_skill(request):
    if request.method == "POST":
        form = MusicalSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MusicalSkillForm()
        return render(request, "ParticipantDB/musical_skill_form.html", {'form': form})

@login_required
def add_family(request):
    if request.method == "POST":
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = FamilyForm()
        return render(request, "ParticipantDB/family_form.html", {'form': form})

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
            return redirect('/adult/' + str(adult_id))
    else:
        form = SpeaksForm(initial = {'person': adult})
    return render(request, "ParticipantDB/speaks_form.html", {'form': form})
    
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
            return redirect('/adult/' + str(adult_id))
    else:
        form = MusicalExperienceForm(initial = {'person': adult})
    return render(request, "ParticipantDB/musical_experience_form.html", {'form': form})
    