#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:12:09 2019
Bouncy ball assignment:
Calculates the time for a bouncy ball to complete n bounces above a given minimum height.
Calculates the associated values of the variables in the equations i.e. time taken to complete
the bounces and the number of bounces completed etc. 

@author: solbridger
"""

import numpy as np

def validation(question, lower_bound, upper_bound): 
    """
    defines the validation for the bounds of all inputs i.e. eta, initial height, number of bounces etc.
    
    """
    
    value_valid = True
    
    while value_valid:
    
        try:
            value_given = float(input(question))
            
            if value_given < lower_bound:
 
                print("The value given is lower than", lower_bound, "so please enter another value.")
            
            elif value_given > upper_bound:
            
                print("The value given is greater than", upper_bound, "so please enter another value.")
            
            else:
            
                value_valid = False
                
                print("Value is ok")
                
        except ValueError:
            
            print("The value given must be a number.")
            
        except TypeError:
            
            print("The value given must be a number.")
            
    return value_given
            
def number_of_bounces_function(h_min, h_i, eta):
    
    """
    The function that calculates the number of bounces
    """

    n = (1.0/float(np.log(eta)))*float(np.log(h_min/h_i))
    
    return n
    
def time_function(h_i, eta, n):
    
    """
    The function that calculates the total time taken to complete the bounces
    """
    t = np.sqrt(2*h_i/g) * (1 + 2*eta**0.5 * ((1 - eta**(np.floor(n)/2)) / (1 - eta**(0.5))))
     
    return t#print("The time taken to complete all of these bounces is {0:3.2f}".format(t) + "s")
               
    

    
#h_i is the inital height from which the ball is dropped
    
h_i = validation("In metres, what is the initial height of the ball?", 0.2, 10000)
    
#h_min is the minimum height the ball must reach
    
h_min = validation("In metres, what is the minimum height the ball should reach?", 0.01, h_i)
        
#g is the value of g given by the user
        
g = validation("In metres per second per second, what is your value of g?", 0.5, 50)
        
#eta is the energy lost per bounce
        
eta = validation("What is the energy lost per bounce, η?", 0, 1)
        
n = number_of_bounces_function(h_min, h_i, eta)

t = time_function(h_i, eta, n)

print('The ball dropped from {:3.2f}'.format(h_i),'metres, bounced', np.floor(n), 'times and in a time of {:3.2f}'.format(t), 's')


