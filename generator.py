import os
from api import *
from urllib.parse import unquote

universities = ["uib"]#, "uio", "uit", "ntnu", "oslomet"]

for uni in universities:
    filePrefix = "content/"
    if not os.path.exists(filePrefix):
            os.makedirs(filePrefix)

    areaJson = getAreas(uni)

    for areaIndex in range(len(areaJson)):
        area = areaJson[areaIndex]
        areaID = unquote(area["id"])
        buildingsInAreaJson = getBuildingsInArea(uni, areaID)

        for buildingIndex in range(len(buildingsInAreaJson)):
            building = buildingsInAreaJson[buildingIndex]
            buildingID = unquote(building["id"])
            roomsInBuildingJson = getRoomsInBuilding(uni, areaID, buildingID)
            for roomIndex in range(len(roomsInBuildingJson)):
                roomsInBuildingJson[roomIndex]["university"] = uni
                roomsInBuildingJson[roomIndex]["area"] = areaID
                roomsInBuildingJson[roomIndex]["building"] = buildingID

            buildingsInAreaJson[buildingIndex]["rooms"] = roomsInBuildingJson
            buildingsInAreaJson[buildingIndex]["university"] = uni
            buildingsInAreaJson[buildingIndex]["area"] = areaID

        areaJson[areaIndex]["buildings"] = buildingsInAreaJson
        areaJson[areaIndex]["university"] = uni

        with open(filePrefix + uni +".json", "w+") as uniFile:
            uniFile.write(json.dumps(areaJson))
