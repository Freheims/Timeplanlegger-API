import os
from api import *
from urllib.parse import unquote

universities = ["uit"]

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
        areaID = unquote(area["id"])
        buildingsInAreaJson = getBuildingsInArea(uni, areaID)
        buildingsFile = open(filePrefix + "buildings/" + areaID + ".json", "w+")
        buildingsFile.write(json.dumps(buildingsInAreaJson))
        buildingsFile.close()

        for building in buildingsInAreaJson["data"]:
            print(building["id"])
            buildingID = unquote(building["id"])
            print(buildingID)
            roomsInBuildingJson = getRoomsInBuilding(uni, areaID, buildingID)
            roomsFile = open(filePrefix + "rooms/" + areaID + buildingID + ".json", "w+")
            roomsFile.write(json.dumps(roomsInBuildingJson))
            roomsFile.close()

            for room in roomsInBuildingJson["data"]:
                roomID = unquote(room["id"])
                roomDataJson = getRoomData(uni, areaID, buildingID, roomID)
                roomDataFile = open(filePrefix + "roomdata/" + areaID + buildingID + roomID + ".json", "w+")
                roomDataFile.write(json.dumps(roomDataJson))
                roomDataFile.close()

