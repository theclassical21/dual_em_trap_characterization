import pandas as pd
import numpy as np
def imdata_flist_df():
    path_to_flist = '../data/raw_images/file_list.txt'
    return pd.read_csv(path_to_flist, delimiter='\t')
def unpack_image(flists, time=0):
    path_to_files = '../data/raw_images/absorption_images/'
    
    leads = [" 'S' "," 'N' "," 'D' "," 'L' "]
    masks = [
            np.array(flists['cat'] == lc) &
            np.array(flists['time(s)'] == time)
            for lc in leads
            ]
    flist_specific_sloppy = [
            np.array(flists[mask]['file_list']) for mask in masks
            ]
    flist_specific = [
            flist[0][5:-3].split("', '")
            for flist in flist_specific_sloppy
            ]
    shadow, null, dark, alt_processed = [
                [
                pd.read_csv(
                    path_to_files + snda_file,
                    delimiter="\t",
                    header=None
                    )
                for snda_file in file
                ]
            for file in flist_specific
            ]
    return shadow, null, dark, alt_processed
