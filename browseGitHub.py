import requests
import json
import os
import arrow

class GitHubConnector:

	def __init__(self):
		self.github_user = os.environ["GITHUB_USER"]
		self.github_password = os.environ["GITHUB_PASSWORD"]
		self.last_update = arrow.get( "1970-01-01T00:00:01Z" )
		self.cached_return_json = {}


	def getAppsJSON(self):
		repo = requests.get("https://api.github.com/repos/lundalogik/limebootstrap",auth=(self.github_user, self.github_password))
		repo_json = json.loads(repo.text)

		if self.last_update < arrow.get(repo_json["updated_at"]):
			
			self.last_update = arrow.get(repo_json["updated_at"])
			return_json = {}
			return_json["apps"] = []
			appDir = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps",auth=(self.github_user, self.github_password))
			if appDir.ok:
				appDir_json = json.loads(appDir.text)
				j = 0
				for i, item in enumerate(appDir_json):
					if appDir_json[i]["type"] == "dir":
						appname = appDir_json[i]["name"]
					
						return_json["apps"].append({})
						return_json["apps"][j].update({"name":appname})
						#Load README
						readme = requests.get("https://api.github.com/repos/lundalogik/limebootstrap/contents/apps/"+appname+"/"+"README.md?ref=master",auth=(self.github_user, self.github_password))
						if readme.ok:
							json_readme = json.loads(readme.text)
							#print json_readme
							return_json["apps"][j].update( {"readme":json_readme["content"]})
							j += 1
						#Load app.json
			self.cached_return_json = return_json
			return return_json
		else:
			return self.cached_return_json
