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

DATA.date_title = dt.datetime.strftime(DATA.date, "%a %d %b : %Y-%m-%d")

# iff any record is pending will this be true
# it's used for modifying the subtotal with "*" to show there are pending records
DATA.pending_records = any(r.duration == recorder.PENDING_CHAR for r in DATA.records)

# get all records as a string with each encased in <p></p>
DATA.record_string = "".join("<p>{record}</p>".format(record=record.emailFormat()) for record in DATA.records)

#########################################################################################################

ider = labeler.Labeler(len(DATA.records)-1)
namer = labeler.Labeler()

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
	
	<%
	include('header.tpl', DATA=DATA)
	%>

	<div class="row">
	<div class="col-md-10">
	<div class="records">
		
		<div class="panel-group" id="accordion">
			
			<!-- NEW RECORD -->
			<div class="panel panel-default">
				<%
				previousRecord = recorder.getPrevRecord(DATA.records, len(DATA.records))

				FORM = argparse.Namespace()
				FORM.index = -1
				FORM.start = previousRecord.fend if previousRecord and not previousRecord.isPending() else ""
				FORM.end = ""
				FORM.min = previousRecord.fstart if previousRecord else "0000"
				FORM.max = "2345"
				FORM.notes = DATA.notes if DATA.anchor == str(FORM.index) else ""

				include('new_record_header.tpl', numRecords=len(DATA.records))
				include('record_form.tpl', FORM=FORM)
				%>
			</div>

			<!-- EXISTING RECORDS -->
			% for record in reversed(DATA.records):
				
				<div class="panel panel-default">
					<%
					previousRecord = recorder.getPrevRecord(DATA.records, ider.i)
					nextRecord = recorder.getNextRecord(DATA.records, ider.i)

					DISPLAY = argparse.Namespace()
					DISPLAY.record = record
					DISPLAY.index = ider.i

					FORM = argparse.Namespace()
					FORM.index = ider.i
					FORM.start = previousRecord.fend if previousRecord and not previousRecord.isPending() else ""
					FORM.end = nextRecord.fstart if nextRecord else ""
					FORM.min = previousRecord.fstart if previousRecord else "0000"
					FORM.max = nextRecord.fend if nextRecord and not nextRecord.isPending() else "2345"
					FORM.notes = DATA.notes if DATA.anchor == str(FORM.index) else ""

					include('record_display.tpl', DISPLAY=DISPLAY)
					include('record_form.tpl', FORM=FORM)
					%>
				</div>

				% ider.dec()
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

