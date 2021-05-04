import pandas as pd
import numpy as np
def imdata_flist_df():
    path_to_flist = '../data/raw_images/file_list.txt'
    return pd.read_csv(path_to_flist, delimiter='\t')
def unpack_image(flists, time=0):
    leads = ['S','N','D','L']
    masks = [
            flists['cat'] == lc for lc in leads
            ]
    flist_specific = flists['file_list'][mask]
    col_name = np.linpace(-1,1,100)
    shadow, null, dark, alt_processed = [
            pd.read_csv(
                    flist_specific[mask],
                    delimiter="\t",
                    columns=col_name
                    ) for mask in masks
            ]
    return shadow, null, dark, alt_processed
