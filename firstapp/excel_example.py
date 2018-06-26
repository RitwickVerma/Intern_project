# This is Example file
from integration import excel as excel_sheet

existing_template_path='this is file path'
template_sheet_list = ['sheet1', 'sheet2']
template_index = 0
column_index = 0
row_index = 0
data = 'this is data what you want to write'
data_type = 'this is type of data'

'''
    Intialization of excel sheet
    1. Already saved file(template) is used for download
    2. Intialize your excelfile like below
    3. template_sheet_list -> is sheet names in excel sheet 
'''
excel = excel_sheet.Excel(existing_template_path, template_sheet_list)

'''
    Get data and add in cell
    1. Add data like below
    2. Excel.py code works for multiple template so template_index is required
'''
excel.add_cell(index=template_index, column=column_index, row_index=row_index, data='value', data_type='str')