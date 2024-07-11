import arcpy, os, datetime

fc = r"\\nasarcgis\arcmapshare_analyst\ESS_Connections\web_mercator\ENTEGDBAP01_Connections\arcgis_ags_writer_wire_insp@entegdbap01.sde\GRID.WireInsp_PhotoPoints"
shp_dir = r'\\Cdcgpnas02\IVVC_P\DronePhotos\PhotoPoints'
shp = []

def append_SHP():
    start = datetime.datetime.now()
    for root, dirs, files in os.walk(shp_dir): 
        for file in files:
            if file.endswith('.shp'):
                seen = os.path.join(root,file)
                shp.append(seen)
            else:
                pass 

    end = datetime.datetime.now()
    et = (end - start)
    print("\nTime Elapsed for SHP Search: ", et,'\n')

                
    print("\nThere are", len(shp), 'Files')


    if len(shp) > 0:
        print("\nPreparing shp files for append")
        for file in shp: #change test back to shp for production
            try:
                print("Adding Circuit Column for Circuit " + file)
                arcpy.management.AddField(file, 'CIRCUIT','TEXT')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
        
            try:
                print("Adding POINT_X Column " + file)
                arcpy.management.AddField(file, 'POINT_X','DOUBLE')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
        
            try:
                print("Adding POINT_Y Column " + file)
                arcpy.management.AddField(file, 'POINT_Y','DOUBLE')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())

            try:
                print("Calculating Circuit Column " + file)
                arcpy.management.CalculateField(file, 'CIRCUIT', '!Name![:11]')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())  

            try:
                print("Calculating POINT_X Column " + file)
                arcpy.management.CalculateField(file, 'POINT_X', '!X!')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())  

            try:
                print("Calculating POINT_Y Column " + file)
                arcpy.management.CalculateField(file, 'POINT_Y', '!Y!')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())  
            try:
                print('Calculating the URL ' + file)
                arcpy.management.CalculateField(file, 'PHOTOSURL',"!PATH!.replace('\\Cdcgpnas02\IVVC_P\', 'https://egisapps.duke-energy.com/WireSizePhotos\')")
                arcpy.management.CalculateField(file,'PHOTOSURL','!PHOTOSURL![1:]')
            except arcpy.ExecuteError:
                print(arcpy.GetMessages())
    else:
        pass

    if len(shp) > 0:
        
    #Append all files in list to PhotoPoints
        print("Appending all SHP files to IVVC Photopoints")
        try:
            arcpy.management.Append(shp,fc,"NO_TEST") #change test to shp for production

            print("Completed Appending all files to Photopoints")

        except arcpy.ExecuteError:
            print(arcpy.GetMessages(),"\n ")

    else:
        pass
    
