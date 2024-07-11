import os, sys, shutil, csv, arcpy
import pandas as pd

#Centralized location for photopoints shp files
shp_dir = r'\\Cdcgpnas02\IVVC_P\DronePhotos\PhotoPoints'

#Wireinpection Photo Points
fc = r"\\nasarcgis\arcmapshare_analyst\ESS_Connections\web_mercator\ENTEGDBAP01_Connections\arcgis_ags_writer_wire_insp@entegdbap01.sde\GRID.WireInsp_PhotoPoints"

def circuitCheck():
    
    #deletes previously used folder for a fresh one
    if os.path.exists(shp_dir):
        shutil.rmtree(shp_dir)
        print("\nPhotoPoints Directory Deleted\n")
        print('\nCreating new PhotoPoints Directory\n')
        os.makedirs(shp_dir)
        print('\nDirectory Completed\n')
    else:
        print('\nCreating new PhotoPoints Directory')
        os.makedirs(shp_dir)
        
    #Deletes old Photopoints.csv generated previously 
    if os.path.exists(r"C:\Users\public\PhotoPoints.csv"):
        print("\nDeleting Photopoints.csv \n")
        os.remove(r"C:\Users\public\PhotoPoints.csv")
        print("File deleted: Creating New PhotoPoints.csv")


    #Doesn't Work in 2.9 - will work out of session in newer iterations
    print("\nPreparing csv file")
    arcpy.conversion.ExportTable(fc,"C:\\Users\\public\\PhotoPoints.csv")
    print("\nPhotopoints.csv Created\n")

    photopoints = pd.read_csv("C:\\Users\\public\\PhotoPoints.csv", dtype={"CIRCUIT":"string"})
    circuitid =  photopoints.CIRCUIT.dropna().unique().tolist()
    
    return circuitid

circuitCheck()