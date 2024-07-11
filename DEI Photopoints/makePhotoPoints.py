import arcpy,datetime

shp_dir = r'\\Cdcgpnas02\IVVC_P\DronePhotos\PhotoPoints'
invalid_photo = r'\\Cdcgpnas02\IVVC_P\DronePhotos\PhotoPoints\invalid_photo.txt'
dei = r'C:\Users\cgray7\OneDrive - Duke Energy\Documents\ArcGIS\Projects\MyProject5\DEIPHOTOPOINTS.gdb'

def makePhotoPoints(path): 
    try:
        start = datetime.datetime.now()
        filename = path[-11:]
        arcpy.management.GeoTaggedPhotosToPoints(path,shp_dir + '\\' + filename)
        print('\nFinished Copying ', filename, 'to destination dir ' + shp_dir + '\n')
        print("\nRun Time\n")
        end =  datetime.datetime.now()
        et =  end-start
        print('---------------------')
        print("Time Elapsed for SHP Creation: ", et,'\n')
        print('---------------------')
    except arcpy.ExecuteError:
            print("\nError with " + path[-11:]+"\n")
            print(arcpy.GetMessages())
            

    
    