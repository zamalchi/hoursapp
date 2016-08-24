<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>

 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
 	<link rel="shortcut icon" href="{{ url('static', filename='favicon.ico') }}" />
</head>

<body>

	% from Record import Record

	% import time
	% date_obj = time.strptime(date, "%Y-%m-%d")
	% date_title = time.strftime("%a %d %b : %Y-%m-%d", date_obj)

	% from Labeler import Labeler

	<!-- ######################################################################################################### -->
	<!-- SCRIPTS START -->	

	% include('hours_js_functions.tpl')

	<!-- SCRIPTS END -->
	<!-- ######################################################################################################### -->

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


	<!-- X -->
	<!-- X -->
	<!-- X -->


	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->

	<div class="container" name="main">

		<!-- ######################################################################################################### -->			
		<!-- ######################################################################################################### -->
		<!-- HEADER START -->
		
		% include('hours_header.tpl', name=name,
			% sender=sender, receivers=receivers, 
			% record_string=record_string, 
			% pending_records=pending_records,
			% subtotal=subtotal, daily_subtotal=daily_subtotal,
			% date_title=date_title, month=month)
		
		<!-- HEADER END -->
		<!-- ######################################################################################################### -->
		<!-- ######################################################################################################### -->

		<!-- X -->
		<!-- X -->

		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- NO INITIAL RECORDS START -->
		<!-- Creates an initial form if there are no records yet; otherwise, it doesn't exist -->
		
		% if not records:
			<!-- INPUTS -->
			<div class="row">
				<div class="col-md-10">
					<!-- PANEL -->
					<div class="records">
						<div class="panel panel-default">
							
							% include('hours_panel_form.tpl',
								% name=name, date=date,
								% labels=labels, i=0,
								% prev_start="", prev_end="",
								% is_new_record=False, is_initial_record=True)
						
						</div>
					</div>
				</div>
			</div> 
		
		<!-- NO INITIAL RECORDS END -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->

		<!-- X -->
		<!-- X -->
		<!-- X -->

		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- RECORDS LIST START -->
		<!-- Creates a series of records; each record has its own form; the records toggle accordion-style -->

		% else:
			<div class="row">
				<div class="col-md-10">
					<div class="records">
						<div class="panel-group" id="accordion">
							% records = filter(None, records) # remove empty elements from records 

							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->
							<!-- NEW RECORD FORM START -->

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
		    				<div class="panel-collapse collapse in" name={{namer.record()}} id={{ider.record()}} >
			    				
			    				% include('hours_panel_form.tpl',
			    					% name=name, date=date,
			    					% labels=labels, i=len(records),
			    					% prev_start=records[-1].fend, prev_end="",
			    					% is_new_record=True, is_initial_record=False)
			    			
			    			</div>
			    			
			    			<!-- PANEL BODY/COLLAPSE END -->
			    			<!-- ######################################################################################################### -->
						
							</div>
							<!-- NEW RECORD FORM END -->
							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->


							<hr />


							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->
							<!-- FOR EACH RECORD START -->

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
			    					
			    					% include('hours_panel_form.tpl',
			    						% name=name, date=date,
			    						% labels=labels, i=ider.i,
			    						% prev_start="", prev_end=r.fstart,
			    						% is_new_record=False, is_initial_record=False)
				    			
				    			</div>					    			
				    			<!-- PANEL BODY/COLLAPSE END -->
									<!-- ######################################################################################################### -->

								</div>
								<!-- PANEL END -->

								<hr />
								
								<!-- Increment counter after -->
								% ider.dec()
								<!-- set the current end time to prev_start for possible use in the next_record -->
								% prev_start = r.fend

							% end # end for each record

							<!-- FOR EACH RECORD END -->
							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->
						
							<!-- X -->
							<!-- X -->

							
							</div> <!-- /.panel-group -->
						</div> <!-- /.records -->
					</div> <!-- /.col-md- -->
			</div> <!-- /.row -->
		% end # if/else

		<!-- RECORDS LIST END -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->

	</div> <!-- /.container -->

<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
<script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

</body>

</html>

