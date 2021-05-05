import numpy as np
import pandas as pd

## Cant really find the data i need to put this all together.
## Thought I had it, but it was not it
## Assume the existance of some data sets and maybe this would work.
## Put more time into the parts that I had data to work with so this
## part really sucks.

## Assuming that there is a 6XN tab seperated txt file with coloumns containing
##  x,y,z and vx,vy,vz for N atoms with headers
path = '/dummy'
x,y,z,vx,vy,vz = pd.read_csv(path,delimiter='\t')

## Assuming that the acceleration fields for OH in the appropriate state within
## our particular electrostatic trap are in three csvs containing
## the fields in three arrays
