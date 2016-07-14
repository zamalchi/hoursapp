if (__name__ == "__main__"):
	print("Import class: from Record import *")
	print("Exiting...")
	exit()


import time


class Record:

	########################################################################################################
	########################################################################################################
	########################################################################################################	
	########################################################################################################
	# START OF STATIC METHODS

	########################################################################################################
	########################################################################################################
	# START OF IO METHODS

	@staticmethod
	def readRecords(filePath):
		try:
			f = open(filePath, 'r')
			records = f.read().split('\n')
			f.close()
			return records
		except IOError:
			return []

	# filters any empty records
	# parses record strings and returns record objects
	# raw_records: accept [list[str]] return [list[Record]]
	@staticmethod
	def parseRecords(raw_records):
		r_r = filter(None, raw_records)
		records = []
		for r in r_r:
			records.append(Record(r))
		return records

	@staticmethod
	def parseRecordsFromFile(filePath):
		return Record.parseRecords(Record.readRecords(filePath))


	@staticmethod
	def writeRecords(filePath, records):
		try:
			s = ""
			for r in records:
				s += str(r) + "\n"

			f = open(filePath, 'w')
			f.write(s)
			f.close()
		except IOError:
			pass

	# END OF IO METHODS
	########################################################################################################
	########################################################################################################

	
	########################################################################################################
	########################################################################################################
	@staticmethod
	def getRecordFromHTML(request):
		name = request.forms.get('name').strip().lower()

		start = Record.parseTime(request.forms.get('start').strip())
		end = Record.parseTime(request.forms.get('end').strip())
		###
		duration = request.forms.get('duration').strip()
		billable = request.forms.get('billable')
		emergency = request.forms.get('emergency')
		###
		label = request.forms.get('label').strip().upper()
		description = request.forms.get('description').strip().translate(None, '|')

		#######################################################
		durationLocked = False
		# if not supplied, calculate duration
		if not duration:
			duration = Record.getDuration(start, end)
		# if supplied, lock the duration to prevent adjustments
		else:
			durationLocked = True

		### restore colon in times
		start = Record.formatTime(start)
		end = Record.formatTime(end)

		###
		date = time.strftime("%Y-%m-%d")
		startTime = date + " " + start
		endTime = date + " " + end
		#######################################################
		# determine billable/emergency checked status
		if billable:
			billable = "Y"
		else:
			billable = "N"
		if emergency:
			emergency = "Y"
		else:
			emergency = "N"

		# durationLocked is being added to the end of this string so it can be saved on file
		# durationLocked is NOT part of the string that gets sent in an email
		record_string = "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}|{10}".format(
			name,
			date, start,
			date, end,
			duration,
			billable, emergency,
			label, description,
			durationLocked)

		return Record(record_string)
	########################################################################################################


	# removes colon and adds leading '0' if missing
	# time: accept [*] return [str]
	@staticmethod
	def parseTime(time):
		return str(time).translate(None, ':').zfill(4)

	# adds a colon between hours and minutes
	# ensures time is parsed correctly
	# time: accept [*] return [str]
	@staticmethod
	def formatTime(time):
		p = Record.parseTime(time)
		return str(p)[:2] + ':' + p[2:]

	# takes [hrmn | hr:mn] format and returns as number of minutes
	# time: accept [*] return [int]
	@staticmethod
	def getMinFromTime(time):
		# if it is an int, it has already been processed, so return
		# ex: called from getDuration()
		if (type(time) == int):
			return time
		p = Record.parseTime(time)
		return (int(p[:2]) * 60) + int(p[2:])

	# takes number of minutes and returns as [hrmn] format
	# min: accept [str | int] return [str]
	@staticmethod
	def getTimeFromMin(min):
		i = int(min)
		hours = str(i/60).zfill(2)
		minutes = str(i%60).zfill(2)
		return hours + minutes


	@staticmethod
	def getDuration(start, end):
		s = Record.getMinFromTime(start)
		e = Record.getMinFromTime(end)
		return float((e - s)/float(60))


	#############################################################
	@staticmethod
	def adjustAdjacentRecords(records, index):
		if not records:
			raise Exception("Record.spliceInRecords(): records var is null")

		new_record = records[index]
		prev_record = None
		next_record = None
		
		try:
			if (index-1 >= 0):
				prev_record = records[index-1]
		except IndexError:
			prev_record = None
			pass
		try:
			if (index+1 < len(records)-1):
				next_record = records[index+1]
		except IndexError:
			next_record = None
			pass

		# prevent list wrap-around issues with negative indices by comparing the objects
		if (new_record == prev_record):
			prev_record = None
		if (new_record == next_record):
			new_record = None

		# if the previous record exists
		if prev_record:
			# calculate duration : new_start - prev_end : if overlap => negative duration
			# if the new start time is less than the previous end time: adjustment needed
			duration = Record.getDuration(prev_record.end, new_record.start)
			# if there was overlap
			if (duration < 0):
				# modify the prev_end time by subtracting the overlap duration
				prev_record.modifyEnd(duration)

		# if the next record exists
		if next_record:
			# calculate duration : next_start - new_end : if overlap => negative duration
			duration = Record.getDuration(new_record.end, next_record.start)
			# if there was overlap
			if (duration < 0):
				# modify next_start time by subtracting overlap duration
				next_record.modifyStart(duration)

	#############################################################

	# END OF STATIC METHODS
	########################################################################################################
	########################################################################################################
	########################################################################################################	
	########################################################################################################
	
	def __init__(self, string):
		elems = string.split('|')
		start_DT = elems[1].split(" ")
		end_DT = elems[2].split(" ")

		self.name = elems[0]

		self.date = start_DT[0]
		self.fstart = start_DT[1]
		self.start = Record.parseTime(self.fstart)
		self.fend = end_DT[1]
		self.end = Record.parseTime(self.fend)

		self.duration = elems[3]

		self.billable = elems[4]
		self.emergency = elems[5]

		self.label = elems[6]
		self.description = elems[7]

		# if manually entered, the duration will NOT be adjustable
		if (elems[8] == "True"):
			self.durationLocked = True
		else:
			self.durationLocked = False

	#############################################################

	def setStart(self, time):
		t = str(time)
		i = Record.parseTime(t)
		s = Record.formatTime(i)

		self.start = i
		self.fstart = s


	def setEnd(self, time):
		t = str(time)
		i = Record.parseTime(t)
		s = Record.formatTime(i)

		self.end = i
		self.fend = s

	############################################################

	def modifyStart(self, amount):
		start = Record.getMinFromTime(self.start)
		new = float(start) - (float(amount)*60)
		self.setStart(Record.getTimeFromMin(int(new)))
		self.modifyDuration(float(amount))

	def modifyEnd(self, amount):
		end = Record.getMinFromTime(self.end)
		new = float(end) + (float(amount)*60)
		self.setEnd(Record.getTimeFromMin(int(new)))
		self.modifyDuration(float(amount))

	def modifyTimes(self, amount):
		self.modifyStart(amount)
		self.modifyEnd(amount)

	#############################################################

	def setDuration(self, duration):
		self.duration = float(duration)

	def modifyDuration(self, duration):
		if not self.durationLocked:
			d = float(self.duration)
			d += float(duration)
			self.duration = str(d)

	#############################################################


	def __str__(self):
		return "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}|{10}".format(
			self.name,
			self.date, self.fstart,
			self.date, self.fend,
			self.duration,
			self.billable, self.emergency,
			self.label, self.description,
			self.durationLocked)

	# does not contain durationLocked
	def emailFormat(self):
		return "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}".format(
			self.name,
			self.date, self.fstart,
			self.date, self.fend,
			self.duration,
			self.billable, self.emergency,
			self.label, self.description)