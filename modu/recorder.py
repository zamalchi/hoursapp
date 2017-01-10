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

PERIOD_END = 25


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
    new = float(start) + (float(amount) * 60)
    
    # set start to new value (converted back into a string)
    self.setStart(getTimeFromMin(int(new)))
    
    # modify the duration by subtracting the amount added to the start time
    self.modifyDuration(-float(amount))
  
  ### MODIFY END TIME AND DURATION BY A SUPPLIED AMOUNT ##################################################
  def modifyEnd(self, amount):
    
    # get the end time in minutes
    end = getMinFromTime(self.end)
    
    # convert amount into minutes and add to end time
    new = float(end) + (float(amount) * 60)
    
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

#### MODULE METHODS START ##############################################################################
########################################################################################################
########################################################################################################

#
#

### GENERATOR METHODS START ############################################################################
########################################################################################################

def generateFileName(name, date):
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


def generateHiddenFileName(name, date):
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


########################################################################################################
### GENERATOR METHODS END ##############################################################################

#
#

### IO METHODS START ###################################################################################
########################################################################################################

def readRecords(name, date):
  """
  Attempts to read records from a file corresponding to the name and date supplied
  :param name: <str> name of user
  :param date: <str|datetime.date> date of records
  :return: <list[str] or []> unparsed list of records as strings
  """
  
  # uses hidden version of the file, since it contains extra info (durationLocked)
  fileName = generateHiddenFileName(name, date)
  
  if os.path.exists(fileName):
    try:
      with open(fileName, 'r') as f:
        records = f.read().split('\n')
        return records
    
    except IOError:
      pass
  
  return []


def writeRecords(name, date, records):
  """
  Writes a list of records to a file with a name generated from name and date
  :param name: <str> name of user
  :param date: <str|datetime.date> date of records
  :param records: <list[recorder.Record]> records to write to file
  """
  
  fileName = generateFileName(name, date)
  
  # used to store extra information (durationLocked)
  hiddenFileName = generateHiddenFileName(name, date)
  
  # will contain joined records and be written to files
  res, hiddenRes = "", ""
  
  #######################################################
  
  # join the records into strings
  for r in records:
    res += r.emailFormat() + "\n"
    hiddenRes += str(r) + "\n"
  
  #######################################################
  
  # write strings to files
  try:
    with open(fileName, 'w') as f:
      f.write(res)
    
    with open(hiddenFileName, 'w') as f:
      f.write(hiddenRes)
  
  except IOError:
    pass


def deleteRecords(name, date):
  """
  Uses a system call to delete the normal and hidden files corresponding to a name and date
  :param name: <str> name of user
  :param date: <str|datetime.date> date of records
  """
  
  fileName = generateFileName(name, date)
  
  # used to store extra information (durationLocked)
  hiddenFileName = generateHiddenFileName(name, date)
  
  # system calls to delete both normal and hidden file
  os.system("rm -f {}".format(fileName))
  os.system("rm -f {}".format(hiddenFileName))


########################################################################################################
### IO METHODS END #####################################################################################

#
#

### SUBTOTAL & TOTAL METHODS START #####################################################################
########################################################################################################

def getSubtotalForDay(name, date):
  """ PUBLIC
  Adds up the hours worked on a specific day by a user
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date of records
  :return: <float> total hours worked during the day
  """
  records = parseRecordsFromFile(name, validateDate(date))
  subtotal = countSubtotal(records)
  return subtotal


def getTotalForPayPeriod(name, date):
  """ PUBLIC
  Adds up subtotals of each record in the pay period (adjusted for the 25th of the month)
  :param name: <str> name of user
  :param date: <str>|<datetime.date> date within the pay period
  :return: <float> total hours worked during the pay period
  """
  
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
  
  # these statements reference beforeCutoff<Month,Year> and not date to consolidate the following logic
  afterCutoffMonth = beforeCutoffMonth + 1 if beforeCutoffMonth < 12 else 1
  afterCutoffYear = beforeCutoffYear + 1 if afterCutoffMonth == 1 else beforeCutoffYear
  
  # GET TOTAL FOR DAYS IN RANGE : 26th - LAST DAY OF MONTH
  for day in range(PERIOD_END + 1, beforeCutoffMonthEnd + 1):
    beforeCutoffDate = dt.date(year=beforeCutoffYear, month=beforeCutoffMonth, day=day)
    total += getSubtotalForDay(name, beforeCutoffDate)
    # print("DATE : {} -- SUBTOTAL : {} -- TOTAL : {}".format(beforeCutoffDate, getSubtotalForDay(name, beforeCutoffDate), total))
  
  # GET TOTAL FOR DAYS IN RANGE : 1st - 25th
  for day in range(1, PERIOD_END + 1):
    afterCutoffDate = dt.date(year=afterCutoffYear, month=afterCutoffMonth, day=day)
    total += getSubtotalForDay(name, afterCutoffDate)
    # print("DATE : {} -- SUBTOTAL : {} -- TOTAL : {}".format(afterCutoffDate, getSubtotalForDay(name, afterCutoffDate), total))
  
  return total


def getPayPeriodMonth(date):
  """ PUBLIC
  Produces the datetime.date string representation of the pay period month
  :param date: <str|datetime.date> date within the pay period
  :return: <str> corresponding to the pay period month (ex: "2016-12-26" --> "Jan")
  """
  date = validateDate(date)
  
  if date.day <= PERIOD_END:
    month_int = date.month
  else:
    # if past the cutoff, increment the month and wrap around if necessary
    month_int = date.month + 1 if date.month < 12 else 1
  
  # correcting for year is not necessary because only the month string is returned
  date = dt.date(date.year, month_int, date.day)
  
  # get the str name for the month
  return date.strftime("%b")


def countSubtotal(records):
  """ PRIVATE
  Sums the durations of a list of recorder.Record objects
    will parse a list of record strings into objects
  :param records: <list[recorder.Record|str]>
  :return: <float> subtotal
  """
  subtotal = 0.0
  
  for r in records:
    
    # if it is a valid duration
    if r.duration != PENDING_CHAR:
      
      # if the record is a string, make it an object first
      if type(r) is str:
        subtotal += float(Record(r).duration)
      
      # else just add its duration
      else:
        subtotal += float(r.duration)
  
  return subtotal

########################################################################################################
### SUBTOTAL & TOTAL METHODS END #######################################################################

#
#

### PARSING METHODS START ##############################################################################
########################################################################################################

def parseRecords(raw_records):
  """ PRIVATE
  Parses string records into recorder.Record objects
  :param raw_records: <list[str]>
  :return: <list[recorder.Record]>
  """
  # filter out empty records
  records = filter(None, raw_records)
  
  # return list mapped to Record objects
  return [Record(r) for r in records]


def parseRecordsFromFile(name, date):
  """ PUBLIC
  Reads records from a file and parses the strings into a list of recorder.Record objects
  :param name: <str> name of user
  :param date: <str|datetime.date> date of records
  :return: <list[recorder.Record]> parsed records for the date and user
  """
  # read in records
  raw_records = readRecords(name, date)
  
  # return parsed Record objects
  return parseRecords(raw_records)


def parseRecordFromHTML(request):
  """ PUBLIC
  Parses the data from an HTML form into a recorder.Record object
  :param request: <bottle.request> contains HTML form data
  :return: <recorder.Record> parsed object
  """
  
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
  # filters out "|" char to not confuse the later parsing (better solution would be a check in the HTML)
  notes = request.forms.get('notes').strip().translate(None, '|')
  
  #######################################################
  
  # duration locked is only present in the hidden file, since it is extra data for each record
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
  
  # format the string that will be supplied to the Record constructor
  record_string = \
      "{name}|{startDate} {start}|{endDate} {end}|{duration}|{label}|{billable}|{emergency}|{notes}|{durationLocked}" \
      .format(
        name=name,
        startDate=date, start=start,
        endDate=date, end=end,
        duration=duration,
        label=label,
        billable=billable, emergency=emergency,
        notes=notes,
        durationLocked=durationLocked)
  
  return Record(record_string)

########################################################################################################
### PARSING METHODS END ################################################################################

#
#

### TIME METHODS START #################################################################################
########################################################################################################

def parseTime(t):
  """
  Conforms a time string to format "HHMM"
    Removes ':' and fills with leading '0'
  :param t: <str> time to parse
  :return: <str> time in format "HHMM"
  """
  
  if t:
    # return if pending
    if t == PENDING_CHAR:
      return t
    
    # removes colon and adds leading '0' if missing
    return str(t.strip()).translate(None, ':').zfill(4)
  
  # if not supplied, return empty string
  return ""


### FORMAT TIME INTO ("HH:MM") FORMAT ##################################################################

def formatTime(t):
  """
  Conforms a time string to format "HH:MM"
    calls parseTime(t) beforehand
  :param t: <str> time to format
  :return: <str> time in format "HH:MM"
  """
  # ensures time is parsed correctly
  p = parseTime(t)
  
  # adds a colon between hours and minutes
  return "{HH}:{MM}".format(HH=p[:2], MM=p[2:])

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
    #### MODULE METHODS END ################################################################################
    
    #
    #
    #
    #
    #
    #
    #
    #
