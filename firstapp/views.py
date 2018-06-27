from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .integration.resources import * 
from .integration import excel as excel_sheet


def index(request):

######################################################################################################
    
    #print_row prints a list to excel
    def print_row(excelsheet,datalist,row=1):
        for index,item in enumerate(datalist):
            excelsheet.add_cell(index=0, column=index, row=row, value=item, value_type='str')

#######################################################################################################
    
    excelsheet = excel_sheet.Excel('data.xlsx', ['Sheet1']) #Creating excel sheet object using excel.py
    
    filtered_organisations=Organisations.objects.filter(id=1).values()      #Getting organisations by id
    organisation=filtered_organisations[0]  #Getting organisation to search for

    column_headers=[]   #list of headers for each column

    column_headers_from_organisation ,temporary_list1=get_fields_values(organisation)  #get_fields_values is defined in .integration.resources.py, returns a tuple.
    column_headers+=column_headers_from_organisation

    filtered_templates=Template.objects.filter(project__name=organisation['name']).values() #Get templated based on selected organisation

    flag_for_column_headers=True   #To print column header as it needs to be printed only once

    all_data_from_right_subtree=[] #List of lists that will hold all the data from template side model subtree and written into excel later 

    for template in filtered_templates:  
        column_headers_from_template, temporary_list2 = get_fields_values(template)
        if(flag_for_column_headers):
            column_headers+=column_headers_from_template
        temporary_list2=temporary_list1+temporary_list2 #Temporary lists are used all around for storing data from previous level of model

        filtered_configurabletemplates=ConfigurableTemplate.objects.filter(template__name=template['name']).values()
        
        for configurabletemplate in filtered_configurabletemplates:
            column_headers_from_configurabletemplate, temporary_list3 = get_fields_values(configurabletemplate)
            if(flag_for_column_headers):
                column_headers+=column_headers_from_configurabletemplate
            temporary_list3=temporary_list2+temporary_list3

            if(flag_for_column_headers):
                column_headers=[x.upper() for x in column_headers] 
                flag_for_column_headers=False

            all_data_from_right_subtree.append(temporary_list3)


    filtered_subprojects=SubProject.objects.filter(organisation__name=organisation['name']).values()  #Get Subprojects based on selected organisation

    all_data_from_left_subtree=[] #List of lists that will hold all the data from subproject side model subtree and written into excel later 

    flag_for_column_headers=True
    for subproject in filtered_subprojects:  
        column_headers_from_subproject, temporary_list1 = get_fields_values(subproject)
        if(flag_for_column_headers):
            column_headers+=column_headers_from_subproject

        filtered_testtypes=TestType.objects.filter(project__name=subproject['name']).values()
         
        for testtype in filtered_testtypes:
            column_headers_from_testtype, temporary_list2 = get_fields_values(testtype)
            if(flag_for_column_headers):
                column_headers+=column_headers_from_testtype
            
            temporary_list2=temporary_list1+temporary_list2
            filtered_protocols=Protocol.objects.filter(test_type__name=testtype['name']).values()
        
            for protocol in filtered_protocols:
                column_headers_from_protocol, temporary_list3 = get_fields_values(protocol)
                if(flag_for_column_headers):
                    column_headers+=column_headers_from_protocol
                
                temporary_list3=temporary_list2+temporary_list3

                if(flag_for_column_headers):
                    column_headers=[x.upper() for x in column_headers]
                    flag_for_column_headers=False
                all_data_from_left_subtree.append(temporary_list3)


    all_data_in_tree=[]    #complete data in full tree
    for datarow_in_right_subtree in all_data_from_right_subtree:    #combining all data from both trees
        for datarow_in_left_subtree in all_data_from_left_subtree:
            all_data_in_tree.append(datarow_in_right_subtree+datarow_in_left_subtree)


    print_row(excelsheet,column_headers)
    for index, data_row in enumerate(all_data_in_tree):   #printing data into excel
        print_row(excelsheet,data_row,index+2)
    

    excel=excelsheet.export_xlsx()
    excel.save('data.xlsx')

    return render(request,'firstapp/index.html')