import os, csv
 
def circuitcomplete(circuitid):
    header = ['Filename','Longitude','Latitude','Camera_Angle']
    completed_circuits = r'\\Cdcgpnas02\CGDI\Top_Down'
    
    try:
        csv_file = circuitid + ".csv"
        full_path = os.path.join(completed_circuits,csv_file)
        
        with open(full_path, 'w')  as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvfile.close()
        
    except Exception as e:
        print(e)
        pass
        
        
