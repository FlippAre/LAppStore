from bottle import route, run
import browseGitHub
import os

print("Starting LappStore!")

connection = browseGitHub.GitHubConnector()

print("Loading data from GitHub...")
connection.getAppsJSON()

print("Server is ready!")

@route('/')
def getAllApps():
	return connection.getAppsJSON()

@route('/app/<app>' , method='GET')
def getApp(app = ""):
	apps = connection.getAppsJSON()
	if app in apps['apps']:
		return apps['apps'][app]
	else:
		return {'error':'App does not exists'}

@route('/refresh', method='POST')
def refreshApps():
	connection.getAppsJSON(True)
	return {"status":"refresh successfull!"}


run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))