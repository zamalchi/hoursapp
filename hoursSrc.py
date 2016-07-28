if (__name__ == "__main__"):
	print("Run webapp through wrapper.")
	print("Exiting...")
	exit()

#TO RUN FROM WRAPPER CLASSES:
# - smtpInit(mailTo)
# - setDevMode(dmode)
# - labelsInit(labels)

########################################################################################################
########################################################################################################

### PACKAGES ###########################################################################################

import os
import time
import smtplib
import sys

### APACHE #############################################################################################

os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

### IMPORTS ############################################################################################

from bottle import Bottle, route, run, request, response, template, static_file, default_app, redirect, SimpleTemplate, url, get, post

# Record class
from Record import Record
# Labeler class
from Labeler import Labeler
namer = Labeler()

# for css reading in templates
SimpleTemplate.defaults["url"] = url

### DIRECTORY ##########################################################################################

# directory for saving hours information
Record.hoursDir = "hours/"
# if the directory doesn't exist, create it
if not os.path.exists(Record.hoursDir):
	os.makedirs(Record.hoursDir)

### SMTP ###############################################################################################

receivers = []

def smtpInit(mailTo):
	# this is called from the wrapper file
	# sets the admin email
	global receivers
	receivers = [mailTo]

### DEV MODE ###########################################################################################

def setDevMode(dmode):
	global devMode
	devMode = dmode
	print("DEV MODE: " + str(devMode))

# dev print : prints when in dev mode
def devp(msg):
	global devMode
	if devMode:
		print(msg)

### LABELS #############################################################################################

# sets labels for populating dropdown list in /hours
def labelsInit(l):
	global labels
	labels = l

### CSS ROUTING ########################################################################################

# for css reading in templates
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')

### COOKIE GETTERS/SETTERS #############################################################################

### NAME ###
def getNameCookie(request):
	return request.get_cookie("name") or ""

def setNameCookie(response, name):
	response.set_cookie("name", name)

### DATE ###
def getDateCookie(request):
	return request.get_cookie("date") or time.strftime("%Y-%m-%d")

def setDateCookie(response, date):
	response.set_cookie("date", date)

########################################################################################################
########################################################################################################










########################################################################################################
######################################  	HOURS FORM START	 ###########################################
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
	name = getNameCookie(request)
	date = getDateCookie(request)
	
	month = Record.getSubtotalMonth(date)

	start = request.get_cookie(namer.start()) or ""

	subtotal = Record.readSubtotal(name, date)
	#######################################################

	# try to open file with user's name and retrieve data
	# for each record, create a new Record object and add to list to pass to template
	# list of records as Record obj
	records = Record.parseRecordsFromFile(name, date)
	
	#######################################################
	return template('hours', records=records, labels=labels, name=name, date=date, month=month, subtotal=subtotal, start=start)

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
		# when inserting between two records (whose durations are not locked) (i.e. splicing a record in), the subtotal should not change
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
######################################  	HOURS FORM END	 #############################################
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
#####################################  	MISC ROUTES START	   ###########################################
########################################################################################################


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

@route('/setCookies', method="POST")
def set_name():
	# get name of user provided in specified field
	name = request.forms.get("setName") or ""
	date = request.forms.get("setDate") or time.strftime("%Y-%m-%d")

	# set name cookie
	setNameCookie(response, name)
	setDateCookie(response, date)

	# redirect to /hours to read file
	redirect('hours')


########################################################################################################
########################################################################################################
########################################################################################################

### deletes records of current user
@route('/delete', method="POST")
def delete_records():
	# get the name cookie
	name = getNameCookie(request)
	date = getDateCookie(request)

	deleteConfirm = request.forms.get("deleteConfirm")

	# delete the name cookie
	#setNameCookie(response, "")
	#setDateCookie(response, "")

	if (deleteConfirm == "true") and name:
		# get records
		records = Record.parseRecordsFromFile(name, date)
		# get summed duration of records
		summed_subtotal = Record.countSubtotal(records)
		# subtract that amount from the subtotal on file
		Record.subtractFromSubtotal(name, date, summed_subtotal)

		# delete both of the user's record files
		Record.deleteRecords(name, date)

	# redirect back to hours page
	redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################

### deletes a single record
@route('/deleteOne', method="POST")
def delete_single_record():

	# get w/o last char, since it comes in with a trailing '/'
	index = int(request.forms.get('recordIndex')[:-1])
	# print("unedited index in deleteOne:", request.forms.get('recordIndex'))

	# get name cookie
	name = getNameCookie(request)
	date = getDateCookie(request)

	if name:
		try:
			# read and parse records from file
			records = Record.parseRecordsFromFile(name, date)

			# get the duration of the record to be deleted
			deletedRecordDuration = records[index].duration
			# subtract that amount from the subtotal on file
			Record.subtractFromSubtotal(name, date, deletedRecordDuration)

			# delete record
			del records[index]
			#records = records[:index] + records[index+1:]

			Record.writeRecords(name, date, records)

		except IOError:
			pass

	redirect('hours')

########################################################################################################
########################################################################################################

### fill in end time and duration for partial record
@route('/completeRecord', method="POST")
def complete_record():
	name = getNameCookie(request)
	date = getDateCookie(request)

	index = int(request.forms.get("completeIndex"))

	records = Record.parseRecordsFromFile(name, date)

	####
	record = records[index]

	record.setEnd(Record.getCurrentRoundedTime())
	record.getAndSetDuration()
	
	records[index] = record
	####
	
	Record.adjustAdjacentRecords(records, index)
	Record.addToSubtotal(name, date, record.duration)

	Record.writeRecords(name, date, records)

	redirect('hours')


########################################################################################################
########################################################################################################


### emails records
@route('/email', method="POST")
def email_records():
	redirect('hours')

	curTimeLong = time.strftime("%Y %b %d %X")
	curTimeShort = time.strftime("%m-%d")
		
	sender = "root"
	subject = "Hours " + curTimeShort + " (Subtotal: xx.x)"
	body =  ""

	name = request.get_cookie(namer.name()) or ""

	if name:
		# try to open file with user's name and retrieve data
		filePath = Record.hoursDir + "/" + name

		# for each record, create a new Record object and add to list to pass to template
		# list of records as [obj]
		records = Record.parseRecordsFromFile(filePath)

		for r in records:
			body += r.emailFormat() + "\n"

		message = "Subject: %s\n\n%s" % (subject, body)

		try:
			mail = smtplib.SMTP("localhost")
			mail.sendmail(sender, receivers, message)
			mail.quit()
			# print("Sender:", sender, "\nReceivers:", receivers)
			return("<h2>Message sent???</h2>")

		except smtplib.SMTPException:
			return("<h2>Error: could not send email.</h2>")
	 
	else:
		redirect('hours')


# DEPRECTAED
# @route('/view', method="POST")
# def viewRecords():
# 	# get name cookie
# 	name = request.get_cookie("name")
# 	date = request.get_cookie("date") or time.strftime("%Y-%m-%d")

# 	if name:
# 		try:
# 			# read and parse records from file
# 			records = Record.parseRecordsFromFile(name, date)
# 			return template('view', records=records)

# 		except IOError:
# 			redirect('hours')

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


########################################################################################################
######################################  	MISC ROUTES END	   ###########################################
########################################################################################################

