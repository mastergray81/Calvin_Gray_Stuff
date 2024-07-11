import os, sys, shutil, csv, arcpy
import pandas as pd
import scriptStartTime, circuitcheck,circuitFolderList,circuitsearch,totalTimeElapsed,makePhotoPoints,os,append,emptyFolder
import pandas as pd
import pathlib
from arcpy import env

#Global ENV Settings - This is set to FALSE 
env.overwriteOutput = False
env.workspace = r"\\nasarcgis\arcmapshare_analyst\ESS_Connections\web_mercator\ENTEGDBAP01_Connections\arcgis_ags_writer_wire_insp@entegdbap01.sde"

#Wireinpection Photo Points
fc = r"\\nasarcgis\arcmapshare_analyst\ESS_Connections\web_mercator\ENTEGDBAP01_Connections\arcgis_ags_writer_wire_insp@entegdbap01.sde\GRID.WireInsp_PhotoPoints"

#Centralized location for photopoints shp files
shp_dir = r'\\Cdcgpnas02\IVVC_P\DronePhotos\PhotoPoints'

#folder to start search
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'

#valid file exts
pix = ('.jpg','.JPG')

circuits = []

#Required Interpreter
#C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe

print('Starting Script:\n')
#script global start time
starttime = scriptStartTime.startTime()

print("\nFinding Completed Circuits\n")
#returns all completed circuits to a list
completed_circuits = circuitcheck.circuitCheck()
#return circuitid

#returns all circuits and folders in a list and a dictionary
all_circuits = circuitFolderList.circuitFolderList(ind_circuits)
#return(circuit_dict,subdirs2)

#returns only the folders that have not been completed already
circuits_to_process = circuitsearch.circuitSearch(completed_circuits,all_circuits[0])
# return circuit_paths

#Gets list of all circuits which have "Top_down" previously ran
top_down_circuits = emptyFolder.crossCheck()
#return circuit_list

#remove folders from list that has not been run by top_down
for y in top_down_circuits:
    for x in circuits_to_process:
        if y in x:
            circuits.append(x)

#iterate over folders            
for i in circuits:
    print('\n There are', len(circuits),'circuits')    
    print('\nCurrent folder:',i)
    makePhotoPoints.makePhotoPoints(i)

#prepare and append SHP to database
append.append_SHP()
#nothing to return

#prints the end time with input from "starttime"
totalTimeElapsed.endTime(starttime)