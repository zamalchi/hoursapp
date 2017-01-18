#!/usr/bin/env python
"""
Bottle Python webapp for recording hours worked

TODO:
  doc this whole file
  finish working on recorder module
  git flow feature finish docs
  git flow feature start date-nav (add forward/backward buttons for navigating through dates)
  git flow release ...
  update readme and updates
"""

### IMPORTS ############################################################################################

from __future__ import print_function

## BUILTIN
import argparse
import datetime as dt
import os
import smtplib
import sys
import time

## INSTALLED
import markdown
import modu.bottle as bottle

## CUSTOM
# allows sending encrypted logs to remote server
import modu.crypto as crypto
# provides methods for printing in color
import modu.color_printer as cp
# provides names and ids for HTML elements
import modu.labeler as labeler
# module for creating, manipulating, and storing record data
import modu.recorder as recorder

## INSTANTIATION OF GLOBAL OBJECTS
# bottle app object to which the routes are attached
app = bottle.Bottle()
# provides names for extracting data from HTML requests
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
ENV.WARNINGS = []
ENV.ERRORS = []

### APACHE #############################################################################################

# changes directory to the project root
os.chdir(ENV.ROOT)
# inserts the project root into the system path
sys.path.insert(1, ENV.ROOT)

### FOR CSS READING IN TEMPLATES #######################################################################

bottle.SimpleTemplate.defaults["url"] = bottle.url

### STATIC ROUTING #####################################################################################

""" CSS """
@app.get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/css'))

""" JAVASCRIPT """
@app.get('/js/<filename:re:.*\.js>')
def javascripts(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/js'))

""" IMAGES """
@app.get('/img/<filename:re:.*\.(jpg|png|gif)>')
def images(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/img'))

""" FONTS """
@app.get('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
  return bottle.static_file(filename, root=os.path.join(ENV.ROOT, 'static/fonts'))

""" FAVICON """
@app.get('/favicon.ico')
def favicon():
  return bottle.static_file('favicon.ico', root=os.path.join(ENV.ROOT, 'static'))

### DIRECTORIES ########################################################################################

# make recorder module aware of the project root
recorder.ROOT_DIR = ENV.ROOT
# set recorder module to save hours logs in project root's subdir "hours"
recorder.HOURS_DIR = os.path.join(ENV.ROOT, "hours")

# if the hours-logging directory doesn't exist, create it
if not os.path.exists(recorder.HOURS_DIR):
  os.makedirs(recorder.HOURS_DIR)

# make the crypto module aware of the project root
crypto.ROOT_DIR = ENV.ROOT

### LOGGING SERVER AND SMTP ############################################################################

""" LOGGING is being used solely as a namespace/enumerator ; the useful values are stored in ENV """
LOGGING = argparse.Namespace()
LOGGING.SETTINGS_FILE = os.path.join(ENV.ROOT, "config/settings")

LOGGING.ADDRESS_KEY = "loggingServerAddress"
LOGGING.PORT_KEY = "loggingServerPort"
LOGGING.SENDER_KEY = "sender"
LOGGING.RECEIVERS_KEY = "receivers"
LOGGING.SETTINGS_DICT = {}

# if the settings file exists, attempt to read and parse logging and SMTP settings
if os.path.exists(LOGGING.SETTINGS_FILE):
  with open(LOGGING.SETTINGS_FILE) as f:
    rawSettings = filter(None, f.read().split("\n"))

    for each in rawSettings:
      key, val = each.split("=")
      LOGGING.SETTINGS_DICT[key] = val

# display warning if in debug mode
elif ENV.DEBUG:
  ENV.WARNINGS.append("'config/settings' file not found. Some features may not work.")

# transfer logging values into ENV
ENV.LOGGING_SERVER_ADDRESS = LOGGING.SETTINGS_DICT.get(LOGGING.ADDRESS_KEY, "")
ENV.LOGGING_SERVER_PORT = LOGGING.SETTINGS_DICT.get(LOGGING.PORT_KEY, "")
# transfer SMTP values into ENV
ENV.SENDER = LOGGING.SETTINGS_DICT.get(LOGGING.SENDER_KEY, "root")
ENV.RECEIVERS = filter(None, list(LOGGING.SETTINGS_DICT.get(LOGGING.RECEIVERS_KEY, "").split(","))) or []

### LABELS #############################################################################################

""" Provides a list of valid labels to tag work done ; iff the list is missing, any string will be accepted """

labelsFile = os.path.join(ENV.ROOT, "config/labels.txt")
ENV.LABELS = []

# if the labels file exists, read the values into ENV
if os.path.exists(labelsFile):
  with open(labelsFile, 'r') as f:
    
    # parses into list and filters out any empty lines (ex. trailing \n)
    ENV.LABELS = filter(None, f.read().split("\n"))

# display warning if in debug mode
elif ENV.DEBUG:
  ENV.WARNINGS.append("'config/labels.txt' file not found. Labels will not be populated.")

### COOKIES ############################################################################################

""" Namespace that consolidates the manipulation of session cookies """

Cookies = argparse.Namespace()
# prepends each cookie with the currently-used port
# this prevents another server instance from overwriting the cookies
Cookies.id = ENV.PORT

# GET namespace : receives bottle.request
Cookies.get = argparse.Namespace()
Cookies.get.name = lambda req: req.get_cookie(Cookies.id + "name") or ""
Cookies.get.date = lambda req: recorder.validateDate(req.get_cookie(Cookies.id + "date") or dt.date.today())
Cookies.get.anchor = lambda req: req.get_cookie(Cookies.id + "anchor") or "-1"
Cookies.get.notes = lambda req: req.get_cookie(Cookies.id + "notes") or ""

# SET namespace : receives bottle.response
Cookies.set = argparse.Namespace()
Cookies.set.name = lambda res, name: res.set_cookie(Cookies.id + "name", str(name))
Cookies.set.date = lambda res, date: res.set_cookie(Cookies.id + "date", str(recorder.validateDate(date)))
Cookies.set.anchor = lambda res, anchor: res.set_cookie(Cookies.id + "anchor", str(anchor))
Cookies.set.notes = lambda res, notes: res.set_cookie(Cookies.id + "notes", str(notes))

# DELETE namespace : receives bottle.response
Cookies.delete = argparse.Namespace()
Cookies.delete.name = lambda res: res.delete_cookie(Cookies.id + "name")
Cookies.delete.date = lambda res: res.delete_cookie(Cookies.id + "date")
Cookies.delete.anchor = lambda res: res.delete_cookie(Cookies.id + "anchor")
Cookies.delete.notes = lambda res: res.delete_cookie(Cookies.id + "notes")

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
######################################### ROUTES START #################################################
########################################################################################################

@app.get('/')
@app.get('/hours')
def hours():
  """ Main page ; serves up base template ; other routes redirect to here
  1) check for message from logging server
  2) get and manipulate cookies
  3) get subtotal and total
  4) read records from file
  5) return base template with appropriate values passed to it
  """
  # used to send all the required data to the template in one variable
  TEMPLATE = argparse.Namespace()
  
  #######################################################
  
  # if an encrypted message was returned from the logging server, get it and decrypt it
  TEMPLATE.msg = ""
  try:
    TEMPLATE.msg = crypto.getDecodedString(bottle.request.query['msg'])
  except KeyError:
    pass

  #######################################################
  
  # get name and date cookies
  TEMPLATE.name = Cookies.get.name(bottle.request)
  TEMPLATE.date = Cookies.get.date(bottle.request)
  
  # get anchor cookie in case a record has been just edited
  TEMPLATE.anchor = Cookies.get.anchor(bottle.request)
  # delete anchor cookie after getting it
  Cookies.delete.anchor(bottle.response)
  
  # get notes cookie ; in the case a record was just deleted, this cookie tracks the notes the record had
  TEMPLATE.notes = Cookies.get.notes(bottle.request)
  # delete notes cookie after getting it
  Cookies.delete.notes(bottle.response)
  
  #######################################################
  
  # parses through the saved records and counts the hours worked for the day / pay period
  TEMPLATE.subtotal = recorder.getSubtotalForDay(TEMPLATE.name, TEMPLATE.date)
  TEMPLATE.total = recorder.getTotalForPayPeriod(TEMPLATE.name, TEMPLATE.date)

  #######################################################
  
  # try to read and parse saved records corresponding to the name and date provided
  TEMPLATE.records = recorder.parseRecordsFromFile(TEMPLATE.name, TEMPLATE.date)
  
  #######################################################
  
  # additional data to send to template
  TEMPLATE.month = recorder.getPayPeriodMonth(TEMPLATE.date)
  TEMPLATE.LABELS = ENV.LABELS
  TEMPLATE.SENDER = ENV.SENDER
  TEMPLATE.RECEIVERS = ENV.RECEIVERS
  TEMPLATE.LOGGING_SERVER_ADDRESS = ENV.LOGGING_SERVER_ADDRESS
  TEMPLATE.LOGGING_SERVER_PORT = ENV.LOGGING_SERVER_PORT
  
  #######################################################

  return bottle.template('hours', DATA=TEMPLATE)

########################################################################################################
########################################################################################################
########################################################################################################

@app.post('/hours')
def hours_post():
  
  #######################################################
  
  # name of user
  name = bottle.request.forms.get(namer.name()).strip()
  
  # date : either picked by user or default today
  date = Cookies.get.date(bottle.request)
  
  # index for inserting new Record into the list of records
  index = int(bottle.request.forms.get(namer.insert()))
  
  #######################################################
  
  # parses form data and returns a Record obj
  new_record = recorder.parseRecordFromHTML(bottle.request)
  
  #######################################################
  
  # reads and parses Records on file
  records = recorder.parseRecordsFromFile(name, date)

  # TODO: remove
  # count current subtotal for ONLY the day's records
  # current_local_subtotal = recorder.countSubtotal(records)
  
  #######################################################
  
  # if the cookie is set, the user has pulled any existing files
  # if there are no existing files, the cookie will be null
  records_pulled = bool(Cookies.get.name(bottle.request))
  
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
      
      # TODO: remove
      # after adjusting the durations, recount total duration for the day
      # new_local_subtotal = recorder.countSubtotal(records)
      # TODO: remove
      # add the difference in summed durations back to the file
      # when inserting between two records (whose durations are not locked)
      # (i.e. splicing a record in), the subtotal should not change
      # recorder.addToSubtotal(name, date, (new_local_subtotal - current_local_subtotal))
    
    #######################################################
    
    # write back updated list
      recorder.writeRecords(name, date, records)
    
    # after posting a new record, delete the anchor cookie to reset it
    Cookies.delete.anchor(bottle.response)
    Cookies.delete.notes(bottle.response)
  
  else:
    Cookies.set.notes(bottle.response, new_record.notes)
  
  #######################################################
  
  # set name cookie with most recently used name (for insurance mostly)
  Cookies.set.name(bottle.response, name)
  
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
  Cookies.set.name(bottle.response, name)
  Cookies.set.date(bottle.response, date)
  
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
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  # sets flag based on user's confirmation / denial from popup alert
  deleteConfirm = bottle.request.forms.get("deleteConfirm")
  
  #######################################################
  
  if (deleteConfirm == "true") and name:
    # get records
    records = recorder.parseRecordsFromFile(name, date)

    # TODO: remove
    # get summed duration of records
    # summed_subtotal = recorder.countSubtotal(records)

    # TODO: remove
    # subtract that amount from the subtotal on file
    # recorder.subtractFromSubtotal(name, date, summed_subtotal)
    
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
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  #######################################################
  
  # read and parse records from file
  records = recorder.parseRecordsFromFile(name, date)
  
  # set the notes to be in the form
  Cookies.set.notes(bottle.response, records[index].notes)

  # TODO: remove
  # get the duration of the record to be deleted
  # deletedRecordDuration = records[index].duration

  # TODO: remove
  # subtract that amount from the subtotal on file
  # recorder.subtractFromSubtotal(name, date, deletedRecordDuration)
  
  # delete record
  del records[index]
  
  # write back updated records
  recorder.writeRecords(name, date, records)
  
  # upon redirect, anchor to where the record was deleted
  # open that form and insert notes, etc. from the deleted record
  Cookies.set.anchor(bottle.response, index)
  
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
  
  Cookies.set.anchor(bottle.response, index)
  
  notes = bottle.request.forms.get("notesDisplay")
  
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
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
    Cookies.delete.anchor(bottle.response)
  
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
  
  Cookies.set.anchor(bottle.response, index)
  
  # get the submitted end time (which has already been pattern matched) OR get current rounded time
  end = recorder.parseTime(bottle.request.forms.get('completeEnd')) or recorder.getCurrentRoundedTime()
  
  # get name and date cookies
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
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
    
      # TODO: remove
      # add the new duration to the subtotal
      # recorder.addToSubtotal(name, date, record.duration)
    
    # write back record
    records[index] = record
    recorder.writeRecords(name, date, records)
    
    # delete cookie if task completed
    Cookies.delete.anchor(bottle.response)
  
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
  
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  index = int(bottle.request.forms.get('index'))
  
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  Cookies.set.anchor(bottle.response, index)
  
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
  
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  index = int(bottle.request.forms.get('index'))
  
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  Cookies.set.anchor(bottle.response, index)
  
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
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  # sets flag based on user's confirmation / denial from popup alert
  emailConfirm = bottle.request.forms.get("emailConfirm")
  
  #######################################################

  # TODO: remove
  # subtotal = recorder.readSubtotal(name, date) or '0.0'
  
  total = recorder.getTotalForPayPeriod(name, date)
  
  #######################################################
  
  curTimeShort = time.strftime("%m/%d")
  
  subject = "Hours {0} (Total: {1})".format(curTimeShort, str(total))
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
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
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
#######################################  	 ROUTES END	   ###############################################
########################################################################################################




########################################################################################################
#######################################  	APP LAUNCHER	   #############################################
########################################################################################################

border = "* * * * * * * * * * * * * * * * * * * * * * * * * * * "

cp.printHeader(border)

######################################

if ENV.DEBUG:
  ENV.WARNINGS.insert(0, "TEST WARNING")
  ENV.ERRORS.insert(0, "TEST ERROR")

######################################

if ENV.WARNINGS or ENV.ERRORS:
  
  for warning in ENV.WARNINGS:
    cp.printWarn("WARNING : " + warning)
  
  for error in ENV.ERRORS:
    cp.printFail("ERROR   : " + error)

  cp.printHeader(border)

######################################

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

######################################

app.run(host=ENV.HOST, port=ENV.PORT, debug=ENV.DEBUG, reloader=ENV.RELOAD)

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
