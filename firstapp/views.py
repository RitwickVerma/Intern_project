from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .utils.excel import *     #custom util (will grow with use)

def index(request):

    workbook=ExcelFile()
    worksheet=workbook.active_excelsheet()
    
    filtered_organisations=Organisations.objects.filter(id=1)

    column_headers=['NAME','DESCRIPTION','TEMPLATE NAME','OBJECT_ID','TYPE','DB_FIELD','DATA_TYPE','LABEL','REQUIRED','ACTIVE','DISABLED']
    worksheet.print_row(column_headers)

    organisation=filtered_organisations[0]
    list1=[organisation.name,organisation.description]
    filtered_templates=Template.objects.filter(project__name=organisation.name)
    
    for template in filtered_templates:
        list2=list1+[template.name,template.object_id,template.type]
        filtered_configurabletemplates=ConfigurableTemplate.objects.filter(template__name=template.name)
        
        for configurabletemplate in filtered_configurabletemplates:
            list3=list2+[configurabletemplate.db_field,configurabletemplate.data_type,configurabletemplate.label,'True' if configurabletemplate.required else 'False','True' if configurabletemplate.active else 'False','True' if configurabletemplate.disabled else 'False']
            worksheet.print_row(list3)

    workbook.save()

    return render(request,'firstapp/index.html')