#!flask/bin/python3
from flask import Flask, jsonify, render_template
from flask.ext.restful import Api, Resource
from api import *
import json

app = Flask(__name__)
webapi = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

class AreasAPI(Resource):
    def get(self, uni):
        filename = "content/" + uni + "/areas.json"
        with open(filename.encode("utf-8"), "r") as file:
            return json.load(file)

class BuildingsAPI(Resource):
    def get(self, uni, area):
        filename = "content/" + uni + "/buildings/" + area + ".json"
        with open(filename.encode("utf-8"), "r") as file:
            return json.load(file)

class RoomsAPI(Resource):
    def get(self, uni, area, building):
        filename = "content/" + uni + "/rooms/" + area + building + ".json"
        with open(filename.encode("utf-8"), "r") as file:
            return json.load(file)

class RoomDataAPI(Resource):
    def get(self, uni, area, building, room):
        filename = "content/" + uni + "/roomdata/" + area + building + room + ".json"
        with open(filename.encode("utf-8"), "r") as file:
            return json.load(file)

class ScheduleAPI(Resource):
    def get(self, uni, area, building, room, week, year):
        return getWeekScheduleForRoom(uni, area, building, room, week, year)

webapi.add_resource(AreasAPI, '/api/areas/<string:uni>', endpoint = 'areas')
webapi.add_resource(BuildingsAPI, '/api/buildings/<string:uni>/<string:area>', endpoint = 'buildings')
webapi.add_resource(RoomsAPI, '/api/rooms/<string:uni>/<string:area>/<string:building>', endpoint = 'rooms')
webapi.add_resource(RoomDataAPI, '/api/rooms/<string:uni>/<string:area>/<string:building>/<string:room>', endpoint = 'roomdata')
webapi.add_resource(ScheduleAPI, '/api/schedule/<string:uni>/<string:area>/<string:building>/<string:room>/<int:week>/<int:year>', endpoint = 'schedule')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


