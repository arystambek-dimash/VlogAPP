from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Vlogs)
admin.site.register(models.Comments)
admin.site.register(models.Documents)
admin.site.register(models.Videos)
admin.site.register(models.Images)