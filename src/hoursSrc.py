
# TO RUN FROM WRAPPER CLASSES:
# - labelsInit(labelsFileName) - required
# - loggingServerInit(address)

########################################################################################################
########################################################################################################
########################################################################################################

### PACKAGES ###########################################################################################

import os
import time
import smtplib
import sys
import datetime as dt

### IMPORTS ############################################################################################

from src.bottle import \
    get, post, redirect, \
    request, response,\
    template, static_file,\
    SimpleTemplate, url

# for help button which displays README.md and UPDATES.md
from markdown import markdown

# Record class
from classes.Record import Record
# Labeler class
from classes.Labeler import Labeler

from src.crypto import *

# root directory for project
from config.dirs import ROOT_DIR

namer = Labeler()

### APACHE #############################################################################################

os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

### RUNNING AS MAIN ####################################################################################

if __name__ == "__main__":
    print("Run webapp through wrapper.")
    print("Exiting...")
    exit()

### FOR CSS READING IN TEMPLATES #######################################################################

SimpleTemplate.defaults["url"] = url

### DIRECTORY ##########################################################################################

# project root and directory for saving hours information : overwrites default values in class
Record.rootDir = ROOT_DIR
Record.hoursDir = os.path.join(ROOT_DIR, "hours")

# if the directory doesn't exist, create it
if not os.path.exists(Record.hoursDir):
    os.makedirs(Record.hoursDir)

### LOGGING SERVER #####################################################################################

# ip and port as a string
loggingServerAddress = ""
loggingServerPort = ""

def loggingServerInit(address, port):
    global loggingServerAddress
    global loggingServerPort

    loggingServerAddress = address.strip()
    loggingServerPort = port.strip()

    print("SERVER: {0}:{1}".format(loggingServerAddress, loggingServerPort))

### SMTP ###############################################################################################

sender = ""
receivers = ""
def smtpInit(mailTo=[], mailFrom='root'):
    # this is called from the wrapper file
    # sets the sender and receiver for emails
    global receivers
    global sender

    receivers = mailTo
    sender = mailFrom

    print("SMTP: {0} -> {1}".format(sender, receivers))

### LABELS #############################################################################################

# sets labels for populating dropdown list in /hours
labels = []

def labelsInit(filename):
    # read labels from labels.txt
    global labels
    try:
        f = open(filename, 'r')

        # parses into list and filters out any empty lines (ex. trailing \n)
        labels = filter(None, f.read().split("\n"))

        f.close()
    except IOError:
        print("***\nERROR: Labels file not found. Labels will not be populated.\n***")

### STATIC ROUTING ########################################################################################

# CSS
@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root=os.path.join(ROOT_DIR, 'static/css'))

# JAVASCRIPT
@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root=os.path.join(ROOT_DIR, 'static/js'))

# IMAGES
@get('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root=os.path.join(ROOT_DIR, 'static/img'))

# FONTS
@get('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
    return static_file(filename, root=os.path.join(ROOT_DIR, 'static/fonts'))

### COOKIE GETTERS/SETTERS #############################################################################

### NAME ########################################################
def getNameCookie(req):
    return req.get_cookie("name") or ""

def setNameCookie(res, name):
    res.set_cookie("name", name)

### DATE ########################################################
def getDateCookie(req):
    return Record.validateDate(req.get_cookie("date") or dt.date.today())

def setDateCookie(res, date):
    res.set_cookie("date", str(Record.validateDate(date)))

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

@get('/hours')
def hours():

    #######################################################

    msg = ""
    try:
        msg = getDecodedString(request.query['msg'])
    except KeyError:
        pass

    # get name and date cookies
    name, date = getCookies(request)

    # get anchor cookie in case record has been just edited
    anchor = getAnchorCookie(request)

    # set anchor cookie to null after getting it
    deleteAnchorCookie(response)

    notes = getNotesCookie(request)

    deleteNotesCookie(response)

    # get the month to use for the monthly subtotal
    month = date.month

    subtotal = Record.readSubtotal(name, date)
    #######################################################

    # try to open file with user's name and retrieve data
    # for each record, create a new Record object and add to list to pass to template
    # list of records as Record obj
    records = Record.parseRecordsFromFile(name, date)

    #######################################################

    return template('hours',
                    name=name, date=date,
                    records=records, labels=labels,
                    month=month, subtotal=subtotal,
                    anchor=anchor, notes=notes,
                    sender=sender, receivers=receivers,
                    loggingServerAddress=loggingServerAddress, loggingServerPort=loggingServerPort,
                    msg=msg)


########################################################################################################
########################################################################################################
########################################################################################################

@post('/hours')
def hours_post():
    #######################################################

    # name of user
    name = request.forms.get(namer.name()).strip()

    # date : either picked by user or default today
    date = getDateCookie(request)

    # index for inserting new Record into the list of records
    index = int(request.forms.get(namer.insert()))

    #######################################################

    # parses form data and returns a Record obj
    new_record = Record.getRecordFromHTML(request)

    #######################################################

    # reads and parses Records on file
    records = Record.parseRecordsFromFile(name, date)

    # count current subtotal for ONLY the day's records
    current_local_subtotal = Record.countSubtotal(records)

    #######################################################

    # if the cookie is set, the user has pulled any existing files
    # if there are no existing files, the cookie will be null
    records_pulled = getNameCookie(request)

    # checks if new_record.start < new_record.end
    # and that new_record doesn't exceed the outer limits of adjacent records
    if Record.checkIfValid(records, new_record, index):

        if records and not records_pulled:
            # append to the end of unpulled existing records
            # prevents adding to the beginning of an unexpected list
            records.append(new_record)
        else:
            # insert new record at index provided from template form
            records.insert(index, new_record)

            # adjust timings of adjacent records in case of overlap
            Record.adjustAdjacentRecords(records, index)

            # after adjusting the durations, recount total duration for the day
            new_local_subtotal = Record.countSubtotal(records)

            # add the difference in summed durations back to the file
            # when inserting between two records (whose durations are not locked)
            # (i.e. splicing a record in), the subtotal should not change
            Record.addToSubtotal(name, date, (new_local_subtotal - current_local_subtotal))

        #######################################################

        # write back updated list
        Record.writeRecords(name, date, records)

        # after posting a new record, delete the anchor cookie to reset it
        deleteAnchorCookie(response)

        deleteNotesCookie(response)

    else:

        setNotesCookie(response, new_record.notes)

    #######################################################

    # set name cookie with most recently used name (for insurance mostly)
    setNameCookie(response, name)

    #######################################################

    redirect('hours')

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

@post('/setCookies')
def set_cookies():
    #######################################################

    # get name of user provided in specified field
    name = request.forms.get("setName") or ""

    # get date: either set manually or defaults to current day
    date = Record.validateDate(request.forms.get("setDate") or dt.date.today())

    #######################################################

    # set name and date cookie
    setCookies(response, name, date)

    #######################################################

    # redirect to /hours to read file
    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### deletes records of current user
@post('/delete')
def delete_records():
    #######################################################

    # get name and date cookies
    name, date = getCookies(request)

    # sets flag based on user's confirmation / denial from popup alert
    deleteConfirm = request.forms.get("deleteConfirm")

    #######################################################

    if (deleteConfirm == "true") and name:
        # get records
        records = Record.parseRecordsFromFile(name, date)

        # get summed duration of records
        summed_subtotal = Record.countSubtotal(records)

        # subtract that amount from the subtotal on file
        Record.subtractFromSubtotal(name, date, summed_subtotal)

        # delete both of the user's record files
        Record.deleteRecords(name, date)

    #######################################################

    # redirect back to hours page
    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### deletes one record from those currently displayed
@post('/deleteOne')
def delete_single_record():
    #######################################################

    # get index based on which delete button was clicked / which form was submitted
    index = int(request.forms.get('index'))

    # get name and date cookies
    name, date = getCookies(request)

    #######################################################

    # read and parse records from file
    records = Record.parseRecordsFromFile(name, date)

    # set the notes to be in the form
    setNotesCookie(response, records[index].notes)

    # get the duration of the record to be deleted
    deletedRecordDuration = records[index].duration

    # subtract that amount from the subtotal on file
    Record.subtractFromSubtotal(name, date, deletedRecordDuration)

    # delete record
    del records[index]

    # write back updated records
    Record.writeRecords(name, date, records)

    # upon redirect, anchor to where the record was deleted
    # open that form and insert notes, etc. from the deleted record
    setAnchorCookie(response, index)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### updates the notes field of a specific record ; triggered by the save button
@post('/completeNotes')
def complete_notes():
    #######################################################

    # get index of completed record
    index = int(request.forms.get("index"))

    setAnchorCookie(response, index)

    notes = request.forms.get("notesDisplay")

    name, date = getCookies(request)

    #######################################################

    if notes:
        records = Record.parseRecordsFromFile(name, date)

        record = records[index]

        # replace <br> with " " in case of enter button being pressed
        notes = notes.replace("<br>", " ").strip()

        record.notes = notes

        records[index] = record

        Record.writeRecords(name, date, records)

        # delete cookie if task completed
        deleteAnchorCookie(response)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

@post('/completeEndTime')
def complete_end_time():
    #######################################################

    # get index of completed record
    index = int(request.forms.get('index'))

    setAnchorCookie(response, index)

    # get the submitted end time (which has already been pattern matched) OR get current rounded time
    end = Record.parseTime(request.forms.get('completeEnd')) or Record.getCurrentRoundedTime()

    # get name and date cookies
    name, date = getCookies(request)

    #######################################################

    # get records from file
    records = Record.parseRecordsFromFile(name, date)

    # get particular record to complete
    record = records[index]

    # set the end time - THEN check if it is valid
    record.setEnd(end)

    # don't accept an invalid or invalidly placed record
    if not Record.checkIfValid(records, record, index):
        redirect('hours')

    # else block for clarity
    else:
        if not record.durationLocked:

            # calculate and set duration
            record.calculateAndSetDuration()

            # add the new duration to the subtotal
            Record.addToSubtotal(name, date, record.duration)

        # write back record
        records[index] = record
        Record.writeRecords(name, date, records)

        # delete cookie if task completed
        deleteAnchorCookie(response)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### returns a list (read from file) of updates
@get('/viewUpdates')
def view_updates():

    readme = updates = ""

    try:
        f = open(os.path.join(ROOT_DIR, 'README.md'), 'r')
        raw = f.read()
        f.close()

        readme = markdown(raw)

    except IOError:
        readme = "<h2>Readme not found.</h2>"

    ##############################################

    try:
        f = open(os.path.join(ROOT_DIR, "docs/UPDATES.md"), 'r')
        raw = f.read()
        f.close()

        updates = markdown(raw)

    except IOError:
        updates = "<h2>Updates not found.</h2>"

    ##############################################

    return template('updates', readme=readme, updates=updates)

########################################################################################################
########################################################################################################
########################################################################################################

@post('/toggleBillable')
def toggle_billable():

    name, date = getCookies(request)

    index = int(request.forms.get('index'))

    # don't delete on task completion (stay anchored to edited record to easily view the change)
    setAnchorCookie(response, index)

    records = Record.parseRecordsFromFile(name, date)

    r = records[index]

    if r.billable == "Y":
        r.billable = "N"
    else:
        r.billable = "Y"

    records[index] = r

    Record.writeRecords(name, date, records)

    redirect('hours')


@post('/toggleEmergency')
def toggle_emergency():

    name, date = getCookies(request)

    index = int(request.forms.get('index'))

    # don't delete on task completion (stay anchored to edited record to easily view the change)
    setAnchorCookie(response, index)

    records = Record.parseRecordsFromFile(name, date)

    r = records[index]

    if r.emergency == "Y":
        r.emergency = "N"
    else:
        r.emergency = "Y"

    records[index] = r

    Record.writeRecords(name, date, records)

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### emails records
@post('/email')
def email_records():

    global sender, receivers

    #######################################################

    # get name and date cookies
    name, date = getCookies(request)

    # sets flag based on user's confirmation / denial from popup alert
    emailConfirm = request.forms.get("emailConfirm")

    #######################################################

    subtotal = Record.readSubtotal(name, date) or '0.0'

    #######################################################

    curTimeShort = time.strftime("%m/%d")

    sen = sender
    rec = receivers

    subject = "Hours {0} (Subtotal: {1})".format(curTimeShort, subtotal)
    body = ""

    #######################################################

    if (emailConfirm == "true") and name and sen and rec:

        # try to open file with user's name and retrieve data
        records = Record.parseRecordsFromFile(name, date)

        for r in records:
            body += r.emailFormat() + "\n"

        message = "Subject: %s\n\n%s" % (subject, body)

        try:
            mail = smtplib.SMTP("localhost")
            mail.sendmail(sen, rec, message)
            mail.quit()

        except smtplib.SMTPException:
            pass

    redirect('hours')

########################################################################################################
########################################################################################################

@post('/send')
def send_records():

    global loggingServerAddress, loggingServerPort

    # get cookies
    name, date = getCookies(request)

    confirm = request.forms.get('confirm')

    address = request.forms.get('address').strip() or loggingServerAddress
    port = request.forms.get('port').strip() or loggingServerPort

    if (confirm == "true") and name and address and port:

        print("SENDING TO: {0}:{1}".format(address, port))

        # parse records from file
        records = Record.parseRecordsFromFile(name, date)

        # turn records into a string separated by \n
        string = "\n".join([r.emailFormat() for r in records])

        try:
            # encrypt and encode string
            records_encrypted = getEncodedString(string)

            addr = "/".join(request.url.split("/")[:-1]) + "/ack"

            # encrypts and encodes host address for rerouting back to hours
            addr_encrypted = getEncodedString(addr)

            # send name, date, and encoded records to receiving server
            redirect('http://{0}:{1}/receive?n={2}&d={3}&r={4}&a={5}'.format(address, port, name, date, records_encrypted, addr_encrypted))

        # thrown if config/crypto not found
        except TypeError:
            print("Couldn't send to server because config/crypto is missing.")

    redirect('hours')

@get('/ack')
def ack_sent_records():

    msg = request.query['msg'] or ''

    redirect('hours?msg={0}'.format(msg))

########################################################################################################
######################################  	MISC ROUTES END	   ###########################################
########################################################################################################
