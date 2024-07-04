import os, sys, shutil, csv, time, datetime, glob, re, logging
import pandas as pd
from exif import Image
import get_failed_exif, makecsv, circuitcomplete, foldersearch, get_exifs, circuitcheck, circuitsearch, circuitFolderList

#test folder to get the script to work proper
top_down = r'\\Cdcgpnas02\CGDI\Top_Down'
testy = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2\Indiana North\Carmel\N1323101243'
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'


#requires topdown folder input
all_circuits = circuitFolderList.circuitFolderList(ind_circuits)
#return(circuit_dict,subdirs2)



#requires topdown folder input
completed_circuits = circuitcheck.circuitCheck(top_down)
#return completed_circuits




#requires list of all folders to be completed to check against and a dictionary object of all available circuits from "circuitfolderlist"
to_be_processed_circuits = circuitsearch.circuitSearch(completed_circuits,all_circuits[0])


for x in to_be_processed_circuits:
    print(x)
    
    #requires a list of folder to input - for this testing it is a single circuit
    pic_files = foldersearch.foldersearch(x) #to_be_processed_circuits
    # return piclist,folder
    if pic_files[0] == []:
        print('\nThe folder has no photographs, skipping folder:',x,'\n')
        continue
    else:
        pass
    
    #requires a full path list of pictures from a circuit
    star_exif = get_exifs.getexif(pic_files[0])
    #return rows,file_logger,current_circuit


    #requires a circuitID, Directory, and the list of rows aquired by the get_exif output
    tocsv = makecsv.makecsv(star_exif[2],pic_files[1],star_exif[0])

    #requires the failed picture files from get_exifs - Accepts Dictionary object from get_exif
    bad_exif = get_failed_exif.getFailedExif(star_exif[1],star_exif[2])

    #requires the circuitID Ideally from "makecsv"
    circuitcomplete.circuitcomplete(star_exif[2])
