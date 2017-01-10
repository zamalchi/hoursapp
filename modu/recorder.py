#!/usr/bin/env python

### INSTRUCTIONS #######################################################################################

# from Record import \
#   Record
#   RecordMalformedException (required by Record)

# (optional) after importing, set:
#   Record.ROOT_DIR - default: '.'
#   Record.HOURS_DIR - default: './hours'

### PACKAGES ###########################################################################################

import calendar
import datetime as dt
import os
import time

### IMPORTS ############################################################################################

### RUNNING AS MAIN ####################################################################################

if __name__ == "__main__":
  print("Import class: from Record import Record, RecordMalformedException")
  print("Exiting...")
  exit()



# default values : set after importing class
ROOT_DIR = "."
HOURS_DIR = os.path.join(ROOT_DIR, "hours")

# used as a placeholder for the end time in an ongoing record
# it is replaced when the next record is created (with the new start time)
PENDING_CHAR = "***"


########################################################################################################
#######################################  	CLASS DEF START	 #############################################
########################################################################################################
class Record:
  
  ### CONSTRUCTOR START ##################################################################################
  ########################################################################################################
  
  ### DEFAULT CONSTRUCTOR: PARSES PROPERLY FORMATTED STRING INTO RECORD OBJECT ###########################
  def __init__(self, string):
    
    try:
      
      #######################################################
      
      elems = string.split('|')
      start_DT = elems[1].split(" ")
      end_DT = elems[2].split(" ")
      
      #######################################################
      
      self.name = elems[0]
      
      self.date = validateDate(start_DT[0])
      
      #######################################################
      
      # formatted start ("HH:MM")
      self.fstart = start_DT[1]
      
      # start ("HHMM")
      self.start = parseTime(self.fstart)
      
      # formatted end ("HH:MM")
      self.fend = end_DT[1]
      
      # end ("HHMM")
      self.end = parseTime(self.fend)
      
      #######################################################
      
      self.duration = elems[3]
      
      self.label = elems[4]
      
      self.billable = elems[5]
      self.emergency = elems[6]
      
      self.notes = elems[7]
      
      #######################################################
      
      # in the case of trying to construct a record without a durationLocked field (elems[8])
      if len(elems) < 9:
        # default to False
        self.durationLocked = False
      
      else:
        # if manually entered, the duration will NOT be adjustable
        # this field is only visible in the Record object or in the hidden version of the file
        if elems[8] == "True":
          self.durationLocked = True
        else:
          self.durationLocked = False
    
    except Exception:
      raise RecordMalformedException("ERROR - INVALID __init__ STRING : " + string)
  
  ########################################################################################################
  ### CONSTRUCTOR END ####################################################################################
  
  #
  #
  
  ### DURATION METHODS START #############################################################################
  ########################################################################################################
  
  ### SETS DURATION TO SUPPLIED VALUE ####################################################################
  def setDuration(self, duration):
    self.duration = float(duration)
  
  ### CALCULATES THE DURATION FROM START AND END TIMES, THEN SETS THE DURATION ###########################
  def calculateAndSetDuration(self):
    self.setDuration(getDuration(self.start, self.end))
  
  ### IF NOT LOCKED, *MODIFIES* THE DURATION BY THE SUPPLIED AMOUNT ######################################
  def modifyDuration(self, amount):
    
    if not self.durationLocked:
      
      # get the duration
      d = float(self.duration)
      
      # add the amount (supplying a negative amount will subtract from the duration)
      d += float(amount)
      
      # set modified duration
      self.duration = str(d)
  
  ########################################################################################################
  ### DURATION METHODS END ###############################################################################
  
  #
  #
  
  ### TIME METHODS START #################################################################################
  ########################################################################################################
  
  ### SET START TIME WHILE ENSURING CORRECT PARSING/FORMATTING ###########################################
  def setStart(self, time):
    
    t = str(time)
    
    # parse time for start field
    i = parseTime(t)
    
    # format parsed time for fstart (formatted start) field
    s = formatTime(i)
    
    self.start = i
    self.fstart = s
  
  ### SET END TIME WHILE ENSURING CORRECT PARSING/FORMATTING #############################################
  def setEnd(self, time):
    t = str(time)
    
    # parse time for end field
    i = parseTime(t)
    
    # format parsed time for fend (formatted end) field
    s = formatTime(i)
    
    self.end = i
    self.fend = s
  
  ### MODIFY START TIME AND DURATION BY ADDING SUPPLIED AMOUNT ###########################################
  def modifyStart(self, amount):
    
    # get start time in minutes
    start = getMinFromTime(self.start)
    
    # convert amount into minutes and add to start time
    new = float(start) + (float(amount)*60)
    
    # set start to new value (converted back into a string)
    self.setStart(getTimeFromMin(int(new)))
    
    # modify the duration by subtracting the amount added to the start time
    self.modifyDuration(-float(amount))
  
  ### MODIFY END TIME AND DURATION BY A SUPPLIED AMOUNT ##################################################
  def modifyEnd(self, amount):
    
    # get the end time in minutes
    end = getMinFromTime(self.end)
    
    # convert amount into minutes and add to end time
    new = float(end) + (float(amount)*60)
    
    # set end to new value (converted back into a string)
    self.setEnd(getTimeFromMin(int(new)))
    
    # modify the duration by adding the amount added to the end time
    self.modifyDuration(float(amount))
  
  ### MODIFY START AND END TIMES BY A SUPPLIED AMOUNT (SHIFTS RECORD AS A WHOLE W/O MODIFYING DURATION) ##
  def modifyTimes(self, amount):
    self.modifyStart(amount)
    self.modifyEnd(amount)
  
  ########################################################################################################
  ### TIME METHODS END ###################################################################################
  
  #
  #
  
  ### TO_STRING METHODS START ############################################################################
  ########################################################################################################
  
  ### DEFAULT TO_STRING CALLED VIA str() #################################################################
  def __str__(self):
    # contains durationLocked --> intended for writing to hidden file
    return "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}|{10}".format(
      self.name,
      self.date, self.fstart,
      self.date, self.fend,
      self.duration,
      self.label,
      self.billable, self.emergency,
      self.notes,
      self.durationLocked)
  
  ### SECONDARY TO_STRING TO MATCH CORRECT RECORD STRING FORMAT (FOR PAYROLL) ############################
  def emailFormat(self):
    # does not contain durationLocked
    return "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}".format(
      self.name,
      self.date, self.fstart,
      self.date, self.fend,
      self.duration,
      self.label,
      self.billable, self.emergency,
      self.notes)
    
    ########################################################################################################
    ### TO_STRING METHODS END ##############################################################################

########################################################################################################
####################################### CLASS DEF END ##################################################
########################################################################################################

class RecordMalformedException(Exception):
  pass


#
#
#
#
#
#
#
#
#
#
#
#
#
#

#### STATIC METHODS START ##############################################################################
########################################################################################################
########################################################################################################

#
#

### GENERATOR METHODS START ############################################################################
########################################################################################################

def getFileName(name, date):
  """
  Produces a filename for a specific day of records
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date of records
  :return: <str> filename with format "YYYY-MM-DD-name"
  """
  # get current date if supplied date is ""
  date = validateDate(date)
  
  # "-" between date and name in filename
  filename = "{0}-{1}".format(str(date), name)
  
  # return filename
  return os.path.join(HOURS_DIR, filename)


def getHiddenFileName(name, date):
  """
  Produces a hidden filename for a specific day of records
    The hidden file contains an extra piece of info (durationLocked) for each record that day
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date of records
  :return: <str> filename with format ".YYYY-MM-DD-name"
  """
  # get current date if supplied date is ""
  date = validateDate(date)
  
  # "." prepended and "-" between date and name in filename
  filename = ".{0}-{1}".format(str(date), name)
  
  # return filename: uses hidden version of the file, since it contains extra info (durationLocked)
  return os.path.join(HOURS_DIR, filename)


### GENERATE SUBTOTAL FILENAME: (YYYY-MM-NAME-subtotal) ################################################
def getSubtotalFileName(name, date):
  """
  
  :param name:
  :param date:
  :return:
  """
  #######################################################
  
  date = validateDate(date)
  
  month = date.month
  
  # adjust for pay period which ends on the 25th
  if date.day > 25:
    month += 1
  
  # add leading 0 if < 10 ; also convert to str
  month = str(month).zfill(2)
  
  #######################################################
  
  # ("YYYY-MM-")
  filename = ".{0}-{1}-subtotal-{2}".format(date.year, month, name)
  
  # ("DIR/.YYYY-MM-subtotal-NAME")
  return os.path.join(HOURS_DIR, filename)


########################################################################################################
### GENERATOR METHODS END ##############################################################################

#
#

### IO METHODS START ###################################################################################
########################################################################################################

### READ RECORDS FROM FILE #############################################################################
def readRecords(name, date):
  #######################################################
  
  # set filename: uses hidden version of the file, since it contains extra info (durationLocked)
  fileName = getHiddenFileName(name, date)
  
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
def writeRecords(name, date, records):
  #######################################################
  
  # set filename
  fileName = getFileName(name, date)
  
  # set hidden filename: used to store extra information (durationLocked)
  hiddenFileName = getHiddenFileName(name, date)
  
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
def deleteRecords(name, date):
  #######################################################
  
  # set filename
  fileName = getFileName(name, date)
  
  # set hidden filename: used to store extra information (durationLocked)
  hiddenFileName = getHiddenFileName(name, date)
  
  #######################################################
  
  # system calls to delete both normal and hidden file
  os.system("rm -f " + fileName)
  os.system("rm -f " + hiddenFileName)


### READS SUBTOTAL FILE ################################################################################
def readSubtotal(name, date):
  # get filename
  fileName = getSubtotalFileName(name, date)
  
  try:
    f = open(fileName, 'r')
    subtotal = f.read()
    f.close()
    return float(subtotal or 0.0)
  except IOError:
    return 0.0


### WRITES SUBTOTAL FILE ###############################################################################
def writeSubtotal(name, date, subtotal):
  # get filename
  fileName = getSubtotalFileName(name, date)
  
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

def getSubtotalForDay(name, date):
  """
  Adds up the hours worked on a specific day by a user
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date of records
  :return: <float> total hours worked during the day
  """
  records = parseRecordsFromFile(name, validateDate(date))
  subtotal = countSubtotal(records)
  return subtotal
  

def getTotalForPayPeriod(name, date):
  """
  Adds up subtotals of each record in the pay period (adjusted for the 25th of the month)
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date within the pay period
  :return: <float> total hours worked during the pay period
  """
  PERIOD_END = 25
  
  date = validateDate(date)
  total = 0.0
  
  """ NOTE:
  beforeCutoff<Month,Year> is the part of the pay period that occurs between the 26th and the end of the month
    in actuality, this is kind of erroneous naming, since all the counted days happen after the cutoff
    (by nature of being within the pay period);
  
  afterCutoff<Month,Year> is the part of the pay period that occurs between the 1st and the 25th of the month
  """
  
  if date.day <= PERIOD_END:
    # DATE IS BEFORE THE 25th, meaning the cutoff happened in the previous month
    beforeCutoffMonth = date.month - 1 if date.month > 1 else 12
    beforeCutoffYear = date.year - 1 if beforeCutoffMonth == 12 else date.year
    
  else:
    # DATE IS AFTER THE 25th, meaning the cutoff happened in this month
    beforeCutoffMonth = date.month
    beforeCutoffYear = date.year
  
  # get the last day of the month
  beforeCutoffMonthEnd = calendar.monthrange(beforeCutoffYear, beforeCutoffMonth)[1]
  
  # these statements reference beforeCutoff<Month,Year> and not date to normalize the following logic
  afterCutoffMonth = beforeCutoffMonth + 1 if beforeCutoffMonth < 12 else 1
  afterCutoffYear = beforeCutoffYear + 1 if afterCutoffMonth == 1 else beforeCutoffYear

  # GET TOTAL FOR DAYS IN RANGE : 26th - LAST DAY OF MONTH
  for day in range(26, beforeCutoffMonthEnd + 1):
    beforeCutoffDate = dt.date(year=beforeCutoffYear, month=beforeCutoffMonth, day=day)
    total += getSubtotalForDay(name, beforeCutoffDate)
    print("DATE : {} -- SUBTOTAL : {} -- TOTAL : {}".format(beforeCutoffDate, getSubtotalForDay(name, beforeCutoffDate), total))

  # GET TOTAL FOR DAYS IN RANGE : 1st - 25th
  for day in range(1, 26):
    afterCutoffDate = dt.date(year=afterCutoffYear, month=afterCutoffMonth, day=day)
    total += getSubtotalForDay(name, afterCutoffDate)
    print("DATE : {} -- SUBTOTAL : {} -- TOTAL : {}".format(afterCutoffDate, getSubtotalForDay(name, afterCutoffDate), total))

  # RETURN SUM
  return total
  


### ADDS TO SUBTOTAL FILE ##############################################################################
def addToSubtotal(name, date, amount):
  # if the duration passed in is valid (it exists / not pending)
  if amount != PENDING_CHAR:
    # read in subtotal
    subtotal = readSubtotal(name, date)
    
    # add the duration
    subtotal += float(amount)
    
    # write back the updated subtotal
    writeSubtotal(name, date, subtotal)


### SUBTRACTS FROM SUBTOTAL FILE #######################################################################
def subtractFromSubtotal(name, date, amount):
  # if the duration passed in is valid (it exists / not pending)
  if amount != PENDING_CHAR:
    # read in subtotal
    subtotal = readSubtotal(name, date)
    
    # subtract the duration
    subtotal -= float(amount)
    
    # write back the updated subtotal
    writeSubtotal(name, date, subtotal)


### GET SUBTOTAL MONTH INTEGER #########################################################################
def getSubtotalMonthInt(date):
  date = validateDate(date)
  
  # get the integer of the day
  day_int = date.day
  
  # get the integer of the month
  month_int = date.month
  
  # if the day is past the 25th, increase the month by 1
  # this is when the pay period switches over to the next month
  if day_int > 25:
    month_int += 1
  
  return month_int


### GET SUBTOTAL MONTH STRING ##########################################################################
def getSubtotalMonth(date):
  # get updated month ; defines the pay period ; used for labeling the subtotal counter
  month_int = getSubtotalMonthInt(date)
  
  # replace month with the one used for the subtotal
  date = date.replace(date.year, month_int, date.day)
  
  # get the str name for the month
  return date.strftime("%b")


### GET SUBTOTAL COUNT #################################################################################
def countSubtotal(records):
  new_subtotal = 0.0
  
  for r in records:
    
    # if it is a valid duration
    if r.duration != PENDING_CHAR:
      
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

def parseRecords(raw_records):
  # filter out empty records
  r_r = filter(None, raw_records)
  
  # return list mapped to Record objects
  return [Record(r) for r in r_r]


### READ RECORDS FILE AND PARSE INTO RECORD OBJECTS ####################################################

def parseRecordsFromFile(name, date):
  # read in records
  raw_records = readRecords(name, date)
  
  # return parsed Record objects
  return parseRecords(raw_records)


### PARSE HTML FORM INTO RECORD OBJECT #################################################################

def getRecordFromHTML(request):
  #######################################################
  
  name = request.forms.get('name').strip().lower()
  
  start = parseTime(request.forms.get('start'))
  end = parseTime(request.forms.get('end'))
  ###
  duration = request.forms.get('duration').strip()
  ### billable/emergency are each either 'Y' or 'N'
  billable = request.forms.get('billable')
  emergency = request.forms.get('emergency')
  ###
  label = request.forms.get('label').strip().upper()
  notes = request.forms.get('notes').strip().translate(None, '|')
  
  #######################################################
  
  durationLocked = False
  
  # if a duration is entered
  if duration:
    # lock it to prevent changing
    durationLocked = True
  
  # if there is no duration and the end time was provided
  elif start and end:
    # calculate the duration
    duration = getDuration(start, end)
  
  # if end is not supplied
  else:
    # replace duration with PENDING_CHAR
    duration = PENDING_CHAR
  
  #######################################################
  
  # restore colon in start time
  start = formatTime(start)
  
  # if end is supplied
  if end:
    # restore the colon
    end = formatTime(end)
  
  # if not supplied
  else:
    # set as PENDING_CHAR
    end = PENDING_CHAR
  
  #######################################################
  
  # get the date cookie or default to current date ; save as str
  date = str(validateDate(request.get_cookie("date")))
  
  #######################################################
  
  # duration locked is only present in the hidden file, since it is extra data for each record
  
  # format the string that will be supplied to the Record constructor
  record_string = "{0}|{1} {2}|{3} {4}|{5}|{6}|{7}|{8}|{9}|{10}".format(
    name,
    date, start,
    date, end,
    duration,
    label,
    billable, emergency,
    notes,
    durationLocked)
  
  #######################################################
  
  return Record(record_string)


########################################################################################################
### PARSING METHODS END ################################################################################

#
#

### TIME METHODS START #################################################################################
########################################################################################################

### PARSE TIME INTO ("HHMM") FORMAT ####################################################################

def parseTime(time):
  if time:
    # return if pending
    if time == PENDING_CHAR:
      return time
    
    # removes colon and adds leading '0' if missing
    return str(time.strip()).translate(None, ':').zfill(4)
  
  return ""


### FORMAT TIME INTO ("HH:MM") FORMAT ##################################################################

def formatTime(time):
  # ensures time is parsed correctly
  p = parseTime(time)
  
  # adds a colon between hours and minutes
  return str(p)[:2] + ':' + p[2:]


### CONVERT TIME INTO NUMBER OF MINUTES ################################################################

def getMinFromTime(time):
  # checks for not present time
  if time == PENDING_CHAR:
    return None
  
  # if it is an int, it has already been processed, so return
  # ex: called from getDuration()
  if type(time) == int:
    return time
  
  # ensures it is parsed
  p = parseTime(time)
  
  # returns number of minutes
  return (int(p[:2]) * 60) + int(p[2:])


### CONVERT NUMBER OF MINUTES INTO ("HHMM") ############################################################

def getTimeFromMin(min):
  # ensures int type
  i = int(min)
  
  # gets hours through integer division
  hours = str(i / 60).zfill(2)
  
  # gets minutes through modulus
  minutes = str(i % 60).zfill(2)
  
  # return ("HHMM")
  return hours + minutes


### CALCULATE THE DURATION USING THE START AND END TIMES ###############################################

def getDuration(start, end):
  # get number of minutes from start time
  s = getMinFromTime(start)
  
  # get number of minutes from end time
  e = getMinFromTime(end)
  
  # return number of hours as float (x.xx)
  return float((e - s) / float(60))


### ROUND PASSED IN TIME TO NEAREST 15-MINUTE MARK #####################################################

def roundTime(t):
  hours = minutes = 0
  
  #######################################################
  
  if type(t) is dt.time:
    
    hours = t.hour
    minutes = t.minute
  
  #######################################################
  
  else:
    return ""
  
  # else:
  #     # ensure the time is parsed correctly
  #     time = parseTime(t)
  #
  #     # parse the hours
  #     hours = int(time[:2])
  #
  #     # parse the minutes
  #     minutes = int(time[2:])
  #
  #######################################################
  
  # calculate the number of quarter-hour units (rounded down) the minutes equal
  quarters = minutes / 15
  
  # calculate how far from the next quarter-hour mark the minutes are
  remainder = minutes % 15
  
  #######################################################
  
  # if the time is at least 7 minutes into the current quarter-hour, increment quarters
  if remainder > 7:
    quarters += 1
  
  # if there are over three quarters, the hour has been passed: add an hour and reset quarters to 0
  if quarters > 3:
    hours += 1
    quarters = 0
  
  #######################################################
  
  # return ("HHMM") now rounded to the quarter-hour
  return str(hours).zfill(2) + str(quarters * 15).zfill(2)


### ROUND CURRENT TIME TO NEAREST 15-MINUTE MARK #######################################################

def getCurrentRoundedTime():
  # get current time ; round it to 15-minute mark
  return roundTime(dt.datetime.now().time())


########################################################################################################
### TIME METHODS END ###################################################################################

#
#

### RECORD METHODS START ###############################################################################
########################################################################################################

### RETURNS PREVIOUS RECORD IN LIST or NONE ############################################################

def getPrevRecord(records, index):
  try:
    # if the previous index is a valid index
    if index - 1 >= 0:
      # return the previous record
      return records[index - 1]
  
  except IndexError:
    pass
  
  # if returning the prev record was unsuccessful, return None
  return None


### RETURNS NEXT RECORD IN LIST or NONE ################################################################

def getNextRecord(records, index):
  try:
    # if the next index is a valid index
    if index + 1 < len(records):
      # return the next record
      return records[index + 1]
  
  except IndexError:
    pass
  
  # if returning the prev record was unsuccessful, return None
  return None


### CHECKS IF RECORD OVERLAPS WITH ADJACENT RECORDS AND ADJUSTS ADJACENT START/END TIMES ACCORDINGLY ###

def adjustAdjacentRecords(records, index):
  #######################################################
  
  # if the records list is empty, print error statement and return from function
  if not records:
    print("ERROR: empty records list passed into adjustAdjacentRecords()")
    return
  
  #######################################################
  
  # get the newly inserted record
  new_record = records[index]
  
  # get the previous record if it exists
  prev_record = getPrevRecord(records, index)
  
  # get the next record if it exists
  next_record = getNextRecord(records, index)
  
  #######################################################
  # FUNCTION: SETS PREVIOUS RECORD'S END TIME
  
  if prev_record:
    
    # if the previous record's end time has not been supplied
    if prev_record.duration == PENDING_CHAR:
      # set the previous record's end time to be the new record's start time
      prev_record.setEnd(new_record.start)
      
      # the new record *FINISHES* the previous record
      # visually: [START]~previous~[PENDING --> END]   [START]~new~[PENDING|END]
  
  #######################################################
  # FUNCTION: SHIFTS NEXT RECORD'S START TIME (IF PARTIAL RECORD)
  
  if next_record:
    
    # if (the next record's end time has not been supplied) and (the new record has an end time)
    # NOTE: if the next record doesn't have a supplied end time, the new record MUST have an end time (required by HTML input)
    if (next_record.duration == PENDING_CHAR) and (new_record.end != PENDING_CHAR):
      # supply the next record's start time using the new record's end time
      next_record.setStart(new_record.end)
      
      # the new record *SHIFTS* the next record forward to match its end time
      # visually: [START]~new~[END]   [START --> MODIFIED START]~next~[PENDING]
    
    ####### REQUIRED TAG IN HTML END TIME INPUT BYPASSES THIS CODE ######
    
    # FUNCTION: SETS NEW RECORD'S END TIME (REDUNDANT)
    
    # NOTE: this case seems to work, but the HTML requires the end time in this case, so this isn't currently executed
    
    # if (a next record exists) and (the new record has a pending duration)
    if new_record.duration == PENDING_CHAR:
      # set the end time of the new record to be the next record's start time
      new_record.setEnd(next_record.start)
      
      #######
  
  #######################################################
  
  # after ensuring the previous record's end time is set
  
  if prev_record:
    
    # calculate the previous record's duration using its start and end times
    prev_record.duration = getDuration(prev_record.start, prev_record.end)
    
    # update the record in the list
    records[index - 1] = prev_record
    
    # calculate overlap : new_start - prev_end : if overlap => negative duration
    # if the new start time is less than the previous end time: adjustment needed
    overlap = getDuration(prev_record.end, new_record.start)
    
    # if there was overlap
    if overlap < 0:
      # modify the prev_end time by subtracting the overlap duration
      prev_record.modifyEnd(overlap)
  
  #######################################################
  
  # if the next record exists, the new record has been ensured to be complete (can't have two pending records)
  
  if next_record:
    
    # calculate the new record's duration using its start and end times
    new_record.duration = getDuration(new_record.start, new_record.end)
    
    # update the record in the list
    records[index] = new_record
    
    # calculate overlap : next_start - new_end : if overlap => negative duration
    # if the next record's start is less than the new record's end: adjustment needed
    overlap = getDuration(new_record.end, next_record.start)
    
    # if there was overlap
    if overlap < 0:
      # modify next_start time by subtracting overlap duration
      next_record.modifyStart(-overlap)


### CHECKS IF A NEW RECORD IS TEMPORALLY SOUND ITSELF AND IN RELATION TO ADJACENT RECORDS ##############
def checkIfValid(records, record, index):
  ################################################
  
  # get records to check positioning of the new record
  prev = next = None
  
  # for checking the relationship with the adjacent records
  prevValid = nextValid = False
  
  ################################################
  ################################################
  
  if records:
    prev = getPrevRecord(records, index)
    next = getNextRecord(records, index)
  
  ################################################
  
  # either there is no previous record or the new start is greater than the previous start
  if (not prev) or (prev and (record.start > prev.start)):
    prevValid = True
  
  # either there is no next record or the new end is less than the next end
  if (not next) or (next and (record.end < next.end)):
    nextValid = True
  
  ################################################
  
  # END != PENDING
  if record.end != PENDING_CHAR:
    return record.start < record.end
  
  ################################################
  ################################################
  
  # END == PENDING
  elif next:
    # cannot have a pending end time within the list (must be at the end)
    return False
  
  ################################################
  
  else:
    # can't compare pending end time to record.start
    # so return whether or not both adjacency checks were passed
    return prevValid and nextValid
    
    ################################################
    ################################################


### EITHER RETURNS A VALIDATED DATETIME.DATE OBJECT BASED ON SUPPLIED DATE, OR RETURNS THE CURRENT DATE

def validateDate(d):
  # if datetime.date
  if type(d) is dt.date:
    return d
  
  # if str and not ''
  elif (type(d) is str) and d:
    try:
      # could throw ValueError
      # could throw a TypeError
      year, month, day = [int(x) for x in d.split("-")]
      
      return dt.date(year, month, day)
    
    except (ValueError, TypeError):
      # if invalid date supplied, return current date
      return dt.date.today()
  
  else:
    return dt.date.today()
    
    ########################################################################################################
    ### RECORD METHODS END #################################################################################
    
    #
    #
    
    ########################################################################################################
    ########################################################################################################
    #### STATIC METHODS END ################################################################################
    
    #
    #
    #
    #
    #
    #
    #
    #