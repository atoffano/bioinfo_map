import geojson
import json

with open("C:/Users/antoi/VSC_projects/bioinfo_map/data.json") as dic:        
    #store file data in object        
    data = json.load(dic)

marker = []
for loc in data.keys():
    print(loc)
    latlong = loc.split(",")
    marker.append(eval(latlong[1] + "," + latlong[0]))

with open('bioinfo_map/marker.geojson', 'w') as f:
   geojson.dump(MultiPoint(marker), f, indent=4)


