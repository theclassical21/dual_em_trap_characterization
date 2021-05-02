import numpy as np
import matplotlib.pyplot as plt

############################## ATOMIC CLOUD CLASS ##############################
## Defines a class to encapsulate mean field properties of an atomic cloud.
## Specifically this class has two attributes fully specified on instance,
##    these define the initial trapped population and the 

class atomic_Cloud:
    #################### CLASS INITIALIZATION, ATOMIC CLOUD ###################
    ## Initializes the cloud,
    ##    setting the default widths of the cloud to unity and the default
    ##    initial population to 1e7 atoms.
    def __init__(self, widths=[1,1,1],trapped_Pop=1e7):
        self.dimensions = widths
        self.n_Atoms = trapped_Pop

    ######################### CLOUD DENSITY FUNCTION #########################
    ## Uses an input position, r at the origin by default, and the class
    ##    attributes defined above to model the density of the atomic cloud 
    def cloud_density(self,r=[0,0,0]):
        ## Unpacks dimensions of the cloud and the position vector provided,
        ##   purely for legibility.
        X,Y,Z = self.dimensions
        x,y,z = r
       
        ## Defines an effective volume and number of atoms at r.
        eff_Volume = (2*np.pi)**1.5*X*Y*Z
        eff_number = self.n_Atoms*np.exp( -0.5*( (x/X)**2+(y/Y)**2+(z/Z)**2 ) )
        return eff_Volume/eff_number

    ######################### CLOUD DENSITY FUNCTION #########################

    ######################### FWHM of Width FUNC #############################
    ## Sol'n to 1/2 = exp(-0.5 delta**2/width**2), term by term for the input
    ##    widths array.
    ## Inputs self, returns an array of the same size of FWHM's
    def fwhm_width(self):
        return 2*np.sqrt(-2*np.log(0.5)*self.dimensions**2)
    ####################### END FWHM of Width FUNC ###########################

########################### END ATOMIC CLOUD CLASS ###########################
