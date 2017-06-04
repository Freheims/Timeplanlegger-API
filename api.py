# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import json
import re

def getAreas(university):
    allAreas = []
    baseURL = getBaseURL(university)
    r = requests.get(baseURL)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    sel = soup.find("select")
    for option in sel.find_all("option"):
        if option.has_attr("value"):
            areaId = option["value"]
            areaName = option.text
            area = {"id" : areaId, "name" : areaName}
            allAreas.append(area)
    allAreasJson = {"name" : "Areas", "data" : allAreas}
    return allAreasJson

def getBuildings(university):
    allBuildings = []
    areas = getAreas(university)
    for area in areas:
        buildingsInArea = getBuildingsInArea(university, area["areaId"])
        allBuildings += buildingsInArea
    buildingDict = {"buildings" : allBuildings}
    return buildingDict

def getBuildingsInArea(university, areaId):
    buildings = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + quote(areaId)
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    buildingSelecter = soup.find("select", attrs={"name": "building"})
    for option in buildingSelecter.find_all("option"):
        if not option["value"] == "":
            buildingId = option["value"]
            buildingName = option.text
            building = {"id" : buildingId, "name" : buildingName}
            buildings.append(building)
    buildingsInAreaJson = {"name" : "Buildings", "data" : buildings}
    return buildingsInAreaJson

def getRoomsInBuilding(university, areaId, buildingId):
    roomsInBuilding = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + quote(areaId) + "&building=" + quote(buildingId)
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    roomSelecter = soup.find("select", attrs={"name": "id"})
    for optGroup in roomSelecter.find_all("optgroup"):
        typeId = optGroup["label"].strip()
        for option in optGroup.find_all("option"):
            if not option["value"] == "":
                roomId = option["value"]
                nameSize = re.split("(\(\d+\spl.\))", option.text)
                roomName = nameSize[0].strip()
                if len(nameSize)>1:
                    size = re.split("(\d+)", nameSize[1])[1]
                else:
                    size = -1
                room = {"id" : roomId, "name" : roomName, "typeid" : typeId, "size" : size}
                roomsInBuilding.append(room)
    roomsInBuildingJson = {"name" : "Rooms", "data" : roomsInBuilding}
    return roomsInBuildingJson

def getRoomData(university,areaId, buildingId, roomId):
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + quote(areaId) + "&building=" + quote(buildingId) + "&id=" + quote(roomId)
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")


    someURL = soup.find("div", id="rominfo").find("a")
    buildingName = soup.find("section", id="building").find("option", selected="selected").text.strip()

    if someURL:
        if buildingName == someURL.text.strip():
            buildingURL = someURL["href"]
            roomURL = "null"
        else:
            buildingURL = "null"
            roomURL = someURL["href"]
    else:
        buildingURL = "none"
        roomURL = "none"

    buildingAcronym = buildingName[:4].strip() #Not ideal, but works for now

    try:
        imageURL = soup.find("div", id="rombilde").find("img")["src"].strip()
    except:
        imageURL = "null"

    if imageURL == "":
        imageURL = "null"

    roomAcronym = soup.find("section", id="room").find("option", selected="selected").text.strip()[:4].strip()

    data = {"buildingurl" : buildingURL, "buildingacronym" : buildingAcronym, "roomimg_url" : imageURL, "roomacronym" : roomAcronym, "roomurl" : roomURL}

    equipmentList = []
    try:
        equipment = re.split(",", soup.find("div", id="equip").find("span", class_=None).text)
    except:
        equipment = ""
    try:
        av = soup.find("div", id="avinfo").find("span", class_=None).tex.strip()
    except:
        av = ""
    try:
        special = soup.find("div", id="specialities").find("span", class_=None).text.strip()
    except:
        special = ""

    for eq in equipment:
        equipmentList.append(eq.strip())
    if not av == "":
        equipmentList.append(av)
    if not special == "":
        equipmentList.append(special)

    roomDataJson = {"name" : "Roomdata", "data" : data, "equipment" : equipmentList}

    return roomDataJson


def getWeekScheduleForRoom(university, areaId, buildingId, roomId, weeknumber, year):
    events = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + areaId + "&building=" + buildingId + "&id=" + roomId + "&week=" + str(weeknumber) + "&ar=" + str(year)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    calendar = soup.find("div", class_="week-calendar")
    for day in calendar.find_all("ul", class_="week-calendar__list--7"):
        date = day.find("span", class_="is-visible--lg").text.strip().split(" ",1)[1].split("/", 1)
        dateString = date[1] + "-" + date[0]
        for eventSlot in day.find_all("li", class_="week-calendar__cell"):
            if len(eventSlot.contents)>0:
                weekday = getWeekday(eventSlot["id"])
                content = eventSlot.find("div", class_="week-calendar__event__content")
                contentList = content.find("a").text.split(":",1)
                teachingMethodName = contentList[0]
                summary = contentList[1]
                timeTag = content.find("time")
                if timeTag == None: #Some events has the time defined in a weird place...
                    time = eventSlot.find("div", class_="modal__content ").find_all("span")[1].string
                else:
                    time = timeTag.text.strip()
                
                time = time.split("-",1)
                timeStart = str(year) + "-" + dateString + "T" + time[0] + ":00+01"
                timeEnd = str(year) + "-" + dateString + "T" + time[1] + ":00+01"
                event = {"weekday" : weekday, "teaching-method-name": teachingMethodName, "summary": summary, "dtstart" : timeStart, "dtend" :timeEnd}
                events.append(event)
    return events

def getWeekday(weekdayID):
    wid = int(weekdayID[-1])-1
    return ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][wid]

def getBaseURL(university):
    if university == "uio":
        url = "https://tp.uio.no/timeplan/rom.php"
    else:
        url = "https://tp.uio.no/" + university + "/timeplan/rom.php"
    return url


