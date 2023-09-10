# import pandas as pd
# import xlrd

# # df = []

# # with open_xlsm('/1-3-hcsa-fees-calculator_jan2022.xlsm') as wb:
# # YOU MUST PUT sheet_name=None TO READ ALL CSV FILES IN YOUR XLSM FILE


# This script is made for convert xlsm files to xlsx
# Used for pass xlsm file to phpExcel

import os
import zipfile
import shutil
import tempfile
import sys
from xml.dom import minidom
import pandas as pd

def to_xlsx(fname, *filenames):
    """
    This function create a xlsx file from
    xlsm file

    Args:
        fname (string): file to convert

    Filenames:
        name (string): string representing files tu update
    """
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(fname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
                    else:
                        zipwrite.writestr(item, update_files(
                                item.filename, zipread.read(item.filename)
                                ))
        os.remove(fname)
        fname = fname.split('.')[0]
        fname = fname + '.xlsx'
        shutil.move(tempname, fname)
    finally:
        shutil.rmtree(tempdir)


def update_files(filename, data):
    """
    This function dispatch the data for return good xml values
    Use it if you need to update more files
    """
    if '[Content_Types].xml' in filename:
        return update_content_types(data)

def update_content_types(data):
    """
    This function remove macro and set
    correct file type in headers
    """
    xml = minidom.parseString(data)
    types = xml.getElementsByTagName('Types')[0]
    for item in xml.getElementsByTagName('Types'):
        if item.hasAttribute('PartName') and item.getAttribute('PartName') == '/xl/vbaProject.bin':
            item.parentNode.removeChild(item)
    
    for item in types.getElementsByTagName('Override'):
        if item.hasAttribute('PartName') and item.getAttribute('PartName') == '/xl/workbook.xlk':
            item.setAttribute('ContentType', 'vnd.openxmlformats-officedocument.extended-properties+xml')
    return xml.toxml()

def to_csv():
    xls_file = r'/Download-Sample-File-xlsm.xlsx'
    output_csv = r'/Download-Sample-File-xlsm.csv'

    # Read the XLS file using pandas and openpyxl as the engine
    data = pd.read_excel(xls_file, engine='openpyxl')

    # Save the data as a CSV file
    data.to_csv(output_csv, index=False)

if __name__ == '__main__':
    file_path='/Download-Sample-File-xlsm.xlsm'
    f = ''
    if f == '': f = file_path
    to_xlsx(f, '[Content_Types].xml')
    to_csv()

