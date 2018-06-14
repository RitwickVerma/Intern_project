from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from openpyxl import Workbook

# Create your views here.
def index(request):
    #return HttpResponse("Hello from firstapp")
    wb=Workbook() 
    ws=wb.active
    ws.title="Organisations"
    wb.create_sheet(title="Template")
    wb.create_sheet(title="TemplateConfiguration")
    wb.create_sheet(title="ConfigurableTemplate")
    

    orgs=Organisations.objects.values()
    temp=Template.objects.values()
    tempconf=TemplateConfiguration.objects.values()
    conftemp=ConfigurableTemplate.objects.values()
    
    models=[orgs,temp,tempconf,conftemp]

    i=0
    for ws in wb:
        r=1
        c=1
        for o in models[i]:
            for val in o.values():
                ws.cell(row=r,column=c).value=val
                c+=1
            c=1
            r+=1
        i+=1

    wb.save("data.xlsx")
    return render(request,'firstapp/index.html')