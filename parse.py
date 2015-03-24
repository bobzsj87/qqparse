import time, datetime
import re
import sys

if len(sys.argv) == 3:
	filename = sys.argv[1]
	f = open(filename, 'r')
	fo = open(time.strftime("%Y%m%d%H%M%.sql"), 'w')
	text = f.read()
	result = re.finditer("(\d{4}-\d{2}-\d{2} \d+:\d+:\d+ \wM) (.+?)\((\d+)\)", text)
	for r in result:
		#print r.group(0)
		if not re.match("10+",r.group(3)):
			t = time.strptime(r.group(1), "%Y-%m-%d %I:%M:%S %p")
			sql = "INSERT IGNORE INTO message_log (time, name, qq, group) VALUES ('%s', '%s', %s, '%s');\n" % (
				time.strftime("%Y-%m-%d %H:%M:%S", t), r.group(2), r.group(3), sys.argv[2])
			fo.write(sql)
	f.close()
	fo.close()
else:
	print """
	Usage: 2 arguments: import file location which is dumped from QQ as a txt, and the qq group (such as reading or lang)\n
	Like: python parse.py test.txt lang\n
	And you will get a sql with the current timestamp then upload it and wait for the task to complete
	"""
