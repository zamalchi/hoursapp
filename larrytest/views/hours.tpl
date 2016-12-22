<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="/css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="css/hours.css" />

 	<link rel="shortcut icon" href="img/favicon.ico" />

 	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<!-- ######################################################################################################### -->
	<!-- SCRIPTS START -->	

 	<!-- jquery must come first and is required by bootstrap -->
	<script src="js/jquery-3.1.0.min.js"></script>
	<script src="js/bootstrap.min.js"></script>

	% include('hours_js_functions.tpl')

	<!-- SCRIPTS END -->
	<!-- ######################################################################################################### -->

</head>

<body data-index="{{anchor}}" data-server-response="{{msg}}">

<input type="hidden" id="foobar" value="17:45" pattern="(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))" data-min="1345" data-max="1730">

	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->


	<!-- X -->
	<!-- X -->
	<!-- X -->


	<!-- PYTHON VARS START -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->

		<!-- REGEX -->

		<!-- times must match 15-minute interval pattern -->
		% TIME_REGEX = "(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))"

		% NAME_REGEX = "[a-zA-Z0-9]{2,}"

		<!-- used for duration field -->
		% FLOAT_REGEX = "(0|[1-9]{1,})(\.(0|25|5|75))?"

		<!-- only labels from the list can be entered -->
		% LABEL_REGEX = "({0})".format( "|".join( [l.split(" | ")[0] for l in labels] ) )

		<!-- ######################################################################################################### -->

		% from classes.Record import Record

		% import datetime as dt

		% date_title = date.strftime("%a %d %b : %Y-%m-%d")

		% from classes.Labeler import Labeler

		<!-- pending_records is for modifying the subtotal with "*" to show there are pending records -->
		% pending_records = False
		
		<!-- ######################################################################################################### -->

		<!-- GET RECORDS AND DAILY SUBTOTAL -->
		% record_string = ""
		% for r in records:

			% if r.duration == Record.PENDING_CHAR:
				
				% pending_records = True
			% end
			
			% record_string += "<p>" + r.emailFormat() + "</p>"
		% end

		% daily_subtotal = Record.countSubtotal(records)


	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- PYTHON VARS END -->


	<!-- X -->
	<!-- X -->
	<!-- X -->


	<!-- MAIN HTML START -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->

	<!-- default anchor tag -->
	<a name="-1"></a>

	<input type="hidden" id="num-records" value="{{len(records)}}" />


	<div class="container" name="main">

		<!-- HEADER START -->
		<!-- ######################################################################################################### -->			
		<!-- ######################################################################################################### -->
		
		% include('hours_header.tpl', name=name,
			% record_string=record_string, 
			% pending_records=pending_records,
			% subtotal=subtotal, daily_subtotal=daily_subtotal,
			% date_title=date_title, month=Record.getSubtotalMonth(date))
		
		<!-- ######################################################################################################### -->
		<!-- ######################################################################################################### -->
		<!-- HEADER END -->


		<!-- X -->
		<!-- X -->
		<!-- X -->


		<!-- NO INITIAL RECORDS START -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- Creates an initial form if there are no records yet; otherwise, it doesn't exist -->
		
		% if not records:
			<!-- INPUTS -->
			<div class="row">
				<div class="col-md-10">
					<!-- PANEL -->
					<div class="records">
						<div class="panel panel-default">
							
							% include('hours_panel_form.tpl',
								% name=name, date=date, notes=notes,
								% labels=labels, i=0,
								% form_start="", form_end="", min="0000", max="2345",
								% is_new_record=False, is_initial_record=True)
						
						</div>
					</div>
				</div>
			</div> 
		
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- NO INITIAL RECORDS END -->


		<!-- X -->
		<!-- X -->
		<!-- X -->


		<!-- RECORDS LIST START -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
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
			    				% r=None, i=len(records),
			    				% is_new_record=True)
			    			
			    			<!-- PANEL HEADING END -->
			    			<!-- ######################################################################################################### -->


			    			<!-- ######################################################################################################### -->
			    			<!-- PANEL COLLAPSE/BODY START -->
			    			<!-- differentiated because this form stays open: class="in" -->
			    			
			    			% namer = Labeler()
			    			% ider = Labeler(len(records))
		    				<div class="panel-collapse collapse" name={{namer.record()}} id={{ider.record()}} >
			    				
			    				% form_start = ""

			    				% min = "0000"
			    				% max = "2345"

			    				% prev_record = Record.getPrevRecord(records, ider.i)
				    				
			    				% if prev_record:
			    					% if (prev_record.end != Record.PENDING_CHAR):
			    						% form_start = prev_record.fend
			    					% end

			    					% min = prev_record.start 
			    				% end

			    				% form_notes = ""
			    				% if anchor == "-1":
			    					% form_notes = notes
			    				% end

			    				% include('hours_panel_form.tpl',
			    					% name=name, date=date, notes=form_notes,
			    					% labels=labels, i=len(records),
			    					% form_start=form_start, form_end="", min=min, max=max,
			    					% is_new_record=True, is_initial_record=False)
			    			
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
							% namer = Labeler()
							<!-- PROVIDES IDS FOR HTML ELEMS -->
							% ider = Labeler(len(records)-1)

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

				    				% form_start = ""
				    				% form_end = r.fstart

				    				% min = "0000"
				    				% max = "2345"
				    				% if (r.end != Record.PENDING_CHAR):
				    					% max = r.end
				    				% end

				    				% prev_record = Record.getPrevRecord(records, ider.i)
				    				
				    				% if prev_record:
				    					% if (prev_record.end != Record.PENDING_CHAR):
				    						% form_start = prev_record.fend
				    					% end

				    					% min = prev_record.start 
				    				% end

			    					% form_notes = ""
			    					% if anchor == str(ider.i):
			    						% form_notes = notes
			    					% end

			    					% include('hours_panel_form.tpl',
			    						% name=name, date=date, notes=form_notes,
			    						% labels=labels, i=ider.i,
			    						% form_start=form_start, form_end=form_end, min=min, max=max,
			    						% is_new_record=False, is_initial_record=False)
				    			
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

</body>

</html>

