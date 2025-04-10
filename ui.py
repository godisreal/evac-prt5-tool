
import os, sys
import multiprocessing as mp
from visualize_func import *
from read_evac import *
#import matplotlib.pyplot as plt
#from data_func.py import *
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")

'''
# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
    import tkinter.filedialog as tkf
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    import tkFileDialog as tkf
'''

if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    #from tkinter import ttk
    from tkinter.ttk import Notebook
    from tkinter.ttk import Treeview
    from tkinter.ttk import Button
    import tkinter.filedialog as tkf
    import tkinter.messagebox as msg
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    from ttk import Treeview
    from ttk import Entry
    import tkFileDialog as tkf
    import tkMessageBox as msg

    
class GUI(object):

    def __init__(self, FN_FDS=None, FN_EVAC=None):

        #self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        #self.FN=[None, None] #, None]
        #self.FN[0]=FN_FDS
        #self.FN[1]=FN_EVAC
        self.fname_FDS=FN_FDS
        self.fname_EVAC=FN_EVAC
        self.FNTemp=os.getcwd() +'/log.txt'
        
        self.openfn  = None
        self.opendir = None

        self.fname_EVACtxt = None
        self.fname_EVACnpz = None

        self.window = Tk()
        self.window.title('evac prt5 tool')
        self.window.geometry('970x470')

        self.notebook = Notebook(self.window)      
        self.notebook.pack(side=TOP, padx=2, pady=2)
        
        # added "self.rootWindow" by Hiroki Sayama 10/09/2018
        #self.frameRun = Frame(self.window)
        #self.frameSettings = Frame(self.window)
        #self.frameParameters = Frame(self.window)
        #self.frameInformation = Frame(self.window)


        # --------------------------------------------
        # frameInformation
        # --------------------------------------------
        scrollInfo = Scrollbar(self.window)#frameInformation)
        self.textInformation = Text(self.window, width=45,height=6,fg='cyan', bg='black',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textInformation.pack(side=RIGHT, fill=BOTH, expand=YES)
        scrollInfo.config(command=self.textInformation.yview)
        self.textInformation.config(yscrollcommand=scrollInfo.set)
        self.textInformation.insert(END, 'Please select .fds file or prt5 file to read in data or visualize the data!')

        
        #self.notebook.add(self.frameRun,text="Run")
        #self.notebook.add(self.frameSettings,text="Settings")
        #self.notebook.add(self.frameParameters,text="Parameters")
        #self.notebook.add(self.frameInformation,text="Info")
        #self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5 ,side=TOP)
        # self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')   # commented out by toshi on 2016-06-21(Tue) 18:31:02

        self.statusStr = ""
        self.statusText = StringVar(self.window, value=self.statusStr) # at this point, statusStr = ""
        # added "self.rootWindow" above by Hiroki Sayama 10/09/2018
        self.setStatusStr("Simulation not yet started")
        self.status = Label(self.window, width=40,height=3, fg='cyan', bg='black', relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        
        #self.status = Label(window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        # self.status.grid(row=1,column=0,padx=5,pady=5,sticky='nswe') # commented out by toshi on 2016-06-21(Tue) 18:31:17
        #self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        #from Tkinter.tkFileDialog import askopenfilename
        #fname = tkFileDialog.askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") )) 
        #def quit_botton(event):

        # --------------------------------------------
        # frameRun
        # --------------------------------------------
        self.lb_guide = Label(self.window, text =  "Please select the input files.")
        self.lb_guide.pack()

        self.lb0 = Label(self.window,text =  "Optional: The FDS input file selected: "+str(self.fname_FDS)+"\n")
        self.lb0.pack()

        self.lb1 = Label(self.window,text =  "The EVAC data file selected: "+str(self.openfn)+"\n")
        self.lb1.pack()

        self.lb2 = Label(self.window, text =  "The working path: "+str(self.opendir)+"\n")
        self.lb2.pack()

        self.buttonSelectFDS =Button(self.window, text='Optional: choose fds input file', width=38, command=self.selectFDSFile)
        self.buttonSelectFDS.pack()
        self.showHelp(self.buttonSelectFDS, "Only for FDS+Evac: Select FDS input file!")

        self.buttonBinParser =Button(self.window, text='Parser for binary data file', width=38, command=self.parseEvacFile)
        self.buttonBinParser.pack()
        self.showHelp(self.buttonBinParser, "Select binary data file and show if the binary data file is \n for CrowdEgress or FDS+Evac!")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        self.buttonRead = Button(self.window, text='Write binary data into txt file', width=38, command=self.readData)
        self.buttonRead.pack()
        self.showHelp(self.buttonRead, "Write binary Data into a text file! \n This action may take some time, \n depending on the size of data file!")

        self.buttonStart = Button(self.window, text='Visualize binary data in Pygame', width=38, command=self.startSim)
        self.buttonStart.pack()
        self.showHelp(self.buttonStart, "Visualize a binary data file \n for either CrowdEgress or FDS+Evac!")
        #buttonStart.place(x=5,y=220)
        #print(self.fname_FDS, self.fname_EVAC)

        self.buttonPlotTpre =Button(self.window, text='plot pre-movement time data',  width=38, command=self.plotTpre)
        self.buttonPlotTpre.pack()
        self.showHelp(self.buttonPlotTpre, "Select an output text file of CrowdEgress \n Plot pre-movement time from data selected!")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        self.buttonPlotStress =Button(self.window, text='plot agent stress level data',  width=38, command=self.plotStress)
        self.buttonPlotStress.pack()
        self.showHelp(self.buttonPlotStress, "Select an output text file of CrowdEgress \n Plot agent stress level from data selected!")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        self.buttonPlotDoorProb = Button(self.window, text='plot exit selection probability data', width=38, command=self.plotExitProb)
        self.buttonPlotDoorProb.pack()
        self.showHelp(self.buttonPlotDoorProb, "Select an output text file of CrowdEgress \n Plot exit selection probability from data selected!")
        #buttonStart.place(x=5,y=220)
        #print(self.fname_FDS, self.fname_EVAC)

        self.lb_exit = Label(self.window,text =  "Select the exit index number for probability plot as below:")
        self.lb_exit.pack()

        self.spin_exitnumber = Spinbox(self.window, from_=0, to=100, width=5, bd=8) 
        self.spin_exitnumber.pack() #place(x=689, y=360)
        self.showHelp(self.spin_exitnumber, "Select the exit index to show the probability.  \n The exit index starts from 0 to the number_of_exit-1. \n To identify the exit index, please show exit data in TestGeom. ")

        if os.path.exists(self.FNTemp) and self.fname_FDS is None and self.fname_EVAC is None and self.fname_EVACtxt is None:
        #if self.FNTemp is not None:
            for line in open(self.FNTemp, "r"):
                if re.match('FN_FDS', line):
                    temp =  line.split('=')
                    self.fname_FDS = temp[1].strip()
                    self.lb0.config(text = "The FDS data file selected in the last run.\n"+str(self.fname_FDS))

                if re.match('FN_EVAC', line):
                    temp =  line.split('=')
                    self.fname_EVAC = temp[1].strip()
                    self.openfn  = os.path.basename(self.fname_EVAC)
                    self.opendir = os.path.dirname(self.fname_EVAC)
                    self.lb1.config(text = "The input binary data file selected:\n"+str(self.openfn))
                    self.lb2.config(text = "Working path:\n"+str(self.opendir))

                    temp=self.fname_EVAC.split('.')
                    self.fname_EVACtxt = temp[0]+'.txt' 
                    self.fname_EVACnpz = temp[0]+'.npz'

                    temp = self.openfn.split('.')
                    suffix = str(temp[-1].strip())
                    if suffix == 'bin':
                        self.buttonPlotTpre.configure(state='enabled')
                        self.buttonPlotStress.configure(state='enabled')
                        self.buttonPlotDoorProb.configure(state='enabled')
                    if suffix == 'prt5':
                        self.buttonPlotTpre.configure(state='disabled')
                        self.buttonPlotStress.configure(state='disabled')
                        self.buttonPlotDoorProb.configure(state='disabled')

                if re.match('FN_EVACtxt', line):
                    temp =  line.split('=')
                    self.fname_EVACtxt = temp[1].strip()
                    #self.lb1.config(text = "The input txt data file selected in the last run\n")

            self.textInformation.insert(END, '\n'+'FDS Input File Selected in the last run:   '+str(self.fname_FDS)+'\n')
            self.textInformation.insert(END, '\n'+'EVAC prt5 Data Selected in the last run:   '+str(self.fname_EVAC)+'\n')
            self.textInformation.insert(END, '\n'+'EVAC txt file Selected:   '+str(self.fname_EVACtxt)+'\n')

    def start(self):
        self.window.mainloop()

    def quitGUI(self):
        #pylab.close('all')
        self.window.quit()
        self.window.destroy()

    def setStatusStr(self,newStatus):
        self.statusStr = newStatus
        self.statusText.set(self.statusStr)

    def showHelp(self, widget, text):
        def setText(self):
            self.statusText.set(text)
            self.status.configure(foreground='cyan')
            
        def showHelpLeave(self):
            self.statusText.set(self.statusStr)
            self.status.configure(foreground='cyan')
        widget.bind("<Enter>", lambda e : setText(self))
        widget.bind("<Leave>", lambda e : showHelpLeave(self))

       
    def selectFDSFile(self):
        self.fname_FDS = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("fds files", "*.fds")), initialdir=self.opendir)
        #self.FN[0]=self.fname_FDS
        #temp=re.split(r'/', self.fname_FDS)
        self.opendir = os.path.dirname(self.fname_FDS)
        temp=self.fname_FDS.split('/')
        self.lb0.config(text = "The compartment layout is created by fds file. \n"+"The FDS data file selected: \n "+str(temp[-1])+"\n")
        self.textInformation.insert(END, '\n'+'FDS Input File Selected:  '+self.fname_FDS+'\n'+'Please note that if users plan to visualize prt5 data file, the compartment geometry is created by fds file as selected. \n However, the program will not check if the prt5 data is exactly generated from the fds file as selected. ')
        print('fname_FDS:', self.fname_FDS)
        self.setStatusStr("Select FDS Input File.")
        if self.fname_FDS is not None and self.fname_FDS is not '':
            if os.path.exists(self.FNTemp):
                f = open(self.FNTemp, "a+")
                f.write('FN_FDS='+str(self.fname_FDS)+'\n')
                f.write('Working path='+os.getcwd()+'\n')
                #f.write('TimeDate='+os.gettime()+'\n')
                f.close()
                print("write FDS filename in log")
            msg.showinfo('Info', 'Please note that fds input file is only used in visualization of prt5 data. \n In other words, if users plan to visualize prt5 data file, the compartment geometry is created by fds file as selected. \n However, the program will not check if the prt5 data is exactly generated from the fds file as selected. \n Thus, please ensure the prt5 data file selected for visualization is produced from this fds input file. ')


    def parseEvacFile(self):
        self.fname_EVAC = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("prt5 files", "*.prt5")), initialdir=self.opendir)
        #self.FN[1]=self.fname_EVAC
        self.openfn  = os.path.basename(self.fname_EVAC)
        self.opendir = os.path.dirname(self.fname_EVAC)
        self.lb1.config(text = "The input binary data file selected: "+ self.openfn +"\n")
        self.textInformation.insert(END, '\n'+'EVAC Binary Data Selected:   '+self.fname_EVAC+'\n')
        print('fname_EVAC', self.fname_EVAC)
        temp = self.openfn.split('.')
        print(temp)
        suffix = str(temp[-1].strip())
        self.setStatusStr("Select Evac Binary Data File.")
        if self.fname_EVAC is not None and self.fname_EVAC is not '':
            if os.path.exists(self.FNTemp):
                #self.opendir = os.getcwd()
                f = open(self.FNTemp, "a+")
                f.write('FN_EVAC='+str(self.fname_EVAC)+'\n')
                f.write('Working path='+ self.opendir + '\n') #os.getcwd()+'\n')
                f.close()
                print("Write EVAC filename in log")
            if suffix == 'bin':
                msg.showinfo("CrowdEgress data file selected",  "CrowdEgress binary data file selected. \n Users may write the binary data into a text file or directly visualize the data file \n" +self.opendir + '\n' + self.openfn)
                temp=self.fname_EVAC.split('.')
                self.fname_EVACtxt = temp[0]+'.txt' 
                self.fname_EVACnpz = temp[0]+'.npz'
                self.buttonPlotTpre.configure(state='enabled')
                self.buttonPlotStress.configure(state='enabled')
                self.buttonPlotDoorProb.configure(state='enabled')

            elif suffix == 'prt5':
                msg.showinfo("FDS+Evac data file selected",  "FDS+Evac binary data file selected. \n Users may write the binary data into a text file or directly visualize the data file \n" +self.opendir + '\n' + self.openfn+'\n Np plot functions for FDS+Evac prt5 data!')
                self.buttonPlotTpre.configure(state='disabled')
                self.buttonPlotStress.configure(state='disabled')
                self.buttonPlotDoorProb.configure(state='disabled')
                
            else:
                msg.showinfo("No proper binary data file selected",  "No binary data file selected.  Please select an binary data file. \n Data file suffix: .bin or .prt5")
        else:
            msg.showinfo("No file selected",  "No file selected.  Please select an binary data file.")
            
            
    def readData(self):
        #self.fname_EVAC = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("prt5 files", "*.prt5")), initialdir=self.opendir)
        #self.FN[1]=self.fname_EVAC
        #self.openfn  = os.path.basename(self.fname_EVAC)
        #self.opendir = os.path.dirname(self.fname_EVAC)
        self.lb1.config(text = "The input binary data file selected: "+ self.openfn +"\n")
        self.textInformation.insert(END, '\n'+'Write Binary Data into text file:   '+self.fname_EVAC+'\n')
        temp = self.openfn.split('.')
        print('fname_EVAC', self.fname_EVAC, temp)
        suffix = str(temp[-1].strip())
        self.setStatusStr("Select Evac Binary Data File.")
        
        #self.setStatusStr("Read Prt5 Data! This action may take a few seconds or minutes, depending on the size of data file!")
        if os.path.exists(self.fname_EVAC) and self.fname_EVAC is not None and self.fname_EVAC is not '':
            print('load binary data file and extract evac-related information', self.fname_EVAC)
            #self.textInformation.insert(END, "\nRead Prt5 Data! This action may take a few seconds or minutes, depending on the size of data file!")
            readPRTfile(self.fname_EVAC, wrtxt=True)
            self.textInformation.insert(END, "\nRead Binary Data Successfully!\n")
            msg.showinfo("Write Binary Data File into Text File",  "Read Binary Data Successfully!")
            return
        
        if os.path.exists(self.fname_FDS):
            print ('load .fds file and extract evac-related information', self.fname_FDS)
            CHID=readCHID(self.fname_FDS)
            print(CHID)

            # The following lines are effective only for the latest version of fds as well as fds6_dump205.exe
            # If you are using the old version of fds, please modify the code to read evac prt5 file.
            #self.textInformation.insert(END, "\nRead Prt5 Data! This action may take a few seconds or minutes, depending on the size of data file!")
            temp=os.path.split(self.fname_FDS)
            self.fname_EVAC=os.path.join(temp[0],CHID+'_evac_0001.prt5')
            readPRTfile(self.fname_EVAC,  wrtxt=True)
            self.textInformation.insert(END, "\nRead Prt5 Data Successfully!\n")
            msg.showinfo("Write Prt5 Data File into Text File",  "Read Prt5 Data Successfully!")
            return
        
        print('No input files found! Please select the data file or fds input file!')
        self.setStatusStr('No input files found! Please select the data file or fds input file!')
        return


    def startSim(self):
        #myTest = simulation()
        #myTest.select_file(self.FN[1], None, "non-gui")
        #myTest.read_data()
        #sunpro1 = mp.Process(target=show_simu(myTest))
        #sunpro1.start()
        #sunpro1.join()
        #show_geom(myTest)
        #myTest.show_simulation()
        #myTest.quit()
        #self.setStatusStr("Visualize Prt5 Data by Pygame!")
        #self.textInformation.insert(END, "\nVisualize Prt5 Data by Pygame!\n")

        #self.fname_EVAC = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("prt5 files", "*.prt5"),  ("binary files", "*.bin")), initialdir=self.opendir)
        #self.openfn  = os.path.basename(self.fname_EVAC)
        #self.opendir = os.path.dirname(self.fname_EVAC)
        temp=self.openfn.split('.')
        fnsuffix=temp[-1]
        self.lb1.config(text = "The input binary data file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, '\n'+'EVAC prt5/binary Data Selected:   '+self.fname_EVAC+'\n')
        print('fname_EVAC', self.fname_EVAC)
        self.setStatusStr("Select prt5/binary Data File.")
        if os.path.exists(self.FNTemp) and self.fname_EVAC is not None and self.fname_EVAC is not '':
            f = open(self.FNTemp, "a+")
            f.write('FN_EVAC='+str(self.fname_EVAC)+'\n')
            f.write('Working path='+os.getcwd()+'\n')
            f.close()
            print("Write EVAC filename in log")
        
        '''
        if self.fname_FDS is not None and os.path.exists(self.fname_FDS):
            print ('load .fds file and extract evac-related information', self.fname_FDS)
            CHID=readCHID(self.fname_FDS)
            print(CHID)

            # The following lines are effective for the latest version of fds as well as previous version of fds.  
            # If you are using the old version of fds, please select evac prt5 file.
            if os.path.exists(self.fname_EVAC):       
                sunpro1 = mp.Process(target=visualizeFdsEvac(self.fname_EVAC, self.fname_FDS))
                sunpro1.start()
                sunpro1.join()
            else:
                temp=os.path.split(self.fname_FDS)
                self.fname_EVAC=os.path.join(temp[0],CHID+'_evac_0001.prt5')
                sunpro1 = mp.Process(target=visualizeFdsEvac(self.fname_EVAC, self.fname_FDS))
                sunpro1.start()
                sunpro1.join()
            #visualizeFdsEvac(CHID+'_evac_0001.npz', self.FN[0])
        else: # No file selected for fds
            print("No file selected for fds input file")
        '''
        
        #if os.path.exists(self.fname_EVAC):
        if fnsuffix=='prt5':
            if self.fname_FDS is not None and os.path.exists(self.fname_FDS):
                visualizeFdsEvac(self.fname_EVAC, self.fname_FDS)
            else:
                print("No file selected for fds input file.")
                visualizeFdsEvac(self.fname_EVAC, None)
        elif fnsuffix=='bin':
            visualizeAgent(self.fname_EVAC, None)
        #sunpro1 = mp.Process(target=visualizeAgent(self.fname_EVAC, None))
        #sunpro1.start()
        #sunpro1.join()
        else:
            print ("Input file %s is neither prt5 data nor binary data!" %self.fname_EVAC)
            #exit(-1)

        
    def plotExitProb(self):
        #myTest = simulation()
        #myTest.select_file(self.FN[1], None, "non-gui")
        #myTest.read_data()
        #sunpro1 = mp.Process(target=show_simu(myTest))
        #sunpro1.start()
        #sunpro1.join()
        #show_geom(myTest)
        #myTest.show_simulation()
        #myTest.quit()
        #self.setStatusStr("Visualize Prt5 Data by Pygame!")
        #self.textInformation.insert(END, "\nVisualize Prt5 Data by Pygame!\n")
        self.fname_EVACtxt = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("txt files", "*.txt")), initialdir=self.opendir)
        self.opendir = os.path.dirname(self.fname_EVACtxt)
        temp=self.fname_EVACtxt.split('/') 
        self.lb1.config(text = "The output exit probability data file selected: \n"+str(temp[-1])+"\n")
        self.textInformation.insert(END, '\n'+'EVAC exit probability Data Selected:   '+self.fname_EVACtxt+'\n')
        print('fname_EVACtxt', self.fname_EVACtxt)
        self.setStatusStr("Select Evac output txt data File.")
        if os.path.exists(self.FNTemp) and self.fname_EVACtxt is not None:
            f = open(self.FNTemp, "a+")
            f.write('FN_EVACtxt='+str(self.fname_EVACtxt)+'\n')
            f.write('Working path='+os.getcwd()+'\n')
            f.close()
            print("Write EVACtxt filename in log")

        if os.path.exists(self.fname_EVACtxt):
            exitNum = self.spin_exitnumber.get()
            print('Exit index in plot:', int(exitNum))
            self.textInformation.insert(END, 'Exit index in plot:'+str(exitNum))
            readDoorProb(self.fname_EVACtxt, doorIndex= int(exitNum))
            #sunpro1 = mp.Process(target=plt.plot(doorProb))
            #sunpro1.start()
            #sunpro1.join()
        else:
            print ("Input file %s does not exist!" %self.fname_EVACtxt)
            #exit(-1)


    def plotTpreTemp(self):
        self.fname_EVACtxt = tkf.askopenfilename(filetypes=(("All files", "*.*"), ("bin files", "*.bin")), initialdir=self.opendir)
        temp=self.fname_EVACtxt.split('/') 
        self.lb1.config(text = "The output exit probability data file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, '\n'+'EVAC exit probability Data Selected:   '+self.fname_EVACtxt+'\n')
        print('fname_EVACtxt', self.fname_EVACtxt)
        self.setStatusStr("Select Evac output txt data File.")
        if os.path.exists(self.FNTemp) and self.fname_EVACtxt is not None:
            f = open(self.FNTemp, "a+")
            f.write('FN_EVACtxt='+str(self.fname_EVACtxt)+'\n')
            f.write('Working path='+os.getcwd()+'\n')
            f.close()
            print("Write EVACtxt filename in log")
            

    def plotTpre(self):
        #tempdir=os.path.dirname(self.fname_EVAC)
        #print(tempdir)
        self.fname_TpreBinFile = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("All files", "*.*")), initialdir=self.opendir)
        self.opendir = os.path.dirname(self.fname_TpreBinFile)
        temp=re.split(r'/', self.fname_TpreBinFile)
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_TpreBinFile:', self.fname_TpreBinFile)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'Output Tpre Binary File Selected (Pre-Evacuation Time): '+self.fname_TpreBinFile+'\n')
        visualizeTpre(self.fname_TpreBinFile)

    def plotStress(self):
        #tempdir=os.path.dirname(self.fname_EVAC)
        #print(tempdir)
        self.fname_StressBinFile = tkf.askopenfilename(filetypes=(("bin files", "*.bin"),("All files", "*.*")), initialdir=self.opendir)
        self.opendir = os.path.dirname(self.fname_StressBinFile)
        temp=re.split(r'/', self.fname_StressBinFile)
        #temp=self.fname_OutTXT.split('/') 
        #self.lb_outbin.config(text = "The output bin file selected: "+str(temp[-1])+"\n")
        #self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_StressBinFile:', self.fname_StressBinFile)
        self.setStatusStr("Simulation not yet started!")
        self.textInformation.insert(END, '\n'+'Output Stress Binary File Selected (Agent Stress Level): '+self.fname_StressBinFile+'\n')
        visualizeStress(self.fname_StressBinFile)


if __name__ == '__main__':
    myGUI=GUI()
    myGUI.start()


    
