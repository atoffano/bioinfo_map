import googlemaps
import os
import pandas as pd
import pubmed_parser as pp
import json
import geojson
from geojson import MultiPoint

publisher = "bioinfo" # String present in target journal to get articles from
pubmed_oa_path = 'D:/pubmed_oa_bulk/xml_ASCII'
maps_api_key = 'AIzaSyD68GqenM81t462k5c180Vv5IZDgafwo0s'

# Parses pubmed oa database (frist downloaded as xml) to get PMIDs of articles from the publisher
def scrapper(publisher):
    articles = pd.DataFrame()
    with os.scandir(pubmed_oa_path) as entries:
        for entry in entries:
            if '.csv' in entry.name:
                df = pd.read_csv(entry)
                parse = df[df['Article Citation'].str.contains(publisher, case=False)]
                articles = pd.concat([articles, parse], axis = 0)
        return articles

# Queries GMap API with a human readable adress. Returns multiple info as a dict, including adress and lat/long.
def get_geocode(adress):
    gmaps = googlemaps.Client(key = maps_api_key)
    geocode_result = gmaps.geocode(adress)
    return geocode_result[0]

#Parses GMap's returned dict to get the location's adress in a formatted way.
def get_adress(geocode):
    return geocode['formatted_address']

#Parses GMap's returned dict to get the location's GPS coordinates as lat and long.
def get_location(geocode):
    return str(geocode['geometry']['location']['lat']) + "," + str(geocode['geometry']['location']['lng'])

# Cleans email adress from 1st author's affiliation
def clean_mail(dict_out):
    aff = dict_out['affiliation'].split()
    if "@" in aff[-1]:
        aff.remove(aff[-1])
        dict_out['affiliation'] = " ".join(aff)
    return dict_out

def marker_list(data_path):
    with open(data_path) as dic:        
        data = json.load(dic)
        marker = []
        for key in data.keys():
            marker.append(eval(key))
    with open('bioinfo_map/marker.geojson', 'w') as f:
        geojson.dump(MultiPoint(marker), f, indent=4)


articles = scrapper(publisher)
print(articles)
data = {}
i = 1
# parses pubmed oa, returning PMIDs that are used to query pubmed's etuils api to get infos about an article.
# Then queries GMaps API to get adress and gps coord. before dumping all that to json
with open("C:/Users/antoi/VSC_projects/bioinfo_map/data.json", 'w', encoding ='utf8') as data_file:
    for pmid in articles['PMID']:
        try:
            dict_out = pp.parse_xml_web(pmid, save_xml=False)
            dict_out = clean_mail(dict_out)
            geocode = get_geocode(dict_out['affiliation'])
            dict_out['adress'] = get_adress(geocode)
            data[get_location(geocode)] = dict_out
            print(i, articles['PMID'])
            i += 1
        except:
            print("Error from pubmed api or google maps api")
    json.dump(data, data_file, indent = 6, ensure_ascii = False)
    data_file.close()
marker_list("C:/Users/antoi/VSC_projects/bioinfo_map/data.json")
print("...Done")

