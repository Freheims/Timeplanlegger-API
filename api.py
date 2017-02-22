# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests

def getAreas(university):
    allAreas = []
    baseURL = getBaseURL(university)
    r = requests.get(baseURL)
    html = r.text #content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    sel = soup.find("select")
    for option in sel.find_all("option"):
        if option.has_attr("value"):
            areaCode = option["value"]
            areaName = option.text
            area = {"areaCode" : areaCode, "areaName" : areaName}
            allAreas.append(area)
    return allAreas

def getBuildings(university):
    allBuildings = []
    areas = getAreas(university)
    for area in areas:
        buildingsInArea = getBuildingsInArea(university, area["areaCode"])
        allBuildings += buildingsInArea
    buildingDict = {"buildings" : allBuildings}
    return buildingDict

def getBuildingsInArea(university, areaCode):
    buildings = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + quote(areaCode, encoding="latin1")
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    buildingSelecter = soup.find("select", attrs={"name": "building"})
    for option in buildingSelecter.find_all("option"):
        if not option["value"] == "":
            buildingCode = option["value"]
            buildingName = option.text
            rooms = getRoomsInBuilding(university, areaCode, buildingCode)
            building = {"areaCode" : areaCode, "buildingCode" : buildingCode, "buildingName" : buildingName, "rooms" : rooms}
            buildings.append(building)
    print("Area: " + areaCode)
    return buildings

def getRoomsInBuilding(university,areaCode, buildingCode):
    roomsInBuilding = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + quote(areaCode, encoding="latin1") + "&building=" + quote(buildingCode, encoding="latin1")
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    roomSelecter = soup.find("select", attrs={"name": "id"})
    for option in roomSelecter.find_all("option"):
        if not option["value"] == "":
            roomCode = option["value"]
            roomName = option.text
            equipment, av, special, imageURL = getExtraRoomInformation(university, areaCode, buildingCode, roomCode)
            room = {"roomCode" : roomCode, "roomName" : roomName, "equipment" : equipment, "av" : av, "special": special, "imageURL" : imageURL}
            roomsInBuilding.append(room)
    return roomsInBuilding

#Returns equipment, av, special, image
def getExtraRoomInformation(university,areaCode, buildingCode, roomCode):
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + areaCode + "&building=" + buildingCode + "&id=" + roomCode
    r = requests.get(url)
    html = r.text #content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    try:
        equipment = soup.find("div", id="equip").find("span", class_=None).text
    except:
        equipment = "None"
    try:
        av = soup.find("div", id="avinfo").find("span", class_=None).tex.strip()
    except:
        av = "None"
    try:
        special = soup.find("div", id="specialities").find("span", class_=None).text.strip()
    except:
        special = "None"
    try:
        imageURL = soup.find("div", id="rombilde").find("img")["src"].strip()
    except:
        imageURL = "None"
    if equipment == "":
        equipment = "None"
    if av == "":
        av = "None"
    if special == "":
        special = "None"
    if imageURL == "":
       imageURL = "None"

    return equipment, av, special, imageURL


def getWeekScheduleForRoom(university, areaCode, buildingCode, roomCode, weeknumber, year):
    events = []
    baseURL = getBaseURL(university)
    url = baseURL + "?area=" + areaCode + "&building=" + buildingCode + "&id=" + roomCode + "&week=" + str(weeknumber) + "&ar=" + str(year)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    calendar = soup.find("div", class_="week-calendar")
    for day in calendar.find_all("ul", class_="week-calendar__list--7"):
        for eventSlot in day.find_all("li", class_="week-calendar__cell"):
            if len(eventSlot.contents)>0:
                weekday = getWeekday(eventSlot["id"])
                content = eventSlot.find("div", class_="week-calendar__event__content")
                title = content.find("a").text
                timeTag = content.find("time")
                if timeTag == None: #Some events has the time defined in a weird place...
                    time = eventSlot.find("div", class_="modal__content ").find_all("span")[1].string
                else:
                    time = timeTag.text.strip()
                event = {"weekday" : weekday, "title" : title, "time" : time}
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

