import os, sys, shutil, csv, time, datetime, glob, re, logging


def circuitCheck(topdownfolder):
    top_down = r'\\Cdcgpnas02\CGDI\Top_Down'
    completed_circuits=[]
    
    if os.path.exists(topdownfolder):
        print('\nTop Down Folder Exists')
    else:
        print ('\nCreating Top Down folder')
        os.makedirs(topdownfolder)  
        print('Folder Creation Completed')  

#reads previously completed circuits so that those folders can be skipped. 
#needs work to avoid processing previously processed folders


    for txtfile in os.listdir(topdownfolder):
        txtfilename = txtfile[:-4]
        completed_circuits.append(txtfilename)
    return completed_circuits
    