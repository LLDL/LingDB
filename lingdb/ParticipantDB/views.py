from django.http import HttpResponse
from .models import Adult
from .models import Child
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from .utils import make_unique_id

@login_required
def index(request):
    return render(request, 'ParticipantDB/index.html', {})

@login_required
def adult_detail(request, adult_id):
    adult = get_object_or_404(Adult, pk=adult_id)
    return render(request, 'ParticipantDB/adult_detail.html', {'adult': adult})

@login_required
def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'ParticipantDB/child_detail.html', {'child': child})

@login_required
def add_adult(request):
    if request.method == "POST":
        form = AdultForm(request.POST, initial={'id': make_unique_id()})
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AdultForm(initial={'id': make_unique_id()})
        return render(request, "ParticipantDB/adult_form.html", {'form': form})

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
        form = Musical_Skill_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = Musical_Skill_Form()
        return render(request, "ParticipantDB/musical_skill_form.html", {'form': form})