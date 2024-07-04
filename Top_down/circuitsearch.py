import os, sys, shutil, csv, time, datetime, glob, re, logging

def circuitSearch(circuits_complete, all_circuits_dict):
    
    circuit_paths = list(all_circuits_dict.values())
    for x in circuits_complete:
        for y in circuit_paths:
            if x in y:
                circuit_paths.remove(y)
    
    
    print("Number of circuits to be processed:",len(circuit_paths),'\n------------\n',circuit_paths)
    
    return circuit_paths

#Test Validity
#c = ['N1323101243']
#c = ['N1325531203']
#circuitSearch(c)
'''
test = {'N1323101243':'\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1323101243', 'N1323101245':'\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1323101245', 'N1324011291':'\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324011291'}#, '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324011293', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301242', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301243', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301244', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301245', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301246', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1324301247', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325451221', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325471282', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325471284', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325471286', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325531203', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325531204', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325531205', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325761261', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325761262', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1325761263', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1327941262', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1327941264', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Huntington\\N1143081232', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Huntington\\N1143081235', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1143081235', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1302801201', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1302801203', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1302801205', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1304891281', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1304891283', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1304891285', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305091221', '\\N1305411271', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305411272', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305411273', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana NTDSIC2\\Indiana North\\Noblesville\\N1305411277', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305791251', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305791252', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305791253', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1305791254', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1307681242', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1307681243', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1307681244', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1307681245', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1307681247', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Noblesville\\N1308591201', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\IDEI_TDSIC2\\Indiana North\\Rochester\\N1137281205', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Rochester\\N1137281206', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Rochester\\N1137281207', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Rochester\\N1137281208', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana South\\Franklin_IN\\N5161781237', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana South\\Franklin_IN\\N5164111251']
test_complete = ['\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1323101243', '\\\\Cdcgpnas02\\CGDI\\DEI_TDSIC2\\Indiana North\\Carmel\\N1323101245']

kim = circuitSearch(test_complete,test)
print(len(kim))
'''