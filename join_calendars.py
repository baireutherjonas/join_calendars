import caldav
from caldav.elements import dav, cdav
import urllib
import os
import json
import datetime
import dateutil.relativedelta

eventlist=[]

def main():
    # Read Config
    with open(os.path.dirname(os.path.realpath(__file__))+"/config.json", "r") as read_file:
        data = json.load(read_file)

        #get events from ical
        for key, value in data["icalsource"].items():
            for calendar in value:
                cal_url = calendar["url"]
                print("source calendar: " + cal_url)
                create_events_from_ical(cal_url)
                print("number of events: " + str(len(eventlist)))
            
        #get events from dav
        for key, value in data["davsource"].items():
            for calendar in value:
                cal_url = calendar["url"]
                if "https://" in cal_url:
                    cal_url = cal_url[-7:]
                url = "https://" + calendar["username"] + ":" + calendar["password"] + "@" + cal_url
                print("source calendar: " + url)
                get_events_from_caldav(url,calendar["calendar_name"])
                print("number of events: " + str(len(eventlist)))

        #write events to dav
        cal_url = data["davtarget"]["url"]
        if "https://" in cal_url:
            cal_url = cal_url[-7:]
        url = "https://" + data["davtarget"]["username"] + ":" + data["davtarget"]["password"] + "@" + cal_url
        print("target calendar: " + url)
        add_events_to_caldav(url, data["davtarget"]["calendar_name"])
        
def get_events_from_caldav( url, calendar_name ):
    client = caldav.DAVClient(url)
    principal = client.principal()
    calendars = principal.calendars()
    for calendar in calendars:
        if "{'{DAV:}displayname': '"+calendar_name+"'}" == str(calendar.get_properties([dav.DisplayName(),])): 
            print ("Using calendar: " + str(calendar))
            loaded_events = 0
            startdate = datetime.datetime.now() - dateutil.relativedelta.relativedelta(years = 1)
            enddate = startdate + dateutil.relativedelta.relativedelta(months=1)
            while startdate < datetime.datetime.now() + dateutil.relativedelta.relativedelta(years = 3):
                print("time: " + str(startdate) + " - " + str(enddate))
                for event in calendar.date_search(startdate,enddate):
                    eventlist.append(event.data)
                    loaded_events = loaded_events + 1
                startdate = enddate
                enddate = startdate + dateutil.relativedelta.relativedelta(months=1)
    return

def add_events_to_caldav( url, calendar_name ):
    client = caldav.DAVClient(url)
    principal = client.principal()
    calendars = principal.calendars()
    for calendar in calendars:
        if "{'{DAV:}displayname': '"+calendar_name+"'}" == str(calendar.get_properties([dav.DisplayName(),])): 
            print ("Using calendar: " + str(calendar))
            total_events = len(eventlist)
            saved_events = 0
            for event in eventlist:
                try:
                    calendar.add_event(event)
                    print("saved event " + str(saved_events) + " of " + str(total_events) + " events")
                    saved_events = saved_events + 1
                except:
                    print("An exception occurred")
                    print(event)
                    f = open("join_calendars.log", "a")
                    f.write("##############################################")
                    f.write(event)
                    f.close()
    return


def create_events_from_ical(url):
    temp_file = "temp_cal.ics"
    urllib.urlretrieve (url, temp_file)
    with open(temp_file) as f:
        lines = f.readlines()
        event_basis = ""
        datatype = 0
        eventdata = event_basis
        for line in lines:
            if(datatype == 1):
                eventdata = eventdata + line
            if(datatype == 0 and "METHO" not in line):
                event_basis = event_basis + line
            if("BEGIN:VEVENT" in line):
                datatype = 1
                eventdata = event_basis
            if("END:VEVENT" in line):
                eventdata = eventdata + "END:VCALENDAR"
                eventlist.append(eventdata)
                datatype = 2
    os.remove(temp_file)



if __name__=='__main__':
    main()
