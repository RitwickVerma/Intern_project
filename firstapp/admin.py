from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Organisations)
admin.site.register(Template)
admin.site.register(TemplateConfiguration)
admin.site.register(ConfigurableTemplate)
admin.site.register(SubProject)
admin.site.register(TestType)
admin.site.register(Protocol)