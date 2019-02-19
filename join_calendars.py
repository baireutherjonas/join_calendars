import caldav
from icalendar import Calendar, Event
import urllib
from caldav.elements import dav, cdav
import os
import datetime
import json


eventlist=[]

def main():
    # Read Config
    with open("config.json", "r") as read_file:
        data = json.load(read_file)

        #get events from ical
        print datetime.datetime.now()
        for key, value in data["icalsource"].items():
            print(value)
            create_events_from_ical(value)
            print("number of events: " + str(len(eventlist)))
            
        #get events from dav
        print datetime.datetime.now()
        for key, value in data["davsource"].items():
            for calendar in value:
                url = "https://" + calendar["username"] + ":" + calendar["password"] + "@" + calendar["url"]
                print(url)
                get_events_from_caldav(url,calendar["calendar_name"])
                print("number of events: " + str(len(eventlist)))

        #write events to dav
        print datetime.datetime.now()
        url = "https://" + data["davdestination"]["username"] + ":" + data["davdestination"]["password"] + "@" + data["davdestination"]["url"]
        print(url)
        add_events_to_caldav(url, data["davdestination"]["calendar_name"])


        print datetime.datetime.now()
        
def get_events_from_ical(url):
    ics = urllib.urlopen(url).read()
    return ics

def get_events_from_caldav( url, calendar_name ):
    client = caldav.DAVClient(url)
    principal = client.principal()
    calendars = principal.calendars()
    for calendar in calendars:
        if calendar_name in str(calendar.get_properties([dav.DisplayName(),])): 
            print ("Using calendar: " + str(calendar))
            for event in calendar.events():
                eventlist.append(event.data)
    return

def add_events_to_caldav( url, calendar_name ):
    client = caldav.DAVClient(url)
    principal = client.principal()
    calendars = principal.calendars()
    for calendar in calendars:
        if calendar_name in str(calendar.get_properties([dav.DisplayName(),])): 
            print ("Using calendar: " + str(calendar))
            for event in eventlist:
                calendar.add_event(event)
    return


def create_events_from_ical(url):
    temp_file = "temp_cal.ics"
    urllib.urlretrieve (url, temp_file)
    with open(temp_file) as f:
        lines = f.readlines()
        event_basis = """BEGIN:VCALENDAR
VERSION:2.0
X-WR-TIMEZONE:Europe/Vienna
X-PUBLISHED-TTL:PT4H0M
PRODID:-//Universitaet Stuttgart//DE
BEGIN:VEVENT
"""
        datatype = 0
        eventdata = event_basis
        for line in lines:
            if(datatype == 1):
                eventdata = eventdata + line
            if("BEGIN:VEVENT" in line):
                datatype = 1
            if("END:VEVENT" in line):
                eventdata = eventdata + "END:VCALENDAR"
                eventlist.append(eventdata)
                eventdata = event_basis
                datatype = 0
    os.remove(temp_file)



if __name__=='__main__':
    main()