import requests
from ics import Calendar, Event
from requests_html import HTMLSession
from datetime import datetime, timedelta
import re
from redmail import EmailSender
#from requests_html import HTMLSession
import os
from dotenv import load_dotenv

load_dotenv()
session = HTMLSession()
current_datetime = datetime.now()


def generateDate():
    day = current_datetime.strftime("%a")
    month = current_datetime.strftime("%b")
    date = re.sub("^0", "", current_datetime.strftime("%d"))
    full_date = day + " " + month + " " + date
    return full_date


def generateNextDate():
    presentday = datetime.today()
    if presentday.strftime("%a") == "Fri":
        tomorrow_datetime = presentday + timedelta(3)
    else:
        tomorrow_datetime = presentday + timedelta(1)
    day = tomorrow_datetime.strftime("%a")
    month = tomorrow_datetime.strftime("%b")
    date = re.sub("^0", "", tomorrow_datetime.strftime("%d"))
    full_date = day + " " + month + " " + date
    return full_date


def getData(data,mode):
    if data is None:
         return ""
    if mode == "normal":
        today = generateDate()
        tommorrow = generateNextDate()
        regex_text = f"(?<={today})(.*)(?={tommorrow})"
        data = data.replace('\n', 'SPECIALCODEK')
        if data is None or regex_text is None or re.search(regex_text, data) is None:
            return ""
        todaysMenu = re.search(regex_text, data)[0]
        todaysMenu = todaysMenu.replace("SPECIALCODEK", "\n")
        todaysMenu = todaysMenu.split("Middle & Upper School")[1]
        todaysMenu = todaysMenu.split(tommorrow)[0]
        # format data for html
        todaysMenu = todaysMenu.split("\n")
        res = "<ul>"
        for i in todaysMenu:
            if i != "":
                res += "<li style='font-size: 1.5em; font-family: source-serif-pro;margin-top:0;color:black'>" + i + "</li>"
        res + "</ul>"
        return res
    if mode == "special":
        today = generateDate()
        tommorrow = "3825 Wisconsin Ave. NW"
        regex_text = f"(?<={today})(.*)(?={tommorrow})"
        data = data.replace('\n', 'SPECIALCODEK')
        todaysMenu = re.search(regex_text, data)[0]
        print(todaysMenu)
        todaysMenu = todaysMenu.replace("SPECIALCODEK", "\n")
        todaysMenu = todaysMenu.split("Middle & Upper School")[1]
        todaysMenu = todaysMenu.split(tommorrow)[0]
        # format data for html
        todaysMenu = todaysMenu.split("\n")
        res = "<ul>"
        for i in todaysMenu:
            if i != "" and i != "Middle and Upper School":
                res += "<li style='font-size: 1.5em; font-family: source-serif-pro;margin-top:0;color:black'>" + i + "</li>"
        res + "</ul>"
        return res
    return ""

MENU_URL = "https://www.sidwell.edu/student-life/dining-services/lunch-menu-calendar"
r = session.get(MENU_URL)
print(getData(r.html.find("body", first=True).text,"special"))

data = ""
if r.html.find("body", first=True) is not None:
    if getData(r.html.find("body", first=True).text,"normal") is not None :
        data = getData(r.html.find("body", first=True).text,"normal")
if len(getData(r.html.find("body", first=True).text,"normal")) < 50:
    data = getData(r.html.find("body", first=True).text,"special")
# send formated emails
# Find All Upper School Sports Games for current day
TeamCalendarData = [
    "https://www.sidwell.edu/calendar/team_198.ics",
    "https://www.sidwell.edu/calendar/team_197.ics",
    "https://www.sidwell.edu/calendar/team_210.ics",
    "https://www.sidwell.edu/calendar/team_207.ics",
    "https://www.sidwell.edu/calendar/team_208.ics",
    "https://www.sidwell.edu/calendar/team_211.ics",
    "https://www.sidwell.edu/calendar/team_209.ics",
    "https://www.sidwell.edu/calendar/team_338.ics",
    "https://www.sidwell.edu/calendar/team_215.ics",
    "https://www.sidwell.edu/calendar/team_216.ics",
    "https://www.sidwell.edu/calendar/team_219.ics",
    "https://www.sidwell.edu/calendar/team_218.ics",
    "https://www.sidwell.edu/calendar/team_229.ics",
    "https://www.sidwell.edu/calendar/team_225.ics",
    "https://www.sidwell.edu/calendar/team_232.ics",
    "https://www.sidwell.edu/calendar/team_243.ics",
    "https://www.sidwell.edu/calendar/team_241.ics",
    "https://www.sidwell.edu/calendar/team_244.ics",
    "https://www.sidwell.edu/calendar/team_242.ics",
    "https://www.sidwell.edu/calendar/team_251.ics",
    "https://www.sidwell.edu/calendar/team_249.ics",
    "https://www.sidwell.edu/calendar/team_252.ics",
    "https://www.sidwell.edu/calendar/team_250.ics",
    "https://www.sidwell.edu/calendar/team_257.ics",
    "https://www.sidwell.edu/calendar/team_250.ics",
    "https://www.sidwell.edu/calendar/team_262.ics",
    "https://www.sidwell.edu/calendar/team_263.ics",
    "https://www.sidwell.edu/calendar/team_270.ics",
    "https://www.sidwell.edu/calendar/team_256.ics",
    "https://www.sidwell.edu/calendar/team_268.ics",
    "https://www.sidwell.edu/calendar/team_271.ics",
    "https://www.sidwell.edu/calendar/team_269.ics",
    "https://www.sidwell.edu/calendar/team_275.ics",
    "https://www.sidwell.edu/calendar/team_276.ics",
    "https://www.sidwell.edu/calendar/team_278.ics",
    "https://www.sidwell.edu/calendar/team_281.ics",
    "https://www.sidwell.edu/calendar/team_280.ics",
    "https://www.sidwell.edu/calendar/team_289.ics"
]
 
todaysEvents = ""
for team in TeamCalendarData:
	TeamCal = Calendar(requests.get(team).text)
	TeamCalEvents = str(TeamCal.events).split(",")
	for event in TeamCalEvents:
		d = str(datetime.today())
		if re.search(d, event):
            		todaysEvents += re.findall("(?<=\')(.*?)(?=\')", event)[0] + "<br>"
print(todaysEvents)

if datetime.today().strftime('%A') != 'Saturday' and datetime.today().strftime(
        '%A') != 'Sunday' and len(data) > 50:
    email = EmailSender(host='smtp-mail.outlook.com.',
                        port=587,
                        username=os.getenv("EMAIL_ADDRESS"),
                        password=os.getenv("EMAIL_PASSWORD"))

    email.send(
        subject=f"Today's Lunch - {generateDate()}",
        sender=os.getenv("EMAIL_ADDRESS"),
        bcc=os.getenv("RECIPIENTS").split(" "),
#        bcc=['qroshan5@gmail.com','gbankoff24@sidwell.edu','patwardhana@sidwell.edu','stacypatwardhan@gmail.com'],
        text="!",
        html=
        f"<style>@import url('https://use.typekit.net/tnn4sor.css');</style><h1 style='font-size: 18pt; font-family: source-serif-pro; color:black;margin-bottom:0'> Today's Lunch:</h1>{data}<h1 style='font-size: 18pt; font-family: source-serif-pro;color:black;'> From Quinn Patwardhan <br><a href='https://quinnpatwardhan.com' style='color:black;'>quinnpatwardhan.com </h1>"
    )
