from bottle import route, run
import browseGitHub
import os

apps = browseGitHub.fetch()

@route('/')
def getAllApps():
	return apps

@route('/app/<app>' , method='GET')
def getApp(app = ""):
	if app in apps['apps']:
		return apps['apps'][app]
	else:
		return {'error':'App does not exists'}

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))