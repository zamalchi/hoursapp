
# TO RUN FROM WRAPPER CLASSES:
# - smtpInit(mailTo)
# - setDevMode(dmode)
# - labelsInit(labels)

########################################################################################################
########################################################################################################
########################################################################################################

### PACKAGES ###########################################################################################

import os
import time
import smtplib
import sys

### IMPORTS ############################################################################################

from bottle import route, request, response, template, static_file, redirect, SimpleTemplate, url

# Record class
from Record import Record
# Labeler class
from Labeler import Labeler

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

# directory for saving hours information
Record.hoursDir = "hours/"
# if the directory doesn't exist, create it
if not os.path.exists(Record.hoursDir):
    os.makedirs(Record.hoursDir)

### SMTP ###############################################################################################

receivers = []

def smtpInit(mailTo='', mailFrom='root'):
    # this is called from the wrapper file
    # sets the sender and receiver for emails
    global receivers
    global sender

    receivers = [mailTo]
    sender = mailFrom

### LABELS #############################################################################################

# sets labels for populating dropdown list in /hours
def labelsInit(l):
    # read labels from labels.txt
    global labels
    try:
        f = open(l, 'r')

        # parses into list and filters out any empty lines (ex. trailing \n)
        labels = filter(None, f.read().split("\n"))

        f.close()
    except IOError:
        print("***\nERROR: Labels file not found. Labels will not be populated.\n***")

### STATIC ROUTING ########################################################################################

# for css and favicon reading in templates
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')


### COOKIE GETTERS/SETTERS #############################################################################

### NAME ########################################################
def getNameCookie(request):
    return request.get_cookie("name") or ""

def setNameCookie(response, name):
    response.set_cookie("name", name)

### DATE ########################################################
def getDateCookie(request):
    return request.get_cookie("date") or time.strftime("%Y-%m-%d")

def setDateCookie(response, date):
    response.set_cookie("date", date)

### CONSOLIDATED ################################################
def getCookies(request):
    return getNameCookie(request), getDateCookie(request)

def setCookies(response, name, date):
    setNameCookie(response, name)
    setDateCookie(response, date)

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

@route('/hours')
def hours():
    #######################################################

    # get name and date cookies
    name, date = getCookies(request)

    # get the month to use for the monthly subtotal
    month = Record.getSubtotalMonth(date)

    subtotal = Record.readSubtotal(name, date)
    #######################################################

    # try to open file with user's name and retrieve data
    # for each record, create a new Record object and add to list to pass to template
    # list of records as Record obj
    records = Record.parseRecordsFromFile(name, date)

    #######################################################

    return template('hours', records=records, labels=labels, name=name, date=date, month=month, subtotal=subtotal,
                    sender=sender, receivers=receivers)


########################################################################################################
########################################################################################################
########################################################################################################

@route('/hours', method="POST")
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

@route('/setCookies', method="POST")
def set_cookies():
    #######################################################

    # get name of user provided in specified field
    name = request.forms.get("setName") or ""

    # get date: either set manually or defaults to current day
    date = request.forms.get("setDate") or time.strftime("%Y-%m-%d")

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
@route('/delete', method="POST")
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
@route('/deleteOne', method="POST")
def delete_single_record():
    #######################################################

    # get index based on which delete button was clicked / which form was submitted
    index = int(request.forms.get('index'))

    # get name and date cookies
    name, date = getCookies(request)

    #######################################################

    # read and parse records from file
    records = Record.parseRecordsFromFile(name, date)

    # get the duration of the record to be deleted
    deletedRecordDuration = records[index].duration

    # subtract that amount from the subtotal on file
    Record.subtractFromSubtotal(name, date, deletedRecordDuration)

    # delete record
    del records[index]

    # write back updated records
    Record.writeRecords(name, date, records)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### updates the notes field of a specific record ; triggered by the save button
@route('/completeNotes', method="POST")
def complete_notes():
    #######################################################

    # get index of completed record
    index = int(request.forms.get("index"))

    notes = request.forms.get("notes")

    name, date = getCookies(request)

    #######################################################

    if notes:
        records = Record.parseRecordsFromFile(name, date)

        record = records[index]

        # replace <br> with " " in case of enter button being pressed
        notes = notes.replace("<br>", " ").strip()

        # TODO: description --> notes
        record.description = notes

        records[index] = record

        Record.writeRecords(name, date, records)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

@route('/completeEndTime', method="POST")
def complete_end_time():
    #######################################################

    # get index of completed record
    index = int(request.forms.get('index'))

    # get the submitted end time (which has already been pattern matched) OR get current rounded time
    end = request.forms.get('completeEnd') or Record.getCurrentRoundedTime()

    # get name and date cookies
    name, date = getCookies(request)

    #######################################################

    # get records from file
    records = Record.parseRecordsFromFile(name, date)

    # get particular record to complete
    record = records[index]

    # set the end time
    record.setEnd(end)

    # calculate and set duration
    record.calculateAndSetDuration()

    # add the new duration to the subtotal
    Record.addToSubtotal(name, date, record.duration)

    # write back record
    records[index] = record
    Record.writeRecords(name, date, records)

    #######################################################

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### returns a list (read from file) of updates
@route('/viewUpdates')
def view_updates():

    updates = []

    try:
        f = open("UPDATES", 'r')
        updates = filter(None, f.read().split("\n"))
        f.close()
    except IOError:
        updates = "Updates not found."

    return template('updates', updates=updates)

########################################################################################################
########################################################################################################
########################################################################################################

@route('/toggleBillable', method="POST")
def toggle_billable():

    name, date = getCookies(request)

    index = int(request.forms.get('index'))
    billable = request.forms.get('billable')

    records = Record.parseRecordsFromFile(name, date)

    r = records[index]

    if r.billable == "Y":
        r.billable = "N"
    else:
        r.billable = "Y"

    records[index] = r

    Record.writeRecords(name, date, records)

    redirect('hours')


@route('/toggleEmergency', method="POST")
def toggle_emergency():

    name, date = getCookies(request)

    index = int(request.forms.get('index'))
    emergency = request.forms.get('emergency')

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
@route('/email', method="POST")
def email_records():

    #######################################################

    # get name and date cookies
    name, date = getCookies(request)

    # sets flag based on user's confirmation / denial from popup alert
    emailConfirm = request.forms.get("emailConfirm")

    #######################################################

    subtotal = Record.readSubtotal(name, date) or '0.0'

    #######################################################

    curTimeShort = time.strftime("%m/%d")

    sender = "zamalchi@intranet.techsquare.com"
    subject = "Hours {0} (Subtotal: {1})".format(curTimeShort, subtotal)
    body = ""

    #######################################################

    if (emailConfirm == "true") and name:

        # try to open file with user's name and retrieve data
        records = Record.parseRecordsFromFile(name, date)

        for r in records:
            body += r.emailFormat() + "\n"

        message = "Subject: %s\n\n%s" % (subject, body)

        try:
            mail = smtplib.SMTP("localhost")
            mail.sendmail(sender, receivers, message)
            mail.quit()

        except smtplib.SMTPException:
            pass

    redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


########################################################################################################
######################################  	MISC ROUTES END	   ###########################################
########################################################################################################
