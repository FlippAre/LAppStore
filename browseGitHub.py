import requests
import json
import os
import arrow
import base64

class GitHubConnector:

	def __init__(self):
		self.github_user = os.environ["GITHUB_USER"]
		self.github_password = os.environ["GITHUB_PASSWORD"]
		self.last_update = arrow.get( "1970-01-01T00:00:01Z" )
		self.cached_return_json = {}

	def getAppsJSON(self, forceRefresh = False):
		repo = requests.get("https://api.github.com/repos/lundalogik/limebootstrap",auth=(self.github_user, self.github_password))
		repo_json = json.loads(repo.text)
		#Should new data be loaded or cache returned?
		if self.last_update < arrow.get(repo_json["updated_at"]) or forceRefresh:
			self.last_update = arrow.get(repo_json["updated_at"])
			return_json = {}
			return_json["apps"] = []

			#Find all apps
			appDir = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps",auth=(self.github_user, self.github_password))
			if appDir.ok:
				appDir_json = json.loads(appDir.text)
				j = 0
				for i, item in enumerate(appDir_json):
					if appDir_json[i]["type"] == "dir":
						appname = appDir_json[i]["name"]
						return_json["apps"].append({})
						return_json["apps"][j].update({"name":appname})

						#Load README for a app
						readme = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps/"+appname+"/"+"README.md?ref=master",auth=(self.github_user, self.github_password))
						if readme.ok:
							json_readme = json.loads(readme.text)
							return_json["apps"][j].update( {"readme":json_readme["content"]})
						info = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps/"+appname+"/"+"app.json?ref=master",auth=(self.github_user, self.github_password), headers={"Accept":"application/vnd.github.VERSION.raw"})
						#Load app.json for a app
						if info.ok:
							json_info = json.loads(info.text)
							print(json_info)
							#string = (base64.urlsafe_b64decode(json_info ["content"]).decode('utf-8'))
							#json_string = json.loads(json_info ["content"])
							return_json["apps"][j].update( {"info": json_info})
						if readme.ok or info.ok:
							j += 1
			#setup cache for faster responses
			self.cached_return_json = return_json
			return return_json
		else:
			return self.cached_return_json
