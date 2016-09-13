
### INSTRUCTIONS #######################################################################################

# from Record import \
#   Record
#   RecordMalformedException (required by Record)

# (optional) after importing, set:
#   Record.rootDir - default: '.'
#   Record.hoursDir - default: './hours'

### PACKAGES ###########################################################################################

import time
import os

### IMPORTS ############################################################################################

### RUNNING AS MAIN ####################################################################################

if __name__ == "__main__":
    print("Import class: from Record import Record, RecordMalformedException")
    print("Exiting...")
    exit()

########################################################################################################
#######################################  	CLASS DEF START	 #############################################
########################################################################################################


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# noinspection SpellCheckingInspection
class Record:

    ### CLASS VARIABLES ####################################################################################

    # default values : set after importing class
    rootDir = "."
    hoursDir = os.path.join(rootDir, "hours")

    # used as a placeholder for the end time in an ongoing record
    # it is replaced when the next record is created (with the new start time)
    PENDING_CHAR = "***"

    ########################################################################################################

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

    ### GENERATE FILE NAME: (YYYY-MM-DD-NAME) ##############################################################
    @staticmethod
    def getFileName(name, date):

        # get current date if supplied date is ""
        date = date or time.strftime("%Y-%m-%d")

        # "-" between date and name in filename
        date += "-"

        # return filename
        return os.path.join(Record.hoursDir, date + name)

    ### GENERATE FILE NAME: (.YYYY-MM-DD-NAME) #############################################################
    @staticmethod
    def getHiddenFileName(name, date):

        # get current date if supplied date is ""
        date = date or time.strftime("%Y-%m-%d")

        # "-" between date and name in filename
        date += "-"

        # return filename: uses hidden version of the file, since it contains extra info (durationLocked)
        return os.path.join(Record.hoursDir, "." + date + name)

    ### GENERATE SUBTOTAL FILENAME: (YYYY-MM-NAME-subtotal) ################################################
    @staticmethod
    def getSubtotalFileName(name, date):

        #######################################################

        if not date:
            # if not supplied, get current date
            date = date or time.strftime("%Y-%m")

        else:
            # turn date into date object
            date_obj = time.strptime(date, "%Y-%m-%d")

            # get year from date object
            year = time.strftime("%Y", date_obj)

            # get adjusted month from date
            month_int = Record.getSubtotalMonthInt(date)

            # format month int into string
            month = str(month_int).zfill(2)

        #######################################################

        # ("YYYY-MM-")
        date = year + "-" + month + "-"

        # ("DIR/.YYYY-MM-subtotal-NAME")
        return os.path.join(Record.hoursDir, "." + date + "subtotal-" + name)

    ########################################################################################################
    ### GENERATOR METHODS END ##############################################################################

    #
    #

    ### IO METHODS START ###################################################################################
    ########################################################################################################

    ### READ RECORDS FROM FILE #############################################################################
    @staticmethod
    def readRecords(name, date):

        #######################################################

        # set filename: uses hidden version of the file, since it contains extra info (durationLocked)
        fileName = Record.getHiddenFileName(name, date)

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
    @staticmethod
    def writeRecords(name, date, records):

        #######################################################

        # set filename
        fileName = Record.getFileName(name, date)

        # set hidden filename: used to store extra information (durationLocked)
        hiddenFileName = Record.getHiddenFileName(name, date)

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
    @staticmethod
    def deleteRecords(name, date):

        #######################################################

        # set filename
        fileName = Record.getFileName(name, date)

        # set hidden filename: used to store extra information (durationLocked)
        hiddenFileName = Record.getHiddenFileName(name, date)

        #######################################################

        # system calls to delete both normal and hidden file
        os.system("rm -f " + fileName)
        os.system("rm -f " + hiddenFileName)

    ### READS SUBTOTAL FILE ################################################################################
    @staticmethod
    def readSubtotal(name, date):

        # get filename
        fileName = Record.getSubtotalFileName(name, date)

        try:
            f = open(fileName, 'r')
            subtotal = f.read()
            f.close()
            return float(subtotal or 0.0)
        except IOError:
            return 0.0

    ### WRITES SUBTOTAL FILE ###############################################################################
    @staticmethod
    def writeSubtotal(name, date, subtotal):

        # get filename
        fileName = Record.getSubtotalFileName(name, date)

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

    ### ADDS TO SUBTOTAL FILE ##############################################################################
    @staticmethod
    def addToSubtotal(name, date, amount):

        # if the duration passed in is valid (it exists / not pending)
        if amount != Record.PENDING_CHAR:

            # read in subtotal
            subtotal = Record.readSubtotal(name, date)

            # add the duration
            subtotal += float(amount)

            # write back the updated subtotal
            Record.writeSubtotal(name, date, subtotal)

    ### SUBTRACTS FROM SUBTOTAL FILE #######################################################################
    @staticmethod
    def subtractFromSubtotal(name, date, amount):

        # if the duration passed in is valid (it exists / not pending)
        if amount != Record.PENDING_CHAR:

            # read in subtotal
            subtotal = Record.readSubtotal(name, date)

            # subtract the duration
            subtotal -= float(amount)

            # write back the updated subtotal
            Record.writeSubtotal(name, date, subtotal)

    ### GET SUBTOTAL MONTH INTEGER #########################################################################
    @staticmethod
    def getSubtotalMonthInt(date):

        # convert string to date object
        date_obj = time.strptime(date, "%Y-%m-%d")

        # get the integer of the day
        day_int = int(time.strftime("%d", date_obj))

        # get the integer of the month
        month_int = int(time.strftime("%m", date_obj))

        # if the day is past the 25th, increase the month by 1
        # this is when the pay period switches over to the next month
        if day_int > 25:
            month_int += 1

        return month_int

    ### GET SUBTOTAL MONTH STRING ##########################################################################
    @staticmethod
    def getSubtotalMonth(date):
        # defines the pay period ; used for labeling the subtotal counter

        # get integer of month
        month_int = Record.getSubtotalMonthInt(date)

        # convert to date object
        month_obj = time.strptime(str(month_int), "%m")

        # conver to month string
        month = time.strftime("%b", month_obj)

        return month

    ### GET SUBTOTAL COUNT #################################################################################
    @staticmethod
    def countSubtotal(records):

        new_subtotal = 0.0

        for r in records:

            # if it is a valid duration
            if r.duration != Record.PENDING_CHAR:

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
    @staticmethod
    def parseRecords(raw_records):

        # filter out empty records
        r_r = filter(None, raw_records)

        # return list mapped to Record objects
        return [Record(r) for r in r_r]

    ### READ RECORDS FILE AND PARSE INTO RECORD OBJECTS ####################################################
    @staticmethod
    def parseRecordsFromFile(name, date):

        # read in records
        raw_records = Record.readRecords(name, date)

        # return parsed Record objects
        return Record.parseRecords(raw_records)

    ### PARSE HTML FORM INTO RECORD OBJECT #################################################################
    @staticmethod
    def getRecordFromHTML(request):

        #######################################################

        name = request.forms.get('name').strip().lower()

        start = Record.parseTime(request.forms.get('start'))
        end = Record.parseTime(request.forms.get('end'))
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
            duration = Record.getDuration(start, end)

        # if end is not supplied
        else:
            # replace duration with Record.PENDING_CHAR
            duration = Record.PENDING_CHAR

        #######################################################

        # restore colon in start time
        start = Record.formatTime(start)

        # if end is supplied
        if end:
            # restore the colon
            end = Record.formatTime(end)

        # if not supplied
        else:
            # set as Record.PENDING_CHAR
            end = Record.PENDING_CHAR

        #######################################################

        # get the date cookie or default to current date
        date = request.get_cookie("date") or time.strftime("%Y-%m-%d")

        # set start datetime
        startTime = date + " " + start

        # set end datetime
        endTime = date + " " + end

        #######################################################

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

        print("GOT RECORD FROM HTML")
        print("RECORD: " + record_string)
        print("END TIME: " + Record(record_string).end)
        print("PENDING CHAR: " + Record.PENDING_CHAR)

        #######################################################

        return Record(record_string)

    ########################################################################################################
    ### PARSING METHODS END ################################################################################

    #
    #

    ### TIME METHODS START #################################################################################
    ########################################################################################################

    ### PARSE TIME INTO ("HHMM") FORMAT ####################################################################
    @staticmethod
    def parseTime(time):

        if time:
            # return if pending
            if time == Record.PENDING_CHAR:
                return time

            # removes colon and adds leading '0' if missing
            return str(time.strip()).translate(None, ':').zfill(4)

        return ""

    ### FORMAT TIME INTO ("HH:MM") FORMAT ##################################################################
    @staticmethod
    def formatTime(time):

        # ensures time is parsed correctly
        p = Record.parseTime(time)

        # adds a colon between hours and minutes
        return str(p)[:2] + ':' + p[2:]

    ### CONVERT TIME INTO NUMBER OF MINUTES ################################################################
    @staticmethod
    def getMinFromTime(time):

        # checks for not present time
        if time == Record.PENDING_CHAR:
            return None

        # if it is an int, it has already been processed, so return
        # ex: called from getDuration()
        if type(time) == int:
            return time

        # ensures it is parsed
        p = Record.parseTime(time)

        # returns number of minutes
        return (int(p[:2]) * 60) + int(p[2:])

    ### CONVERT NUMBER OF MINUTES INTO ("HHMM") ############################################################
    @staticmethod
    def getTimeFromMin(min):

        # ensures int type
        i = int(min)

        # gets hours through integer division
        hours = str(i/60).zfill(2)

        # gets minutes through modulus
        minutes = str(i%60).zfill(2)

        # return ("HHMM")
        return hours + minutes

    ### CALCULATE THE DURATION USING THE START AND END TIMES ###############################################
    @staticmethod
    def getDuration(start, end):

        # get number of minutes from start time
        s = Record.getMinFromTime(start)

        # get number of minutes from end time
        e = Record.getMinFromTime(end)

        # return number of hours as float (x.xx)
        return float((e - s)/float(60))

    ### ROUND PASSED IN TIME TO NEAREST 15-MINUTE MARK #####################################################
    @staticmethod
    def roundTime(t):

        #######################################################

        # ensure the time is parsed correctly
        time = Record.parseTime(t)

        # parse the hours
        hours = int(time[:2])

        # parse the minutes
        minutes = int(time[2:])

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
    @staticmethod
    def getCurrentRoundedTime():

        # get current time
        t = time.strftime("%H%M")

        # round it to 15-minute mark
        return Record.roundTime(t)

    ########################################################################################################
    ### TIME METHODS END ###################################################################################

    #
    #

    ### RECORD METHODS START ###############################################################################
    ########################################################################################################

    ### RETURNS PREVIOUS RECORD IN LIST or NONE ############################################################
    @staticmethod
    def getPrevRecord(records, index):

        try:
            # if the previous index is a valid index
            if index-1 >= 0:

                # return the previous record
                return records[index-1]

        except IndexError:
            pass

        # if returning the prev record was unsuccessful, return None
        return None

    ### RETURNS NEXT RECORD IN LIST or NONE ################################################################
    @staticmethod
    def getNextRecord(records, index):

        try:
            # if the next index is a valid index
            if index+1 < len(records):

                # return the next record
                return records[index+1]

        except IndexError:
            pass

        # if returning the prev record was unsuccessful, return None
        return None


    ### CHECKS IF RECORD OVERLAPS WITH ADJACENT RECORDS AND ADJUSTS ADJACENT START/END TIMES ACCORDINGLY ###
    @staticmethod
    def adjustAdjacentRecords(records, index):

        #######################################################

        # if the records list is empty, print error statement and return from function
        if not records:
            print("ERROR: empty records list passed into Record.adjustAdjacentRecords()")
            return

        #######################################################

        # get the newly inserted record
        new_record = records[index]

        # get the previous record if it exists
        prev_record = Record.getPrevRecord(records, index)

        # get the next record if it exists
        next_record = Record.getNextRecord(records, index)

        #######################################################
        # FUNCTION: SETS PREVIOUS RECORD'S END TIME

        if prev_record:

            # if the previous record's end time has not been supplied
            if prev_record.duration == Record.PENDING_CHAR:

                # set the previous record's end time to be the new record's start time
                prev_record.setEnd(new_record.start)

                # the new record *FINISHES* the previous record
                # visually: [START]~previous~[PENDING --> END]   [START]~new~[PENDING|END]

        #######################################################
        # FUNCTION: SHIFTS NEXT RECORD'S START TIME (IF PARTIAL RECORD)

        if next_record:

            # if (the next record's end time has not been supplied) and (the new record has an end time)
            # NOTE: if the next record doesn't have a supplied end time, the new record MUST have an end time (required by HTML input)
            if (next_record.duration == Record.PENDING_CHAR) and (new_record.end != Record.PENDING_CHAR):

                # supply the next record's start time using the new record's end time
                next_record.setStart(new_record.end)

                # the new record *SHIFTS* the next record forward to match its end time
                # visually: [START]~new~[END]   [START --> MODIFIED START]~next~[PENDING]


            ####### REQUIRED TAG IN HTML END TIME INPUT BYPASSES THIS CODE ######

            # FUNCTION: SETS NEW RECORD'S END TIME (REDUNDANT)

            # NOTE: this case seems to work, but the HTML requires the end time in this case, so this isn't currently executed

            # if (a next record exists) and (the new record has a pending duration)
            if new_record.duration == Record.PENDING_CHAR:

                # set the end time of the new record to be the next record's start time
                new_record.setEnd(next_record.start)

            #######

        #######################################################

        # after ensuring the previous record's end time is set

        if prev_record:

            # calculate the previous record's duration using its start and end times
            prev_record.duration = Record.getDuration(prev_record.start, prev_record.end)

            # update the record in the list
            records[index-1] = prev_record

            # calculate overlap : new_start - prev_end : if overlap => negative duration
            # if the new start time is less than the previous end time: adjustment needed
            overlap = Record.getDuration(prev_record.end, new_record.start)

            # if there was overlap
            if overlap < 0:

                # modify the prev_end time by subtracting the overlap duration
                prev_record.modifyEnd(overlap)

        #######################################################

        # if the next record exists, the new record has been ensured to be complete (can't have two pending records)

        if next_record:

            # calculate the new record's duration using its start and end times
            new_record.duration = Record.getDuration(new_record.start, new_record.end)

            # update the record in the list
            records[index] = new_record

            # calculate overlap : next_start - new_end : if overlap => negative duration
            # if the next record's start is less than the new record's end: adjustment needed
            overlap = Record.getDuration(new_record.end, next_record.start)

            # if there was overlap
            if overlap < 0:

                # modify next_start time by subtracting overlap duration
                next_record.modifyStart(overlap)



    ### CHECKS IF A NEW RECORD IS TEMPORALLY SOUND ITSELF AND IN RELATION TO ADJACENT RECORDS ##############
    @staticmethod
    def checkIfValid(records, record, index):

        ################################################

        # get records to check positioning of the new record
        prev = next = None

        # for checking the relationship with the adjacent records
        prevValid = nextValid = False

        ################################################
        ################################################

        if records:
            print("RECORDS!")
            prev = Record.getPrevRecord(records, index)
            next = Record.getNextRecord(records, index)
        else:
            print("PREV: {0}".format(prev))
            print("NEXT: {0}".format(next))

        ################################################

        # either there is no previous record or the new start is greater than the previous start
        if (not prev) or (prev and (record.start > prev.start)):
            prevValid = True
            print("PREV VALID CHECK: {0}".format(prevValid))

        # either there is no next record or the new end is less than the next end
        if (not next) or (next and (record.end < next.end)):
            nextValid = True
            print("NEXT VALID CHECK: {0}".format(nextValid))

        ################################################

        # END != PENDING
        if record.end != Record.PENDING_CHAR:

            print("START < END CHECK: {0}".format(record.start < record.end))
            return record.start < record.end

        ################################################
        ################################################

        # END == PENDING
        else:
            print("END == PENDING")
            # cannot have a pending end time within the list (must be at the end)
            if next:
                print("NEXT, returning False")
                return False

            ################################################

            # can't compare pending end time to record.start
            # so return whether or not both adjacency checks were passed
            else:
                print("PREV AND NEXT CHECK: {0}".format(prevValid and nextValid))
                return prevValid and nextValid

        ################################################
        ################################################

                #
        #         # if end time == pending
        #     # if next
        #         # return false (can't have a missing end time in the middle of the list)
        #     # else
        #         # if start < prev end
        #
        # # else actual end time
        #     # if start >= end
        #         # return false (can't have non-positive duration)
        #     # else return true
        #
        # # the start time must come before the end time
        # if record.end and (record.end != Record.PENDING_CHAR) and (record.start > record.end):
        #     print("RETURN FALSE 1")
        #     print("END: " + record.end)
        #     return False
        #
        #
        #
        #     # if there is no next record, the new record is permitted to not have an end time
        #     if not next and not record.end:
        #         print("RETURN TRUE 1")
        #         return True
        #
        #     # if the end time is less than the previous start --> invalid (covers the previous record)
        #     # if the start time is greater than the next end --> invalid (covers the next record)
        #     if (prev and record.end < prev.start) or (next and record.start > next.end):
        #         print("RETURN FALSE 2")
        #         return False
        #
        # # else True (also if no records, and the new record is valid within itself, then True)
        # print("RETURN TRUE 2")
        # return True

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

    #### INSTANCE METHODS START ############################################################################
    ########################################################################################################
    ########################################################################################################

    #
    #

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

            self.date = start_DT[0]

            #######################################################

            # formatted start ("HH:MM")
            self.fstart = start_DT[1]

            # start ("HHMM")
            self.start = Record.parseTime(self.fstart)

            # formatted end ("HH:MM")
            self.fend = end_DT[1]

            # end ("HHMM")
            self.end = Record.parseTime(self.fend)

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
        self.setDuration(Record.getDuration(self.start, self.end))

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
        i = Record.parseTime(t)

        # format parsed time for fstart (formatted start) field
        s = Record.formatTime(i)

        self.start = i
        self.fstart = s

    ### SET END TIME WHILE ENSURING CORRECT PARSING/FORMATTING #############################################
    def setEnd(self, time):
        t = str(time)

        # parse time for end field
        i = Record.parseTime(t)

        # format parsed time for fend (formatted end) field
        s = Record.formatTime(i)

        self.end = i
        self.fend = s

    ### MODIFY START TIME AND DURATION BY ADDING SUPPLIED AMOUNT ###########################################
    def modifyStart(self, amount):

        # get start time in minutes
        start = Record.getMinFromTime(self.start)

        # convert amount into minutes and add to start time
        new = float(start) + (float(amount)*60)

        # set start to new value (converted back into a string)
        self.setStart(Record.getTimeFromMin(int(new)))

        # modify the duration by subtracting the amount added to the start time
        self.modifyDuration(-float(amount))

    ### MODIFY END TIME AND DURATION BY A SUPPLIED AMOUNT ##################################################
    def modifyEnd(self, amount):

        # get the end time in minutes
        end = Record.getMinFromTime(self.end)

        # convert amount into minutes and add to end time
        new = float(end) + (float(amount)*60)

        # set end to new value (converted back into a string)
        self.setEnd(Record.getTimeFromMin(int(new)))

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

    #
    #

    ########################################################################################################
    ########################################################################################################
    #### INSTANCE METHODS END ##############################################################################

    #
    #
    #
    #

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


########################################################################################################
####################################### CLASS DEF END ##################################################
########################################################################################################

class RecordMalformedException(Exception):
    pass

