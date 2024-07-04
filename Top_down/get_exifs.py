import os, sys, shutil, csv, time, datetime, glob, re, logging
from exif import Image


def getexif(photos):
    starttime = datetime.datetime.now()
    filecount=0
    rows=[]
    file_logger={}
        
        
    for file in photos:
        filecount += 1
        char = ('\\')
        single_file = str(photos[0])
        try:
            current_circuit = single_file[single_file.rfind(char)+1 : single_file.rfind(char)+12]
        except:
            print('Did it work?', current_circuit)
                
        with open(file,'rb') as image_file:          
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
                char1 = r">"
                char2 = r"</d"
                camera_angle = getvalue[getvalue.find(char1)+1 : getvalue.find(char2)]
                cam_angle = re.sub("[^\d\.]", "", getvalue)
                try:
                    cam_angle = float(cam_angle)
                except:
                    print('There is a problem with',file)

                    file_logger[file] = cam_angle


                rowlist=[]
                try:
                    if type(cam_angle) != str:
                        if abs(cam_angle) > 85 and abs(cam_angle)< 95:
                            rowlist.append(file)
                            rowlist.append(longs)
                            rowlist.append(lats)
                            rowlist.append(cam_angle)
                            rows.append(rowlist) 

                            
                            print('\n')
                            print(filecount)
                            print(file)
                            print('----------------')
                            print("Camera Angle: ", camera_angle)
                            print('----------------')
                            print("X: ", longs)
                            print("Y: ", lats)
                            print('----------------\n')
                            continue
                        else:
                            print(filecount,"\nThe following file is not a top down photo: ", file)
                    else:
                        print(filecount,'\nThe following file has a string for cam angle:',file, "sent to logger")
                        file_logger[file] = cam_angle 
                        continue
                        
                except IOError:
                    print(file, " Cannot be appended, sent to logger!")
                    file_logger[file] = cam_angle 
                    continue 

          
                    
    endtime = datetime.datetime.now()
    print('Time elapsed:',endtime-starttime)
    return rows,file_logger,current_circuit
                
