import os, sys, csv, re
import pandas as pd
from exif import Image


def getFailedExif(mydict,circuitid):
        headers = ['Filename','Longitude','Latitude','Camera_Angle','Issue_Type']
        rows =[]
        csvpath = r'\\Cdcgpnas02\CGDI\Top_Down'
        note_0 = 'This is a Top Down Shot'
        note_1 = "The Camera Angle Cannot Be Resolved"
        note_2 = 'This is not a Top Down Shot'
        
        for x,y in mydict.items():
            rowlist=[]

            try:
                y = float(y)
                #if abs(y) > 85 and abs(y)< 95:
                with open(x,'rb') as image_file:    
                    my_image = Image(image_file)
                    segmentsdict = my_image.get('_segments')
                    image_file.close()
                    segmentsdicts = segmentsdict['succeeding']
                    segmentsdicts = str(segmentsdicts)
                    segmentsdicts = repr(segmentsdicts)
                    lst = list(segmentsdicts.split(r'\\n'))
                    getvalue = lst[53]
                    latitude = lst[22]
                    longitude = lst[23]
                    lats = re.sub("[^\d\.]", "", latitude)
                    longs = re.sub("[^\d\.]", "", longitude)
                    try:
                        rowlist.append(x)
                        rowlist.append(longs)
                        rowlist.append(lats)
                        rowlist.append(y)
                        rowlist.append(note_0)
                        rows.append(rowlist)
                        continue
                

                    except:
                        pass
                #else:
                #    continue          
            except:
                with open(x,'rb') as image_file:    
                    my_image = Image(image_file)
                    segmentsdict = my_image.get('_segments')
                    image_file.close()
                    segmentsdicts = segmentsdict['succeeding']
                    segmentsdicts = str(segmentsdicts)
                    segmentsdicts = repr(segmentsdicts)
                    lst = list(segmentsdicts.split(r'\\n'))
                    getvalue = lst[53]
                    latitude = lst[22]
                    longitude = lst[23]
                    lats = re.sub("[^\d\.]", "", latitude)
                    longs = re.sub("[^\d\.]", "", longitude)
                    rowlist.append(x)
                    rowlist.append(longs)
                    rowlist.append(lats)
                    rowlist.append(y)
                    rowlist.append(note_1)
                    rows.append(rowlist)
                    continue
                                    
                    
        
        try:
            csv_file = 'missed_exif_' + circuitid + '.csv'             
            full_path = os.path.join(csvpath,csv_file)
            with open(full_path, 'w')  as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(headers)
                csvwriter.writerows(rows)
                csvfile.close()

        except IOError:
            pass
        
