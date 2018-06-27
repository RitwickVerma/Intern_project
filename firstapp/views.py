from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .integration.resources import * 
from .integration import excel as excel_sheet


def index(request):

    def print_row(excelsheet,datalist,row=None):
        for index,item in enumerate(datalist):
            excelsheet.add_cell(index=0, column=index, row=row, value=item, value_type='str')


    excelsheet = excel_sheet.Excel('data.xlsx', ['Sheet1'])
    
    filtered_organisations=Organisations.objects.filter(id=1).values()

    column_headers=[]
    organisation=filtered_organisations[0]

    column_headers,temporary_list1=get_fields_values(organisation)
    row=1
    filtered_templates=Template.objects.filter(project__name=organisation['name']).values()
    flag=True
    for template in filtered_templates:
        x,temporary_list2=get_fields_values(template)
        column_headers+=x
        temporary_list2=temporary_list1+temporary_list2
        print(column_headers,temporary_list2)
        filtered_configurabletemplates=ConfigurableTemplate.objects.filter(template__name=template['name']).values()
        
        for configurabletemplate in filtered_configurabletemplates:
            y,temporary_list3=get_fields_values(configurabletemplate)
            column_headers+=y
            temporary_list3=temporary_list2+temporary_list3
            if(flag):
                print_row(excelsheet,[x.upper() for x in column_headers],row)
                flag=False
                row+=1
            print_row(excelsheet,temporary_list3,row)
            row+=1

    excel=excelsheet.export_xlsx()
    excel.save()

    return render(request,'firstapp/index.html')