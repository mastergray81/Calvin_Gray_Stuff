import os, sys

top_down = r'\\Cdcgpnas02\CGDI\Top_Down'

import os, sys

def crossCheck():
    circuit_list = []
    
    if os.path.exists(top_down):
        print('\nTop Down Folder Exists')
    else:
        print ('\nCreating Top Down folder')
        os.makedirs(top_down)  
        print('Folder Creation Completed')  

#reads previously completed circuits so that those folders can be skipped. 
#needs work to avoid processing previously processed folders


    for txtfile in os.listdir(top_down):
        txtfilename = txtfile[:-4]
        circuit_list.append(txtfilename)
    return circuit_list