# import needed libraries
import logging
import json
import os
from datetime import datetime
import numpy as np
import pandas as pd
import functions as func
import search_arrays as sa

# TODO Possibly pivot data

# How long is this gonna take?
begin_time = datetime.now()

# Create and configure logger
LOG_FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(filename=".\Debug.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()

# create the empty lists that will hold the data from each test type
pre_data_output = []
pre_leq_output = []
reg_data_output = []
reg_leq_output = []
pst_data_output = []
pst_leq_output = []
mpl_data_output = []

# Create a list of all the files in a particular directory/sub-directory
filePath = 'CHASMPAS 2020 ITX Tablet Data'
testFiles = []
for root, dirs, files in os.walk(filePath):
    for file in files:
        if file.endswith('.json'):
            testFiles.append(os.path.join(root, file))

# use the json.load function to load a json file
for file in testFiles:

    # with open(file) as j_file:
    # file2 = 'CHASMPAS 2020 ITX Tablet Data\\023-1 post m7 1.json'
    with open(file) as j_file:
        data = json.load(j_file)
        # call the testtype function
        tt = func.testtype(data)
        if tt == 'pre':
            tmp_dict = sa.pre_test_dict.copy()
            r = func.parsetestfile(file, data, sa.pre_test_array, tmp_dict)
            # this returns the pre_test_dictionary
            # need to run triple digit now.
            td, tde = func.tripledigitparse(data)
            # iterate through the triple digit and update the pre_test_dictionary
            for k, v in td.items():
                r[k] = v
            # add the updated dictionary to the output list
            pre_data_output.append(r)
            # iterate through the triple digit exam results and update the pre_test_dictionary
            for k, v in tde.items():
                r[k] = v
            # gather the F/L branches in the FLFT
            flft_right, flft_left = func.flft(data)
            if flft_right is not None:
                r['FLFT_Right_F/L'] = flft_right
            if flft_left is not None:
                r['FLFT_Left_F/L'] = flft_left
            # add the updated dictionary to the output list
            pre_data_output.append(r)
            # perform the Leq part of the exam
            tmp_leq_dict = sa.leq_test_dict.copy()
            leq = func.parsetestfile(file, data, sa.leq_test_array, tmp_leq_dict)
            pre_leq_output.append(leq)

        elif tt == 'reg':
            tmp_dict = sa.reg_test_dict.copy()
            r = func.parsetestfile(file, data, sa.reg_test_array, tmp_dict)
            # this returns the reg_test_dictionary
            # need to run triple digit now.
            td, tde = func.tripledigitparse(data)
            # iterate through the triple digit and update the reg_test_dictionary
            for k, v in td.items():
                r[k] = v
            # add the updated dictionary to the output list
            reg_data_output.append(r)
            # iterate through the triple digit exam results and update the reg_test_dictionary
            for k, v in tde.items():
                r[k] = v
            # gather the F/L branches in the FLFT
            flft_right, flft_left = func.flft(data)
            if flft_right is not None:
                r['FLFT_Right_F/L'] = flft_right
            if flft_left is not None:
                r['FLFT_Left_F/L'] = flft_left
            # add the updated dictionary to the output list
            reg_data_output.append(r)
            # perform the Leq part of the exam
            tmp_leq_dict = sa.leq_test_dict.copy()
            leq = func.parsetestfile(file, data, sa.leq_test_array, tmp_leq_dict)
            reg_leq_output.append(leq)

        elif tt == 'pst':
            tmp_dict = sa.pst_test_dict.copy()
            r = func.parsetestfile(file, data, sa.pst_test_array, tmp_dict)
            # this return the pst_test_dictionary
            # need to run triple digit now.
            td, tde = func.tripledigitparse(data)
            # iterate through the triple digit and update the pst_test_dictionary
            for k, v in td.items():
                r[k] = v
            # add the updated dictionary to the output list
            pst_data_output.append(r)
            # iterate through the triple digit exam results and update the pst_test_dictionary
            for k, v in tde.items():
                r[k] = v
            # gather the F/L branches in the FLFT
            flft_right, flft_left = func.flft(data)
            if flft_right is not None:
                r['FLFT_Right_F/L'] = flft_right
            if flft_left is not None:
                r['FLFT_Left_F/L'] = flft_left
            # add the updated dictionary to the output list
            pst_data_output.append(r)
            # perform the Leq part of the exam
            tmp_leq_dict = sa.leq_test_dict.copy()
            leq = func.parsetestfile(file, data, sa.leq_test_array, tmp_leq_dict)
            pst_leq_output.append(leq)

        elif tt == 'mpl':
            tmp_dict = sa.mpl_test_dict.copy()
            r = func.mpanlparse(file, data, tmp_dict)
            if r is False:
                logger.info('This mpl file errored. There was no mpanlsData branch: ' + str(file))
            else:
                mpl_data_output.append(r)

        elif tt == 'Unknown':
            logger.info('This file had no test type: ' + file)
# End of for loop

# Data Output file to excel.
# Use pandas to write Pre data to excel
df = pd.DataFrame(pre_data_output)
writer = pd.ExcelWriter('test2.xlsx')
df.to_excel(writer, 'Pre data', index=False)
writer.save()

# Use pandas to write Pre Leq data to excel
df = pd.DataFrame(pre_leq_output)
df.to_excel(writer, 'Pre Leq data', index=False)
writer.save()

# Use pandas to write Reg data to excel
df = pd.DataFrame(reg_data_output)
df.to_excel(writer, 'Reg data', index=False)
writer.save()

# Use pandas to write Pre Leq data to excel
df = pd.DataFrame(reg_leq_output)
df.to_excel(writer, 'Reg Leq data', index=False)
writer.save()

# Use pandas to write Post data to excel
df = pd.DataFrame(pst_data_output)
df.to_excel(writer, 'Post data', index=False)
writer.save()

# Use pandas to write Pre Leq data to excel
df = pd.DataFrame(pst_leq_output)
df.to_excel(writer, 'Post Leq data', index=False)
writer.save()

# Use pandas to write MPANL data to excel
df = pd.DataFrame(mpl_data_output)
df.to_excel(writer, 'MPANL data', index=False)
writer.save()

print(datetime.now() - begin_time)

# getting creative here. Delete from here to end when done.
