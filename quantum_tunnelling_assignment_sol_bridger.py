#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:18:15 2019

This code is used to calculate the thickness of a Boron nitride crystal using quantum tunnelling of electrons.
It uses an approximation for the transmission coefficient, T, for electrons to pass through the crystal and a 
minimum chi-squared fit is used to find the thickness, d. Graphs of the expected plots will be shown.
(In case of lab script, mu = lambda in this case).

@author: solbridger
"""
import numpy as np
import matplotlib.pyplot as plt

"""
The function below calculates the array for the transmission coefficients and inputs them  
"""

def transmission_coefficient_function(d, complete_data):

    mu = (np.log(2)) / (8 * (np.pi) * 4 * 0.00553 * d) #eV/angstrom, d in angstroms

    d_1 = (1.2 * mu * d) / 3.0

    d_2 = d - d_1
 
    V_bar = 3.0 - ((1.15 * mu * d) / (d_2 - d_1)) * (np.log((d_2 / d_1) * ((d - d_1) / (d - d_2)))) #eV
    
    E = complete_data[:,1]
    
    T = np.exp(-2.0 * (d_2 - d_1) * 0.512317 * np.sqrt((V_bar - E)))
    
    return T 

"""
The two functions below, calculate the value for chi-squared and reduced chi-squared using the filtered data
"""
def chi_squared(d, complete_data):
    
    chi_sq = np.sum(np.square((complete_data[:,0] - transmission_coefficient_function(d, complete_data)) / complete_data[:,2]))
    
    return chi_sq

def reduced_chi_squared(d, complete_data):
    
    red_chi_sq = chi_squared(d, complete_data) / (len(complete_data) - 1)
    
    return red_chi_sq

"""
The function below checks for the existence of the file within the directory of the data.
"""

def file_existence_check():
    
    exists = False
    
    while not exists:
        
        file_name = input('What is the filepath of the data?')
        
        try:
                
            data_file = open(file_name , 'r')
            
            exists = True
    
        except:
            
            print('This file does not exist. Try again.', 'It must be formatted as: filename.extension', 'and it must be in the same directory as the python file')
            
    data_file.close() 
    
    return file_name
    
def columns_in_file(data_file_name):
    
    data_file = open(data_file_name, 'r')
    
    raw_data = data_file.readline().split(',')
    
    data_file.close()    
    return len(raw_data)

def data_rows(raw_data):
    
    return len(raw_data)

def strip_non_floats(data_file_name):
    
    raw_data = np.zeros((0, 3))
    
    data_file = open(data_file_name, 'r')
    
    for line in data_file:
    
        line = line.split(',')
        
        if is_valid_data(line):
            line[2] = float(line[2].rstrip('\n'))
            line[1] = float(line[1])
            line[0] = float(line[0])
            raw_data = np.vstack((raw_data, line))
                  
    data_file.close()     
    return raw_data
            
                  
def is_valid_data(raw_data):

    row_data_valid = True
    
    for row in raw_data:
        
        try:
            
            if float(row) < 0:
            
                row_data_valid = False
                
        except:
            
            row_data_valid = False
            
    return row_data_valid

def standard_deviation(no_float_data):
    
    std_dev0 = np.std(no_float_data[:,0])
    std_dev1 = np.std(no_float_data[:,1])
    std_dev = [std_dev0, std_dev1]
    return std_dev

def mean(no_float_data):
    
    data_mean0 = (np.array(no_float_data[:,0]))
    data_mean0 = np.mean(data_mean0)
    data_mean1 = (np.array(no_float_data[:,1]))
    data_mean1 = np.mean(data_mean1)
    data_mean = [data_mean0, data_mean1]
    return data_mean

def outliers_exclusion_function(clean_float_data):
    
    data_mean = np.array(mean(clean_float_data))
    
    data_std_dev = np.array(standard_deviation(clean_float_data))
    lower_bound = data_mean - (3 * data_std_dev)
    upper_bound = data_mean + (3 * data_std_dev)
    
    
    valid_data = np.zeros((0,3))
    
    
    for row in range(len(clean_float_data[:,0])):
        
        valid_row = True
        
        for column in range(2):       
            if clean_float_data[row, column] < lower_bound[column] or clean_float_data[row, column] > upper_bound[column]:
                
                valid_row = False
                
        if valid_row == True:
            
            valid_data = np.vstack((valid_data, clean_float_data[row,:]))
    return valid_data
"""
The function below is used to calculate the number of layers of the crystal contained within a boron nitride sample.
"""
def layers(d):
    
    layers = d / 3.0
    
    return layers

"""
Below describes the hill climbing algorithm that finds d, iteratively.
"""

def hill_climb_fit(complete_data):
    
    
    d_initial = 5

    tolerance = 0.00001

    step = 0.0001

    d = d_initial    


    difference = reduced_chi_squared(d, complete_data)

    while difference > tolerance:
    
        comparison_initial = reduced_chi_squared(d, complete_data)
        
        comparison_1 = reduced_chi_squared(d + step, complete_data)
    
        comparison_2 = reduced_chi_squared(d - step, complete_data)
    
        if comparison_initial > comparison_1:
        
            difference = comparison_initial - comparison_1
        
            d += step
            
        
        elif comparison_initial > comparison_2:
        
            difference = comparison_initial - comparison_2
        
            d -= step
        
        else:
        
            print('The desired precision cannot be obtained.')
        
            break
    
    
    return d



"""
The function below plots the graph for reduced chi-squared fit with the data, where complete_data
is the data which is free of outliers and only contains floats.
"""

def graph_plot(d, complete_data):
    
    plt.title('Transmission coefficient against Energy')
    
    plt.xlabel('Energy (eV)')
    
    plt.ylabel('Transmission coeffiecient')
    
    plt.scatter(complete_data[:,1], complete_data[:,0], color = 'blue')
    
    plt.errorbar(complete_data[:,1], complete_data[:,0], complete_data[:,2], linestyle = 'none', color = 'black', label = 'Complete data')

    plt.legend(loc = 'upper left')

    plt.plot(complete_data[:,1], transmission_coefficient_function(d, complete_data), color ='r', label = 'Least squares fit')
    
    plt.show()
    
"""
The function below executes all of the desired functions to output the desired information.
"""
def main():
    
    data_file = file_existence_check()
        
    clean_float_data = strip_non_floats(data_file)
 
    print(clean_float_data)
    
    complete_data = outliers_exclusion_function(clean_float_data)
    
    print(complete_data)
    
    d = hill_climb_fit(complete_data)
    
    print(d)
    
    graph_plot(d,complete_data)
    
    print('The value for the thickness of the Boron nitride sample is {0:4.3f} \u212B'.format(d))
    print('The reduced chi-squared for this fit is {0:3.2f} which is {1:1.0f} layer(s)'.format(reduced_chi_squared(d, complete_data), layers(d)))
    
main()





