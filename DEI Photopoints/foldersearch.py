import os

csvpath = r'\\Cdcgpnas02\CGDI\Top_Down'
ind_circuits = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2'
pix = ('JPG','jpg')
bad_ext = ('.docx', '.DOCX','.db','.DB','.pdf','.PDF','.csv','.CSV') 
test = r'\\Cdcgpnas02\CGDI\DEI_TDSIC2\Indiana North\Carmel\N1325531203'

def foldersearch(folders):
    subdirs = []
    #test folder - remove docx and thumbs from dirs
  
    top_dir = os.listdir(folders)
    for i in top_dir:
        if i.endswith(bad_ext):
            top_dir.remove(i)
    

    #get full dir for the test circuits 
    for i in top_dir:
        dir = os.path.join(folders,i)
        subdirs.append(dir)
    #print(subdirs)

    piclist=[]
    try:
        for i in subdirs:
            item = os.listdir(i)
            for x in item:
                if x.endswith(pix):
                    filename = os.path.join(i,x)
                    piclist.append(filename)
                else:
                    continue
            #print(len(piclist))
    except:
        print("There in an error with file:",item)
    piclist.sort()
        #print(piclist)

    return piclist,folders

