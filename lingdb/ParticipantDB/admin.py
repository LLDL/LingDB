from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Language)
admin.site.register(Musical_Skill)
admin.site.register(Experiment)
admin.site.register(Experiment_Section)
admin.site.register(Adult)
admin.site.register(Child)
admin.site.register(Family)
admin.site.register(IsExposedTo)
admin.site.register(Speaks)
admin.site.register(Musical_Experience)
admin.site.register(IsParentIn)
admin.site.register(IsChildIn)
admin.site.register(Participated)