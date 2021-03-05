
evac-prt5-tool
--------------

|Python2| |Python3|

This program is developed based on numpy, pygame and tkinter (optional).  You will need these three modules installed before you can run the code.  The program is compatible to both Python 2 and Python 3.  If you find any problem when using this program, please use issue trackers to report errors.  Thanks.     

Quick Start
-----------
Run a fds+evac case by using either fds5 or fds6, and ensure you get a .prt5 evac data file.  Then run the python script as below.  
python ui.py  
In the GUI window, please follow two steps:  
(1) Select the .fds input file and .prt5 data file.  You can omit the .prt5 data if you are using the latest version of FDS (e.g, FDS 6.7.15 or above).  For previous version of FDS, you need to select both.  
(2) Read the data into a .txt file or visualize the data by pygame (SDL for python).  In the pygame screen you can zoom in or zoom out the simulation.  Currently this python program deals with one-floor scenario because it displays agents' trajactories in 2D space. 

Please try the following keys when the evac data is visualized by pygame.  Have fun!
<Space> <PageUp> <PageDown> <Home> <End> <Up> <Down> <Left> <Right>

Credits
-------
This python script is extended based on Topi's contribution, please see FDS discussion forum for details.
https://groups.google.com/g/fds-smv/c/dFUWR00T6hw

Thank Topi for sharing his wonderful python script and thank Salah Benkorichi for sending this thread to me!
I mainly modified xyz.shape = (7,nplim) for evac prt5 data. In Topi's script it was initially given by xyz.shape = (3,nplim) for Lagrangian Particles. We use xyz.shape = (7,nplim) for evac prt5 data.  

We need your help to improve this small program! New contributors are welcome.  