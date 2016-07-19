if (__name__ == "__main__"):
	print("Run webapp through wrapper.")
	print("Exiting...")
	exit()


#TO RUN FROM WRAPPER CLASSES:
# - csvInit(readerFile)
# - smtpInit(mailTo)
# - setClusterName(cname)
# - setDevMode(dmode)

import os
#import csv
import time
import smtplib
import sys
#import zipfile

#apache
os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

from bottle import Bottle, route, run, request, response, template, static_file, default_app, redirect, SimpleTemplate, url, get, post

# Record class
from Record import Record
# Labeler class
from Labeler import Labeler
namer = Labeler()


# for css reading in templates
SimpleTemplate.defaults["url"] = url

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

########################################################################################################


# for css reading in templates
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')


########################################################################################################
######################################  	HOURS FORM START	 ###########################################
########################################################################################################
'''
$ <-- done

TODO: 
	subtotal counter
		modified by adding/removing records

	maybe: ability to drag and drop records into different order, if that's really wanted by sb

	finish commenting Record methods
	
	bootlint

	variables and passing them to other templates

	then also finish doing css for templates, once it fully works

	figure out why SMTP isn't sending properly (even on the account webapp)
'''

########################################################################################################
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
	name = request.get_cookie(namer.name()) or ""
	start = request.get_cookie(namer.start()) or ""
	#######################################################

	# try to open file with user's name and retrieve data
	# for each record, create a new Record object and add to list to pass to template
	# list of records as [obj]
	records = Record.parseRecordsFromFile(name)
	
	# DEBUG
	# print("\n***DEBUG***")
	# for r in records:
	# 	print(r)
	# print("***********\n")

	#######################################################
	return template('hours', records=records, name=name, start=start)


########################################################################################################
########################################################################################################
########################################################################################################

@route('/hours', method="POST")
def hours_post():
	
	#######################################################	
	# name of user
	name = request.forms.get(namer.name()).strip()
	
	# index for inserting new Record into the list of records
	index = int(request.forms.get(namer.insert()))

	#######################################################
	# parses form data and returns a Record obj
	new_record = Record.getRecordFromHTML(request)

	#######################################################

	# reads and parses Records on file
	records = Record.parseRecordsFromFile(name)

	#######################################################

	# if the cookie is set, the user has pulled any existing files
	# if there are no existing files, the cookie will be null
	records_pulled = request.get_cookie("name")

	if records and not records_pulled:
		# append to the end of unpulled existing records
		# prevents adding to the beginning of an unexpected list
		records.append(new_record)
		#print("Appending to list")
	else:
		#print("Inserting in list at index:", index)
		# insert new record at index provided from template form
		records.insert(index, new_record)
		Record.adjustAdjacentRecords(records, index)

	#for i in range(len(records)):
	#	Record.adjustAdjacentRecords(records, i)
	
	# write back updated list
	Record.writeRecords(name, records)
	#######################################################

	response.set_cookie("name", (name or ""))
	#response.set_cookie("start", end) # end of record becomes start of next record

	redirect('hours')


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################











########################################################################################################
########################################################################################################
########################################################################################################

@route('/setName', method="POST")
def set_name():
	# get name of user provided in specified field
	name = request.forms.get("setName")

	# set name cookie
	response.set_cookie("name", (name or ""))

	# redirect to /hours to read file
	redirect('hours')


########################################################################################################
########################################################################################################

### deletes records of current user
@route('/delete', method="POST")
def delete_records():
	# get the name cookie
	name = request.get_cookie("name")
	if name:
		# delete both of the user's record files
		Record.deleteRecords(name)

	# delete the name cookie
		response.set_cookie("name", "")

	# redirect back to hours page
	redirect('hours')

########################################################################################################
########################################################################################################

### deletes a single record
@route('/deleteOne', method="POST")
def delete_single_record():

	# get w/o last char, since it comes in with a trailing '/'
	index = int(request.forms.get('recordIndex')[:-1])
	# print("unedited index in deleteOne:", request.forms.get('recordIndex'))

	# get name cookie
	name = request.get_cookie("name")

	if name:
		try:
			# read and parse records from file
			records = Record.parseRecordsFromFile(name)

			# delete record
			del records[index]
			#records = records[:index] + records[index+1:]

			if records:
				Record.writeRecords(name, records)
			else:
				# if no records are left, delete the file
				Record.deleteRecords(name)

		except IOError:
			pass

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


@route('/view', method="POST")
def viewRecords():
	# get name cookie
	name = request.get_cookie("name")

	if name:
		try:
			# read and parse records from file
			records = Record.parseRecordsFromFile(name)
			return template('view', records=records)

		except IOError:
			redirect('hours')

########################################################################################################
######################################  	HOURS FORM END		 ###########################################
########################################################################################################

