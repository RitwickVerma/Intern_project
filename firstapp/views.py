from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from openpyxl import Workbook

# Create your views here.
def index(request):
    #return HttpResponse("Hello from firstapp")
    wb=Workbook() 
    ws=wb.active
    
    orgs=Organisations.objects.all()

    def printtoexcel(lis,r):
        for i in range(len(lis)):
            ws.cell(row=r,column=i+1).value=lis[i]

    r=1
    for org in orgs:
        l1=[org.name,org.description]
        temps=Template.objects.filter(project__name=org.name)
        for temp in temps:
            l2=l1+[temp.name,temp.object_id,temp.type]
            conftemps=ConfigurableTemplate.objects.filter(template__name=temp.name)
            for conftemp in conftemps:
                l3=l2+[conftemp.db_field,conftemp.data_type,conftemp.label,conftemp.required,conftemp.active,conftemp.disabled]
                printtoexcel(l3,r)
                r+=1


    wb.save("data.xlsx")
    return render(request,'firstapp/index.html')