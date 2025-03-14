import pandas as pd
import datetime, os, sys, glob,arcpy
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

start = datetime.datetime.now()

file = r'\\********\CGDI\DEI-ASSETS&POLES\DEI_WireInpsection_CommentPoints.csv'
fc = r'\\*******\arcgis_ags_writer_wire_insp@entegdbap01.sde\GRID.WireInsp_Comments_DukeCS'
query = r"circuitid LIKE 'N%'"

#Deletes old Photopoints.csv generated previously

if os.path.exists(r'\\********\CGDI\DEI-ASSETS&POLES\DEI_WireInpsection_CommentPoints.csv'):
    print("\nDeleting DEI_WireInpsection_CommentPoints.csv \n")
    os.remove(r'\\******\CGDI\DEI-ASSETS&POLES\DEI_WireInpsection_CommentPoints.csv')
    print("File deleted\n\nCreating DEI_WireInpsection_CommentPoints.csv")

 

#Doesn't Work in 2.9 - will work out of session in newer iterations
print("\nPreparing csv file")
arcpy.conversion.ExportTable(fc,"\\\\**********\\CGDI\\DEI-ASSETS&POLES\\DEI_WireInpsection_CommentPoints.csv",query)
print("\nDEI_WireInpsection_CommentPoints.csv Created\n")

df = pd.read_csv(file,usecols=None)

#top directory
top = r'\\*******\CGDI\DEI_TDSIC2'
ind_n = r'\\******\CGDI\DEI_TDSIC2\Indiana North'
ind_s = r'\\******\CGDI\DEI_TDSIC2\Indiana South'

top_dir = [ind_n,ind_s] 

pix = ('JPG','jpg')
bad_ext = ('.docx', '.DOCX','.db','.DB','.pdf','.PDF','.lnk')

def circuitFolderList():
    picfiles=[]
    for x, y, z in os.walk(top):
        for file in z:
            if file.endswith(pix):
                picfiles.append(os.path.join(x,file))
    return picfiles

#circuitFolderList()
chalme = circuitFolderList()

reflist = []
for x in df.iloc[:,-1]:
    if ',' in x:
        #print(x[:x.index(",")])
        reflist.append(x[:x.index(",")])
    else:
        reflist.append(x)
        #print(x)

print("REFLIST",len(reflist))

empty = 'Not Found'
finals = []
for x in reflist:
    check = 0
    for y in chalme:
        if x in y:
            check = 1
            finals.append(y)
            break
    if check == 0:
        finals.append(empty)

simp = pd.Series(finals)
df['PATH'] = simp
           
print(len(finals))          
#print(df)  
print(finals)
df.to_excel(r'\\*******\CGDI\DEI-ASSETS&POLES\DV_Comment_Point_Index.xlsx')  
#print(df)      

print("XLSX FILE COMPLETED")
end = datetime.datetime.now()
time = end - start

print('ALL DONE!\nTime Eplapsed:',time)
