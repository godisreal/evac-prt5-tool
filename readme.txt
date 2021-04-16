Step (1): Run fds command to get evac prt5 data
fds <inputfilename.fds>
Step (2): Visualize evac prt5 file.  Use the command as below. 
python main.py <inputfilename.fds>

If you just want to read in data, please use the following command. 
python main.py <inputfilename.fds> /readonly

If you have already read in the data and just want to visualize the evac, please use the following command. 
python main.py <inputfilename.fds> /showonly

You can also use a simple GUI built by tkinter.  Please try the following command.  The program is compatible to both python 2 and python 3.  
python ui.py