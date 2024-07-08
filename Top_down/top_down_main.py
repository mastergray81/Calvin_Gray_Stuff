import get_failed_exif, makecsv, circuitcomplete, foldersearch, get_exifs, circuitcheck, circuitsearch, circuitFolderList, scriptStartTime, totalTimeElapsed

#test folder to get the script to work proper
top_down = r'\\Cdcgpnas02\CGDI\Top_Down'
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'

#no requirements - starts timer
start_time = scriptStartTime.startTime()
#returns starttime

#requires topdown folder input
all_circuits = circuitFolderList.circuitFolderList(ind_circuits)
#return(circuit_dict,subdirs2)

#requires topdown folder input
completed_circuits = circuitcheck.circuitCheck(top_down)
#return completed_circuits

#requires list of all folders to be completed to check against and a dictionary object of all available circuits from "circuitfolderlist"
to_be_processed_circuits = circuitsearch.circuitSearch(completed_circuits,all_circuits[0])
#return circuit_paths

#Iterate through the circuits as an input to "foldersearch"
for x in to_be_processed_circuits:
    print(x)
    
    #requires a single circuit from a list
    pic_files = foldersearch.foldersearch(x) #to_be_processed_circuits
    # return piclist,folder
    
    # Evaluates if the foldersearch grabbed ANY photos, if not it will skip processing that directory and move to the next on in the list
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
    #does not return anything but a print statment... here there is a variable but it is unused
    
    #if statement prevents writing of a "missed_exif_###.csv" file if dict input is empty
    if star_exif[1] != {}:
        print('\n*************************************************')
        print('\nThere are',len(star_exif[1]), 'bad photos in', star_exif[2])
        for x,y in star_exif[1].items():
            print(x,':',y)
        print('\n*************************************************\n')
        
        #requires the failed picture files from get_exifs - Accepts Dictionary object from get_exif
        bad_exif = get_failed_exif.getFailedExif(star_exif[1],star_exif[2])
        #does not return anything but generates csv of the "bad exif" extracts, there is a variable but it is unused
    
    else: #validate that there are not any "bad_exif" files caught in logger dict
        print('\n*************************************************')
        print('\nThere are',len(star_exif[1]), 'bad photos in', star_exif[2])
        print('\n*************************************************\n')
        pass # do nothing write the "top_down csv"

    #requires the circuitID Ideally from "makecsv"
    circuitcomplete.circuitcomplete(star_exif[2])
    #does not return anything but it generates an empty csv to track circuits that have been processed in the "top_down" directory

totalTimeElapsed.endTime(start_time)