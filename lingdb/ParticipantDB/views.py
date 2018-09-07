from django.http import HttpResponse
from .models import Adult
from .models import Child
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from ParticipantDB.forms import *
from django.views.generic.edit import CreateView

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

class AdultCreate(CreateView):
    model = Adult
    fields = ['id','given_name','preferred_name','surname','birth_date','gender','sfu_id','address','years_of_education','phone','email','contact_pref','pref_phone_time','health_notes','languages','musical_background']


