# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:42:10 2021

@author: Administrator
"""

from tkinter import Tk,Button,Label,Entry,StringVar,Message
from tkinter import ttk
import os
from scipy.optimize import curve_fit
import time
import pandas as pd
import curve_function as cf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pymysql as psl
import numpy as np
import tkinter.messagebox as tmg


def gettime():
    time_now_var.set(time.strftime("%H:%M:%S"))
    root.after(1000,gettime)
    return
def fit():
#    import curve_function as cf
#    fit_function = cf.curve_function()
    return

def Write_Function():
    para = Parameter_set.get()
    function = Write_function.get()
    txt_function = open("curve_function.py", 'r')
    c = txt_function.readlines()
    txt_function.close()
    cu_function  = "    return " + function
    cur_para = "def curve_function(x," + para + "):" + "\n" 
    c[-1] = cu_function
    c[-2] = cur_para
    txt_function = open("curve_function.py", 'w')
    for i in c:
        txt_function.write(i)
    txt_function.close()
    return

def graph():
   x, y = read_data(data_experment_file.get())
   ax.clear()
   ax.plot(x, y)
   ax.grid()
   canvas.draw()
   return

def read_data(file_path):
    try:
        file_list = os.listdir(file_path)
        file_error = 0
    except:
        tmg.showwarning(message = "file_path is WRONG")
        file_error = -1
    if file_error == 0:
        data_file = []
        for file in file_list:
            if file[len(file)-3::] == "csv":
                data_file.append(file)
                break
            else:
                pass
        if len(data_file) == 0:
            tmg.showwarning(title = "Data Warning",message = "There are no Data File")
            x,y = 0.0, 0.0
        else:
            data_xy = pd.read_csv(os.path.join(file_path,data_file[-1]))
            x = data_xy["x"]
            y = data_xy["y"]
        return x,y
    else:
        pass
        return

def Default_fit():
    default_function_change = default_function.get()
    if default_function_change == "y = kx + b":
        fit_function = cf.Fit_Function_SFT.dafult_linear
        para_list = [0,0]
        bounds_list = ([-1., -1],[1, 1])
    elif default_function_change == 'y = ax^2 + bx + c':
        fit_function = cf.Fit_Function_SFT.dafult_dafult_parabola
        para_list = [0,0,0]
        bounds_list = ([-1., -1,-1],[1, 1,1])
    else:
        pass
    
    try:
        x,y = read_data(data_experment_file.get())        
        popt, pcov = curve_fit(fit_function,x,y,p0 = para_list, bounds=bounds_list)
        error = format_result_science(np.sqrt(np.diag(pcov)))
    
        fity = fit_function(x, *popt)
        ax.clear()
        ax.plot(x,y,'.')
        ax.plot(x,fity,'r-')
        ax.grid()
        canvas.draw()
        popt_str.set(str(format_result_science(popt)))
        Error_str.set(str(error))
        Current_Operation_log_var.set("Fit is completed")
    except:
        pass
    return
def format_result_science(x):
    length_x = len(x)
    for i in range(length_x):
        x[i] = "{:.3e}".format(x[i])
    return x
def set_function(event):
    Current_Operation_log_var.set("Change dafult function")
    return

root = Tk()
root.title("SFTool")
root.geometry("1300x500")
"""离子特性参数"""
QMN_para_width  = 20
numberlabelwidth = 100
numberEntrywidth = 50
Qchargelabelheight = 40


label_parameter=Label(root,text="Parameter")
label_parameter.place(x=QMN_para_width + 10,y=Qchargelabelheight + 30,width=numberlabelwidth)
label_parameter_init = StringVar(value='a,b')
Parameter_set = Entry(root,textvariable= label_parameter_init)
Parameter_set.place(x =QMN_para_width + numberlabelwidth + 40,y = Qchargelabelheight + 30,width=numberlabelwidth*3)

labelQ1=Label(root,text = "Fit Function") #建立label对象放到主窗体
labelQ1.place(x=QMN_para_width + 10,y=Qchargelabelheight,width=numberlabelwidth)
Q1addr = StringVar(value='np.log(x)')
Write_function = Entry(root,textvariable= Q1addr)
Write_function.place(x =QMN_para_width + numberlabelwidth + 40,y = Qchargelabelheight,width=numberlabelwidth*3)

label_data_experment=Label(root,text = "Exper Data File") #建立label对象放到主窗体
label_data_experment.place(x=QMN_para_width + 10,y=Qchargelabelheight + 60,width=numberlabelwidth)
Q1addr = StringVar(value=r'E:\Lion\GUIFIT\test')
data_experment_file = Entry(root,textvariable= Q1addr)
data_experment_file.place(x =QMN_para_width + numberlabelwidth + 40,y = Qchargelabelheight + 60,width=numberlabelwidth*3)

"""Default Function"""
label_daf_function=Label(root,text = "General Function") #建立label对象放到主窗体
label_daf_function.place(x=QMN_para_width + 10,y=Qchargelabelheight + 90,width=numberlabelwidth)
n = StringVar()
default_function = ttk.Combobox(root, width = 27, textvariable = n)
default_function['values'] = ('y = kx + b', 
                          'y = ax^2 + bx + c',)
default_function.grid(column = 1, row = 5)
default_function.place(x =QMN_para_width + numberlabelwidth + 40,y = Qchargelabelheight + 90,width=numberlabelwidth*3)
default_function.current(0)
default_function.bind('<<ComboboxSelected>>',set_function)

"""Set Fit Parameters"""
Parameter_x_start = 200
Parameter_y_start = 180
Parameter_y_space = 40
Parameter_x_space = 100
label_init_value=Label(root,text = "init value",font = ("Arial",10))
label_init_value.place(x=Parameter_x_start,y=Parameter_y_start,width=numberlabelwidth)
init_value_str = StringVar(value=r'0,0,0')
init_value = Entry(root,textvariable= init_value_str)
init_value.place(x =Parameter_x_start + Parameter_x_space,y = Parameter_y_start,width=numberlabelwidth)

label_bound_low=Label(root,text = "bound_low",font = ("Arial",10))
label_bound_low.place(x=Parameter_x_start,y=Parameter_y_start + Parameter_y_space,width=numberlabelwidth)
bound_low_str = StringVar(value=r'0,0,0')
bound_low = Entry(root,textvariable= bound_low_str)
bound_low.place(x =Parameter_x_start + Parameter_x_space,y = Parameter_y_start + + Parameter_y_space,width=numberlabelwidth)

label_bound_High=Label(root,text = "bound_High",font = ("Arial",10))
label_bound_High.place(x=Parameter_x_start,y=Parameter_y_start + Parameter_y_space*2,width=numberlabelwidth)
bound_High_str = StringVar(value=r'0,0,0')
bound_High = Entry(root,textvariable= bound_High_str)
bound_High.place(x =Parameter_x_start + Parameter_x_space,y = Parameter_y_start + Parameter_y_space*2,width=numberlabelwidth)

"""Display Result"""
time_now_var = StringVar()
label_time_obverable = Message(root, textvariable=time_now_var,justify="center",relief = "ridge",font = ("Arial",20), width= 800)
time_now_var.set(time.strftime("%H:%M:%S"))
label_time_obverable.place(x = 850 ,y = 450)

result_x_start = 900
result_y_start = 40
result_y_space = 40
result_x_space = 100

label_popt=Label(root,text = "Fit Parameter",font = ("Arial",10))
label_popt.place(x=result_x_start,y=result_y_start,width=numberlabelwidth)
popt_str = StringVar()
popt = Entry(root,textvariable= popt_str)
popt.place(x =result_x_start + result_x_space,y = result_y_start,width=numberlabelwidth*2)

label_error=Label(root,text = "Error",font = ("Arial",10))
label_error.place(x=result_x_start,y=result_y_start + result_y_space,width=numberlabelwidth)
Error_str = StringVar()
Error = Entry(root,textvariable= Error_str)
Error.place(x =result_x_start + result_x_space,y = result_y_start + result_y_space,width=numberlabelwidth*2)
"""Log and State Display"""
#label_log=Label(root,text = "Log",font = ("Arial",15)) #建立label对象放到主窗体
#label_log.place(x=220,y= 170,width=numberlabelwidth*4)
Current_Operation_log_var = StringVar()
label_Current_Operation=Label(root,text = "Current Operation",font=("Arial",10)) #建立label对象放到主窗体
label_Current_Operation.place(x=30,y=450,width=numberlabelwidth*2)
Current_Operation = Entry(root,textvariable= Current_Operation_log_var)
Current_Operation.place(x =80 + numberlabelwidth + 40,y = 450,width=numberlabelwidth*2)
Current_Operation_log_var.set("No Operation")
"""Control Command"""
control_command_x = 40
button=Button(root,text='Made Fit',command=fit,fg='black',font=("Arial",15))
button.place(x=control_command_x,y=180,width=150,height=40)

button=Button(root,text='Default Fit',command=Default_fit,fg='black',font=("Arial",15))
button.place(x=control_command_x,y=250,width=150,height=40)

button=Button(root,text='Write Function',command=Write_Function,fg='black',font=("Arial",15))
button.place(x=control_command_x,y=320,width=150,height=40)

button=Button(root,text='Data Plot',command=graph,fg='black',font=("Arial",15))
button.place(x=control_command_x,y=390,width=150,height=40)

"""figure_frame"""
fig = Figure(dpi=100, figsize=(6.4,4.6))
ax = fig.add_subplot(111)
ax.grid()
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().place(x=500, y=40,width=350, height=350)


toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.place(x=500, y=390, width=200, height=40)
        
root.resizable(width=False,height=False) 
#root.iconphoto(False, PhotoImage(file="ico\ico.png"))
root.after(1000,gettime)
root.mainloop()

