from Record import Record


s = "testtest|2016-06-30 11:00|2016-06-30 13:00|2.0|Y|N|TEST|testing"
l = [Record("testtest|2016-06-30 11:00|2016-06-30 12:00|1.0|Y|N|TEST|prev"),
		 Record("testtest|2016-06-30 11:30|2016-06-30 12:30|1.0|Y|N|TEST|new"),
		 Record("testtest|2016-06-30 12:00|2016-06-30 13:00|1.0|Y|N|TEST|next")]
r = Record(s)

def p(list):
	for l in list:
		print(l)


def run():
	p(l)
	Record.adjustAdjacentRecords(l,0)
	p(l)