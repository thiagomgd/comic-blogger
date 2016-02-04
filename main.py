__author__ = "Thiago Margarida"
__version__ = "0.1"

import os
import json
import pprint
import requests
#http://www.comicvine.com/api/documentation#toc-0-11
#http://josephephillips.com/comic_vine_api_examples_part2/
#http://www.comicvine.com/forums/api-developers-2334/the-new-api-same-as-the-old-api-except-for-the-dif-1449264/

def get_issues():
    url = issues_url.format(apikey, date, sort, format_, field_list, offset.format(off_set))
    r = requests.get(url, timeout=30)
    content = json.loads(r.content.decode("utf-8"))
    return content["results"]

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

arcticle = ""
arcticle_items = []
item_layout = config["item_layout"]
apikey = config["apikey"]
date = "&filter=store_date:2016-02-03"
sort = "&sort=name"
offset = "&offset={}"
off_set = 0

format_ = "&format=json"
field_list = "" #"&field_list=site_detail_url,name"

issues_url = "http://www.comicvine.com/api/issues/?api_key={}{}{}{}{}{}" #&field_list=site_detail_url,name

results = get_issues()

while results:
    #print('***************************************************************')
    #print(len(results))
    #a = 0
    for i in results:
        #a=a+1
        #pprint.pprint(i)
        #print('----------------------------------------------')
        #print(a)
        #print(i["name"])
        if ("name" in i and i["name"] != None and (
            "Vol" in i["name"] or
            "HC" in i["name"] or
            "TPB" in i["name"])):
            #print(i["name"])
            #pprint.pprint(i["name"] + ' ' + i["volume"]["name"])
            pprint.pprint(i)
            arcticle_items.append(item_layout.format_map(i))
            break
    off_set = off_set + 100
    results = get_issues()

print("\n".join(arcticle_items))
