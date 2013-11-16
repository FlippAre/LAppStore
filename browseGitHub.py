import requests
import json
import os

github_user = os.environ["GITHUB_USER"]
github_password = os.environ["GITHUB_PASSWORD"]

def fetch():
	return_json = {}
	return_json["apps"] = []
	response = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps",auth=(github_user, github_password))
	json_data = json.loads(response.text)

	if response.ok:
		j = 0
		for i, item in enumerate(json_data):
			if json_data[i]["type"] == "dir":
				appname = json_data[i]["name"]
			
				return_json["apps"].append({})
				return_json["apps"][j].update({"name":appname})
				#Load README
				readme = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps/"+appname+"/"+"README.md?ref=master",auth=(github_user, github_password))
				if readme.ok:
					json_readme = json.loads(readme.text)
					#print json_readme
					return_json["apps"][j].update( {"readme":json_readme["content"]})
					j += 1
				#Load app.json

	return return_json

