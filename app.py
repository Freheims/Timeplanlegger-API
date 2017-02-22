#!flask/bin/python3
from flask import Flask, jsonify
from flask.ext.restful import Api, Resource
import api
import json

app = Flask(__name__)
webapi = Api(app)

@app.route('/')
def index():
    return "API infopage"

class BuildingsAPI(Resource):
    def get(self, uni):
        filename = uni + ".json"
        file = open(filename, "r")
        content = json.load(file)
        file.close()
        return content
        #return getBuildings(university)

class ScheduleAPI(Resource):
    def get(self, uni, area, building, room, week, year):
        return api.getWeekScheduleForRoom(uni, area, building, room, week, year)

webapi.add_resource(BuildingsAPI, '/api/buildings/<string:uni>', endpoint = 'buildings')
webapi.add_resource(ScheduleAPI, '/api/schedule/<string:uni>/<string:area>/<string:building>/<string:room>/<int:week>/<int:year>', endpoint = 'schedule')



if __name__ == '__main__':
    app.run(debug=True)


