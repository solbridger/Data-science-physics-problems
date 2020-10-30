#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:32:42 2019

@author: solbridger
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
import tkinter as tk
import tkinter.filedialog as filedialog
dcs = [0.0005, 0.005] #Decay constants (initial parameters)
N_79_Sr_0 = 1 * (10 ** -6) * 6.022 * (10 ** 23) 

def file_open():
    
    select_file = tk.Tk()
    filepath = filedialog.askopenfilename(filetypes = [('csv files', '*.csv')]) 
    select_file.update()
    
    return filepath

filepaths = [file_open(), file_open()]
"""
The function below formats the data into time order, removes invalid values and converts into the correct units.
"""
def clean_and_convert_data():
    
    filepath_1 = filepaths[0]; filepath_2 = filepaths[1]

    data_file_1 = np.genfromtxt(filepath_1, comments = '%', delimiter = ',', skip_header = 1)
                                                                                            #Reads in both data files
    data_file_2 = np.genfromtxt(filepath_2, comments = '%', delimiter = ',', skip_header = 1)

    data_file = np.concatenate((data_file_1, data_file_2)) #Joins the two data sets
    
    clean_data = np.reshape(data_file, (-1,3)) #Reshapes the array
      
    clean_data = clean_data[~np.isnan(clean_data).any(axis = 1)] #Removes all nans
    
    clean_data[:,1] *= 10 ** 12; clean_data[:,2] *= 10 ** 12; clean_data[:,0]  *= 3600 #Converts into required units
    
    clean_data = clean_data[clean_data[:,2] > 0] #Removes all uncertainty data values <= 0
    
    clean_data = clean_data[np.argsort(clean_data[:,0]),:] #Sorts the data by row according to the value in the first column
    
    return clean_data
"""
The function below removes outliers from the data set by ensuring the data
points lie within 3 standard deviations of the residual fit.
"""
def outlier_removal():
    
    clean_data = clean_and_convert_data()
    
    true_data = np.zeros((0,3)) #Creates empty array
    
    for i in range(len(clean_data)):
        
        if abs(A_79_Rb_calc(dcs, clean_data[i,0]) - clean_data[i,1]) < 3 * np.mean(clean_data[:,2]): #Residual test on dataset.
            
            temp = np.array((clean_data[i,0], clean_data[i,1], clean_data[i,2]))
            
            true_data = np.vstack((true_data, temp)) #Creates new array with the true, fitted data.
            
        else:
            pass
        
    return true_data
"""
The function below calculates the decay constants from the input data.
"""
def N_79_Rb_calc(dcs, t):
    
    dc_79_Rb = dcs[0]
    
    dc_79_Sr = dcs[1]
    
    N_79_Rb = (N_79_Sr_0 * dc_79_Sr * (np.exp(-dc_79_Sr * t) - np.exp(-dc_79_Rb * t))) / (dc_79_Rb - dc_79_Sr) #Theoretical function
    
    return N_79_Rb
"""
The function below calculates the Activity of the of the Rubidium 79.
"""
def A_79_Rb_calc(dcs, t):
    
    dc_79_Rb = dcs[0]
    
    A_79_Rb = dc_79_Rb * N_79_Rb_calc(dcs, t)
    
    return A_79_Rb
"""
The function below calculates the half lives of the Rubidium 79 sample and the Strontium 79 sample.
"""
def half_life_calc(dcs):
    
    t_half_Rb, t_half_Sr = np.log(2) / dcs[0]  , np.log(2) / dcs[1] #Half life calculation
    
    t_half_Rb /= 60 ; t_half_Sr /= 60 #Conversion of half lifes into minutes
    
    return t_half_Rb, t_half_Sr 
"""
The function below calculates the chi-squared distribution for the true data set.
"""
def chi_squared(dcs):
    
    true_data = outlier_removal()
    
    activity_Rb = A_79_Rb_calc(dcs, true_data[:,0])
    
    chi_sq = np.sum(np.square((true_data[:,1] - activity_Rb) / true_data[:,2])) 
    
    return chi_sq
"""
The function below calculates the value for the reduced chi-squared of the true data set.
"""
def reduced_chi_squared(true_data):
    
    red_chi_sq = chi_squared(dcs) / (len(true_data[:,0]) - 1)
    
    return red_chi_sq
"""
The function below minimizes the chi-squared distribution of the data set to obtain values for the
decay constants of the Rubidium 79 sample and the Strontium 79 sample.
"""
def minimize_function(dcs, true_data, t):
    
    minimized_chi_squared = fmin(chi_squared, dcs, disp = 0) #fmin function find the dcs values for which chi squared is minimized
    
    dcs[0] = minimized_chi_squared[0]; dcs[1] = minimized_chi_squared[1] #Returns the new array of the decay constants
    
    return minimized_chi_squared[0], minimized_chi_squared[1]
"""
The function below plots the graph for the activity against time for the data set and produces a fit.
"""
def graph_plot(true_data):
    
    figure = plt.figure()
    axes = figure.add_subplot(111)
    axes.plot(true_data[:,0], A_79_Rb_calc(dcs, true_data[:,0]) * (10 ** -12), color = 'red')
    axes.errorbar(true_data[:,0], A_79_Rb_calc(dcs, true_data[:,0]) * (10 ** -12), true_data[:,2] * (10 ** -12), linestyle = 'none',
                  label = 'actvitity data', marker = 'o', mec = 'red',ecolor = 'black', markersize = 3, capsize = 5, capthick = 1)
    axes.grid(True, color = 'black', dashes = (4,8))
    axes.set_title('Activity of Rubidium 79 sample against time', fontsize = 16, fontname = 'Arial', color = 'black')
    axes.set_xlabel('Time / s', fontname = 'Arial', fontsize = 14)
    axes.set_ylabel('Activity / TBq', fontname = 'Arial', fontsize = 14)
    axes.set_xlim(0, 4000)
    plt.savefig('Activity vs time plot for Rubidium 79.png', dpi = 300)
"""
The function below is a main function, meaning it executes the script in the order and format I want to.    
"""
def main():
    
    true_data = outlier_removal()
    plt.show(graph_plot(true_data))
    min_func = minimize_function(dcs, true_data, true_data[:,0])
    print('To 3 significant figures:')
    print(' ')
    print('The value for the decay constant for Rubidium 79 is {0:0.6f}'.format(round(min_func[0],6)), 'per second.')
    print(' ')
    print('The value for the decay constant for Strontium 79 is {0:0.3}'.format(min_func[1]), 'per second.')
    print(' ')
    half_life_value = half_life_calc(dcs)
    print('The value for the half life of Rubidium 79 is {0:3.1f}'.format(half_life_value[0]), 'minutes.')
    print(' ')
    print('The value for the half life of Strontium 79 is {0:3.2f}'.format(half_life_value[1]), 'minutes.')
    print(' ')
    print('To 2 decimal places:')
    print(' ')
    red_chi_sq = reduced_chi_squared(true_data)
    print('The value for the reduced chi squared is {0:3.2f}'.format(red_chi_sq))
        
main()
    

