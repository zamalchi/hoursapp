#!/usr/bin/env python
"""
Module for manipulating records of hours worked
  
Record
  Object that simulates a single record of work done
RecordMalFormedException
  Wrapped exception used and required, internally, by the Record class

After importing, set (optional):
  ROOT_DIR - default: '.'
  HOURS_DIR - default: './hours'
"""

### IMPORTS ############################################################################################

import calendar
import datetime as dt
import os

### RUNNING AS MAIN ####################################################################################

if __name__ == "__main__":
  print("Import class.")
  print("Exiting...")
  exit(1)

### MODULE VARS ########################################################################################

ROOT_DIR = "."
""" Allows the module to reference the root project directory
Recommended to manually set after importing """

HOURS_DIR = os.path.join(ROOT_DIR, "hours")
""" Where the module will save recorded-hours files
Recommended to manually set after importing """

PENDING_CHAR = "***"
""" Used as a placeholder for the end time and duration in a record
It is replaced (within the record) when the next record is created or when the end time is supplied """

PERIOD_END = 25
""" Day of the month on which the pay period ends """

########################################################################################################
#### CLASS DEF START ###################################################################################
########################################################################################################

class Record:
  """
  Object that simulates a single record of work done
  """
  
  def __init__(self, string):
    """ PUBLIC - Default Constructor
    Parses a properly-formatted string into a Record object
    :param string: <str> to parse - must be in correct format
    
    Format: "name|startDate start|endDate end|duration|label|billable|emergency|notes(|durationLocked)"
    Example: "test|2017-01-12 12:00|2017-01-12 16:30|4.5|TS|N|N|test0|False"
    
    Optional field 'durationLocked': will default to False
    Invalid string: throws a RecordMalformedException
    """
    try:
      #######################################################
  
      elems = string.split('|')
      start_DT = elems[1].split(" ")
      end_DT = elems[2].split(" ")
  
      #######################################################
  
      self.name = elems[0]
      """ <str> : username of the person working """
  
      self.date = validateDate(start_DT[0])
      """ <datetime.date> : date of work done """
  
      #######################################################
  
      self.fstart = start_DT[1]
      """ <str> : "HH:MM"-formatted start time for work done """
  
      self.start = parseTime(self.fstart)
      """ <str> : "HHMM"-formatted start time for work done """
  
      self.fend = end_DT[1]
      """ <str> : "HH:MM"-formatted end time for work done """
  
      self.end = parseTime(self.fend)
      """ <str> : "HHMM"-formatted end time for work done """
  
      #######################################################
  
      self.duration = elems[3]
      """ <str> : number of hours, in decimal, of work done """
  
      self.label = elems[4]
      """ <str> : label of project/entity for which work was done """
  
      self.billable = elems[5]
      """ <str/char> : 'Y'|'N' flag for whether work is billable """
  
      self.emergency = elems[6]
      """ <str/char> : 'Y'|'N' flag for whether work was emergent """
  
      self.notes = elems[7]
      """ <str> : description of what work was done """
  
      #######################################################
  
      self.durationLocked = False
      """ <bool> : if True, prevents future changes to the duration of the work done
      This is set to True by manually entering a duration for the work
      It is only visible in the Record object or in the hidden version of the log file
      """

      if (len(elems) == 9) and (elems[8] == "True"):
        self.durationLocked = True
      
      #######################################################

    except Exception:
      raise RecordMalformedException("ERROR - INVALID __init__ STRING : " + string)
  
  
  ### DURATION METHODS ###################################################################################
  ########################################################################################################
  
  def setDuration(self, duration):
    """
    Sets the duration to a supplied value
    :param duration: <float|(str)> new duration value (casts to float)
    """
    # TODO: decide if I want to change this to @duration.setter and add @property functions
    self.duration = float(duration)
  
  
  def calculateAndSetDuration(self):
    """
    Calculates the duration from own start and end times, then sets the duration
    """
    # TODO: decide if I want to change up getDuration (module func) in relation to setDuration (class func)
    self.setDuration(getDuration(self.start, self.end))
  
  
  def modifyDuration(self, amount):
    """
    Modifies the existing duration by a specified amount, iff not durationLocked
    :param amount: <float|(str)> number of hours, in decimal, by which to shift the duration (casts to float)
    """
    if not self.durationLocked:
      # get the duration
      d = float(self.duration)
      
      # add the amount (supplying a negative amount will subtract from the duration)
      d += float(amount)
      
      # set modified duration
      self.duration = str(d)
  
    
  ### TIME METHODS #######################################################################################
  ########################################################################################################
  
  def isPending(self):
    """
    True iff an end time has not been supplied
    If pending, self.end and self.duration have been set as PENDING_CHAR
    :return: <bool> pending status of record
    """
    return self.end == PENDING_CHAR

  
  def setStart(self, time):
    """
    Sets the start time while ensuring correct parsing/formatting
    :param time: <str> value to set as start time
    """
    time = str(time)
    
    # parse time for start field (format "HHMM")
    parsed = parseTime(time)
    
    # format parsed time for fstart (formatted start) field (format "HH:MM")
    formatted = formatTime(parsed)
    
    self.start = parsed
    self.fstart = formatted
  
  
  def setEnd(self, time):
    """
    Sets the end time while ensuring correct parsing/formatting
    :param time: <str> value to set as start time
    """
    time = str(time)

    # parse time for start field (format "HHMM")
    parsed = parseTime(time)

    # format parsed time for fstart (formatted start) field (format "HH:MM")
    formatted = formatTime(parsed)
    
    self.end = parsed
    self.fend = formatted
  
  
  def modifyStart(self, amount):
    """
    Modify the start time and duration by the supplied amount
    :param amount: <float|(str)> number of hours, in decimal, by which to shift the start and duration (casts to float)
    """
    # get start time in minutes
    start = convertTimeToMinutes(self.start)
    
    # convert amount into minutes and add to start time
    newStart = float(start) + (float(amount) * 60)
    
    # TODO: double check that the int casting is needed
    # set start to newStart value (converted back into a string)
    self.setStart(convertMinutesToTime(int(newStart)))
    
    # modify the duration by subtracting the amount added to the start time
    self.modifyDuration(-float(amount))
  
  
  def modifyEnd(self, amount):
    """
    Modify the end time and duration by the supplied amount
    :param amount: <float|(str)> number of hours, in decimal, by which to shift the end and duration (casts to float)
    """
    # get the end time in minutes
    end = convertTimeToMinutes(self.end)
    
    # convert amount into minutes and add to end time
    newEnd = float(end) + (float(amount) * 60)
    
    # TODO: double check that the int casting is needed
    # set end to newEnd value (converted back into a string)
    self.setEnd(convertMinutesToTime(int(newEnd)))
    
    # modify the duration by adding the amount added to the end time
    self.modifyDuration(float(amount))
  
  
  def modifyTimes(self, amount):
    """
    Modify both the start and end times by the supplied amount
    This shifts the entire time frame and does *not* change the duration
    :param amount: <float|(str)> number of hours, in decimal, by which to shift the start and end times(casts to float)
    """
    self.modifyStart(amount)
    self.modifyEnd(amount)
  
  
  ### TO_STRING METHODS ##################################################################################
  ########################################################################################################
  
  def __str__(self):
    """ Default to_string - called via str(record)
    This format contains durationLocked and is intended for writing to a hidden file
    :return: <str> formatted record data
    """
    return "{emailFormat}|{durationLocked}".format(
      emailFormat=self.emailFormat(), durationLocked=self.durationLocked)

  
  def emailFormat(self):
    """ Secondary to_string
    This format doesn't contain durationLocked and is intended for emailing/submitting to payroll
    :return: <str> formatted record data
    """
    return "{name}|{startDate} {start}|{endDate} {end}|{duration}|{label}|{billable}|{emergency}|{notes}".format(
      name=self.name,
      startDate=self.date, start=self.fstart,
      endDate=self.date, end=self.fend,
      duration=self.duration,
      label=self.label,
      billable=self.billable, emergency=self.emergency,
      notes=self.notes)


########################################################################################################
#### CLASS DEF END #####################################################################################
########################################################################################################

#

########################################################################################################
#### HELPER CLASS DEF START ############################################################################
########################################################################################################

class RecordMalformedException(Exception):
  """
  Wrapped exception used and required, internally, by the Record class
  """
  pass

########################################################################################################
#### HELPER CLASS DEF END ##############################################################################
########################################################################################################

#
#
#
#
#
#
#
#
#

########################################################################################################
#### MODULE METHODS START ##############################################################################
########################################################################################################


### GENERATOR METHODS ##################################################################################
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


### IO METHODS #########################################################################################
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


### SUBTOTAL & TOTAL METHODS ###########################################################################
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
  # likewise, the day value is not needed, so hard-coding as 1 prevents day-out-of-range error
  date = dt.date(date.year, month_int, 1)
  
  # get the str name for the month
  return date.strftime("%b")


def countSubtotal(records):
  """ PRIVATE
  Sums the durations of a list of recorder.Record objects
  Will parse record strings into objects
  :param records: <list[recorder.Record|str]>
  :return: <float> subtotal
  """
  subtotal = 0.0
  
  for each in records:
    
    if type(each) is str:
      subtotal += float(Record(each).duration)
    
    elif isRecord(each) and not each.isPending():
      subtotal += float(each.duration)
  
  return subtotal


### PARSING METHODS ####################################################################################
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
  date = str(validateDate(request.get_cookie("hours-app-date")))
  
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


### TIME METHODS #######################################################################################
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


def convertTimeToMinutes(t):
  """
  Converts a time string into an int representing the number of minutes since 00:00
  :param t: <str|(int)> time to convert to minutes (will accept but simply return an int)
  :return: <int> number of minutes since 00:00; 0 if the end time is pending
  """
  # checks for not present time
  if t == PENDING_CHAR:
    #TODO: ensure that changing this from `return None` to `return 0` doesn't break anything
    return 0
  
  # if it is an int, it has already been processed, so return
  # ex: called from getDuration()
  if type(t) is int:
    return t
  
  # ensures it is parsed to "HHMM"
  p = parseTime(t)
  
  # returns number of minutes (HH*60 + MM)
  return (int(p[:2]) * 60) + int(p[2:])


def convertMinutesToTime(minutes):
  """
  Converts a number of minutes since 00:00 into a time string
  :param minutes: <int|(str)> number of minutes (will cast to int)
  :return: <str> time string in the format "HHMM"
  """
  # ensures int type
  i = int(minutes)
  
  # gets hours through integer division
  hours = str(i / 60).zfill(2)
  
  # gets minutes through modulus
  minutes = str(i % 60).zfill(2)
  
  # return ("HHMM")
  return hours + minutes


def getDuration(start, end):
  """
  Calculate a duration using start and end times
  :param start: <str> starting time string
  :param end: <str> ending time string
  :return: <float or 0.0> number of hours between start and end
  """
  # get number of minutes from start time
  start = convertTimeToMinutes(start)
  
  # get number of minutes from end time
  end = convertTimeToMinutes(end)
  
  if start and end:
    # return number of hours as float (x.xx)
    return float((end - start) / float(60))
  
  # if end == PENDING_CHAR
  return 0.0


# TODO: decide whether to keep this and figure out how overloading is done best in Python
# def getDuration(record):
#   """
#   Calculate a duration from a record's data
#   :param record: <recorder.Record>
#   :return: <float> either the record's duration or the value calculated from its start and end times
#   """
#
#   if record.duration:
#     return float(record.duration)
#
#   start = convertTimeToMinutes(record.start)
#   end = convertTimeToMinutes(record.end)
#
#   return getDuration(start, end)


def roundTime(t):
  """
  Rounds the passed in time to the nearest 15-minute mark
  :param t: <str|datetime.time> time to round
  :return: <str> rounded time in the format "HHMM"
  """
  
  if type(t) is dt.time:
    
    hours = t.hour
    minutes = t.minute
  
  else:
    
    t = formatTime(t)
    hours, minutes = (int(i) for i in t.split(':'))
  
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
  return "{HH}{MM}".format(HH=str(hours).zfill(2), MM=str(quarters * 15).zfill(2))


def getCurrentRoundedTime():
  """
  Rounds the current time to the nearest 15-minute mark
  :return: <str> rounded time in the format "HHMM"
  """
  # get current time ; round it to 15-minute mark
  return roundTime(dt.datetime.now().time())


### RECORD METHODS #####################################################################################
########################################################################################################

def getPrevRecord(records, index):
  """
  Attempts to get the chronologically previous record
  :param records: <list[recorder.Record|(str)]> list of records (type doesn't matter)
  :param index: <int> index value of starting record (index - 1 should be the previous record)
  :return: <recorder.Record|(str) or None> previous record from list (returns whatever the list element type is)
  """
  try:
    # if the previous index is a valid index
    if index - 1 >= 0:
      # return the previous record
      return records[index - 1]
  
  except IndexError:
    pass
  
  # if returning the prev record was unsuccessful, return None
  return None


def getNextRecord(records, index):
  """
  Attempts to get the chronologically next record
  :param records: <list[recorder.Record|(str)]> list of records (type doesn't matter)
  :param index: <int> index value of starting record (index + 1 should be the next record)
  :return: <recorder.Record|(str) or None> next record from list (returns whatever the list element type is)
  """
  try:
    # if the next index is a valid index
    if index + 1 < len(records):
      # return the next record
      return records[index + 1]
  
  except IndexError:
    pass
  
  # if returning the prev record was unsuccessful, return None
  return None


def adjustAdjacentRecords(records, index):
  """
  Checks if a specific record overlaps with adjacent records and adjusts adjacent start/end times accordingly
  :param records: <list[recorder.Record]> list of records
  :param index: <int> index of the record to use as the base for adjusting
  """
  # if the records list is empty, print error statement and return from function
  # TODO: decide if this print statement is ok or what to do with it
  if not records:
    print("ERROR: empty records list passed into adjustAdjacentRecords()")
    return
  
  #######################################################
  
  # get the newly-inserted / base record
  base_record = records[index]
  
  # get the previous record if it exists
  prev_record = getPrevRecord(records, index)
  
  # get the next record if it exists
  next_record = getNextRecord(records, index)
  
  #######################################################
  """ FUNCTION: ADJUSTS THE PREVIOUS RECORD'S END TIME
  the base record *FINISHES* the previous record
  visually:
    previous: [START][PENDING --> END]
    base: [START][PENDING|END]
  """
  if prev_record and isRecord(prev_record):
    # if the previous record's end time has not been supplied
    if prev_record.duration == PENDING_CHAR:
      # set the previous record's end time to be the new record's start time
      prev_record.setEnd(base_record.start)
      
  #######################################################
  """ FUNCTION: SHIFTS NEXT RECORD'S START TIME (IF PARTIAL RECORD)
  the base record *SHIFTS* the next record forward to match its end time
  visually:
    base: [START][END]
    next: [START --> MODIFIED START][PENDING|END]
  """
  if next_record and isRecord(next_record):
    # if (the next record's end time has not been supplied) and (the base record has an end time)
    if (next_record.duration == PENDING_CHAR) and (base_record.end != PENDING_CHAR):
      # supply the next record's start time using the new record's end time
      next_record.setStart(base_record.end)
      
     
    # TODO: FIX THE REST OF THIS METHOD
    # TODO: make sure for all : isRecord(r)
    """
    I don't think I changed any logic, but I need to decide how this will work
      specifically, if two records in a row can have pending end times
    Pseudocode out the steps
      1)  set previous end time to base start time
      2)  if next is pending and base isn't: set next start time to base end time
      3?) if base is pending: set base end to next start
      4?) ?
      5?) ?
    Create an as-simple-as-possible overview of the method at the top
    """
    ####### REQUIRED TAG IN HTML END TIME INPUT BYPASSES THIS CODE ######
    
    # FUNCTION: SETS NEW RECORD'S END TIME (REDUNDANT)
    
    # NOTE: this case seems to work, but the HTML requires the end time in this case, so this isn't currently executed
    
    """
    if the next record doesn't have a supplied end time, the new record MUST have an end time (required by HTML input)
    """
    # if (a next record exists) and (the new record has a pending duration)
    if base_record.duration == PENDING_CHAR:
      # set the end time of the new record to be the next record's start time
      base_record.setEnd(next_record.start)
      
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
    overlap = getDuration(prev_record.end, base_record.start)
    
    # if there was overlap
    if overlap < 0:
      # modify the prev_end time by subtracting the overlap duration
      prev_record.modifyEnd(overlap)
  
  #######################################################
  
  # if the next record exists, the new record has been ensured to be complete (can't have two pending records)
  
  if next_record:
    
    # calculate the new record's duration using its start and end times
    base_record.duration = getDuration(base_record.start, base_record.end)
    
    # update the record in the list
    records[index] = base_record
    
    # calculate overlap : next_start - new_end : if overlap => negative duration
    # if the next record's start is less than the new record's end: adjustment needed
    overlap = getDuration(base_record.end, next_record.start)
    
    # if there was overlap
    if overlap < 0:
      # modify next_start time by subtracting overlap duration
      next_record.modifyStart(-overlap)


def checkIfValid(records, record, index):
  """
  Checks if a new record is temporally sound with itself and in relation to adjacent records
    i.e. checks that a record's start comes before its end
      and checks that a record doesn't overlap an entire adjacent record
  :param records: <list[recorder.Record]> list of records not including the one passed in
  :param record: <recorder.Record> single record to check if it fits validly in the record list
  :param index: <int> index where the new record is trying to be placed
  :return: <bool> returns True only if record fits between (existing) adjacent records
  """
  # get records to check positioning of the new record
  prevRecord = nextRecord = None
  
  # for checking the relationship with self and the adjacent records
  prevValid = nextValid = selfValid = False
  
  ################################################
  
  if not record or not isRecord(record):
    return False
  
  if records:
    prevRecord = getPrevRecord(records, index)
    nextRecord = getNextRecord(records, index)
  
  ################################################
  
  # either there is no previous record
  if not prevRecord:
    prevValid = True
    
  # or the new start is greater than the previous start
  elif isRecord(prevRecord):
    prevValid = record.start > prevRecord.start
  
  ################################################

  # either there is no nextRecord record
  if not nextRecord:
    nextValid = True
    
  # or the new end is less than the nextRecord end
  # (implied) if record is pending, the nextRecord record must not exist
  elif not record.isPending() and isRecord(nextRecord):
    nextValid = record.end < nextRecord.end
  
  ################################################
  
  # if a record is pending, it is valid with itself
  if record.isPending():
    selfValid = True
  
  # else, the start must come before the end
  else:
    selfValid = record.start < record.end

  ################################################

  # true iff all checks are passed
  return prevValid and nextValid and selfValid
    
  # TODO: maybe return a second var that's a list of reasons why the record was invalid


def validateDate(d):
  """
  Normalizes dates as datetime.date objects
  :param d: <str|(datetime.date)> to convert to datetime.date (will return unchanged a passed-in datetime.date object)
  :return: <datetime.date> converted date if supplied else the current date
  """
  # TODO: does this belong in this section? Helper methods section?
  # if datetime.date
  if type(d) is dt.date:
    return d
  
  # if str and not ''
  elif (type(d) is str) and d:
    try:
      # could throw ValueError
      # could throw a TypeError
      year, month, day = [int(x) for x in d.split("-")]
    
      return dt.date(year=year, month=month, day=day)
  
    except (ValueError, TypeError):
      pass

  # if invalid date supplied, return current date
  return dt.date.today()


def isRecord(r):
  return r.__class__.__name__ == "Record"

########################################################################################################
########################################################################################################
#### MODULE METHODS END ################################################################################
