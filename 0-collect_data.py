# %%
import os
from glob import glob

# Data are downloaded in a directory composed of many sub-directories
# We need to move _uncal.fits files to a directory named uncal

MAST_dir = "/data/public/JWST-MAST-DATA/dead_proposal_1837/MIRI/data"
uncal_dir = "./uncal"

uncal_files_path = glob(os.path.join(MAST_dir, "*/*_uncal.fits"))
print("Number of uncal files: ", len(uncal_files_path))
os.makedirs(uncal_dir, exist_ok=True)
for url in uncal_files_path:
    os.system(f"cp {url} {uncal_dir}")

# %%
import jwst
from astropy.io import fits
# If you want to directly use the _rate.fits data from MAST, you can use the following code to prepare the data
# Then you can skip the 1-uncal-to-rate.py step.
# But you have to make sure that the data are calibrated with the latest pipeline.
MAST_dir = "/data/public/JWST-MAST-DATA/dead_proposal_1837/MIRI/data"
uncal_dir = "./stage1"

uncal_files_path = glob(os.path.join(MAST_dir, "*/*_rate.fits"))
print("Number of rate files: ", len(uncal_files_path))
os.makedirs(uncal_dir, exist_ok=True)
jwst_versions = []
for url in uncal_files_path:
    os.system(f"cp {url} {uncal_dir}")
    jwst_versions.append(fits.getheader(url)['CAL_VER'])
jwst_version = list(set(jwst_versions))

print('The _rate.fits data were calibrated with the pipeline version:', jwst_version)
print('You are using jwst pipeline version:', jwst.__version__)

# %%
