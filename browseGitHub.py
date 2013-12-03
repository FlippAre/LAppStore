import requests
import json
import os
import arrow
import base64

class GitHubConnector:

	def __init__(self):
		self.github_user = os.environ["GITHUB_USER"]
		self.github_password = os.environ["GITHUB_PASSWORD"]
		self.baseURL = "https://api.github.com/repos/Lundalogik/LimeBootstrapAppStore"
		self.last_update = arrow.get( "1970-01-01T00:00:01Z" )
		self.cached_return_json = {}

	def getAppsJSON(self, forceRefresh = False):
		repo = requests.get(self.baseURL,auth=(self.github_user, self.github_password))
		repo_json = json.loads(repo.text)
		#Should new data be loaded or cache returned?

		if self.last_update < arrow.get(repo_json["updated_at"]) or forceRefresh:
			print("Fetching new data from GitHub")
			self.last_update = arrow.get(repo_json["updated_at"])
			return_json = {}
			return_json["apps"] = []

			#Find all apps
			appDir = requests.get(self.baseURL + "/contents",auth=(self.github_user, self.github_password))
			if appDir.ok:
				appDir_json = json.loads(appDir.text)
				j = 0
				for i, item in enumerate(appDir_json):
					#Check if it is an app, i.e a directory
					if appDir_json[i]["type"] == "dir":
						appname = appDir_json[i]["name"]
						return_json["apps"].append({})
						return_json["apps"][j].update({"name":appname})

						#Load README for a app
						readme = requests.get(self.baseURL+"/contents/"+appname+"/"+"README.md?ref=master",auth=(self.github_user, self.github_password))
						if readme.ok:
							json_readme = json.loads(readme.text)
							return_json["apps"][j].update( {"readme":json_readme["content"]})

						#Load app.json for a app
						info = requests.get(self.baseURL+"/contents/"+appname+"/"+"app.json?ref=master",auth=(self.github_user, self.github_password), headers={"Accept":"application/vnd.github.VERSION.raw"})
						if info.ok:
							json_info = json.loads(info.text)
							return_json["apps"][j].update( {"info": json_info})

						images = requests.get(self.baseURL+"/contents/"+appname,auth=(self.github_user, self.github_password))
						if images.ok:
							json_images = json.loads(images.text)
							imageFiles = []
							for k, item in enumerate(json_images):
								if json_images[k]["type"] == "file":
									if json_images[k]["name"].rsplit('.',1)[1] in {'jpeg', 'jpg', 'png'}:
										imageFiles.append("https://raw.github.com/Lundalogik/LimeBootstrapAppStore/master/"+appname+"/"+json_images[k]["name"])	
							return_json["apps"][j].update({"images":imageFiles})
						#An app was added and the index counter should be increased
						if readme.ok or info.ok:
							j += 1

			#setup cache for faster responses
			self.cached_return_json = return_json
			return return_json
		else:
			print("Serving cached data")
			return self.cached_return_json
