import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gvar as gv
import lsqfit

############################# EVOLVED WIDTH FUNC #############################
## Defines a function that evolves the cloud widths through time,
##    one time input and one array output with all three widths at that time.

## This function uses 15 hardcoded parameters to determine the widths.
## I may potentially update this with an actual fit for the data,
##    in one direction at least as an example calculation.
## For each axis there are three contributions to the width at any given time,
##    there are then three width parameters for each of three axis.
## We organize these into arrays,
##    each of which contains one of the widths for each axis.
## Two of these contributions are transients each with a respective lifetime,
##    there are then two time parameters for each axis.
## These arrays are repeated for each time step,
##    i.e. if t is a single value these arrays have a single coloumn.
##    but if t is  1xN shaped, the resultant arrays have repeated coloumns.
def evolve_widths(t=0):
    ## Determines if we need to produce 3xN outputs,
    ##    sets a variable, num_time_steps, to carry this information.
    num_time_steps = np.size(t)
    if num_time_steps > 1:
        t = np.array(3*[t])
    else:
        t = np.array([3*[t]]).transpose()
    #Defines the 15 variables, organized as stated.
    L1,L2,L3 = np.array([
                num_time_steps*[0.18,0.74,0.59],
                num_time_steps*[0.08,0.14,0.09],
                num_time_steps*[0.35,0.55,0.34]
            ])
    B1,B2 = np.array([
                num_time_steps*[0.07,0.08,0.05],
                num_time_steps*[0.75,1.18,1.02]
            ])
    ## Reshapes the above in the appropriate way,
    ##    reshaped as such then transposed to avoid jumbling up the elements.
    ## Want to keep rows as X,Y, or Z and coloumns as time.
    L1, L2, L3, B1, B2 = [
            L.reshape(num_time_steps,3).transpose() for L in [L1,L2,L3,B1,B2]
            ]
    #Returns the width as a 3 element array by appending the time dependance
    OUT_pre = np.multiply(L1,np.exp(-t/B1))+np.multiply(L2,np.exp(-t/B2))+L3 
    OUT = OUT_pre.transpose()
    return OUT
########################### END EVOLVED WIDTH FUNC ###########################


################################## X WIDTHS ##################################
## Simpler implementation of evolve_widths.
## Evolve widths in one dimension to be used for fitting,
##    with variable parameters for lsqfitting.
## Inputs the time and choice of length and time parameters.
## Outputs the modeled width of the cloud at that time.

def x_widths(t,p):
    ### All fit:
    # return p[0]*np.exp(-t/p[3])+p[1]*np.exp(-t/p[4])+p[2]

    ## Time fit:
    return 0.18*np.exp(-t/p[0])+0.08*np.exp(-t/p[1])+0.35
################################ END X WIDTHS ################################

################################## FIT DATA ##################################

### All fit:
#def fitter(guess=[0.18,0.08,0.35,70,750]):

### time fit:
def fitter(guess=[70,750]):
    path_to_data = '../data/widthsVtime_8kV.txt'
    measurement_df = pd.read_csv(path_to_data,'\t')
    col_names = ['time (ms)', 'width (cm)', 'unc (cm)']
    x,y,unc = [
        np.array(measurement_df[col]) for col in col_names
        ]
    measurement_stat = gv.gvar(y,unc)
    fit = lsqfit.nonlinear_fit(data=(x, measurement_stat), p0=guess, fcn=x_widths)
    plt.plot(x,x_widths(x,guess),'r.')
    def plot_gvar(x,y_gv):
        return plt.errorbar(x, gv.mean(y_gv), yerr=gv.sdev(y_gv),
                linestyle='', marker='o')
    plot_gvar(x,measurement_stat)
    print(y)
    params = np.array([ el.mean for el in fit.p])
    print(params)
    plt.plot(x,x_widths(x,params),'g.')
    print(fit)
################################ END FIT DATA ################################
