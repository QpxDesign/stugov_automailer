import requests
from datetime import date
import time
from requests_html import HTMLSession
from ics import Calendar, Event
import re
from redmail import EmailSender

session = HTMLSession()

# start timer
PROGRAM_START_TIME = time.time()

# Find Lunch Menu for current day


def DateToDaysSince():
    d0 = date(2022, 9, 30)  # First Valid Menu Day
    d1 = date(date.today().year, date.today().month, date.today().day)
    delta = d1 - d0
    return delta.days


c = 76061456 + DateToDaysSince()

todaysLunch = ""
try:
    r = session.get(
        f'https://www.school_name.edu/fs/elements/8133?occur_id={c}&show_event=true&is_draft=false&_=1664648774780')
    menu = r.html.find(".fsDescription", first=True)
    menuDate = r.html.find(".fsDate", first=True)
    todaysLunch = (menu.text).replace("\n", "<br>")
except:
    todaysLunch = "No Valid Menu Found For Today"

# Find All Upper School Sports Games for current day
TeamCalendarData = [
    "https://www.school_name.edu/calendar/team_198.ics",
    "https://www.school_name.edu/calendar/team_197.ics",
    "https://www.school_name.edu/calendar/team_210.ics",
    "https://www.school_name.edu/calendar/team_207.ics",
    "https://www.school_name.edu/calendar/team_208.ics",
    "https://www.school_name.edu/calendar/team_211.ics",
    "https://www.school_name.edu/calendar/team_209.ics",
    "https://www.school_name.edu/calendar/team_338.ics",
    "https://www.school_name.edu/calendar/team_215.ics",
    "https://www.school_name.edu/calendar/team_216.ics",
    "https://www.school_name.edu/calendar/team_219.ics",
    "https://www.school_name.edu/calendar/team_218.ics",
    "https://www.school_name.edu/calendar/team_229.ics",
    "https://www.school_name.edu/calendar/team_225.ics",
    "https://www.school_name.edu/calendar/team_232.ics",
    "https://www.school_name.edu/calendar/team_243.ics",
    "https://www.school_name.edu/calendar/team_241.ics",
    "https://www.school_name.edu/calendar/team_244.ics",
    "https://www.school_name.edu/calendar/team_242.ics",
    "https://www.school_name.edu/calendar/team_251.ics",
    "https://www.school_name.edu/calendar/team_249.ics",
    "https://www.school_name.edu/calendar/team_252.ics",
    "https://www.school_name.edu/calendar/team_250.ics",
    "https://www.school_name.edu/calendar/team_257.ics",
    "https://www.school_name.edu/calendar/team_250.ics",
    "https://www.school_name.edu/calendar/team_262.ics",
    "https://www.school_name.edu/calendar/team_263.ics",
    "https://www.school_name.edu/calendar/team_270.ics",
    "https://www.school_name.edu/calendar/team_256.ics",
    "https://www.school_name.edu/calendar/team_268.ics",
    "https://www.school_name.edu/calendar/team_271.ics",
    "https://www.school_name.edu/calendar/team_269.ics",
    "https://www.school_name.edu/calendar/team_275.ics",
    "https://www.school_name.edu/calendar/team_276.ics",
    "https://www.school_name.edu/calendar/team_278.ics",
    "https://www.school_name.edu/calendar/team_281.ics",
    "https://www.school_name.edu/calendar/team_280.ics",
    "https://www.school_name.edu/calendar/team_289.ics"
]

todaysEvents = ""
for team in TeamCalendarData:
    TeamCal = Calendar(requests.get(team).text)
    TeamCalEvents = str(TeamCal.events).split(",")
    for event in TeamCalEvents:
        d = str(date.today())
        if re.search(d, event):
            todaysEvents += re.findall("(?<=\')(.*?)(?=\')", event)[0] + "<br>"

# send formated emails
email = EmailSender(
    host='smtp-mail.outlook.com.',
    port=587,
    username='email@example.com',
    password='password'
)
email.send(
    subject=f'Better Daily Email - {date.today()}',
    sender="quinnposter@outlook.com",
    receivers=['qroshan5@gmail.com'],
    text="!",
    html=f"<h1 style='font-size: 18pt; font-family: Arial, Helvetica, sans-serif'> Hello School, </h1> <h2 style=' font-size: 18pt; font-family: Arial, Helvetica, sans-serif; color: red; margin-bottom: 5px; font-weight: 500; ' > Todays Lunch Is: </h2> <p style=' font-size: 18pt; font-family: Arial, Helvetica, sans-serif; margin-top: 0; '> {todaysLunch} </p><h2 style=' color: blue; font-size: 18pt; font-family: Arial, Helvetica, sans-serif; margin-bottom: 5px; font-weight: 500; ' > Athletic Events: </h2> <p style=' font-size: 18pt; font-family: Arial, Helvetica, sans-serif; margin-top: 0; ' > {todaysEvents} </p> <h1 style='font-size: 18pt; font-family: Arial, Helvetica, sans-serif'> From StuGov </h1>"
)

PROGRAM_END_TIME = time.time()
print(
    f'Process Completed - Runtime: {round(PROGRAM_END_TIME-PROGRAM_START_TIME,2)} seconds')
