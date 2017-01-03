#!/usr/bin/env python

########################################################################################################
########################################################################################################
########################################################################################################

### IMPORTS ############################################################################################

from __future__ import print_function

import argparse
import datetime as dt
import os
import smtplib
import sys
import time

import markdown

import modu.bottle as bottle
import modu.color_printer as cp
import modu.crypto as crypto
import modu.labeler as labeler
import modu.recorder as recorder

app = bottle.Bottle()

namer = labeler.Labeler()

### ARG PARSING ########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-p', help="Port number", action="store", dest="p", required=True)
parser.add_argument('-d', help="Dev mode", action="store_true", required=False)
parser.add_argument('-r', help="Live reloading", action="store_true", required=False)

args = parser.parse_args()

# GLOBAL ENVIRONMENT VARIABLES
ENV = argparse.Namespace()
ENV.HOST = "localhost"
ENV.PORT = args.p
ENV.DEBUG = True if args.d else False
ENV.RELOAD = True if args.r else False
ENV.ROOT = os.getcwd()

### APACHE #############################################################################################

os.chdir(ENV.ROOT)
sys.path.insert(1, ENV.ROOT)

### FOR CSS READING IN TEMPLATES #######################################################################

bottle.SimpleTemplate.defaults["url"] = bottle.url

### STATIC ROUTING ########################################################################################

# CSS
@app.get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/css'))

# JAVASCRIPT
@app.get('/js/<filename:re:.*\.js>')
def javascripts(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/js'))

# IMAGES
@app.get('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/img'))

# FONTS
@app.get('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/fonts'))

### DIRECTORY ##########################################################################################

# project root and directory for saving hours information : overwrites default values in class
recorder.rootDir = ENV.ROOT
recorder.hoursDir = os.path.join(ENV.ROOT, "hours")

# if the directory doesn't exist, create it
if not os.path.exists(recorder.hoursDir):
  os.makedirs(recorder.hoursDir)
  
crypto.ROOT_DIR = ENV.ROOT

### LOGGING SERVER AND SMTP ############################################################################

LOGGING = argparse.Namespace()
LOGGING.ADDRESS_KEY = "loggingServerAddress"
LOGGING.PORT_KEY = "loggingServerPort"
LOGGING.SENDER_KEY = "sender"
LOGGING.RECEIVERS_KEY = "receivers"

LOGGING.SETTINGS_FILE = os.path.join(ENV.ROOT, "config/settings")
LOGGING.SETTINGS_DICT = {}

if os.path.exists(LOGGING.SETTINGS_FILE):
  with open(LOGGING.SETTINGS_FILE) as f:
    rawSettings = filter(None, f.read().split("\n"))

    for each in rawSettings:
      key, val = each.split("=")
      LOGGING.SETTINGS_DICT[key] = val

elif ENV.DEBUG:
  cp.printWarn("`config/settings` file not found. Some features may not work.")

ENV.LOGGING_SERVER_ADDRESS = LOGGING.SETTINGS_DICT.get(LOGGING.ADDRESS_KEY, "")
ENV.LOGGING_SERVER_PORT = LOGGING.SETTINGS_DICT.get(LOGGING.PORT_KEY, "")
    
ENV.SENDER = LOGGING.SETTINGS_DICT.get(LOGGING.SENDER_KEY, "root")
ENV.RECEIVERS = filter(None, list(LOGGING.SETTINGS_DICT.get(LOGGING.RECEIVERS_KEY, "").split(","))) or []


### LABELS #############################################################################################

labelsFile = os.path.join(ENV.ROOT, "config/labels.txt")
ENV.LABELS = []

if os.path.exists(labelsFile):
  with open(labelsFile, 'r') as f:
    
    # parses into list and filters out any empty lines (ex. trailing \n)
    ENV.LABELS = filter(None, f.read().split("\n"))
  
elif ENV.DEBUG:
  cp.printWarn("`config/labels.txt` file not found. Labels will not be populated.")

### COOKIE GETTERS/SETTERS #############################################################################

### NAME ########################################################
def getNameCookie(req):
  return req.get_cookie("name") or ""

def setNameCookie(res, name):
  res.set_cookie("name", name)

### DATE ########################################################
def getDateCookie(req):
  return recorder.validateDate(req.get_cookie("date") or dt.date.today())

def setDateCookie(res, date):
  res.set_cookie("date", str(recorder.validateDate(date)))

### CONSOLIDATED ################################################
def getCookies(req):
  return getNameCookie(req), getDateCookie(req)

def setCookies(res, name, date):
  setNameCookie(res, name)
  setDateCookie(res, date)

### ANCHOR ######################################################
def getAnchorCookie(req):
  return req.get_cookie("anchor") or "-1"

def setAnchorCookie(res, anchor):
  res.set_cookie("anchor", str(anchor))

def deleteAnchorCookie(res):
  res.delete_cookie("anchor")

### NOTES #######################################################

def getNotesCookie(req):
  return req.get_cookie("notes") or ""

def setNotesCookie(res, notes):
  res.set_cookie("notes", notes)

def deleteNotesCookie(res):
  res.delete_cookie("notes")

########################################################################################################
########################################################################################################
########################################################################################################

#
#
#
#
#
#
#
#

########################################################################################################
######################################### HOURS FORM START #############################################
########################################################################################################


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

@app.get('/')
@app.get('/hours')
def hours():
  
  #######################################################
  
  msg = ""
  try:
    msg = crypto.getDecodedString(bottle.request.query['msg'])
  except KeyError:
    pass
  
  # get name and date cookies
  name, date = getCookies(bottle.request)
  
  # get anchor cookie in case record has been just edited
  anchor = getAnchorCookie(bottle.request)
  
  # set anchor cookie to null after getting it
  deleteAnchorCookie(bottle.response)
  
  notes = getNotesCookie(bottle.request)
  
  deleteNotesCookie(bottle.response)
  
  # get the month to use for the monthly subtotal
  month = date.month
  
  subtotal = recorder.readSubtotal(name, date)
  #######################################################
  
  # try to open file with user's name and retrieve data
  # for each record, create a new Record object and add to list to pass to template
  # list of records as Record obj
  records = recorder.parseRecordsFromFile(name, date)
  
  #######################################################
  
  return bottle.template('hours',
                         name=name, date=date,
                         records=records, labels=ENV.LABELS,
                         month=month, subtotal=subtotal,
                         anchor=anchor, notes=notes,
                         sender=ENV.SENDER, receivers=ENV.RECEIVERS,
                         loggingServerAddress=ENV.LOGGING_SERVER_ADDRESS, loggingServerPort=ENV.LOGGING_SERVER_PORT,
                         msg=msg)


########################################################################################################
########################################################################################################
########################################################################################################

@app.post('/hours')
def hours_post():
  #######################################################
  
  # name of user
  name = bottle.request.forms.get(namer.name()).strip()
  
  # date : either picked by user or default today
  date = getDateCookie(bottle.request)
  
  # index for inserting new Record into the list of records
  index = int(bottle.request.forms.get(namer.insert()))
  
  #######################################################
  
  # parses form data and returns a Record obj
  new_record = recorder.getRecordFromHTML(bottle.request)
  
  #######################################################
  
  # reads and parses Records on file
  records = recorder.parseRecordsFromFile(name, date)
  
  # count current subtotal for ONLY the day's records
  current_local_subtotal = recorder.countSubtotal(records)
  
  #######################################################
  
  # if the cookie is set, the user has pulled any existing files
  # if there are no existing files, the cookie will be null
  records_pulled = getNameCookie(bottle.request)
  
  # checks if new_record.start < new_record.end
  # and that new_record doesn't exceed the outer limits of adjacent records
  if recorder.checkIfValid(records, new_record, index):
    
    if records and not records_pulled:
      # append to the end of unpulled existing records
      # prevents adding to the beginning of an unexpected list
      records.append(new_record)
    else:
      # insert new record at index provided from template form
      records.insert(index, new_record)
      
      # adjust timings of adjacent records in case of overlap
      recorder.adjustAdjacentRecords(records, index)
      
      # after adjusting the durations, recount total duration for the day
      new_local_subtotal = recorder.countSubtotal(records)
      
      # add the difference in summed durations back to the file
      # when inserting between two records (whose durations are not locked)
      # (i.e. splicing a record in), the subtotal should not change
      recorder.addToSubtotal(name, date, (new_local_subtotal - current_local_subtotal))
    
    #######################################################
    
    # write back updated list
      recorder.writeRecords(name, date, records)
    
    # after posting a new record, delete the anchor cookie to reset it
    deleteAnchorCookie(bottle.response)
    
    deleteNotesCookie(bottle.response)
  
  else:
    
    setNotesCookie(bottle.response, new_record.notes)
  
  #######################################################
  
  # set name cookie with most recently used name (for insurance mostly)
  setNameCookie(bottle.response, name)
  
  #######################################################
  
  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


########################################################################################################
######################################## HOURS FORM END ################################################
########################################################################################################

#
#
#
#
#
#
#
#

########################################################################################################
##################################### MISC ROUTES START ################################################
########################################################################################################


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

@app.post('/setCookies')
def set_cookies():
  #######################################################
  
  # get name of user provided in specified field
  name = bottle.request.forms.get("setName") or ""
  
  # get date: either set manually or defaults to current day
  date = recorder.validateDate(bottle.request.forms.get("setDate") or dt.date.today())
  
  #######################################################
  
  # set name and date cookie
  setCookies(bottle.response, name, date)
  
  #######################################################
  
  # redirect to /hours to read file
  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### deletes records of current user
@app.post('/delete')
def delete_records():
  #######################################################
  
  # get name and date cookies
  name, date = getCookies(bottle.request)
  
  # sets flag based on user's confirmation / denial from popup alert
  deleteConfirm = bottle.request.forms.get("deleteConfirm")
  
  #######################################################
  
  if (deleteConfirm == "true") and name:
    # get records
    records = recorder.parseRecordsFromFile(name, date)
    
    # get summed duration of records
    summed_subtotal = recorder.countSubtotal(records)
    
    # subtract that amount from the subtotal on file
    recorder.subtractFromSubtotal(name, date, summed_subtotal)
    
    # delete both of the user's record files
    recorder.deleteRecords(name, date)
  
  #######################################################
  
  # redirect back to hours page
  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### deletes one record from those currently displayed
@app.post('/deleteOne')
def delete_single_record():
  #######################################################
  
  # get index based on which delete button was clicked / which form was submitted
  index = int(bottle.request.forms.get('index'))
  
  # get name and date cookies
  name, date = getCookies(bottle.request)
  
  #######################################################
  
  # read and parse records from file
  records = recorder.parseRecordsFromFile(name, date)
  
  # set the notes to be in the form
  setNotesCookie(bottle.response, records[index].notes)
  
  # get the duration of the record to be deleted
  deletedRecordDuration = records[index].duration
  
  # subtract that amount from the subtotal on file
  recorder.subtractFromSubtotal(name, date, deletedRecordDuration)
  
  # delete record
  del records[index]
  
  # write back updated records
  recorder.writeRecords(name, date, records)
  
  # upon redirect, anchor to where the record was deleted
  # open that form and insert notes, etc. from the deleted record
  setAnchorCookie(bottle.response, index)
  
  #######################################################
  
  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### updates the notes field of a specific record ; triggered by the save button
@app.post('/completeNotes')
def complete_notes():
  #######################################################
  
  # get index of completed record
  index = int(bottle.request.forms.get("index"))
  
  setAnchorCookie(bottle.response, index)
  
  notes = bottle.request.forms.get("notesDisplay")
  
  name, date = getCookies(bottle.request)
  
  #######################################################
  
  if notes:
    records = recorder.parseRecordsFromFile(name, date)
    
    record = records[index]
    
    # replace <br> with " " in case of enter button being pressed
    notes = notes.replace("<br>", " ").strip()
    
    record.notes = notes
    
    records[index] = record

    recorder.writeRecords(name, date, records)
    
    # delete cookie if task completed
    deleteAnchorCookie(bottle.response)
  
  #######################################################
  
  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

@app.post('/completeEndTime')
def complete_end_time():
  #######################################################
  
  # get index of completed record
  index = int(bottle.request.forms.get('index'))
  
  setAnchorCookie(bottle.response, index)
  
  # get the submitted end time (which has already been pattern matched) OR get current rounded time
  end = recorder.parseTime(bottle.request.forms.get('completeEnd')) or recorder.getCurrentRoundedTime()
  
  # get name and date cookies
  name, date = getCookies(bottle.request)
  
  #######################################################
  
  # get records from file
  records = recorder.parseRecordsFromFile(name, date)
  
  # get particular record to complete
  record = records[index]
  
  # set the end time - THEN check if it is valid
  record.setEnd(end)
  
  # don't accept an invalid or invalidly placed record
  if not recorder.checkIfValid(records, record, index):
    bottle.redirect('hours')
  
  # else block for clarity
  else:
    if not record.durationLocked:
      
      # calculate and set duration
      record.calculateAndSetDuration()
      
      # add the new duration to the subtotal
      recorder.addToSubtotal(name, date, record.duration)
    
    # write back record
    records[index] = record
    recorder.writeRecords(name, date, records)
    
    # delete cookie if task completed
    deleteAnchorCookie(bottle.response)
  
  #######################################################

  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### returns a list (read from file) of updates
@app.get('/viewUpdates')
def view_updates():
  
  readme = updates = ""
  
  try:
    with open(os.path.join(ENV.ROOT, 'README.md'), 'r') as f:
      raw = f.read()
    
    readme = markdown.markdown(raw)
  
  except IOError:
    readme = "<h2>Readme not found.</h2>"
  
  ##############################################
  
  try:
    with open(os.path.join(ENV.ROOT, "docs/UPDATES.md"), 'r') as f:
      raw = f.read()
    
    updates = markdown.markdown(raw)
  
  except IOError:
    updates = "<h2>Updates not found.</h2>"
  
  ##############################################
  
  return bottle.template('updates', readme=readme, updates=updates)

########################################################################################################
########################################################################################################
########################################################################################################

@app.post('/toggleBillable')
def toggle_billable():
  
  name, date = getCookies(bottle.request)
  
  index = int(bottle.request.forms.get('index'))
  
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  setAnchorCookie(bottle.response, index)
  
  records = recorder.parseRecordsFromFile(name, date)
  
  record = records[index]
  
  if record.billable == "Y":
    record.billable = "N"
  else:
    record.billable = "Y"
  
  records[index] = record

  recorder.writeRecords(name, date, records)

  bottle.redirect('hours')


@app.post('/toggleEmergency')
def toggle_emergency():
  
  name, date = getCookies(bottle.request)
  
  index = int(bottle.request.forms.get('index'))
  
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  setAnchorCookie(bottle.response, index)
  
  records = recorder.parseRecordsFromFile(name, date)
  
  record = records[index]
  
  if record.emergency == "Y":
    record.emergency = "N"
  else:
    record.emergency = "Y"
  
  records[index] = record

  recorder.writeRecords(name, date, records)

  bottle.redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### emails records
@app.post('/email')
def email_records():
  
  #######################################################
  
  # get name and date cookies
  name, date = getCookies(bottle.request)
  
  # sets flag based on user's confirmation / denial from popup alert
  emailConfirm = bottle.request.forms.get("emailConfirm")
  
  #######################################################
  
  subtotal = recorder.readSubtotal(name, date) or '0.0'
  
  #######################################################
  
  curTimeShort = time.strftime("%m/%d")
  
  subject = "Hours {0} (Subtotal: {1})".format(curTimeShort, subtotal)
  body = ""
  
  #######################################################
  
  if (emailConfirm == "true") and name and ENV.SENDER and ENV.RECEIVERS:
    
    # try to open file with user's name and retrieve data
    records = recorder.parseRecordsFromFile(name, date)
    
    for record in records:
      body += record.emailFormat() + "\n"
    
    message = "Subject: %s\n\n%s" % (subject, body)
    
    try:
      mail = smtplib.SMTP("localhost")
      mail.sendmail(ENV.SENDER, ENV.RECEIVERS, message)
      mail.quit()
    
    except smtplib.SMTPException:
      pass

  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/send')
def send_records():
  
  # get cookies
  name, date = getCookies(bottle.request)
  
  confirm = bottle.request.forms.get('confirm')
  
  address = bottle.request.forms.get('address').strip() or ENV.LOGGING_SERVER_ADDRESS
  port = bottle.request.forms.get('port').strip() or ENV.LOGGING_SERVER_PORT
  
  if (confirm == "true") and name and address and port:
    
    print("SENDING TO: {0}:{1}".format(address, port))
    
    # parse records from file
    records = recorder.parseRecordsFromFile(name, date)
    
    # turn records into a string separated by \n
    string = "\n".join([r.emailFormat() for r in records])
    
    try:
      # encrypt and encode string
      records_encrypted = crypto.getEncodedString(string)
      
      addr = "/".join(bottle.request.url.split("/")[:-1]) + "/ack"
      
      # encrypts and encodes host address for rerouting back to hours
      addr_encrypted = crypto.getEncodedString(addr)
      
      # send name, date, and encoded records to receiving server
      bottle.redirect('http://{0}:{1}/receive?n={2}&d={3}&r={4}&a={5}'.format(address, port, name, date, records_encrypted, addr_encrypted))
    
    # thrown if config/crypto not found
    except TypeError:
      print("Couldn't send to server because config/crypto is missing.")

  bottle.redirect('hours')

@app.get('/ack')
def ack_sent_records():
  
  msg = bottle.request.query['msg'] or ''

  bottle.redirect('hours?msg={0}'.format(msg))

########################################################################################################
######################################  	MISC ROUTES END	   ###########################################
########################################################################################################

border = "* * * * * * * * * * * * * * * * * * * * * * * * * * * "

cp.printHeader(border)

print("APP RUNNING FROM : {project_dir}".format(project_dir=ENV.ROOT))
print("HOST ADDRESS     : {hostAddr}".format(hostAddr=ENV.HOST))
print("HOST PORT        : {hostPort}".format(hostPort=ENV.PORT))

sender = "SMTP SENDER      : {senderStr}".format(senderStr=ENV.SENDER)
receivers = "SMTP RECEIVERS   : {receiversStr}".format(receiversStr=", ".join(ENV.RECEIVERS))
debug = "DEBUG            : {devMode}".format(devMode=ENV.DEBUG)
reloader = "LIVE RELOAD      : {liveReload}".format(liveReload=ENV.RELOAD)

print(sender) if ENV.SENDER else cp.printWarn(sender)
print(receivers) if ENV.RECEIVERS else cp.printWarn(receivers)

cp.printOK(debug) if ENV.DEBUG else print(debug)
cp.printOK(reloader) if ENV.RELOAD else print(reloader)

cp.printHeader(border)

app.run(host=ENV.HOST, port=ENV.PORT, debug=ENV.DEBUG, reloader=ENV.RELOAD)

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
