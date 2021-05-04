import pandas as pd
import numpy as np
import gavar as gv
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
                for file in category
                ]
            for category in flist_specific
            ]
    return shadows, nulls, darks, alt_processeds
def shift_mat(mat,left = 1, direction = 0):
    if direction == 0 and left == 1:
        return np.append(mat[1:,:],mat[:1,:],axis=0)
    if direction == 0 and left == 0:
        return np.append(mat[-1:,:],mat[:-1,:],axis=0)
    if direction == 1 and left == 1:
        return np.append(mat[:,1:],mat[:,:1],axis=1)
    if direction == 1 and left == 0:
        return np.append(mat[:,-1:],mat[0,:-1],axis=1)

def process_image(shadows, nulls, darks, OD_sat=2.8,f=1):
    OD_Meas = [
            np.log(( 1+abs( nulls[i]-darks[i] ))/( 1+abs(shadows[i]-darks[i])))
            for i in range( len(shadows) )
            ]
    OD_mod = [
            np.log( (1-np.exp(-OD_sat))/( np.exp(-OD_M)-np.exp(-OD_sat) ) )
            for OD_M in OD_Meas
            ]
    OD_actual = [ OD_m + f*(1-np.exp(-OD_m)) for OD_m in OD_mod ]
    i_max,j_max,k_max = len(OD_actual[0][0,:]), len(OD_actual[0][:,0]), len(OD_actual)
    I,J,K = np.arange(0,i_max,2),np.arange(0,j_max,2),np.arange(0,k_max,2)
    OD_statted = np.zeros(len(I),len(J),len(K))
   for k in K:
       for i in I:
           for j in J:
               M = np.array(OD_actual[k])
               window = [ 
                       M[i][j] +
                       shift_mat(M)[i][j] +
                       shift_mat(M,left = 0, direction = 1 )[i][j] +
                       shift_mat(M,left = 0, direction = 0 )[i][j] +
                       shift_mat(M,left = 1, direction = 1 )[i][j]
                ]
               OD_statted[i/2][j/2][k/2] = gv.gvar(np.mean(window),np.std(window))
