if (__name__ == "__main__"):
	print("Import class: from Record import *")
	print("Exiting...")
	exit()

### PACKAGES ###########################################################################################

import time
import os

########################################################################################################
#######################################  	CLASS DEF START	 #############################################
########################################################################################################


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

class Record:

	### CLASS VARIABLES ####################################################################################

	hoursDir = "hours/"

	# used as a placeholder for the end time in an ongoing record
	# it is replaced when the next record is created (with the new start time)
	PENDING_CHAR = "***"

	#### STATIC METHODS START ##############################################################################
	########################################################################################################
	########################################################################################################

	#
	#

	### GENERATOR METHODS START ############################################################################
	########################################################################################################

	### GENERATE FILE NAME: (YYYY-MM-DD-NAME) ##############################################################
	@staticmethod
	def getFileName(name, date):

		# get current date if supplied date is ""
		date = date or time.strftime("%Y-%m-%d")
		
		# "-" between date and name in filename
		date += "-"
		
		# return filename
		return Record.hoursDir + date + name

	### GENERATE FILE NAME: (.YYYY-MM-DD-NAME) #############################################################
	@staticmethod
	def getHiddenFileName(name, date):

		# get current date if supplied date is ""
		date = date or time.strftime("%Y-%m-%d")
		
		# "-" between date and name in filename
		date += "-"
		
		# return filename: uses hidden version of the file, since it contains extra info (durationLocked)
		return Record.hoursDir + "." + date + name

	### GENERATE SUBTOTAL FILENAME: (YYYY-MM-NAME-subtotal) ################################################
	@staticmethod
	def getSubtotalFileName(name, date):
		
		if not date:
			# if not supplied, get current date
			date = date or time.strftime("%Y-%m")
		
		else:	
			# turn date into date object
			date_obj = time.strptime(date, "%Y-%m-%d")
			
			# get year from date object
			year = time.strftime("%Y", date_obj)
			
			# get adjusted month from date
			month_int = Record.getSubtotalMonthInt(date)
			
			# format month int into string
			month = str(month_int).zfill(2)

		date = year + "-" + month + "-"

		fileName = Record.getHiddenFileName(name, date)

		return fileName

	########################################################################################################
	### GENERATOR METHODS END ##############################################################################

	#
	#

	### IO METHODS START ###################################################################################
	########################################################################################################

	### READ RECORDS FROM FILE #############################################################################
	@staticmethod
	def readRecords(name, date):
		
		#######################################################
		
		# set filename: uses hidden version of the file, since it contains extra info (durationLocked)
		fileName = Record.getHiddenFileName(name, date)
		
		#######################################################

		# read from file and return list of strings
		try:
			f = open(fileName, 'r')
			records = f.read().split('\n')
			f.close()
			return records

		# if the file doesn't exist, return an empty list
		except IOError:
			return []

	### WRITE RECORDS TO FILE ##############################################################################
	@staticmethod
	def writeRecords(name, date, records):
		
		#######################################################

		# set filename
		fileName = Record.getFileName(name, date)
		
		# set hidden filename: used to store extra information (durationLocked)
		hiddenFileName = Record.getHiddenFileName(name, date)

		# string vars: will contain joined records, will be written to file
		res, hiddenRes = "", ""

		#######################################################

		# join the records into strings
		for r in records:
			res += r.emailFormat() + "\n"
			hiddenRes += str(r) + "\n"

		# write strings to file
		try:
			f = open(fileName, 'w')
			f.write(res)
			f.close()

			f = open(hiddenFileName, 'w')
			f.write(hiddenRes)
			f.close()
		except IOError:
			pass

	### DELETES RECORDS FILES ##############################################################################
	@staticmethod
	def deleteRecords(name, date):
		
		#######################################################

		# set filename
		fileName = Record.getFileName(name, date)
		
		# set hidden filename: used to store extra information (durationLocked)
		hiddenFileName = Record.getHiddenFileName(name, date)

		#######################################################

		# system calls to delete both normal and hidden file
		os.system("rm -f " + filename)
		os.system("rm -f " + hiddenFileName)

	### READS SUBTOTAL FILE ################################################################################
	@staticmethod
	def readSubtotal(name, date):

		# get filename
		fileName = Record.getSubtotalFileName(name, date)

		try:
			f = open(fileName, 'r')
			subtotal = f.read()
			f.close()
			return float(subtotal or 0.0)
		except IOError:
			return 0.0

	### WRITES SUBTOTAL FILE ###############################################################################
	@staticmethod
	def writeSubtotal(name, date, subtotal):

		# get filename
		fileName = Record.getSubtotalFileName(name, date)
		
		try:
			f = open(fileName, 'w')
			f.write(str(subtotal))
			f.close()

		except IOError:
			pass

	########################################################################################################
	### IO METHODS END #####################################################################################

	#
	#

	### SUBTOTAL METHODS START #############################################################################
	########################################################################################################
	
	### ADDS TO SUBTOTAL FILE ##############################################################################
	@staticmethod
	def addToSubtotal(name, date, amount):

		# if the duration passed in is valid (it exists / not pending)
		if amount != Record.PENDING_CHAR:

			# read in subtotal 
			subtotal = Record.readSubtotal(name, date)

			# add the duration
			subtotal += float(amount)

			# write back the updated subtotal
			Record.writeSubtotal(name, date, subtotal)

	### SUBTRACTS FROM SUBTOTAL FILE #######################################################################
	@staticmethod
	def subtractFromSubtotal(name, date, amount):
		
		# if the duration passed in is valid (it exists / not pending)
		if amount != Record.PENDING_CHAR:
			
			# read in subtotal 
			subtotal = Record.readSubtotal(name, date)

			# subtract the duration
			subtotal -= float(amount)

			# write back the updated subtotal
			Record.writeSubtotal(name, date, subtotal)

	### GET SUBTOTAL MONTH INTEGER #########################################################################
	@staticmethod
	def getSubtotalMonthInt(date):

		# convert string to date object
		date_obj = time.strptime(date, "%Y-%m-%d")
		
		# get the integer of the day
		day_int = int(time.strftime("%d", date_obj))
		
		# get the integer of the month
		month_int = int(time.strftime("%m", date_obj))
		
		# if the day is past the 25th, increase the month by 1
		# this is when the pay period switches over to the next month
		if day_int > 25:
			month_int += 1
		
		return month_int

	### GET SUBTOTAL MONTH STRING ##########################################################################
	@staticmethod
	def getSubtotalMonth(date):
		# defines the pay period ; used for labeling the subtotal counter
		
		# get integer of month
		month_int = Record.getSubtotalMonthInt(date)

		# convert to date object
		month_obj = time.strptime(str(month_int), "%m")

		# conver to month string
		month = time.strftime("%b", month_obj)
		
		return month

	### GET SUBTOTAL COUNT #################################################################################
	@staticmethod
	def countSubtotal(records):

		new_subtotal = 0.0
		
		for r in records:
			
			# if it is a valid duration
			if r.duration != Record.PENDING_CHAR:
					
				# if the record is a string, make it an object first
				if type(r) is str:
					new_subtotal += float(Record(r).duration)

				# else just add its duration
				else:
					new_subtotal += float(r.duration)

		return new_subtotal

	########################################################################################################
	### SUBTOTAL METHODS END ###############################################################################

	#
	#
	
	### PARSING METHODS START ##############################################################################
	########################################################################################################

	### PARSE LIST OF STRINGS INTO LIST OF RECORD OBJECTS ##################################################
	@staticmethod
	def parseRecords(raw_records):

		# filter out empty records
		r_r = filter(None, raw_records)
		
		# return list mapped to Record objects
		return [Record(r) for r in r_r]

	### READ RECORDS FILE AND PARSE INTO RECORD OBJECTS ####################################################
	@staticmethod
	def parseRecordsFromFile(name, date):
		return Record.parseRecords(Record.readRecords(name, date))

	### PARSE HTML FORM INTO RECORD OBJECT #################################################################
	@staticmethod
	def getRecordFromHTML(request):

		#######################################################

		name = request.forms.get('name').strip().lower()

		start = Record.parseTime(request.forms.get('start'))
		end = Record.parseTime(request.forms.get('end'))
		###
		duration = request.forms.get('duration').strip()
		billable = request.forms.get('billable')
		emergency = request.forms.get('emergency')
		###
		label = request.forms.get('label').strip().upper()
		description = request.forms.get('description').strip().translate(None, '|')

		#######################################################
		
		durationLocked = False
		
		# if a duration is entered
		if duration:
			# lock it to prevent changing
			durationLocked = True
		
		# if there is no duration and the end time was provided
		elif start and end:
			# calculate the duration
			duration = Record.getDuration(start, end)

		# if end is not supplied
		else:
			# replace duration with Record.PENDING_CHAR
			duration = Record.PENDING_CHAR

		#######################################################

		# restore colon in start time
		start = Record.formatTime(start)

		# if end is supplied
		if end:
			# restore the colon
			end = Record.formatTime(end)
		
		# if not supplied
		else:
			# set as Record.PENDING_CHAR 
			end = Record.PENDING_CHAR

		#######################################################
		
		# get the date cookie or default to current date
		date = request.get_cookie("date") or time.strftime("%Y-%m-%d")

		# set start datetime 
		startTime = date + " " + start
		
		# set end datetime
		endTime = date + " " + end

		#######################################################
		
		# determine billable checked status
		if billable:
			billable = "Y"
		else:
			billable = "N"
		
		# determine emergency checked status
		if emergency:
			emergency = "Y"
		else:
			emergency = "N"

		#######################################################

		# duration locked is only present in the hidden file, since it is extra data for each record

		# format the string that will be supplied to the Record constructor
		record_string = "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}|{10}".format(
			name,
			date, start,
			date, end,
			duration,
			billable, emergency,
			label, description,
			durationLocked)

		#######################################################

		return Record(record_string)

	########################################################################################################
	### PARSING METHODS END ################################################################################

	#
	#

	### TIME METHODS START #################################################################################
	########################################################################################################

	# removes colon and adds leading '0' if missing
	# time: accept [*] return [str]
	@staticmethod
	def parseTime(time):
		if time:
			return str(time.strip()).translate(None, ':').zfill(4)
		return ""

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
		if time == Record.PENDING_CHAR:
			return None
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


	# will round to the nearest quarter hour mark
	@staticmethod
	def roundTime(t):
		time = Record.parseTime(t)                                                                                                                                                                                                                            
		hours = int(time[:2])                                                                                                                                                                                                                    
		minutes = int(time[2:])                                                                                                                                                                                                                      
		quarters = minutes / 15                                                                                                                                                                                                                             
		remainder = minutes % 15                                                                                                                                                                                                                             
		if remainder > 7:                                                                                                                                                                                                                                
			quarters += 1                                                                                                                                                                                                                               
		if quarters > 3:                                                                                                                                                                                                                                
			hours += 1                                                                                                                                                                                                                           
			quarters = 0                                                                                                                                                                                                                                
		return str(hours).zfill(2) + str(quarters * 15).zfill(2)       

	# reutrns current time rounded to nearest quarter hour mark
	@staticmethod
	def getCurrentRoundedTime():
		t = time.strftime("%H%M")
		return Record.roundTime(t)

	########################################################################################################
	### TIME METHODS END ###################################################################################

	#
	#


	#############################################################
	@staticmethod
	def getPrevRecord(records, index):
		try:
			if (index-1 >= 0):
				return records[index-1]
		except IndexError:
			pass
		return None

	@staticmethod
	def getNextRecord(records, index):
		try:
			if (index+1 < len(records)):
				return records[index+1]
		except IndexError:
			pass
		return None

	#############################################################
	@staticmethod
	def adjustAdjacentRecords(records, index):
		if not records:
			raise Exception("Record.spliceInRecords(): records var is null")

		new_record = records[index]

		prev_record = Record.getPrevRecord(records, index)
		if prev_record:
			# if end time hasn't been supplied, supply it now from new_record
			if prev_record.duration == Record.PENDING_CHAR:
				prev_record.setEnd(new_record.start)

		next_record = Record.getNextRecord(records, index)
		if next_record:
			# if next_record has a pending duration, and new_record has an end time, set next_record.start = new_record.end
			if (next_record.duration == Record.PENDING_CHAR) and (new_record.end != Record.PENDING_CHAR):
				next_record.setStart(new_record.end)
			# if end time is not supplied but next record exists, use that time
			if new_record.duration == Record.PENDING_CHAR:
				new_record.setEnd(new_record.start)


		# if the previous record exists
		if prev_record:
			#	after checking both prev and next records in case of PENDING_CHAR...
			prev_record.duration = Record.getDuration(prev_record.start, prev_record.end)
			records[index-1] = prev_record

			# calculate overlap : new_start - prev_end : if overlap => negative duration
			# if the new start time is less than the previous end time: adjustment needed
			overlap = Record.getDuration(prev_record.end, new_record.start)
			# if there was overlap
			if (overlap < 0):
				# modify the prev_end time by subtracting the overlap duration
				prev_record.modifyEnd(overlap)
				# print("Modifying prev_record by:", overlap)
				# print("prev_record:", str(prev_record))
				# print("new_record:", str(new_record))

		# if the next record exists
		if next_record:
			#	after checking both prev and next records in case of PENDING_CHAR...
			new_record.duration = Record.getDuration(new_record.start, new_record.end)
			records[index] = new_record
		
			# calculate overlap : next_start - new_end : if overlap => negative duration
			overlap = Record.getDuration(new_record.end, next_record.start)
			# if there was overlap
			if (overlap < 0):
				# modify next_start time by subtracting overlap duration
				next_record.modifyStart(overlap)
				# print("Modifying next_record by:", overlap)
				# print("new_record:", str(new_record))
				# print("next_record:", str(next_record))

	#############################################################




	#
	#

	########################################################################################################
	########################################################################################################
	#### STATIC METHODS END ################################################################################


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

	def calculateAndSetDuration(self):
		self.setDuration(Record.getDuration(self.start, self.end))

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

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


########################################################################################################
#######################################  	CLASS DEF END	 ###############################################
########################################################################################################