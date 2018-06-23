from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .integration.resources import * 

def index(request):

    excelfile=ExcelFile()
    excelsheet=excelfile.active_excelsheet()
    
    filtered_organisations=Organisations.objects.filter(id=1).values()

    column_headers=[]
    organisation=filtered_organisations[0]

    column_headers,temporary_list1=get_lists_fields_values(organisation)

    filtered_templates=Template.objects.filter(project__name=organisation['name']).values()
    flag=True
    for template in filtered_templates:
        x,temporary_list2=get_lists_fields_values(template)
        column_headers+=x
        temporary_list2=temporary_list1+temporary_list2
        print(column_headers,temporary_list2)
        filtered_configurabletemplates=ConfigurableTemplate.objects.filter(template__name=template['name']).values()
        
        for configurabletemplate in filtered_configurabletemplates:
            y,temporary_list3=get_lists_fields_values(configurabletemplate)
            column_headers+=y
            temporary_list3=temporary_list2+temporary_list3
            if(flag):
                excelsheet.print_row([x.upper() for x in column_headers])
                flag=False
            excelsheet.print_row(temporary_list3)

    excelfile.save()

    return render(request,'firstapp/index.html')