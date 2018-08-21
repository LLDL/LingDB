from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Family)
admin.site.register(Musical_Experience)
admin.site.register(Adult)
admin.site.register(Child)
admin.site.register(Speaks)
admin.site.register(IsExperiencedIn)
admin.site.register(Language)
admin.site.register(Experiment)
admin.site.register(Experiment_Section)