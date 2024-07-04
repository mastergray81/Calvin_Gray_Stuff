import os, sys, shutil, csv, time, datetime, glob, re, logging


def makecsv(circuitid,dir,csvrows):
    header = ['Filename','Longitude','Latitude','Camera_Angle']
    
    try:
        
        csv_file = circuitid + ".csv"
        full_path = os.path.join(dir,csv_file)
        print (full_path)
        
        with open(full_path, 'w')  as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvwriter.writerows(csvrows)
            csvfile.close()
            print("CSV file complete!\n")
        
    except Exception as e:
        print(e)
        pass
    return print("The Top-Down CSV file is complete for the following circuit:", circuitid,'\n')
        
