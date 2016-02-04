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
    url = issues_url.format(apikey, date, sort, res_format, field_list, offset.format(off_set))
    r = requests.get(url, timeout=30)
    content = json.loads(r.content.decode("utf-8"))
    return content["results"]

def get_volume(api_detail_url):
    url = "{}?api_key={}{}".format(api_detail_url, apikey, res_format)
    r = requests.get(url, timeout=30)
    content = json.loads(r.content.decode("utf-8"))
    return content["results"]

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

arcticle = ""
arcticle_items = []
issues = {}

item_layout = config["item_layout"]
apikey = config["apikey"]
date = "&filter=store_date:2016-02-03"
sort = "&sort=name"
offset = "&offset={}"
off_set = 0

res_format = "&format=json"
field_list = "" #"&field_list=site_detail_url,name"

issues_url = "http://www.comicvine.com/api/issues/?api_key={}{}{}{}{}{}" #&field_list=site_detail_url,name

results = get_issues()

while results:
    for i in results:
        if ("name" in i and i["name"] != None and (
                "Vol" in i["name"] or
                "HC" in i["name"] or
                "TPB" in i["name"])):

            volume = get_volume(i["volume"]["api_detail_url"])

            if volume["publisher"]:
                pub_name = volume["publisher"]["name"]
                item = item_layout.format_map(i)
                #issues[pub_name] = issues[pub_name].append(item) if pub_name in issues else [item]
                if pub_name in issues:
                    issues[pub_name].append(item)
                else:
                    issues[pub_name] = [item]

    off_set = off_set + 100
    results = get_issues()

order = [
'Marvel',
'DC Comics',
'Image',
'IDW Publishing',
'Dynamite Entertainment',
'Dark Horse Comics',
'Boom! Studios',
'Archie Comics',
'Kodansha Comics USA',
'Action Lab',
'Dark Horse Manga',
'Delcourt',
'Antarctic Press',
'Comixtribe',
"Joe's Comics",
'Skybound',
'Viz',
'First Second Books',
'Les Humanoïdes Associés'
]

for pub in order:
    if pub in issues:
        pub_text = "<h4>Editora: {}</h4>\n\n{}".format(pub, "\n".join(issues[pub]))
        arcticle = "{}{}\n\n".format(arcticle, pub_text)

with open('arcticle.txt', 'wb') as outfile:
    outfile.write(bytes(arcticle, 'UTF-8'))
