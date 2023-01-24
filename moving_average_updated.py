# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:57:04 2022

@author: nano-bio
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import signal
import tkinter as tk


# add the sourcepath to your datafile and optionally select a savepath where you want it to be saved to. by default, the processed data is saved in the same directory the initial data was taken from.
SourcePath = r''
SavePath = SourcePath
os.chdir(SourcePath)

# insert the name of the specific data file (for example 'data.tex'
filename = ""

# if you get the Error 'list index out of range', check if the txt file has the correct delimiter (for example d='\t' for spaces or d=',' for commas)
d = '\t'
Yield = np.loadtxt(filename ,skiprows=2, usecols=1, encoding=None, delimiter = d)
n = np.loadtxt( filename ,skiprows=2, usecols=0, delimiter = d , dtype='int')

# setting the number of datapoints left and right, you want to use for the moving average
window_radius = 3

# introducing a gaussian weighting with the desired std (standard deviation, not herpes)
std = 1
weight = signal.gaussian(window_radius * 2 + 1, std)
weight[weight == 1]= 0
#testweight = np.array([1,2,3,0,5,6,7])

# set the number of decimal points you want your moving average data to show
dp = 12
  
# initialize an empty list to store moving averages
moving_averages = []
  
i = 0

# this while loop, iterates through i, takes the adjacent values to the i-th datapoint whitin the window_radius and multiplies a weighting to the neighbours in dependance to the distance to the i-th datapoint.
# subsequently, the average of each of these points with their weighted neighbours is taken and saved into the 'moving_averages' array.
# when i < the first or > last 'window_radius' points, the window is shrunk down to the corresponding side. (for example: left side is shrunk dowwn for i < window_size)
while i < len(Yield):
     
    if i < window_radius  :
        
        window = Yield[  : i + window_radius + 1]
       
        window = window * weight[ window_radius - i : ]
      
        window_average = round(sum(window) / len(window), dp)
        
        moving_averages.append(window_average)
        
        i += 1 

    elif window_radius <= i < len(Yield) - window_radius - 1:
       
            # Store elements from i to i+window_size
            # in list to get the current window
            window = Yield[ i - window_radius : i + window_radius + 1]
   
            # weighting the moving average
            window = window * weight
           
            # Calculate the average of current window
            window_average = round(sum(window) / len(window), dp)
              
            # Store the average of current
            # window in moving average list
            moving_averages.append(window_average)
              
            # Shift window to right by one position
            i += 1
    else:
    #len(Yield) -1 - window_size < i :
        
        window = Yield[ i - window_radius   : ]
        
        window = window * weight[ : (len(Yield) - i + window_radius)]
       
        window_average = round(sum(window) / len(window), dp)
        
        moving_averages.append(window_average)
        
        i += 1 


moving_averages=np.array(moving_averages)


# Yield_cut = Yield[-(len(Yield)-int((window_size -1)/2)):-int((window_size -1)/2)]
# n_cut = n[-(len(Yield)-int((window_size -1)/2)):-int((window_size -1)/2)]

# calculate the Yield/Yield_ma
I = np.divide(Yield,moving_averages)

# saving the new data to a csv file in the sourcepath

dict = {'n' : n, 'Yield': Yield, 'Yield_ma': moving_averages, 'Yield/Yield_ma': I}

df = pd.DataFrame(dict)
df.to_csv( SavePath + '\\' +  filename[:-4] + 'moving_average_updated.csv', index = False,)

#plot the data
# plt.plot(n, I, marker = 'x')
# plt.xlabel('n')
# plt.ylabel('I/I_ma')
# output = hstack((n_cut.flatten(),Yield_cut.flatten(),moving_averages.flatten(), I.flatten()))
# pd.DataFrame(output).to_csv(filename[:-4] + 'moving_average.csv', header=['n','Yield', 'Yield_ma', 'Yield/Yield_ma'])


# print(output)
# np.savetxt(filename[:-4] + 'moving_average.csv',output ,delimiter=',', header="n,Yield, Yield_ma, Yield/Yield_ma",fmt="%i")
