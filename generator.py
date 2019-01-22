import os
from api import *
from urllib.parse import unquote

universities = ["uib", "uio", "uit", "ntnu", "oslomet"]

for uni in universities:
    filePrefix = "content/"
    if not os.path.exists(filePrefix):
            os.makedirs(filePrefix)

    areaJson = getAreas(uni)

    for areaIndex in range(len(areaJson)):
        area = areaJson[areaIndex]
        areaID = unquote(area["id"])
        buildingsInAreaJson = getBuildingsInArea(uni, areaID)
        #with open(filePrefix + "buildings/" + areaID + ".json", "w+") as buildingsFile:
        #    buildingsFile.write(json.dumps(buildingsInAreaJson))

        for buildingIndex in range(len(buildingsInAreaJson)):
            building = buildingsInAreaJson[buildingIndex]
            buildingID = unquote(building["id"])
            roomsInBuildingJson = getRoomsInBuilding(uni, areaID, buildingID)
            buildingsInAreaJson[buildingIndex]["rooms"] = roomsInBuildingJson
        #    with open(filePrefix + "rooms/" + areaID + buildingID + ".json", "w+") as roomsFile:
        #        roomsFile.write(json.dumps(roomsInBuildingJson))

        areaJson[areaIndex]["buildings"] = buildingsInAreaJson

        with open(filePrefix + uni +".json", "w+") as uniFile:
            uniFile.write(json.dumps(areaJson))
