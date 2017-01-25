<%
import argparse
import datetime as dt
import time

import modu.labeler as labeler
import modu.recorder as recorder

#########################################################################################################

REGEX = argparse.Namespace()

# used for duration field
REGEX.FLOAT = "(0|[1-9]{1,})(\.(0|25|5|75))?"

# only labels from the list can be entered
# if the labels list is empty, this defaults to accept any string
# "l1|l2|l3|l4..." or "*"
REGEX.LABELS = "({labelsString})".format(labelsString="|".join( [l.split(" | ")[0] for l in DATA.LABELS] ) ) if DATA.LABELS else "*"

# name must be at least two chars and can't contain any special chars
REGEX.NAME = "[a-zA-Z0-9]{2,}"

# times must match 15-minute interval pattern
REGEX.TIME = "(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))"

#########################################################################################################

DATA.dateTitle = dt.datetime.strftime(DATA.date, "%a %d %b : %Y-%m-%d")

# iff any record is pending will this be true
# it's used for modifying the subtotal with "*" to show there are pending records
DATA.pendingRecordsExist = any(r.duration == recorder.PENDING_CHAR for r in DATA.records)

# get all records as a string with each encased in <p></p>
DATA.recordString = "".join("<p>{record}</p>".format(record=record.emailFormat()) for record in DATA.records)

#########################################################################################################

BASE_FORM = lambda index=-1, previousRecord=None, nextRecord=None : argparse.Namespace(
	index = str(index),
	start = previousRecord.fend if previousRecord and not previousRecord.isPending() else "",
	end = nextRecord.fstart if nextRecord else "",
	min = previousRecord.fstart if previousRecord else "0000",
	max = nextRecord.fend if nextRecord and not nextRecord.isPending() else "2345",
	notes = DATA.notes if DATA.anchor == str(index) else "")

BASE_DISPLAY = lambda index, record : argparse.Namespace(
	index = index,
	record = record)

#########################################################################################################

HTML_LABELS = labeler.HTML_LABELS

# this starts as the index 1 beyond the last record
# this value is given to the new-record form
# the last record on the page should have the 0 value
indexCounter = len(DATA.records)

# ider = labeler.Labeler(len(DATA.records)-1)
# namer = labeler.Labeler()

%>

<!DOCTYPE html>
<html>

<head>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="css/hours.css" />
 	<link rel="shortcut icon" href="favicon.ico" />

 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>


<body>
<!-- default anchor tag -->
<a name="-1"></a>


<div class="container" name="main">
	
	% include('header.tpl')

	<div class="row">
	<div class="col-md-10">
	<div class="records">
		
		<div class="panel-group" id="accordion">
			
			<!-- NEW RECORD -->
			<div class="panel panel-default">
				<%

				# FORM = argparse.Namespace()
				# FORM.index = -1
				# FORM.start = previousRecord.fend if previousRecord and not previousRecord.isPending() else ""
				# FORM.end = ""
				# FORM.min = previousRecord.fstart if previousRecord else "0000"
				# FORM.max = "2345"
				# FORM.notes = DATA.notes if DATA.anchor == str(FORM.index) else ""

				# indexCounter should be equal to len(DATA.records)
				# 	giving this form an index 1 beyond the most recent record
				# previousRecord is at index len(DATA.records)-1
				# nextRecord is None (by default)

				previousRecord = recorder.getPrevRecord(DATA.records, len(DATA.records))

				include('new_record_header.tpl', index=indexCounter)
				include('record_form.tpl', FORM=BASE_FORM(index=indexCounter, previousRecord=previousRecord))

				indexCounter -= 1
				%>
			</div>

			<!-- EXISTING RECORDS -->
			% 
			% for record in reversed(DATA.records):
				
				<div class="panel panel-default">
					<%

					# FORM = argparse.Namespace()
					# FORM.index = ider.i
					# FORM.start = previousRecord.fend if previousRecord and not previousRecord.isPending() else ""
					# FORM.end = nextRecord.fstart if nextRecord else ""
					# FORM.min = previousRecord.fstart if previousRecord else "0000"
					# FORM.max = nextRecord.fend if nextRecord and not nextRecord.isPending() else "2345"
					# FORM.notes = DATA.notes if DATA.anchor == str(FORM.index) else ""

					# indexCounter should start at len(DATA.records)-1 and go to 0
					# previousRecord should exist until the last record (index 0, since the list is reversed in this loop)
					# nextRecord should be None during the first iteration (most recent record), and then exist for the rest

					previousRecord = recorder.getPrevRecord(DATA.records, indexCounter)
					nextRecord = recorder.getNextRecord(DATA.records, indexCounter)

					include('record_display.tpl', DISPLAY=BASE_DISPLAY(index=indexCounter, record=record))
					include('record_form.tpl', FORM=BASE_FORM(index=indexCounter, previousRecord=previousRecord, nextRecord=nextRecord))

					# decrement indexCounter
					indexCounter -= 1
					%>
				</div>

			% end

		</div>

	</div>
	</div>
	</div>
</div> <!-- /.container -->


<!-- jquery must come first as it's required by bootstrap -->
<script src="js/jquery-3.1.0.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<%
include('js_functions.tpl')
%>
</body>

</html>

