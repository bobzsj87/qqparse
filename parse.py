import time, datetime
import re
import sys

if len(sys.argv) >= 3:
	filename = sys.argv[1]
	minDate = time.strptime(sys.argv[3], "%Y-%m-%d")  if len(sys.argv) == 4 else 0

	f = open(filename, 'r')
	fo = open(time.strftime("%Y%m%d%H%M.sql"), 'w')
	text = f.read()
	result = re.finditer("(\d{4}-\d{2}-\d{2} \d+:\d+:\d+ \wM) (.+?)\((\d+)\)", text)
	fo.write("INSERT IGNORE INTO message_log (time, name, qq, qqgroup) VALUES \n")
	sql = []
	for r in result:
		#print r.group(0)
		if not re.match("10+",r.group(3)):
			t = time.strptime(r.group(1), "%Y-%m-%d %I:%M:%S %p")
			if t > minDate:
				sql.append("('%s', '%s', '%s', '%s')" % (
					time.strftime("%Y-%m-%d %H:%M:%S", t), r.group(2), r.group(3), sys.argv[2]))
	fo.write(",\n".join(sql))		
	fo.write(";")
	fo.close()
	f.close()

else:
	print ("""
	Usage: 3 arguments: import file location which is dumped from QQ as a txt, and the qq group (such as reading or lang), then optionally, the start date to import
	Like: python parse.py test.txt lang 2015-01-01
	And you will get a sql with the current timestamp then upload it and wait for the task to complete
	""")
