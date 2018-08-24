from django.http import HttpResponse
from .models import Adult
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the DB index.")

def adult_detail(request, adult_id):
    return HttpResponse("Details of Adult %s." % adult_id)