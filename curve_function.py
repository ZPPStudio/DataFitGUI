
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 19:55:19 2021

@author: Administrator
"""
import numpy as np
import scipy.constants as scs

class Fit_Function_SFT():
    def __init__(self):
        self.pi = np.pi
        self.atom_mass = scs.u
        return
    def dafult_guass(x,a,b,c):
        y = a*np.exp(-(x-b)**2/2/c**2)
        return y
    def dafult_linear(x,k,b):
        y = k*x + b
        return y
    def dafult_dafult_parabola(x,a,b,c):
        y = a*x**2 + b*x + c
        return y
    def dafult_dafult_cube(x,a,b,c,d):
        y = a*x**3 + b*x**2 + c*x + d
        return y
    def curve_fit_SFT(x,y,init_value = []):
        return
def curve_function(x,a,b):
    return np.log(x)