# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import quote
from time import localtime, strftime
import requests
import json
import re

def getAreas(university):
    allAreas = []
    baseURL = getBaseURL(university)
    r = requests.get(baseURL)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    allAreas = json.loads(soup.find("script", attrs={"id": "menu-js"}).text)[0]["areas"]
    return allAreas

def getBuildings(university):
    allBuildings = []
    areas = getAreas(university)
    for area in areas:
        buildingsInArea = getBuildingsInArea(university, area["areaId"])
        allBuildings += buildingsInArea
    return allBuildings

def getBuildingsInArea(university, areaId):
    buildings = []
    baseURL = getBaseURL(university)
    url = baseURL + "&area=" + quote(areaId)
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    buildingsInArea = json.loads(soup.find("script", attrs={"id": "menu-js"}).text)[0]["buildings"]
    return buildingsInArea

def getRoomsInBuilding(university, areaId, buildingId):
    roomsInBuilding = []
    baseURL = getBaseURL(university)
    url = baseURL + "&area=" + quote(areaId) + "&building=" + quote(buildingId)
    r = requests.get(url)
    html = r.content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    roomsInBuilding = json.loads(soup.find("script", attrs={"id": "menu-js"}).text)[0]["rooms"]
    return roomsInBuilding

def getWeekScheduleForRoom(university, areaId, buildingId, roomId, weeknumber, year):
    events = []
    timezone = strftime("%z", localtime())[:3]
    baseURL = getBaseURL(university)
    url = baseURL + "&area=" + areaId + "&building=" + buildingId + "&id=" + roomId + "&week=" + str(weeknumber) + "&ar=" + str(year)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    events = json.loads(soup.find("script", attrs={"id": "data-js"}).text)
    for event in events:
        del event["room"]
    return json.dumps(events)

def getBaseURL(university):
    if university == "uio":
        url = "https://tp.uio.no/timeplan/?type=room"
    else:
        url = "https://tp.uio.no/" + university + "/timeplan/?type=room"
    return url


