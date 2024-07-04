import os, sys, shutil, csv, time, datetime, glob, re, logging
import pandas as pd
from exif import Image
#There is a problem with Huntington's second folder not getting captured


csvpath = r'\\Cdcgpnas02\CGDI\Top_Down'
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'
pix = ('JPG','jpg')
bad_ext = ('.docx', '.DOCX','.db','.DB','.pdf','.PDF')

#top directory
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'


def circuitFolderList(circuits):
    subdirs = []
    top_dir = os.listdir(circuits)  #1 level below ind_circuits
    for i in top_dir:
       sync =  os.path.join(ind_circuits,i)
       subdirs.append(sync)
    #print(subdirs)

    subdirs1 = []
    for i in subdirs:
        sub_dir = os.listdir(i)  #2 levels below ind_circuits
        for x in sub_dir:
            sync = os.path.join(i,x)
            subdirs1.append(sync)

    subdirs2 = []
    for i in subdirs1:
        sub_dir2 = os.listdir(i)  #2 levels below ind_circuits
        for x in sub_dir2:
            sync = os.path.join(i,x)
            subdirs2.append(sync)

    circuit_dict = {}
    for i in subdirs2:
        circuit = i[i.rfind('\\')+1:]
        circuit_dict[circuit] = i


    return(circuit_dict,subdirs2)
