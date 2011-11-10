#! usr/bin/python
# -*- coding: utf-8 -*-
import gdata.calendar.service
import gdata.service
import gdata.calendar
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom.data
import time
import sys
import re
import dateutil.parser
from datetime import datetime
usr=""
passwd=""
source=""
my_calendar=""
visibility = 'private'
projection = 'full'
end_date=''
today=datetime.today()

def PrintOwnCalendars(calendar_client):
    feed = calendar_client.GetOwnCalendarsFeed()
    for i, temp_calendar in enumerate(feed.entry):
        if temp_calendar.title.text==my_calendar:
            return temp_calendar.id.text

def DateRangeQuery(calendar_client,calendar_id):
  temp_uri='https://www.google.com/calendar/feeds/'+calendar_id+'/private/full?orderby=starttime&sortorder=a&start-min=%s-%s-%sT00:00:00&start-max=%s' %(today.year,today.month,today.day,end_date)
  feed = calendar_client.GetCalendarEventFeed(uri=temp_uri)
  return feed

def linkURLs(str):
  return re.compile(r'([^"]|^)(https?|ftp)(://[\w:;/.?%#&=+-]+)').sub(r'\1<a href="\2\3?phpMyAdmin=cfc2644bd9c947213a0141747c2608b0">\2\3</a>', str)

def HTMLGenerater(temp):
    fw=open('index.html','w')
    fw.write('''<html>
<title></title>
<table border="1" cellpadding="5">
<caption></caption>
  <tr>
    <th>日程</th>
    <th>イベント</th>
    <th>場所</th>
    <th>説明</th>
  </tr>
''')

    for i,temp_event in enumerate(temp.entry):
        fw.write('<tr><th width="10%">')
        for temp_when in temp_event.when:
            fw.write(dateutil.parser.parse(temp_when.start_time).strftime("%m/%d")+'('+dateutil.parser.parse(temp_when.start_time).strftime("%a")+')'+'<br>'+dateutil.parser.parse(temp_when.start_time).strftime("%H:%M")+'-'+dateutil.parser.parse(temp_when.end_time).strftime("%H:%M"))

        fw.write('</th>')
        fw.write('<th width="30%">')
        fw.write(temp_event.title.text)
        fw.write('</th>')
        fw.write('<th width="10%">')
        fw.write(str(temp_event.where[0].value_string))
        fw.write('</th>')
        fw.write('<th width =50%>')
        fw.write(linkURLs(str(temp_event.content.text)))
        fw.write('</th>')
    fw.write('''</tr>
</table>
</html>''')
    fw.close()


def main():
    client = gdata.calendar.service.CalendarService();
    client.ClientLogin(usr,passwd,source=source)
    calendar_client = gdata.calendar.client.CalendarClient()
    
    calendar_id=PrintOwnCalendars(client)
    calendar_id=calendar_id[calendar_id.rindex("/")+1:]
    temp_feed=DateRangeQuery(client,calendar_id)
    HTMLGenerater(temp_feed)

if __name__=='__main__':
    main()
