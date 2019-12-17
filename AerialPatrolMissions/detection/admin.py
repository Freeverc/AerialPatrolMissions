from django.contrib import admin
from .models import Image, Mission
# Register your models here.


class MissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'level')


admin.site.register(Image)
admin.site.register(Mission, MissionAdmin)
