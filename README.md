# Join multiple calendars into one
This is a small program to merge appointments of several calendars into one.
The source calendars could be either ical or caldav calenders.
The target calender is a caldav calender.

![images](join_calendars.png)

## Setup
* copy the config.dummy.json into a config.json file
* insert the source and target calender data
* install: ``sudo pip install caldav``
* start the script: python join_calendars.py

## example of use
Running the script on a Raspberry Pi every night at 5:00am.
1. ``cd ~``
2. clone the github repo ``git clone https://github.com/baireutherjonas/join_calendars.git``
3. go in the repo folder ``cd join_calendars``
4. copy the config file template ``cp config.dummy.json config.json``
5. insert your urls and data in the ``config.json`` file
6. open the crontab editor ``crontab -e``
7. and insert the following row``0 5 * * * python ~/join_calendars/join_calendars.py &``

## License
[Apache 2.0](./LICENSE)