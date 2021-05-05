import pandas as pd
import numpy as np
import gvar as gv

## imports a data frame that contains in each row a list which corresponds to
## all file names from a specific time corresponding to a specific image
## category (shadow, null, dark, L (just along for the ride) )
def imdata_flist_df():
    path_to_flist = '../data/raw_images/file_list.txt'
    return pd.read_csv(path_to_flist, delimiter='\t')

## uses a list containing lists of files as produced above to unpack the
## relevant txt files.
def unpack_image(flists, time=0):
    ## inputs flists and the time whose images need to be processed
    ## returns lists containing all the relevant shadows, nulls, darks, alts
    ## corresponding to the requested time.
    
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
    shadows, nulls, darks, alt_processeds = [
                [
                pd.read_csv(
                    path_to_files + file,
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
        return np.append(mat[:,-1:],mat[:,:-1],axis=1)
def clipper(OD,OD_sat=2.8):
    OD[ OD >= OD_sat] = 0
    return OD
def process_image(shadows, nulls, darks, OD_sat=2.8,f=1):
    OD_Meas = [
            np.log(( 1+abs( np.array(nulls)[i]-np.array(darks)[i]
                ))/(1+abs(np.array(shadows)[i]-np.array(darks)[i])))
            for i in range( len(shadows) )
            ]
    OD_Meas_clean = [ clipper(OD_M) for OD_M in OD_Meas ]
    OD_mod = [
            np.log( (1-np.exp(-OD_sat))/( np.exp(-OD_M)-np.exp(-OD_sat) ) )
            for OD_M in OD_Meas_clean
            ]
    OD_actual = [ OD_m + f*(1-np.exp(-OD_m)) for OD_m in OD_mod ]
    return OD_actual

def process_OD(OD_actual)
    i_max,j_max,k_max = len(OD_actual[0][0,:]), len(OD_actual[0][:,0]), len(OD_actual)
    I,J,K = np.arange(0,i_max,2),np.arange(0,j_max,2),np.arange(0,k_max,2)
    OD_statted = np.zeros([len(I),len(J),len(K)],dtype=str)
    for k in K:
       M = np.array(OD_actual[k])
       for i in I:
           for j in J:
               window = np.array([ 
                       M[i,j],
                       shift_mat(M)[i,j],
                       shift_mat(M,left = 0, direction = 1 )[i,j],
                       shift_mat(M,left = 0, direction = 0 )[i,j],
                       shift_mat(M,left = 1, direction = 1 )[i,j] ])
               OD_statted[int(i/2),int(j/2),k] = np.mean(window).astype(str) + '(' + np.std(window).astype(str) + ')'
               if not j%100:
                   print('j= ',j)
           if not i%10:
               print('i= ',i)
       print(k)
    return OD_statted

############## TEST #################
def TEST():
    flists = imdata_flists_df()
    s, n, d, a = unpack_image(flists)
    OD_Actual = process_image(s,n,d)

