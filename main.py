from bottle import route, run
import browseGitHub

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

run(host='localhost', port=8080, debug=True)