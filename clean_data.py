import json

with open("C:/Users/antoi/VSC_projects/bioinfo_map/data.json") as dic:        
    #store file data in object        
    data = json.load(dic)

dict_out = {}
for key, value in data.items():
    pmid = value['pmid']
    del value['pmid']
    value['location'] = key
    dict_out[pmid] = value
with open("C:/Users/antoi/VSC_projects/bioinfo_map/data_clean.json", 'w', encoding ='utf8') as data_file:
    json.dump(dict_out, data_file, indent = 6, ensure_ascii = False)
    data_file.close()
