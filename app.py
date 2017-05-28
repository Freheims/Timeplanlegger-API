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

class AreasAPI(Resource):
    def get(self, uni):
        return getAreas(uni)

class BuildingsAPI(Resource):
    def get(self, uni, area):
        return getBuildingsInArea(uni, area)

class RoomsAPI(Resource):
    def get(self, uni, area, building):
        return getRoomsInBuilding(uni, area, building)

class RoomDataAPI(Resource):
    def get(self, uni, area, building, room):
        return getRoomData(uni, area, building, room)

class ScheduleAPI(Resource):
    def get(self, uni, area, building, room, week, year):
        return api.getWeekScheduleForRoom(uni, area, building, room, week, year)

webapi.add_resource(AreasAPI, '/api/areas/<string:uni>', endpoint = 'areas')
webapi.add_resource(BuildingsAPI, '/api/buildings/<string:uni>/<string:area>', endpoint = 'buildings')
webapi.add_resource(RoomsAPI, '/api/rooms/<string:uni>/<string:area>/<string:building>', endpoint = 'rooms')
webapi.add_resource(RoomDataAPI, '/api/rooms/<string:uni>/<string:area>/<string:building>/<string:room>', endpoint = 'roomdata')
webapi.add_resource(ScheduleAPI, '/api/schedule/<string:uni>/<string:area>/<string:building>/<string:room>/<int:week>/<int:year>', endpoint = 'schedule')



if __name__ == '__main__':
    app.run(debug=True)


