from openpyxl import Workbook

class ExcelSheet:
    def __init__(self,excelfile):                                       
        self.excelsheet=excelfile.active
        self.set_current_row()

    
    def get_current_row(self):
        return self.current_row
    
    
    def set_current_row(self,row=1):
        self.current_row=row


    #prints a complete row into excel sheet and pointer(current_row) is incremented (1 based indexing)
    #If row is specified, data will be overwritten in that row if
    def print_row(self,datalist,row=None):
        if(row==None):
            row=self.get_current_row()
        
        for i in range(len(datalist)):
            self.excelsheet.cell(row=row,column=i+1).value=datalist[i]
        
        if(row==self.get_current_row()):
            self.current_row+=1
        elif(row>self.current_row):
            self.current_row=row
    


class ExcelFile:
    def __init__(self):
        self.excelfile=Workbook()
        self.excelsheet=ExcelSheet(self.excelfile)
        self.excelsheets=[]
        self.excelsheets.append(self.excelsheet)
        self.current_active_sheet_index=0

    def get_active_worksheet(self):
        return self.excelsheets[self.current_active_sheet_index]

    def get_active_worksheet_index(self):
        return self.current_active_sheet_index

    def save(self,name='data.xlsx'):
        self.excelfile.save(name)



