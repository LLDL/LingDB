from django.http import HttpResponse
from .models import Adult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404

@login_required
def index(request):
    return render(request, 'ParticipantDB/index.html', {})

def adult_detail(request, adult_id):
    try:
        adult = Adult.objects.get(pk=adult_id)
    except Adult.DoesNotExist:
        raise Http404("Adult does not exist")
    return render(request, 'ParticipantDB/adult.html', {'adult': adult})
