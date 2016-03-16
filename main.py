__author__ = "Thiago Margarida"
__version__ = "0.1"

import os
import json
import pprint
import requests
#http://www.comicvine.com/api/documentation#toc-0-11
#http://josephephillips.com/comic_vine_api_examples_part2/
#http://www.comicvine.com/forums/api-developers-2334/the-new-api-same-as-the-old-api-except-for-the-dif-1449264/

headers = {"User-Agent": "Comic Listing by Thiago"}

def check_tpb_hc(i):
    return ("name" in i and i["name"] != None and (
                "Vol" in i["name"] or
                "HC" in i["name"] or
                "TPB" in i["name"]))

def check_first_issue(i):
    #return (not("name" in i and i["name"] != None and (
    #            "Vol" in i["name"] or
    #            "HC" in i["name"] or
    #            "TPB" in i["name"])) and i["issue_number"] == "1")
    return i["issue_number"] == "1"

def get_issues():
    url = issues_url.format(apikey, date, sort, res_format, field_list, offset.format(off_set))
    r = requests.get(url, timeout=30, headers=headers)
    content = json.loads(r.content.decode("utf-8"))
    return content["results"]

def get_volume(api_detail_url):
    url = "{}?api_key={}{}".format(api_detail_url, apikey, res_format)
    r = requests.get(url, timeout=30, headers=headers)
    content = json.loads(r.content.decode("utf-8"))
    return content["results"]

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

arcticle = ""
arcticle_items = []
issues = {}

item_layout = config["item_layout"]
apikey = config["apikey"]
date = "&filter=store_date:2016-02-21|2016-02-27"
sort = "&sort=name"
offset = "&offset={}"
off_set = 0

res_format = "&format=json"
field_list = "" #"&field_list=site_detail_url,name"

issues_url = "http://www.comicvine.com/api/issues/?api_key={}{}{}{}{}{}" #&field_list=site_detail_url,name

results = get_issues()

while results:
    for i in results:
        #if check_first_issue(i):
        if check_tpb_hc(i):

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
'Vertigo',
'Image',
'IDW Publishing',
'Dynamite Entertainment',
'Dark Horse Comics',
'Boom! Studios',
'Archie Comics',
'Titan Comics',
'Valiant',
'Seven Seas Entertainment',
'Yen Press',
'Kodansha',
'Kodansha Comics USA',
'Kadokawa Shoten',
'Action Lab',
'UDON',
'Dark Horse Manga',
'Delcourt',
'Antarctic Press',
'Comixtribe',
"Joe's Comics",
'Skybound',
'Viz',
'First Second Books',
'Akita Shoten',
'Tokuma Shoten',
'Vertical Inc.',
'Netcomics',
'American Gothic Press',
'Les Humanoïdes Associés',
'Andrews McMeel Publishing'
]

for pub in order:
    if pub in issues:
        pub_text = "<h4>Editora: {}</h4>\n{}<br/><br/>".format(pub, "\n<br/>".join(issues[pub]))
        arcticle = "{}{}\n\n".format(arcticle, pub_text)
        issues[pub] = None

for i in issues:
    if issues[i] != None:
        print(i)

with open('arcticle.txt', 'wb') as outfile:
    outfile.write(bytes(arcticle, 'UTF-8'))
