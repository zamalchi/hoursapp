<%
import argparse
import datetime as dt
import time

import modu.labeler as labeler
import modu.recorder as recorder

# TODO: continue reconstructing the templates ; use the psuedocode ; try starting over and building up if stuck

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
DATA.record_string = "".join("<p>{record}</p>".format(record=r.emailFormat()) for record in DATA.records)

#########################################################################################################
%>

<!DOCTYPE html>
<html>

<head>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="css/hours.css" />
 	<link rel="shortcut icon" href="favicon.ico" />

 	<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>


<!-- TODO: is the message needed here? -->
<body data-index="{{DATA.anchor}}" data-server-response="{{DATA.msg}}">

<!-- default anchor tag -->
<a name="-1"></a>
<!-- TODO: is this needed / can it be done differently? -->
<input type="hidden" id="num-records" value="{{len(DATA.records)}}" />


<div class="container" name="main">

<%
include('hours_header.tpl', DATA=DATA)
%>


<%
"""
LAYOUT:

header

new record header
record form

for each record:
	record display
	record form

look at bootstrap code to figure out panels and media and such
"""
%> 

<div class="row">
<div class="col-md-10">
<div class="records">
	
	<div class="panel-group" id="accordion">
		
		<div class="panel panel-default">
			% include('new_record_header.tpl')
			% include('record_form.tpl')
		</div>

		% for record in DATA.records:
			
			<div class="panel panel-default">
				% include('record_display.tpl', record=record)
				% include('record_form.tpl')
			</div>
			
		% end

	</div>

</div>
</div>
</div>

<!-- Creates an initial form if there are no records yet; otherwise, it doesn't exist -->
<%'''
% if not records:
<!-- INPUTS -->
<div class="row">
<div class="col-md-10">
	<!-- PANEL -->
	<div class="records">
		<div class="panel panel-default">
			
			<% 
			include('hours_panel_form.tpl', DATA=DATA, i=0,
				form_start="", form_end="", min="0000", max="2345",
				is_new_record=False, is_initial_record=True)
			%>

		</div>
	</div>
</div>
</div> 
'''
%>

<!-- Creates a series of records; each record has its own form; the records toggle accordion-style -->

% else:
<div class="row">
<div class="col-md-10">
	<div class="records">
		<div class="panel-group" id="accordion">
			% records = filter(None, records) # remove empty elements from records 

			<!-- NEW RECORD FORM START -->
			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->

			<div class="panel panel-default">
				
				<!-- ######################################################################################################### -->
				<!-- PANEL HEADING START -->
  			
  			% include('hours_panel_display.tpl',
  				% r=None, i=len(records), notes=notes,
  				% is_new_record=True)
  			
  			<!-- PANEL HEADING END -->
  			<!-- ######################################################################################################### -->


  			<!-- ######################################################################################################### -->
  			<!-- PANEL COLLAPSE/BODY START -->
  			<!-- differentiated because this form stays open: class="in" -->
  			<%
  			namer = labeler.Labeler()
  			ider = labeler.Labeler(len(records))
				%>
				
				<div class="panel-collapse collapse" name={{namer.record()}} id={{ider.record()}} >
  				<%
  				form_start = ""

  				min = "0000"
  				max = "2345"

  				prev_record = recorder.getPrevRecord(records, ider.i)
    				
  				if prev_record:
  					if (prev_record.end != recorder.PENDING_CHAR):
  						form_start = prev_record.fend
  					end

  					min = prev_record.start 
  				end

  				form_notes = ""
  				if anchor == "-1":
  					form_notes = notes
  				end

  				include('hours_panel_form.tpl',
  					name=name, date=date, notes=form_notes,
  					labels=labels, i=len(records),
  					form_start=form_start, form_end="", min=min, max=max,
  					is_new_record=True, is_initial_record=False)
  				%>
  			</div>
  			
  			<!-- PANEL BODY/COLLAPSE END -->
  			<!-- ######################################################################################################### -->
		
			</div>
			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->
			<!-- NEW RECORD FORM END -->


			<hr />


			<!-- FOR EACH RECORD START -->
			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->

			<!-- PROVIDES NAMES FOR HTML ELEMS -->
			% namer = labeler.Labeler()
			<!-- PROVIDES IDS FOR HTML ELEMS -->
			% ider = labeler.Labeler(len(records)-1)

			<!-- RECORDS ARE DISPLAYED IN REVERSE -->
			% for r in reversed(records):

				<!-- PANEL START -->
				<div class="panel panel-default">

					<!-- ######################################################################################################### -->
					<!-- PANEL HEADING START -->					    			
    			
    			% include('hours_panel_display.tpl',
    				% r=r, i=ider.i,
    				% is_new_record=False)
    			
    			<!-- PANEL HEADING END -->
    			<!-- ######################################################################################################### -->

					<!-- ######################################################################################################### -->
    			<!-- PANEL COLLAPSE/BODY START -->
  				<div class="panel-collapse collapse" name={{namer.record()}} id={{ider.record()}} >
  					
  					<!-- form_start = prev_record.fend -->
  					<!-- form_end =  r.fstart -->
  					<%
    				form_start = ""
    				form_end = r.fstart

    				min = "0000"
    				max = "2345"
    				if (r.end != recorder.PENDING_CHAR):
    					max = r.end
    				end

    				prev_record = recorder.getPrevRecord(records, ider.i)
    				
    				if prev_record:
    					if (prev_record.end != recorder.PENDING_CHAR):
    						form_start = prev_record.fend
  						end

  						min = prev_record.start 
    				end

  					form_notes = ""
  					if anchor == str(ider.i):
  						form_notes = notes
  					end

  					include('hours_panel_form.tpl',
  						name=name, date=date, notes=form_notes,
  						labels=labels, i=ider.i,
  						form_start=form_start, form_end=form_end, min=min, max=max,
  						is_new_record=False, is_initial_record=False)
    				%>
    			</div>					    			
    			<!-- PANEL BODY/COLLAPSE END -->
					<!-- ######################################################################################################### -->

				</div>
				<!-- PANEL END -->

				<hr />
				
				<!-- Increment counter after -->
				% ider.dec()

			% end # end for each record

			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->
			<!-- FOR EACH RECORD END -->
		

			<!-- X -->
			<!-- X -->
			<!-- X -->

			
		</div> <!-- /.panel-group -->
	</div> <!-- /.records -->
</div> <!-- /.col-md- -->
</div> <!-- /.row -->
% end # if/else

	<!-- ######################################################################################################### -->
	<!-- ********************************************************************************************************* -->
	<!-- ######################################################################################################### -->
	<!-- ********************************************************************************************************* -->
	<!-- RECORDS LIST END -->

</div> <!-- /.container -->


<!-- jquery must come first as it's required by bootstrap -->
<script src="js/jquery-3.1.0.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<%
include('js_functions.tpl')
%>
</body>

</html>

