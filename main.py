import bottle
from bottle import response
import browseGitHub
import os

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

print("Starting LappStore!")
connection = browseGitHub.GitHubConnector()
print("Loading data from GitHub...")
connection.getAppsJSON()
print("Server is ready!")

lappStore = bottle.app()

@lappStore.route('/', method='GET')
def getAllApps():
    return connection.getAppsJSON()

@lappStore.route('/app/<app>' , method='GET')
def getApp(app = ""):
    apps = connection.getAppsJSON()
    print(app)
    print(apps['apps'])
    if app in apps['apps']:
        return apps['apps'][app]
    else:
        return {'error':'App does not exists'}

@lappStore.route('/refresh', method='POST')
def refreshApps():
    connection.getAppsJSON(True)
    return {"status":"refresh successfull!"}

lappStore.install(EnableCors())

lappStore.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))