# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:42:10 2021

@author: Administrator
"""

from tkinter import Tk,Button,Label,Entry,StringVar,Message
from tkinter import ttk
from os import path,listdir#,getcwd
from scipy.optimize import curve_fit
from time import strftime
#import pandas as pd
import curve_function as cf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#from numpy import linspace,sqrt,diag
from tkinter.messagebox import askokcancel,showwarning,showerror

class GUISTF():
    def __init__(self):
        self.root = Tk()
        self.root.title("SFTool")
        self.root.geometry("1300x820")
        """Genertal Parameter"""
        self.QMN_para_width  = 20
        self.numberlabelwidth = 100
        self.numberEntrywidth = 50
        self.Qchargelabelheight = 40
        self.label_parameter=Label(self.root,text="Parameter")
        self.label_parameter.place(x=self.QMN_para_width + 10,y=self.Qchargelabelheight + 30,width=self.numberlabelwidth)
        self.label_parameter_init = StringVar(value='a,b')
        self.Parameter_set = Entry(self.root,textvariable= self.label_parameter_init)
        self.Parameter_set.place(x =self.QMN_para_width + self.numberlabelwidth + 40,y = self.Qchargelabelheight + 30,width=self.numberlabelwidth*3)
        self.labelQ1=Label(self.root,text = "Fit Function") #建立label对象放到主窗体
        self.labelQ1.place(x=self.QMN_para_width + 10,y=self.Qchargelabelheight,width=self.numberlabelwidth)
        self.Q1addr = StringVar(value='np.log(x)')
        self.Write_function = Entry(self.root,textvariable= self.Q1addr)
        self.Write_function.place(x =self.QMN_para_width + self.numberlabelwidth + 40,y = self.Qchargelabelheight,width=self.numberlabelwidth*3)
        self.label_data_experment=Label(self.root,text = "Exper Data File") #建立label对象放到主窗体
        self.label_data_experment.place(x=self.QMN_para_width + 10,y=self.Qchargelabelheight + 60,width=self.numberlabelwidth)
        self.Q1addr = StringVar(value=r'E:\Lion\GUIFIT\test')
        self.data_experment_file = Entry(self.root,textvariable= self.Q1addr)
        self.data_experment_file.place(x =self.QMN_para_width + self.numberlabelwidth + 40,y = self.Qchargelabelheight + 60,width=self.numberlabelwidth*3)
        """Default Function"""
        self.label_daf_function=Label(self.root,text = "General Function") #建立label对象放到主窗体
        self.label_daf_function.place(x=self.QMN_para_width + 10,y=self.Qchargelabelheight + 90,width=self.numberlabelwidth)
        self.n = StringVar()
        self.default_function = ttk.Combobox(self.root, width = 27, textvariable = self.n)
        self.default_function['values'] = ('y = kx + b', 
                                  'y = ax^2 + bx + c',
                                  'y = ax^3 + bx^2 + cx + d',
                                  'Dafult Guass')
        self.default_function.grid(column = 1, row = 5)
        self.default_function.place(x =self.QMN_para_width + self.numberlabelwidth + 40,y = self.Qchargelabelheight + 90,width=self.numberlabelwidth*3)
        self.default_function.current(0)
        self.default_function.bind('<<ComboboxSelected>>',self.set_function)
        """Set Fit Parameters"""
        self.Parameter_x_start = 200
        self.Parameter_y_start = 180
        self.Parameter_y_space = 40
        self.Parameter_x_space = 100
        self.label_init_value=Label(self.root,text = "init value",font = ("Arial",10))
        self.label_init_value.place(x=self.Parameter_x_start,y=self.Parameter_y_start,width=self.numberlabelwidth)
        self.init_value_str = StringVar(value=r'0,0,0')
        self.init_value = Entry(self.root,textvariable= self.init_value_str)
        self.init_value.place(x =self.Parameter_x_start + self.Parameter_x_space,y = self.Parameter_y_start,width=self.numberlabelwidth)
        self.label_bound_low=Label(self.root,text = "bound_low",font = ("Arial",10))
        self.label_bound_low.place(x=self.Parameter_x_start,y=self.Parameter_y_start + self.Parameter_y_space,width=self.numberlabelwidth)
        self.bound_low_str = StringVar(value=r'0,0,0')
        self.bound_low = Entry(self.root,textvariable= self.bound_low_str)
        self.bound_low.place(x =self.Parameter_x_start +self. Parameter_x_space,y = self.Parameter_y_start + self.Parameter_y_space,width=self.numberlabelwidth)
        """Fit Parameter Bound"""
        self.label_bound_High=Label(self.root,text = "bound_High",font = ("Arial",10))
        self.label_bound_High.place(x=self.Parameter_x_start,y=self.Parameter_y_start + self.Parameter_y_space*2,width=self.numberlabelwidth)
        self.bound_High_str = StringVar(value=r'0,0,0')
        self.bound_High = Entry(self.root,textvariable= self.bound_High_str)
        self.bound_High.place(x =self.Parameter_x_start +self.Parameter_x_space,y = self.Parameter_y_start + self.Parameter_y_space*2,width=self.numberlabelwidth)
        self.create_sql_control_command(40,500,100,30,100,fontsize = 10)
        self.ax2,self.canvas2,self.toolbar2 = self.create_figure_position(100,(6.4,4.6),500,430,350,350,grid=True,Figure_number = 2)
        self.ax3,self.canvas3,self.toolbar3 = self.create_figure_position(100,(6.4,4.6),900,430,350,350,grid=True,Figure_number = 3)
        self.display_current_time(40,750)
        self.__clear_figure_button__(280,380,150)
        self.__Change_Data_Button__(40,650,180,50)
        self.__save_data_button__(250,650,180,50)
        """Display Result"""
        self.result_x_start = 900
        self.result_y_start = 40
        self.result_y_space = 40
        self.result_x_space = 100
        self.label_popt=Label(self.root,text = "Fit Parameter",font = ("Arial",10))
        self.label_popt.place(x=self.result_x_start,y=self.result_y_start,width=self.numberlabelwidth)
        self.popt_str = StringVar()
        self.popt = Entry(self.root,textvariable= self.popt_str)
        self.popt.place(x =self.result_x_start + self.result_x_space,y = self.result_y_start,width=self.numberlabelwidth*2)
        self.label_error=Label(self.root,text = "Error",font = ("Arial",10))
        self.label_error.place(x=self.result_x_start,y=self.result_y_start +self.result_y_space,width=self.numberlabelwidth)
        self.Error_str = StringVar()
        self.Error = Entry(self.root,textvariable= self.Error_str)
        self.Error.place(x =self.result_x_start + self.result_x_space,y = self.result_y_start + self.result_y_space,width=self.numberlabelwidth*2)
        """Log and State Display"""
        self.Current_Operation_log_var = StringVar()
        self.label_Current_Operation=Label(self.root,text = "Current Operation",font=("Arial",10)) #建立label对象放到主窗体
        self.label_Current_Operation.place(x=30,y=450,width=self.numberlabelwidth*2)
        self.Current_Operation = Entry(self.root,textvariable= self.Current_Operation_log_var)
        self.Current_Operation.place(x =80 + self.numberlabelwidth + 40,y = 450,width=self.numberlabelwidth*2)
        self.Current_Operation_log_var.set("No Operation")
        self.Current_Operation.configure(fg="red")
        """Control Command"""
        self.control_command_x = 40
        self.button=Button(self.root,text='Made Fit',command=self.fit,fg='black',font=("Arial",15))
        self.button.place(x=self.control_command_x,y=180,width=150,height=40)
        self.button=Button(self.root,text='Default Fit',command=self.Default_fit,fg='black',font=("Arial",15))
        self.button.place(x=self.control_command_x,y=250,width=150,height=40)
        self.button=Button(self.root,text='Write Function',command=self.Write_Function,fg='black',font=("Arial",15))
        self.button.place(x=self.control_command_x,y=320,width=150,height=40)
        self.button=Button(self.root,text='Data Plot',command=self.graph,fg='black',font=("Arial",15))
        self.button.place(x=self.control_command_x,y=390,width=150,height=40)
        """Curren Data"""
#        self.current_x = linspace(0,10,10)
#        self.current_y = linspace(0,10,10)
        """figure_frame"""
        self.fig = Figure(dpi=100, figsize=(6.4,4.6))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().place(x=500, y=40,width=350, height=350)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.place(x=500, y=390, width=200, height=40)
        self.Figure_1=Label(self.root,text = "Figure 1",font = ("Arial",10))
        self.Figure_1.place(x=500 + 250,y=390,width=100)
        self.root.resizable(width=False,height=False) 
        #root.iconphoto(False, PhotoImage(file="ico\ico.png"))
        self.root.after(1000,self.gettime)
        self.Data_source_base = askokcancel(title="Data Source",message="Data is from mysql database???")
        self.root.mainloop()
    def gettime(self):
        self.time_now_var.set(strftime("%H:%M:%S"))
        self.root.after(1000,self.gettime)
        return
    def fit():
    #    import curve_function as cf
    #    fit_function = cf.curve_function()
        return
    def Write_Function(self):
        para = self.Parameter_set.get()
        function = self.Write_function.get()
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
    def graph(self,line_color = "red",grid=True):
       x, y = self.read_data(self.data_experment_file.get())
       self.ax2.clear()
       self.ax2.plot(x, y,c = line_color)
       if grid:
           self.ax2.grid()
       else:
           pass
       self.canvas2.draw()
       return
    def read_data(self,file_path):
        if path.isdir(file_path):
            try:
                file_list = listdir(file_path)
                file_error = 0
            except:
                showwarning(message = "file_path is WRONG")
                file_error = -1
        else:
            if file_path[len(file_path) - 3::] == "csv":
                file_list = [file_path]
                file_error = 0
            else:
                showerror(title="FileError",message="The File type is not csv format")
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
                showwarning(title = "Data Warning",message = "There are no Data File")
                x,y = 0.0, 0.0
            else:
#                data_xy = pd.read_csv(path.join(file_path,data_file[-1]))
#                x = data_xy["x"]
#                y = data_xy["y"]
#                self.current_x = x
#                self.current_y = y
                pass
            return #x,y
        else:
            pass
            return
    def Default_fit(self):
        default_function_change = self.default_function.get()
        if default_function_change == "y = kx + b":
            fit_function = cf.Fit_Function_SFT.dafult_linear
            para_list = [0,0]
            bounds_list = ([-1., -1],[1, 1])
        elif default_function_change == 'y = ax^2 + bx + c':
            fit_function = cf.Fit_Function_SFT.dafult_dafult_parabola
            para_list = [0,0,0]
            bounds_list = ([-1., -1,-1],[1, 1,1])
        elif default_function_change == 'y = ax^3 + bx^2 + cx + d':
            fit_function = cf.Fit_Function_SFT.dafult_dafult_cube
            para_list = [0,0,0,0]
            bounds_list = ([-1., -1,-1,-1],[1, 1,1,1])
        elif default_function_change == 'Dafult Guass':
            fit_function = cf.Fit_Function_SFT.dafult_guass
            para_list = [0,0,0]
            bounds_list = ([-1., -1,-1],[1, 1,1])
        else:
            pass
        try:
            x,y = self.read_data(self.data_experment_file.get())        
            popt, pcov = curve_fit(fit_function,x,y,p0 = para_list, bounds=bounds_list)
#            error = self.format_result_science(sqrt(diag(pcov)))
            fity = fit_function(x, *popt)
            self.ax.clear()
            self.ax.plot(x,y,'.')
            self.ax.plot(x,fity,'r-')
            self.ax.grid()
            self.canvas.draw()
            self.popt_str.set(str(self.format_result_science(popt)))
#            self.Error_str.set(str(error))
            self.Current_Operation_log_var.set("Fit is completed")
        except:
            pass
        return
    def format_result_science(self,x):
        length_x = len(x)
        for i in range(length_x):
            x[i] = "{:.3e}".format(x[i])
        return x
    def set_function(self,event):
        self.Current_Operation_log_var.set("Change dafult function")
        return
    def create_sql_control_command(self,label_x_start,label_y_start,label_x_space,label_y_space,numberlabelwidth,fontsize = 20):
        label_User_Name=Label(self.root,text = "User Name",font = ("Arial",fontsize))
        label_User_Name.place(x=label_x_start,y=label_y_start,width=numberlabelwidth)
        self.User_Name_str = StringVar(value=r'root')
        User_Name = Entry(self.root,textvariable= self.User_Name_str)
        User_Name.place(x =label_x_start + label_x_space,y = label_y_start,width=numberlabelwidth)
        label_Port=Label(self.root,text = "Port",font = ("Arial",fontsize))
        label_Port.place(x=label_x_start,y = label_y_start + label_y_space,width=numberlabelwidth)
        self.Port_value_str = StringVar(value=r'3306')
        Port_value = Entry(self.root,textvariable= self.Port_value_str)
        Port_value.place(x =label_x_start + label_x_space,y = label_y_start + label_y_space,width=numberlabelwidth)
        label_Password=Label(self.root,text = "Password",font = ("Arial",fontsize))
        label_Password.place(x=label_x_start,y = label_y_start + label_y_space*2,width=numberlabelwidth)
        self.Password_value_str = StringVar(value=r'******')
        Password_value = Entry(self.root,textvariable= self.Password_value_str)
        Password_value.place(x =label_x_start + label_x_space,y = label_y_start + label_y_space*2,width=numberlabelwidth)
        return
    def create_figure_position(self,dpi2,figsize2,x,y,width,height,grid=True,Figure_number = 1):
        fig2 = Figure(dpi=dpi2, figsize=figsize2)
        ax2 = fig2.add_subplot(111)
        ax2.grid()
        canvas2 = FigureCanvasTkAgg(fig2, self.root)
        canvas2.get_tk_widget().place(x=x, y=y,width=width, height=height)
        toolbar2 = NavigationToolbar2Tk(canvas2, self.root)
        toolbar2.place(x=x, y=780, width=200, height=40)
        label_number=Label(self.root,text = "Figure "+str(Figure_number),font = ("Arial",10))
        label_number.place(x=x + 250,y=790,width=100)
        return ax2,canvas2,toolbar2
    def display_current_time(self,x_position,y_position,fontsize=10):
        label_time=Label(self.root,text = "Current Time",font = ("Arial",fontsize))
        label_time.place(x=x_position,y=y_position - 20,width = 100)
        self.time_now_var = StringVar()
        self.label_time_obverable = Message(self.root, textvariable=self.time_now_var,justify="center",relief = "ridge",font = ("Arial",fontsize*2), width= 800)
        self.time_now_var.set(strftime("%H:%M:%S"))
        self.label_time_obverable.place(x = x_position ,y = y_position)
        return
    def __clear_figure_button__(self,x_position,y_position,width,height=40,fontsize=15):
        self.button=Button(self.root,text='Clear Figure',command=self.__clear_figure_function__,fg='black',font=("Arial",15))
        self.button.place(x= x_position,y=y_position,width=width,height=height)
        return
    def __clear_figure_function__(self,All_Figure = True):
        self.ax.clear()
        self.ax.grid()
        self.canvas.draw()
        if All_Figure:
            self.ax2.clear()
            self.ax2.grid()
            self.canvas2.draw()
            self.Current_Operation_log_var.set("All Figure is cleared")
        else:
            self.Current_Operation_log_var.set("Figure one is cleared")
            pass
        return
    def __Change_Data_Button__(self,button_x,button_y,width,height):
        label_time=Label(self.root,text = "Current Data Source",font = ("Arial",10))
        label_time.place(x=button_x,y=button_y - 20,width = 150)
        self.text = StringVar()
        self.text.set("Change Data")
        self.button_data_source=Button(self.root,textvariable=self.text,command=self.__Change_Data_Source,fg='black',font=("Arial",15))
        self.button_data_source.place(x= button_x,y=button_y,width=width,height=height)
        return
    def __Change_Data_Source(self):
        if self.Data_source_base:
            self.Data_source_base = False
            self.text.set("Data File Folder")
        else:
            self.text.set("Database")
            self.Data_source_base = True
        return
    def __save_data_button__(self,x_position,y_position,width,height):
        label_path_save=Label(self.root,text = "File Path",font = ("Arial",10))
        label_path_save.place(x=x_position,y=y_position - 80,width = 60)
        self.label_save_file_path = StringVar(value='result.csv')
        self.result_save = Entry(self.root,textvariable= self.label_save_file_path)
        self.result_save.place(x =x_position,y = y_position - 60,width=self.numberlabelwidth*2)
        result_save=Label(self.root,text = "Save Date and Result",font = ("Arial",10))
        result_save.place(x=x_position,y=y_position - 20,width = 150)
        self.button_data_save=Button(self.root,text="save data",command=self.__save_data__,fg='black',font=("Arial",15))
        self.button_data_save.place(x= x_position,y=y_position,width=width,height=height)
        return
#    def __save_data__(self):
##        data = pd.DataFrame([[0,1,2,3],[24,5,6,7]])
#        file_path = self.label_save_file_path.get()
#        if path.isdir(file_path):
#            file_path_absolute = path.join(file_path,"result.csv")
#        else:
#            file_path_absolute = path.join(getcwd(),file_path)
#        try:
#            f = open(file_path_absolute,"r")
#            f.close()
#            file_path_absolute_check = 1
#        except:
#            showerror(title="FileError",message = "File not exist. A new file will be created")
#            file_path_absolute_check = 0
#        if file_path_absolute_check == 1:
#            data.to_csv(file_path_absolute)
#        else:
#            data.to_csv(file_path_absolute)
#        return
        def __save_data__(self):
            return
if __name__ == "__main__":
    GUISTF()
