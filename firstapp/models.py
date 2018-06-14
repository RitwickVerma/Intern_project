from django.db import models
from jsonfield import JSONField
#import ContentType
# Create your models here.
class Organisations(models.Model):
    name = models.CharField(max_length=248) #organisation name
    description = models.CharField(max_length=248, blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Organisations"

class Template(models.Model):
    name = models.CharField(max_length=127)
    project = models.ForeignKey(Organisations,on_delete=models.CASCADE,)
    sheet = JSONField(default=list)
 #   content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    type = models.CharField(max_length=127,default='template')
    def __str__(self):
        return self.name


class TemplateConfiguration(models.Model):
    field_sequence = models.IntegerField(default=0)
    def __str__(self):
        return str(self.field_sequence)

class ConfigurableTemplate(models.Model):
    template = models.ForeignKey(Template, related_name='config',on_delete=models.CASCADE,)
    db_field = models.CharField(max_length=31)
   # data_type = models.CharField(max_length=31, choices=CONFIG_DATATYPE_LIST)
    configurable_setting = JSONField()
    label = models.CharField(max_length=127)
    exceptions = JSONField(default=list, null=True, blank=True)
    required = models.BooleanField(blank=False)
    active = models.BooleanField(blank=False)
    disabled = models.BooleanField(blank=False)
    def __str__(self):
        return self.db_field
