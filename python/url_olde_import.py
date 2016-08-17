from urlparse import urldefrag
import re, time, fileinput
for line in fileinput.input():
    if "://" in line:
        full_uri = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
        time_string = re.findall('20[01][0-9]-[0-9][0-9]-[0-9][0-9]\ [0-9][0-9]:[0-9][0-9]:[0-9][0-9]', line)
        date_object = time.strptime(''.join(time_string), '%Y-%m-%d %H:%M:%S')
        #print str(time.mktime(date_object)) + ' ' + ''.join(full_uri)
        #print line
        urls = []
        urls.insert(date_object, full_uri)
        urls.sort(date_object)
