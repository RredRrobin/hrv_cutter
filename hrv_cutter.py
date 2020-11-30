#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:54:55 2020

@author: RredRrobin

"""

import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class TextScrollCombo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.grid_propagate(True)
        
        self.text = tk.Text(self, wrap="none")
        self.text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        scroll_bar_y = ttk.Scrollbar(self, command=self.text.yview)
        scroll_bar_y.grid(row=0, column=1, sticky='nsew')
        self.text['yscrollcommand'] = scroll_bar_y.set
        
        scroll_bar_x = ttk.Scrollbar(self, command=self.text.xview, orient=tk.HORIZONTAL)
        scroll_bar_x.grid(row=1, column=0, sticky='nsew')
        self.text['xscrollcommand'] = scroll_bar_x.set
        
    def add(self, row):
        self.text.insert("end", row)
        
    def empty(self):
        self.text.delete('1.0', "end")

class program(tk.Frame):
      
    def __init__(self, master):
    
        tk.Frame.__init__(self, master)
        self.grid()
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.menubar = tk.Menu(master)
        master.config(menu=self.menubar)
        self.menu_create()
        
        self.combo = TextScrollCombo(master)
        self.combo.grid(row=0, column=0, sticky='nsew')

        style = ttk.Style()
        style.theme_use('clam')
        
        self.WD_open ="/"   # set root as default directory to open files
        self.WD_save ="/"   # set root as default directory to save files

    def menu_create(self):
        self.progs = tk.Menu(self.menubar, tearoff=False)
        self.progs.add_command(label="Choose directory to OPEN files", command=self.chooseWD_open)
        self.progs.add_command(label="Choose directory to SAVE files", command=self.chooseWD_save)
        self.progs.add_command(label="Close", command=self.close)
        self.menubar.add_cascade(label="Program", menu=self.progs)
        self.menuPs = tk.Menu(self.menubar, tearoff=False)
        self.menuPs.add_command(label="Load data", command=self.data_import)
        self.menuPs.add_command(label="Select interval", command=self.interval_select)
        self.menuPs.add_command(label="Cut & save interval", command=self.interval_cut)
        self.menubar.add_cascade(label="HRdata", menu=self.menuPs)
 
    def data_import(self):
        self.file_name = filedialog.askopenfilename(initialdir = self.WD_open, title = "Select file",filetypes = (("HRM files","*.hrm"),("Text files","*.txt"),("all files","*.*")))
        file = open(self.file_name)
        data = file.read()
        file.close()
        self.combo.add(data)  # to display

        # load dataframe
        self.df = pd.read_csv(self.file_name, sep = ",")
        self.df.columns = ["IBI"] # name column "IBI" (Inter-beat interval)

        # delete unnessecary information
        a = list(self.df.IBI) # convert column from self.df to list
        b = list(self.df.IBI).index('[HRData]') # recognize beginning of HR data in the list
        del a[0:4] # deletes first four rows
        del a[1:b-3] # deletes rows 2 to "[HRData]"
        self.df = pd.DataFrame({'IBI':a}) # writes dataframe

        # create column with forth-counted time
        self.df['IBI'] = self.df['IBI'].str.replace('StartTime=','') # deletes "StartTime=" to obtain just time value
        self.df['IBItime'] = pd.to_timedelta(self.df['IBI'])*1000000  # *1.000.000, because IBI-values are interpreted in microseconds (except for StartTime-value)
        l = len(self.df) # calculate length of DF / number of IBIs
        liste = list(range(1,l)) # create list from 1 to end (the unused ro with the time has the index number '0' and the last row has length minus 1)
        self.df['time'] = pd.to_timedelta(self.df['IBI'][0])
        for i in liste:
            self.df['time'][i] = self.df['time'][i-1] + self.df['IBItime'][i] # adds continuously the respective time value (previous time value plus length of IBI)
        self.combo.empty() # empty screen
        self.combo.add(self.df)

        # save as .csv-file
        filename_w_ext = os.path.basename(self.file_name)          # change file name to be saved in a way that
        filename, file_extension = os.path.splitext(filename_w_ext) # it has the same name as -hrm file, but
        self.n = filename+'.csv'                                    # with .csv as ending
        self.df.to_csv(self.n, sep='\t', index=False) # options: tabulator as seperator; without indexing
        return(self.df)

    def interval_select(self):
        def time_select(num1,num2,num3,num4,num5,num6):
            stime = (num1+":"+num2+":"+num3) # select start time
            dtime = (num4+":"+num5+":"+num6)
            print(stime) # print in console
            print(dtime)
            st = datetime.strptime(stime,"%H:%M:%S")
            dt = datetime.strptime(dtime,"%H:%M:%S")
            self.Stime = timedelta(hours = st.hour, minutes = st.minute, seconds= st.second)# format into sth that can be used later
            self.Dtime = timedelta(hours = dt.hour, minutes = dt.minute, seconds= dt.second)
            return(self.Stime)
            return(self.Dtime)

        # create window
        intwin = tk.Tk()  
        intwin.geometry("200x100+100+100")  
        intwin.title('Interval')
        
        # label
        tk.Label(intwin, text="Start time").grid(row=1, column=0)  
        tk.Label(intwin, text=":").grid(row=1, column=2)  
        tk.Label(intwin, text=":").grid(row=1, column=4)  
        tk.Label(intwin, text="Duration").grid(row=2, column=0)  
        tk.Label(intwin, text=":").grid(row=2, column=2)  
        tk.Label(intwin, text=":").grid(row=2, column=4)  
        
        # set type of variable
        number1 = tk.IntVar()
        number2 = tk.IntVar()  
        number3 = tk.IntVar()  
        number4 = tk.IntVar()  
        number5 = tk.IntVar()  
        number6 = tk.IntVar()  
      
        # create entry slot
        sHH = tk.Entry(intwin, textvariable=number1, width=2) # commentary: it would be nice to limit the entry options to two digits by default - not just visually - , in order to avoid nonsense entries / typos
        sHH.grid(row=1, column=1)  
        sMM = tk.Entry(intwin, textvariable=number2, width=2)
        sMM.grid(row=1, column=3)  
        sSS = tk.Entry(intwin, textvariable=number3, width=2)
        sSS.grid(row=1, column=5)  
        dHH = tk.Entry(intwin, textvariable=number4, width=2)
        dHH.grid(row=2, column=1)  
        dMM = tk.Entry(intwin, textvariable=number5, width=2)
        dMM.grid(row=2, column=3)  
        dSS = tk.Entry(intwin, textvariable=number6, width=2)
        dSS.grid(row=2, column=5)

        tk.Button(intwin, text = "OK", command=lambda: time_select(sHH.get(),sMM.get(),sSS.get(),dHH.get(),dMM.get(),dSS.get()), activebackground = "white", activeforeground = "blue").place(x = 70, y = 50)  
        intwin.mainloop()
        
        self.combo.add(self.Stime)
        self.combo.add(self.Dtime)
                
    def interval_cut(self):
        # load dataframe
        self.df2 = pd.read_csv(self.n, sep = "\t")

        # define times as timedelta data
        self.df2['IBI'] = pd.to_numeric(self.df2['IBI'][1:])
        self.df2['IBItime'] = pd.to_timedelta(self.df2['IBItime'])
        self.df2['time'] = pd.to_timedelta(self.df2['time'])

        x = self.Stime # selected start time
        start = self.df2.loc[self.df2['time'] >= x] # create DF from beginning of the interval
        y = self.Dtime # desired length of interval in minutes
        z = x + y # calculates value for end of the interval
        beg_end = start.loc[start['time'] < z] # creates DF until the end of the interval
                
        # Write IBIs of the interval into a seperate .txt-file
        self.file_name = filedialog.asksaveasfilename(initialdir = self.WD_save,title = "Save as",filetypes = (("Text files","*.txt"),("all files","*.*")))
        self.file = open(self.file_name, "w")
        np.savetxt(self.file_name, beg_end['IBI'].values, fmt='%d')
        self.file.close()
        
        # calculate mean heart beat duration in the interval
        print("\nMean Heart Beat Duration: ", beg_end['IBI'].mean(), "ms")
        # calculate mean heart rate
        print("Mean Heart Rate: ", 60/(beg_end['IBI'].mean()/1000), "bpm\n") # convert ms in s (/1000) and extrapolation to one minute (60/)
        # display table for interval
        print(beg_end)
        
        # display results and table of the interval
        hr = ("Mean Heart Beat Duration: ",beg_end['IBI'].mean(),"ms")
        puls = ("\Mean Heart Rate: ", 60/(beg_end['IBI'].mean()/1000), "bpm\n\n")
        tab = (beg_end)
        self.combo.empty() # empty screen 
        self.combo.add(hr)
        self.combo.add(puls)
        self.combo.add(tab)

    def chooseWD_open(self):
        self.WD_open = filedialog.askdirectory(title = "Choose directory to OPEN raw .hrm-files")  
        self.combo.add(self.WD_open)  # to display

    def chooseWD_save(self):
        self.WD_save = filedialog.askdirectory(title = "Choose directory to SAVE interval .txt-files")  
        self.combo.add(self.WD_save)  # to display

    def close(self):
        root.destroy()
 
root = tk.Tk()
root.resizable(0, 0)
prog = program(root)
prog.mainloop()
