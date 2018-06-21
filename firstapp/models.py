from django.db import models
from jsonfield import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
CONFIG_DATATYPE_LIST = [

('int', 'int'), ('str',
'str'), ('singleselect',
'singleselect'),

('multiselect', 
'multiselect'), ('table', 
'table'), ('date', 
'date'),

('float', 
'float'), ('bool', 
'bool'), ('url', 
'url'),

('longstr', 
'longstr'), ('file', 
'file'), ('image', 
'image')]

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
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()
    type = models.CharField(max_length=127,default='template')
    def __str__(self):
        return self.name


class TemplateConfiguration(models.Model):
    field_sequence = models.IntegerField(default=0)
    def __str__(self):
        return str(self.field_sequence)

class ConfigurableTemplate(models.Model):
    template = models.ForeignKey(Template,related_name='config',on_delete=models.CASCADE,)
    db_field = models.CharField(max_length=31)
    data_type = models.CharField(max_length=31, choices=CONFIG_DATATYPE_LIST,default='int')
    configurable_setting = JSONField()
    label = models.CharField(max_length=127)
    exceptions = JSONField(default=list, null=True, blank=True)
    required = models.BooleanField(blank=False)
    active = models.BooleanField(blank=False)
    disabled = models.BooleanField(blank=False)
    def __str__(self):
        return 'configurable'+self.template.name

class SubProject(models.Model):
    name = models.CharField(max_length=248)
    description = models.CharField(max_length=248, blank=True, null=True)
    organisation = models.ForeignKey(Organisations,null=True, blank=True, on_delete=models.CASCADE)

class TestType(models.Model):
    name = models.CharField(max_length=127)
    project = models.ForeignKey(SubProject, related_name="test_type",on_delete=models.CASCADE)
    description = models.TextField(max_length=256, null=True, blank=True)

class Protocol(models.Model):
    name = models.CharField(max_length=127)#validators=[validate_special_character])
    description = models.TextField(max_length=256, null=True, blank=True)
    test_type = models.ForeignKey(TestType, related_name="protocol",on_delete=models.CASCADE)
    template = GenericRelation(Template)
    condition = JSONField(null=True, blank=True)
        