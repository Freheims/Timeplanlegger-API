import os
from api import *
from urllib.parse import unquote

universities = ["uib", "uio", "uit", "ntnu"]

for uni in universities:
    filePrefix = "content/" + uni + "/"
    if not os.path.exists(filePrefix):
            os.makedirs(filePrefix)
    if not os.path.exists(filePrefix + "buildings"):
            os.makedirs(filePrefix + "buildings")
    if not os.path.exists(filePrefix + "rooms"):
            os.makedirs(filePrefix + "rooms")

    areaJson = getAreas(uni)
    with open(filePrefix + "areas.json", "w+") as areaFile:
        areaFile.write(json.dumps(areaJson))

    for area in areaJson:
        areaID = unquote(area["id"])
        buildingsInAreaJson = getBuildingsInArea(uni, areaID)
        with open(filePrefix + "buildings/" + areaID + ".json", "w+") as buildingsFile:
            buildingsFile.write(json.dumps(buildingsInAreaJson))

        for building in buildingsInAreaJson:
            buildingID = unquote(building["id"])
            roomsInBuildingJson = getRoomsInBuilding(uni, areaID, buildingID)
            with open(filePrefix + "rooms/" + areaID + buildingID + ".json", "w+") as roomsFile:
                roomsFile.write(json.dumps(roomsInBuildingJson))

