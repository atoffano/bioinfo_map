import json
import geojson
from geojson import Feature, Point, FeatureCollection

with open("C:/Users/antoi/VSC_projects/bioinfo_map/data.json") as dic:        
    #store file data in object        
    data = json.load(dic)

features = []
for loc, props in data.items():
    latlong = loc.split(",")
    point = Point((float(latlong[1]), float(latlong[0])))
    features.append(Feature(geometry=point, properties=props))
feature_collection = FeatureCollection(features)

with open('bioinfo_map/data.geojson', 'w') as f:
   geojson.dump(feature_collection, f, indent=4, ensure_ascii = False)


