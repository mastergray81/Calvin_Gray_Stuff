import pyodbc, os, sys, arcpy, traceback, asyncio
from arcpy.management import GeoTaggedPhotosToPoints
import pandas as pd 


"""
Understand assignment operators

Understand comparision operators

Understand data types
    List
    String 
    Int 
    Float

Understand dot notation

Understand for loops

Understand .format() method

Understand exceptin handining
    try:
        ...
    except:
        ...

Understand functions

Understand Classes

Understand modules

Understand pandas

Undertand pyodbc

Understand arcpy
"""

class ETL_Processing():

    """
    def __init__
        this function creats objects in the class that can be used by methods contained in the class.
        the objects can also be used outside the class by calling

        self.jira_server -> this is the server connection properites. 51433 is the port. DBJIRADCP1 is server name. PROD is verison of db on server
        self.jira_database -> the database you connect to
        self.jira_user_name -> 
    """
    def __init__(self, *args) -> None:
        self.jira_server = 'DBJIRADCP1\PROD,51433'
        self.jira_database = 'JiraDC_PROD'
        #self.jira_user_name= "\\".join(["NAM", "ENTSYST"])
        self.password = '9On0~k[o+2E]eJG'
        self.driver = '{ODBC Driver 13 for SQL Server}'
        self.jira_connection_string = f"DRIVER={self.driver};SERVER={self.jira_server};DATABASE={self.jira_database};Trusted_Connection=yes"
        #self.jira_connection_string = f"DRIVER={self.driver};SERVER={self.jira_server};DATABASE={self.jira_database};UID=NAM\ENTSYST;PWD={self.password}"
        self.jira_conn = pyodbc.connect(self.jira_connection_string)
        self.gdb_base = r'\\Cdcgpnas02\cgdi\DroneSurveyImages\MobileMapPackages\Template\Tool Development\subopts-drone-photo\GeoTaggedPhotoPoints.gdb\\fc_{}'
        self.gdb_base_tb = r'\\Cdcgpnas02\cgdi\DroneSurveyImages\MobileMapPackages\Template\Tool Development\subopts-drone-photoGeoTaggedPhotoPoints.gdb\\tb_{}'
        self.directory_base=r'\\Cdcgpnas02\cgdi\DroneSurveyImages\{}\{}\{}\{}'
        self.circuitID_list = []
        self.state_list = []
        self.area_list = []
        self.ops_ctr = []
        self.aprx = r'\\Cdcgpnas02\cgdi\DroneSurveyImages\MobileMapPackages\Template\Tool Development\subopts-drone-photo\GeoTagged_PhotoPoints.aprx'
        self.list_args = args[0]
        self.fc_dronephoto = r'\\nasarcgis\ARCMAPSHARE_ANALYST\ESS_Connections\analyst\ENTEGDBANAP01_Connections\arcgis_ags@entegdbap01.sde\ANALYSIS.cgdi_drone_photo_point'

    async def queryJira(self):

        def sync_connect():
            return pyodbc.connect(self.jira_connection_string)
        
        loop = asyncio.get_running_loop()
        conn = await loop.run_in_executor(None, sync_connect)
        cursor = conn.cursor()
        query = """with CTE as
                (SELECT LEFT(JIssue.SUMMARY,8) AS circuitid, MAX(CG.CREATED) AS Max_Date, CAST(CI.NEWSTRING as nvarchar(50)) 
                AS Last_Status, Jissue.issuestatus FROM [JiraDC_PROD].[jiraschema].jiraissue JIssue JOIN [JiraDC_PROD].[jiraschema].project PRJ 
                ON JIssue.PROJECT = PRJ.id JOIN [JiraDC_PROD].jiraschema.changegroup CG ON JIssue.ID = CG.issueid JOIN [JiraDC_PROD].[jiraschema].changeitem CI 
                ON CG.ID = CI.groupid AND CI.FIELD = 'status' and FIELDTYPE = 'jira' WHERE PRJ.ID = 33113 AND (issuestatus IN ('34817','34818', '34819', '34820','34821', '37201')) 
                GROUP BY LEFT(JIssue.SUMMARY,8), 
                CAST(CI.NEWSTRING as nvarchar(50)), Jissue.issuestatus)

                SELECT circuitid, Count(circuitid) as CircuitID from CTE 
                Group By circuitid"""
        
        cursor.execute(query)
        rows = list(cursor.fetchall())

        catch_list = []
        for row in rows:
            arr=[row[0], row[1]]
            catch_list.append(arr)

        arcMessage = "The list of circuits to be executed: {}".format(catch_list)
        arcpy.AddMessage(arcMessage)
        cursor.close()
        self.jira_conn.close()
        return catch_list
    
    async def compare_jira_xlsx(self):
        arcpy.AddMessage("Searching for circuits")
        #query that gets all jira statuses from kanban sub opts
        jira = await self.queryJira()
        #data frame of jira query to be joined later with merge method
        df_jira = pd.DataFrame(jira, columns=["circuitid","count"])
    
        aprx = arcpy.mp.ArcGISProject(self.aprx)
        map_obj = aprx.listMaps("Map")[0]
        target_layer = map_obj.listLayers("Drone Photo Point")[0]

        column_names = [f.name for f in arcpy.ListFields(target_layer)]
        #print(column_names)
        df_arcpy_photoPoints = pd.DataFrame(arcpy.da.SearchCursor(target_layer, "*"), columns=column_names)
        print(self.list_args)
        df_xlsx_masterCirc = pd.read_excel(r'C:\Users\cgray7\OneDrive - Duke Energy\Circuit Surveys - Sub Opt\CGDI Surveys_SubOpt Circuit Tracking_2023.xlsx', header=1)
        merged_photoPoints = pd.merge(df_jira, df_arcpy_photoPoints, on="circuitid", how="left")
        circ_nonMatch = merged_photoPoints[merged_photoPoints['objectid'].isna()]
        circ_nonMatch = pd.DataFrame(circ_nonMatch['circuitid'])
        circ_nonMatch['circuitid'] = circ_nonMatch['circuitid'].astype(str)
        df_xlsx_masterCirc['circuitid'] = df_xlsx_masterCirc['Circuit ID'].astype(str)
        merge_masterCirc = pd.merge(circ_nonMatch, df_xlsx_masterCirc, on="circuitid", how="left")
        self.circuitID_list = merge_masterCirc['circuitid'].tolist()

        self.state_list = merge_masterCirc['State'].tolist()
        self.area_list = merge_masterCirc['Zone (NEW)'].tolist()
        self.ops_ctr = merge_masterCirc['Ops Ctr (New)'].tolist()
        print(self.ops_ctr)
        for i in range(len(self.ops_ctr)):
            if '(' in self.ops_ctr[i]:
                self.ops_ctr[i] = self.ops_ctr[i][:self.ops_ctr[i].index(' (')]
                print("New List: ",self.ops_ctr)
            else:
                pass



    async def run_geotagged(self):
        try:
            await self.compare_jira_xlsx()
            arcpy.AddMessage("Initiating photo uploading")
            for i, row in enumerate(self.circuitID_list):
                message_one = "Starting {}".format(row)
                print(message_one)
                arcpy.AddMessage(message_one)
                base = self.directory_base.format(self.state_list[i], self.area_list[i], self.ops_ctr[i], self.circuitID_list[i])
                outPutFeatureClass = self.gdb_base.format(self.circuitID_list[i])
                outPutFeatureTable = self.gdb_base_tb.format(self.circuitID_list[i])
                if not arcpy.Exists(outPutFeatureClass):
                    arcpy.AddMessage("Circuit geo tagged photos not created in GIS")
                    base = self.directory_base.format(self.state_list[i], self.area_list[i], self.ops_ctr[i], self.circuitID_list[i])
                    outPutFeatureClass = self.gdb_base.format(self.circuitID_list[i])
                    outPutFeatureTable = self.gdb_base_tb.format(self.circuitID_list[i])
                    arcpy.AddMessage("RUNNING: {} and {}".format(outPutFeatureClass, outPutFeatureTable))
                    try:
                        arcpy.env.overwriteOutput = True
                        GeoTaggedPhotosToPoints(base, outPutFeatureClass, outPutFeatureTable, Include_Non_GeoTagged_Photos='ONLY_GEOTAGGED', Add_Photos_As_Attachments='NO_ATTACHMENTS')
                        self.append_to_photoPoints(outPutFeatureClass, row)
                    except Exception as e:
                        arcpy.AddMessage(e)
                        continue
                else:
                    arcpy.AddMessage("Already Exist")
                    continue
            print("Finished Running Available Photos")
        except Exception as e:
            traceback_info = traceback.format_exc()
            message_error = "Report error, try again, or use manual process", " Error: \n {} \n{}".format(e, traceback_info)
            
            arcpy.AddMessage(message_error)

    def append_to_photoPoints(self, outPutFeatureClass, circuitID):
        aprx = arcpy.mp.ArcGISProject(self.aprx)
        map_obj = aprx.listMaps("Map")[0]
        target_layer = map_obj.listLayers("Drone Photo Point")[0]

        fieldMappings = arcpy.FieldMappings()
        field_map_name= arcpy.FieldMap()
        field_map_path = arcpy.FieldMap()

        field_map_path.addInputField(outPutFeatureClass, "Path")
        field_map_path.addInputField(target_layer, "path")
        
        field_map_name.addInputField(outPutFeatureClass, "Name")
        field_map_name.addInputField(target_layer, "name")

        photo_path = field_map_path.outputField
        photo_path.name = "Path"
        field_map_path.outputField = photo_path

        name_path = field_map_name.outputField
        name_path.name = "Name"
        field_map_name.outputField = name_path

        fieldMappings.addFieldMap(field_map_name)
        fieldMappings.addFieldMap(field_map_path)
        arcpy.Append_management(outPutFeatureClass, target_layer, "NO_TEST", fieldMappings)
        arcpy.SelectLayerByAttribute_management(target_layer, "NEW_SELECTION", "circuitid IS NULL")
        expression = r'{}'.format(circuitID)
        arcpy.CalculateField_management(target_layer, "circuitid", expression, "SQL")
        arcpy.SelectLayerByAttribute_management(target_layer, "CLEAR_SELECTION")

    async def run(self):
        arcpy.AddMessage("Initated")
        await self.run_geotagged()

if __name__ == "__main__":
    
    args = sys.argv[1:]
    env = ETL_Processing(args)
    asyncio.run(env.run())
