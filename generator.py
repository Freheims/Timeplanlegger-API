import os
from api import *

universities = ["uio", "uit", "ntnu"]

for uni in universities:
    filePrefix = "content/" + uni + "/"
    if not os.path.exists(filePrefix):
            os.makedirs(filePrefix)
    if not os.path.exists(filePrefix + "buildings"):
            os.makedirs(filePrefix + "buildings")
    if not os.path.exists(filePrefix + "rooms"):
            os.makedirs(filePrefix + "rooms")
    if not os.path.exists(filePrefix + "roomdata"):
            os.makedirs(filePrefix + "roomdata")

    areaJson = getAreas(uni)
    areaFile = open(filePrefix + "areas.json", "w+")
    areaFile.write(json.dumps(areaJson))
    areaFile.close()

    for area in areaJson["data"]:
        buildingsInAreaJson = getBuildingsInArea(uni, area["id"])
        buildingsFile = open(filePrefix + "buildings/" + area["id"] + ".json", "w+")
        buildingsFile.write(json.dumps(buildingsInAreaJson))
        buildingsFile.close()

        for building in buildingsInAreaJson["data"]:
            roomsInBuildingJson = getRoomsInBuilding(uni, area["id"], building["id"])
            roomsFile = open(filePrefix + "rooms/" + area["id"] + building["id"] + ".json", "w+")
            roomsFile.write(json.dumps(roomsInBuildingJson))
            roomsFile.close()

            for room in roomsInBuildingJson["data"]:
                roomDataJson = getRoomData(uni, area["id"], building["id"], room["id"])
                roomDataFile = open(filePrefix + "roomdata/" + area["id"] + building["id"] + room["id"] + ".json", "w+")
                roomDataFile.write(json.dumps(roomDataJson))
                roomDataFile.close()

