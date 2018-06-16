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
    
    models=[Organisations,Template,TemplateConfiguration,ConfigurableTemplate]

    i=0
    for ws in wb:
        c=1
        m = models[i]._meta.get_fields() 
        lis = [item.get_internal_type() for item in m]
        lis=list(filter(lambda a:a!='ForeignKey',lis))
        lis=list(filter(lambda a:a!='AutoField',lis))
        print(m)
        print(lis)
        for field in lis:
            ws.cell(row=1,column=c).value=field
            c+=1
        i+=1
  

    wb.save("data.xlsx")
    return render(request,'firstapp/index.html')