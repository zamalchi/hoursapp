#!/usr/bin/env python
"""
Bottle Python webapp for recording hours worked ; Version 1.4

TODO:
  [done] doc this whole file
  [?] finish working on recorder module
  git flow feature finish docs
  git flow feature start date-nav (add forward/backward buttons for navigating through dates)
  git flow release ...
  update readme and updates

DIRECTORY:
  imports
  instantiation of global objects
  argument parsing into global environment variables
  augmenting working directory and sys path for apache
  bottle template url default
  static routing for css/js/images/fonts/favicon
  sub-directories and module paths
  logging and smtp functionality
  labels
  cookie manipulation functions
  
  GET   /,/hours
  POST  /hours
  POST  /setCookies
  POST  /delete
  POST  /deleteOne
  POST  /completeNotes
  POST  /completeEndTime
  GET   /viewUpdates
  POST  /toggleBillable
  POST  /toggleEmergency
  POST  /email
  POST  /send
  GET   /ack
  
  console messages and app launching
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

### INSTANTIATION OF GLOBAL OBJECTS ####################################################################

# bottle app object to which the routes are attached
app = bottle.Bottle()

# provides names for extracting data from HTML requests
# TODO: labeler refactoring
namer = labeler.Labeler()
HTML_LABELS = labeler.HTML_LABELS

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
Cookies.id = "hours-app-"

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
###################################### HOURS FORM START ################################################
########################################################################################################

@app.get('/')
@app.get('/hours')
def hours():
  """ GET /hours ; Main page ; serves up base template ; other routes redirect to here
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

@app.post('/hours')
def hours_post():
  """ POST /hours ; Main page post ; parses form data ; reads/writes files ; redirects to GET /hours
  Extra explicit because of logical complexity
  1) get name, date, and index from the request
  2) parse the new record from the request
  3) read records on file for the user and date
  4) using the name and date cookies, check if the user has seen any records for that date
  5) check that the new record is valid and fits in the record list at the index and that no records have gone unseen
  if true:
    5.1) insert the new record at the index
    5.2) adjust adjacent records
    5.3) write the new record list to file
    5.4) delete the anchor cookie (successful POST means anchor back to the top of the page)
    5.5) delete the notes cookies (since it pertains to the inserted record only)
  else:
    5.1) save the index as the anchor cookie for GET /hours
    5.2) save the new (invalid) record's notes to a cookie
  6) set the name and date cookies to the values pulled from the request
  7) redirect to GET /hours
  """
  #######################################################
  
  # name of user
  name = bottle.request.forms.get("name").strip()
  # date : either picked by user or default today
  date = Cookies.get.date(bottle.request)
  # index for inserting new Record into the list of records
  index = int(bottle.request.forms.get("index"))
  
  #######################################################
  
  # parses form data and returns a Record obj
  newRecord = recorder.parseRecordFromHTML(bottle.request)
  
  # reads and parses Records on file
  records = recorder.parseRecordsFromFile(name, date)
  
  #######################################################

  # if the name cookie is equal to the name pulled from the request
  # and the date cookie is equal to the date pulled from the request
  # then any records on file have already been pulled, and it is safe to insert into the list
  recordsPulled = ((Cookies.get.name(bottle.request) == name) and (Cookies.get.date(bottle.request) == date))
  
  # checks if newRecord.start < newRecord.end
  # and that newRecord doesn't exceed the outer limits of adjacent records
  # also ensures that the user has seen any records that exist
  if recorder.checkIfValid(records, newRecord, index) and (recordsPulled or not records):
      
    # insert new record at index provided from template form
    records.insert(index, newRecord)
    
    # adjust timings of adjacent records in case of overlap
    recorder.adjustAdjacentRecords(records, index)
    
    # write back updated list
    recorder.writeRecords(name, date, records)
    
    # after posting a new record, delete the anchor and notes cookies
    Cookies.delete.anchor(bottle.response)
    Cookies.delete.notes(bottle.response)
  
  else:
    # if the record was invalid
    # or there were records the user hadn't seen
    # then save the index to anchor to the correct record form upon reload
    # and save the notes to avoid retyping
    Cookies.set.anchor(bottle.response, index)
    Cookies.set.notes(bottle.response, newRecord.notes)
  
  #######################################################
  
  # set name cookie with most recently used name (for insurance mostly)
  Cookies.set.name(bottle.response, name)
  Cookies.set.date(bottle.response, date)
  
  bottle.redirect('hours')

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

@app.post('/pull')
def set_cookies():
  """ Sets name and date cookies for pulling records without altering them ; redirects to GET /hours """
  #######################################################
  
  # get name of user provided in specified field
  name = bottle.request.forms.get("name") or ""
  
  # the forward and backward arrows set this value so that the date can be modified by it (-1|0|1)
  timeDelta = int(bottle.request.forms.get("time-delta") or 0)
  
  if timeDelta != 0:
    # if a non-zero time delta exists, use the existing date cookie
    # otherwise, the empty HTML date field will cause recorder to always provide the current date
    date = Cookies.get.date(bottle.request)
  else:
    # get date: either set manually or defaults to current day
    date = recorder.validateDate(bottle.request.forms.get("date"))

  date += dt.timedelta(days=timeDelta)
  
  #######################################################
  
  # set name and date cookie
  Cookies.set.name(bottle.response, name)
  Cookies.set.date(bottle.response, date)
  
  #######################################################
  
  # redirect to GET /hours
  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/delete')
def delete_records():
  """ Deletes all the records in the file corresponding to the name and date cookies ; redirects to GET /hours """
  #######################################################
  
  # get name and date cookies
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  # sets flag based on user's confirmation / denial from the popup alert
  deleteConfirm = (bottle.request.forms.get("deleteConfirm") == "true")
  
  #######################################################
  
  if deleteConfirm and name:
    # delete both of the user's record files (hidden and normal)
    recorder.deleteRecords(name, date)
  
  #######################################################
  
  # redirect back to hours page
  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/deleteOne')
def delete_single_record():
  """ Deletes one record from the list of records currently displayed at GET /hours ; redirects to GET /hours """
  #######################################################
  
  # get index based on which delete button was clicked / which form was submitted
  # TODO: ensure this is good, in case of template changes
  index = int(bottle.request.forms.get('index'))
  
  # get name and date cookies
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
    
  # read and parse records from file
  records = recorder.parseRecordsFromFile(name, date)
  
  #######################################################
  
  # upon redirect, anchor to where the record was deleted
  # open that form and insert notes from the deleted record
  Cookies.set.anchor(bottle.response, index)
  Cookies.set.notes(bottle.response, records[index].notes)

  #######################################################

  # delete record
  del records[index]
  
  # write back updated records
  recorder.writeRecords(name, date, records)
  
  #######################################################
  
  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/updateNotes')
def update_notes():
  """ Updates the notes field of a specific record ; redirects to GET /hours """
  #######################################################
  
  # get index of completed record
  # TODO: ensure this is good, in case of template changes
  index = int(bottle.request.forms.get("index"))
  
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  # TODO: again, check after template changes
  newNotes = bottle.request.forms.get("notesDisplay")
  # replace <br> with " " in case of enter button being pressed
  newNotes = newNotes.replace("<br>", " ").strip()

  # set the anchor cookie ; if the record's notes are successfully changed, it gets deleted
  Cookies.set.anchor(bottle.response, index)

  #######################################################

  if newNotes:
    records = recorder.parseRecordsFromFile(name, date)
    
    records[index].notes = newNotes
    
    recorder.writeRecords(name, date, records)
    
    # delete cookie if task completed
    Cookies.delete.anchor(bottle.response)
  
  #######################################################

  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/completeEndTime')
def complete_end_time():
  """ Completes a pending record by supplying an end time ; redirects to GET /hours """
  #######################################################
  
  # get index of completed record
  # TODO: ensure this is good, in case of template changes
  index = int(bottle.request.forms.get('index'))
  
  # get the submitted end time (which has already been pattern matched) OR get current rounded time
  # TODO: ensure this is good, in case of template changes
  end = recorder.parseTime(bottle.request.forms.get('completeEnd')) or recorder.getCurrentRoundedTime()
  
  # get name and date cookies
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)

  # set the anchor cookie ; if the record is successfully completed, it gets deleted
  Cookies.set.anchor(bottle.response, index)
  
  #######################################################
  
  # get records from file
  records = recorder.parseRecordsFromFile(name, date)
  
  # get particular record to complete
  record = records[index]
  
  # set the end time - THEN check if it is valid
  record.setEnd(end)
  
  # don't accept an invalid or invalidly placed record
  if recorder.checkIfValid(records, record, index):
    
    if not record.durationLocked:
      # calculate and set duration
      record.calculateAndSetDuration()
    
    # write back record
    records[index] = record
    recorder.writeRecords(name, date, records)
    
    # delete cookie if task completed
    Cookies.delete.anchor(bottle.response)
  
  #######################################################

  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.get('/viewUpdates')
def view_updates():
  """ Provides readme and updates information ; serves up 'updates' template """
  # TODO: mabye add warnings about missing readme and update files and/or put the file paths into a global var
  
  readmeFile = os.path.join(ENV.ROOT, "README.md")
  updatesFile = os.path.join(ENV.ROOT, "docs/UPDATES.md")
  
  ##############################################
  
  if os.path.exists(readmeFile):
    with open(readmeFile, 'r') as f:
      readme = markdown.markdown(f.read()) or ""
  
  else:
    readme = "<h2>Readme not found.</h2>"
  
  ##############################################
  
  if os.path.exists(updatesFile):
    with open(updatesFile, 'r') as f:
      updates = markdown.markdown(f.read()) or ""

  else:
    updates = "<h2>Updates not found.</h2>"
  
  ##############################################
  
  return bottle.template('updates', readme=readme, updates=updates)

########################################################################################################
########################################################################################################

@app.post('/toggleBillable')
def toggle_billable():
  """ Toggles a single record's Y/N billable field ; writes to file ; redirects to GET /hours """
  ##############################################

  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  ##############################################
  
  # TODO: ensure this is good, in case of template changes
  index = int(bottle.request.forms.get('index'))
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  Cookies.set.anchor(bottle.response, index)

  ##############################################

  records = recorder.parseRecordsFromFile(name, date)
  
  records[index].billable = "N" if records[index].billable == "Y" else "Y"

  recorder.writeRecords(name, date, records)

  bottle.redirect('hours')


@app.post('/toggleEmergency')
def toggle_emergency():
  """ Toggles a single record's Y/N emergency field ; writes to file ; redirects to GET /hours """
  ##############################################

  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  ##############################################

  # TODO: ensure this is good, in case of template changes
  index = int(bottle.request.forms.get('index'))
  # don't delete on task completion (stay anchored to edited record to easily view the change)
  Cookies.set.anchor(bottle.response, index)
  
  ##############################################
  
  records = recorder.parseRecordsFromFile(name, date)

  records[index].emergency = "N" if records[index].emergency == "Y" else "Y"
  
  recorder.writeRecords(name, date, records)

  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/email')
def email_records():
  """ Sends an SMTP email from ENV.SENDER to ENV.RECEIVERS containing records pulled with the name and date cookies ;
    redirects to GET /hours
  """
  #######################################################
  
  # get name and date cookies
  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  # sets flag based on user's confirmation / denial from popup alert
  emailConfirm = (bottle.request.forms.get("emailConfirm") == "true")
  
  #######################################################

  total = recorder.getTotalForPayPeriod(name, date)
  
  #######################################################
  
  currentTimeShort = time.strftime("%m/%d")
  
  subject = "Hours {0} (Total: {1})".format(currentTimeShort, str(total))
  
  #######################################################
  
  if all((emailConfirm, name, ENV.SENDER, ENV.RECEIVERS)):
    
    # get records corresponding to name and date
    records = recorder.parseRecordsFromFile(name, date)
    
    #TODO: check to make sure this works instead of the old commented line (make sure "\n" isn't needed at the end)
    body = "\n".join([record.emailFormat() for record in records])
    # for record in records:
    #   body += record.emailFormat() + "\n"
    
    # message = "Subject: %s\n\n%s" % (subject, body)
    # TODO: check to make sure this works instead of the old commented line
    message = "Subject: {subject}\n\n{body}".format(subject=subject, body=body)
      
    try:
      mail = smtplib.SMTP(ENV.HOST)
      mail.sendmail(ENV.SENDER, ENV.RECEIVERS, message)
      mail.quit()
      
      # if in debug mode, print info on successful email
      if ENV.DEBUG:
        cp.printOk("SENDER: {sender}".format(sender=ENV.SENDER))
        cp.printOk("RECEIVERS: {receivers}".format(receivers=ENV.RECEIVERS))
        cp.printOk("-- MESSAGE --\n{message}".format(message=message))
    
    except smtplib.SMTPException as e:
      # TODO: make sure this works
      cp.printFail(e)
  
  bottle.redirect('hours')

########################################################################################################
########################################################################################################

@app.post('/send')
def send_records():
  """ Uses modu.crypto to encrypt and send records pulled with the name and date cookies ; redirects to GET /hours """
  # TODO: test this ; not sure if it's going to be used
  #######################################################

  name = Cookies.get.name(bottle.request)
  date = Cookies.get.date(bottle.request)
  
  confirm = (bottle.request.forms.get('confirm') == "true")
  
  # will use form-supplied values but defaults to values read from config file
  address = bottle.request.forms.get('address').strip() or ENV.LOGGING_SERVER_ADDRESS
  port = bottle.request.forms.get('port').strip() or ENV.LOGGING_SERVER_PORT
  
  #######################################################
  
  if all((confirm, name, address, port)):
        
    # parse records from file
    records = recorder.parseRecordsFromFile(name, date)
    
    # turn records into a '\n'-separated string
    recordString = '\n'.join([r.emailFormat() for r in records])
    
    # if in debug mode and about to send records, display info
    if ENV.DEBUG:
      cp.printOk("SENDING TO: {0}:{1}".format(address, port))
      cp.printOK("-- RECORDS --\n{records}".format(records=recordString))
    
    try:
      # encrypt and encode recordString
      encryptedRecords = crypto.getEncodedString(recordString)
      
      address = "/".join(bottle.request.url.split("/")[:-1]) + "/ack"
      
      # encrypts and encodes host address for rerouting back to hours
      encryptedAddress = crypto.getEncodedString(address)
      
      # send name, date, and encoded records to receiving server
      bottle.redirect('http://{address}:{port}/receive?n={name}&d={date}&r={encryptedRecords}&a={encryptedAddress}'
        .format(address=address, port=port,
                name=name, date=date,
                encryptedRecords=encryptedRecords, encryptedAddress=encryptedAddress))
    
    # thrown if config/crypto not found
    # TODO: is this error too specific or even accurate?
    except TypeError as e:
      cp.printFail(e)

  bottle.redirect('hours')


@app.get('/ack')
def ack_sent_records():
  """ Catches the return message from the logging server ; redirects to GET /hours with the message as a query param """
  # TODO: again, test, but it doesn't look like it will be used
  
  msg = bottle.request.query['msg'] or ''

  bottle.redirect('hours?msg={0}'.format(msg))

########################################################################################################
####################################### MISC ROUTES END	################################################
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
print("HOST ADDRESS     : {hostAddress}".format(hostAddress=ENV.HOST))
print("HOST PORT        : {hostPort}".format(hostPort=ENV.PORT))

sender = "SMTP SENDER      : {senderStr}".format(senderStr=ENV.SENDER)
receivers = "SMTP RECEIVERS   : {receiversStr}".format(receiversStr=", ".join(ENV.RECEIVERS))
debug = "DEBUG            : {devMode}".format(devMode=ENV.DEBUG)
reloader = "LIVE RELOAD      : {liveReload}".format(liveReload=ENV.RELOAD)

# True -> print ; False -> cp.printWarn
print(sender) if ENV.SENDER else cp.printWarn(sender)
print(receivers) if ENV.RECEIVERS else cp.printWarn(receivers)

# True -> cp.printOk ; False -> print
cp.printOK(debug) if ENV.DEBUG else print(debug)
cp.printOK(reloader) if ENV.RELOAD else print(reloader)

cp.printHeader(border)

######################################

app.run(host=ENV.HOST, port=ENV.PORT, debug=ENV.DEBUG, reloader=ENV.RELOAD)

########################################################################################################
########################################################################################################
########################################################################################################
