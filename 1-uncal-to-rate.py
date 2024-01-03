# -*- encoding: utf-8 -*-
'''
@File    :   1-uncal-to-rate.py
@Time    :   2024/01/03
@Author  :   Mingyu Li
@Contact :   lmytime@hotmail.com
@Content :   This script is used to convert uncalibrated (uncal) data to calibrated (cal) data.
'''


# This step is very time-consuming
# So we run it in the py file instead of the notebook.

# Packages that allow us to get information about objects:
import os
import glob
import jwst

print('Pipeline version:', jwst.__version__)

#Uncomment below two lines if you have not defined CRDS elsewhere
os.environ['CRDS_PATH']= '/data/public/jwst_crds'
os.environ['CRDS_SERVER_URL'] = 'https://jwst-crds.stsci.edu'

# The entire calwebb_detector1 pipeline
from jwst.pipeline import calwebb_detector1

output_dir = './stage1/'

#Directory names for individual steps. If you are not interested in saving them please comment each line after this
output_dir_dq = output_dir+'dq/'
output_dir_saturation = output_dir+'saturation/'
output_dir_ipc = output_dir+'ipc/'
output_dir_firstframe = output_dir+'firstframe/'
output_dir_lastframe = output_dir+'lastframe/'
output_dir_reset = output_dir+'reset/'
output_dir_linearity = output_dir+'linearity/'
output_dir_rscd = output_dir+'rscd/'
output_dir_darkcurrent = output_dir+'darkcurrent/'
output_dir_refpix = output_dir+'refpix/'
output_dir_jump = output_dir+'jump/'
output_dir_rampfitting = output_dir+'rampfitting/'
output_dir_gainscale = output_dir+'gainscale/'

os.makedirs(output_dir, exist_ok=True)

#same as previous cell
# os.makedirs(output_dir_dq, exist_ok=True)
# os.makedirs(output_dir_saturation, exist_ok=True)
# os.makedirs(output_dir_ipc, exist_ok=True)
# os.makedirs(output_dir_firstframe, exist_ok=True)
# os.makedirs(output_dir_lastframe, exist_ok=True)
# os.makedirs(output_dir_reset, exist_ok=True)
# os.makedirs(output_dir_linearity, exist_ok=True)
# os.makedirs(output_dir_rscd, exist_ok=True)
# os.makedirs(output_dir_darkcurrent, exist_ok=True)
# os.makedirs(output_dir_refpix, exist_ok=True)
# os.makedirs(output_dir_jump, exist_ok=True)
# os.makedirs(output_dir_rampfitting, exist_ok=True)
# os.makedirs(output_dir_gainscale, exist_ok=True)

#If some parameters are known to have better results with certain value use the dictionary to edit those parameters
parameter_dict = {"dq_init": {"output_dir": output_dir_dq,"save_results": False},
                  "saturation": {"output_dir": output_dir_saturation,"save_results": False},
                  "ipc": {"output_dir": output_dir_ipc,"save_results": False},
                  "firstframe": {"output_dir": output_dir_firstframe,"save_results": False},
                  "lastframe": {"output_dir": output_dir_lastframe,"save_results": False},
                  "reset": {"output_dir": output_dir_reset,"save_results": False},
                  "linearity": {"output_dir": output_dir_linearity,"save_results": False},
                  "rscd": {"output_dir": output_dir_rscd,"save_results": False},
                  "dark_current": {"output_dir": output_dir_darkcurrent,"save_results": False},
                  "refpix": {"output_dir": output_dir_refpix,"save_results": False,"use_side_ref_pixels":False},
                  "jump": {"rejection_threshold": 5,"output_dir": output_dir_jump,"save_results": False}, # if one sees CR not being flagged properly, this is the step to modify
                  "ramp_fit": {"output_dir": output_dir_rampfitting,"save_results": False},
                  "gain_scale": {"output_dir": output_dir_gainscale,"save_results": False},
                 }

#Directory where the uncalibrated files are
input_dir='./uncal/'

list_files=glob.glob(input_dir+'*_uncal.fits')
print('No of files to be processed:', len(list_files))

# multi process to run the pipeline
from multiprocessing import Pool
from functools import partial

def run_pipeline_stage1(uncal_file, output_dir, save_results=True, steps=parameter_dict, logcfg='stage1-log.cfg'):
    print('File currently being processed:', uncal_file)
    # Call the pipeline method using the dictionary
    miri_output = calwebb_detector1.Detector1Pipeline.call(uncal_file, output_dir=output_dir, save_results=True, steps=parameter_dict,logcfg='stage1-log.cfg')

# If no multiprocessing is needed, use the following code
# for uncal_file in list_files:    
#     run_pipeline_stage1(uncal_file, output_dir)

# If multiprocessing is needed, use the following code
num_cores = 20
with Pool(num_cores) as p:
    p.map(partial(run_pipeline_stage1, output_dir=output_dir), list_files)