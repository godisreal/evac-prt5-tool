
import os, sys
import multiprocessing as mp
from read_evac import *

# Version Check
if sys.version_info[0] == 3: # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
else:
    # Python 2
    from Tkinter import *
    from ttk import Notebook
    import tkFileDialog
    
class GUI(object):

    def __init__(self, FN_FDS=None, FN_EVAC=None):

        self.FN_Info = ['FDS', 'EVAC'] #, 'Doors']
        self.FN=[None, None] #, None]
        self.FN[0]=FN_FDS
        self.FN[1]=FN_EVAC
        self.fname_FDS=None
        self.fname_EVAC=None

        self.window = Tk()
        self.window.title('prt5 tool')
        self.window.geometry('760x300')

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
        self.textInformation = Text(self.window, width=45,height=6,bg='lightgray',wrap=WORD,font=("Courier",10))
        scrollInfo.pack(side=RIGHT, fill=Y)
        self.textInformation.pack(side=LEFT,fill=BOTH,expand=YES)
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
        self.status = Label(self.window, width=40,height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
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
        self.lb_guide = Label(self.window, text =  "Please select the input files of FDS")
        self.lb_guide.pack()

        self.lb0 = Label(self.window,text =  "The FDS data file selected: "+str(self.FN[0])+"\n")
        self.lb0.pack()

        self.lb1 = Label(self.window,text =  "The EVAC data file selected: "+str(self.FN[1])+"\n")
        self.lb1.pack()

        #self.lb2 = Label(frameRun,text =  "The exit data file selected: "+str(FN[2])+"\n")
        #self.lb2.pack()

        self.buttonSelectFDS =Button(self.window, text='choose fds file for FDS data', command=self.selectFDSFile)
        self.buttonSelectFDS.pack()
        self.showHelp(self.buttonSelectFDS, "Select FDS input file!")

        self.buttonSelectPRT =Button(self.window, text='choose prt file for EVAC data', command=self.selectEvacFile)
        self.buttonSelectPRT.pack()
        self.showHelp(self.buttonSelectPRT, "Select prt5 data file!")
        #Button(window, text='choose csv file for door data', command=lambda: selectFile(2)).pack()

        #if CheckVar1.get():
        #    buttonSelectFDS.configure(state=DISABLED)
        #TestV=CheckVar1.get()
        self.buttonRead = Button(self.window, text='read now: read in data', command=self.readData).pack()
        self.buttonStart = Button(self.window, text='start now: read in data', command=self.startSim).pack()
        #buttonStart.place(x=5,y=220)
        print self.FN[0], self.FN[1]


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
            self.status.configure(foreground='black')
            
        def showHelpLeave(self):
            self.statusText.set(self.statusStr)
            self.status.configure(foreground='black')
        widget.bind("<Enter>", lambda e : setText(self))
        widget.bind("<Leave>", lambda e : showHelpLeave(self))

    def selectFile(self, index):
        self.FN[index] = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        if index ==0:
            self.lb0.config(text = "The FDS data file selected: "+str(self.FN[index])+"\n")
        elif index ==1:
            self.lb1.config(text = "The EVAC data file selected: "+str(self.FN[index])+"\n")
        #elif index ==2:
        #    lb2.config(text = "The exit data file selected: "+str(FN[index])+"\n")
        print 'fname', self.FN[index]
        
    def selectFDSFile(self):
        self.fname_FDS = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        self.FN[0]=self.fname_FDS
        temp=re.split(r'/', self.fname_FDS)
        #temp=self.fname_FDS.split('/') 
        self.lb0.config(text = "Optional: If .fds is selected, the compartment geometry is created by .fds file. \n"+"The FDS data file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, 'fname_FDS:   '+self.fname_FDS)
        print('fname_FDS:', self.fname_FDS)
        self.setStatusStr("Simulation not yet started!")

    def selectEvacFile(self):
        self.fname_EVAC = tkFileDialog.askopenfilename(filetypes=(("All files", "*.*"), ("csv files", "*.csv") ))
        self.FN[1]=self.fname_EVAC
        temp=self.fname_EVAC.split('/') 
        self.lb1.config(text = "The input .csv file selected: "+str(temp[-1])+"\n")
        self.textInformation.insert(END, 'fname_EVAC:   '+self.fname_EVAC)
        print('fname', self.fname_EVAC)
        self.setStatusStr("Simulation not yet started!")

    def readData(self):
        self.setStatusStr("Read Prt5 Data! This action may take a few seconds or minutes, depending on the data size")
        if os.path.exists(self.FN[0]):
            print ('load .fds file and extract evac-related information', self.FN[0])
            CHID=readCHID(self.FN[0])
            print CHID

            # The following lines are effective only for the latest version of fds as well as fds6_dump205.exe
            # If you are using the old version of fds, please modify the code to read evac prt5 file.
            readPRTfile(CHID+'_evac_0001.prt5')
            self.setStatusStr("Read Prt5 Data Successfully!")
            return
        if os.path.exists(self.FN[1]):
            print('load .prt5 file and extract evac-related information', self.FN[1])
            readPRTfile(self.FN[1])
            self.setStatusStr("Read Prt5 Data Successfully!")
            return
        
        print('No input files found! Please select the data file or fds input file!')
        self.setStatusStr('No input files found! Please select the data file or fds input file!')
        
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
        self.setStatusStr("Visualize Prt5 Data by Pygame!")
        if os.path.exists(self.FN[0]):
            print ('load .fds file and extract evac-related information', self.FN[0])
            CHID=readCHID(self.FN[0])
            print CHID

            # The following lines are effective only for the latest version of fds as well as fds6_dump205.exe
            # If you are using the old version of fds, please modify the code to read evac prt5 file.
            if os.path.exists(CHID+'_evac_0001.npz'):
                pass
            else:
                readPRTfile(CHID+'_evac_0001.prt5')
                
            sunpro1 = mp.Process(target=visualizeEvac(CHID+'_evac_0001.npz', self.FN[0]))
            sunpro1.start()
            sunpro1.join()
            #visualizeEvac(CHID+'_evac_0001.npz', self.FN[0])
        else:
            print ("Input file %s does not exist!" %self.FN[0])
            exit(-1)
            

if __name__ == '__main__':
    myGUI=GUI()
    myGUI.start()


    
