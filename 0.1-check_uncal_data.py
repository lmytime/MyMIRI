# -*- encoding: utf-8 -*-
'''
@File    :   0.1-check_uncal_data.py
@Time    :   2024/01/05
@Author  :   Mingyu Li
@Contact :   lmytime@hotmail.com
'''

# Here we check the uncalibrated data.

# %%
import os
from glob import glob
from astropy.io import fits

MAST_dir = "/data/public/JWST-MAST-DATA/proposal_1837/MIRI/IMAGE/data"
uncal_dir = "./uncal"

uncal_files_path = glob(os.path.join(MAST_dir, "*/*_uncal.fits"))
print("Number of uncal files: ", len(uncal_files_path))
os.makedirs(uncal_dir, exist_ok=True)
for url in uncal_files_path:
    try:
        with fits.open(url) as hdul:
            pass
    except:
        # download the data
        print(f"Fixing {os.path.basename(url)}")
        uri_prefix = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/"
        os.system(f"rm {url}")
        os.system(f"wget {uri_prefix}{os.path.basename(url)} -O {url}")
# %%
