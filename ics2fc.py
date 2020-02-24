#!/usr/bin/env python
"""Converts the .ics/.ical file into a FullCalendar compatiable JSON file

FullCalendar uses a specific JSON format similar to iCalendar format. This
script creates a JSON file containing renamed event components. Only the
title, description, start/end time, and url data are used. Does not support
repeating events.
"""

import sys
import json

__import__('pytz')
__import__('icalendar')
from icalendar import Calendar


__author__ = "Andy Yin"
__copyright__ = "Copyright (C) 2015, Andy Yin"
__credits__ = ["Eddie Blundell"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Andy Yin"
__email__ = "me@fortheyin.com"
__status__ = "Production"


# quit if the arguments are incorrect, and prints a usage
if (len(sys.argv) != 2 and len(sys.argv) != 3):
	print(sys.argv[0] + ': illegal operation')
	print('usage: python ' + sys.argv[0] + ' file [output]')
	exit(1)

# default output filename (just adds .json extension on the given file)
out_file = sys.argv[1] + '.json'

if (len(sys.argv) == 3):
	# changes output filename to the 2nd arugment
	out_file = sys.argv[2]

# opens the input .ics file and parses it as iCalendar Calendar object
ics_file = open(sys.argv[1],'rb')
ics_cal = Calendar.from_ical(ics_file.read())

# array of event information
result = []
for component in ics_cal.walk():
	if component.name == "VEVENT":
		# set containing all the events
		event = {
		'title':component.get('summary'),
		'backgroundColor':component.get('location'),
		'description':component.get('description'),
		'start':component.decoded('dtstart').isoformat(),
		'end':component.decoded('dtend').isoformat(),
		'url':component.get('url')
		}
		
		# append to the result array
		result.append(event)
ics_file.close()

# saves the result using jsonify
json_out = open(out_file, 'w')
json_out.write(json.dumps(result, sort_keys = False, indent = 4))
json_out.close()
