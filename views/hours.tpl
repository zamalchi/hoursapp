<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
</head>

<body>
	% from Labeler import Labeler

	<!-- ######################################################################################################### -->
	<!-- SCRIPTS START -->	
	% include('hours_js_functions.tpl')
	<!-- SCRIPTS END -->
	<!-- ######################################################################################################### -->

	<div class="container">
		<div class="row">
			<div class="col-md-10">
				<h1 id="title">Hours</h1>
			</div>
		</div>

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
					<div class="panel panel-default">
						% include('hours_panel_body.tpl', prev_start="", i=0, name=name, is_new_record=False, is_initial_record=True)
					</div>
				</div>
			</div> 
		<!-- NO INITIAL RECORDS END -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->
		<!-- ######################################################################################################### -->
		<!-- ********************************************************************************************************* -->





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
			    			<!-- PANEL COLLAPSE/BODY START -->
			    			<!-- differentiated because this form stays open: class="in" -->
			    			% namer = Labeler()
			    			% ider = Labeler(len(records))
		    				<div name={{namer.record()}} id={{ider.record()}} class="panel-collapse collapse in">
			    				% include('hours_panel_body.tpl', prev_start=records[-1].fend, i=len(records), name=name, is_new_record=True, is_initial_record=False)
			    			</div>
			    			<!-- PANEL BODY/COLLAPSE END -->
			    			<!-- ######################################################################################################### -->
						
								<!-- ######################################################################################################### -->
								<!-- PANEL HEADING START -->
			    			% include('hours_panel_heading.tpl', r=None, i=len(records), is_new_record=True)
			    			<!-- PANEL HEADING END -->
			    			<!-- ######################################################################################################### -->
							</div>
							<!-- NEW RECORD FORM END -->
							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->

							<hr />

							<!-- PROVIDES NAMES FOR HTML ELEMS -->
							% namer = Labeler()
							<!-- PROVIDES IDS FOR HTML ELEMS -->
							% ider = Labeler(0)

							% prev_start = ""

							% for r in records:

								<!-- ######################################################################################################### -->
								<!-- ######################################################################################################### -->
								<!-- FOR EACH RECORD START -->

								<!-- PANEL START -->
								<div class="panel panel-default">
									<!-- ######################################################################################################### -->
				    			<!-- PANEL COLLAPSE/BODY START -->
			    				<div name={{namer.record()}} id={{ider.record()}} class="panel-collapse collapse">
			    					% include('hours_panel_body.tpl', prev_start=prev_start, i=ider.i, name=name, is_new_record=False, is_initial_record=False)
				    			</div>					    			
				    			<!-- PANEL BODY/COLLAPSE END -->
									<!-- ######################################################################################################### -->

									<!-- ######################################################################################################### -->
									<!-- PANEL HEADING START -->					    			
				    			% include('hours_panel_heading.tpl', r=r, i=ider.i, is_new_record=False)
				    			<!-- PANEL HEADING END -->
				    			<!-- ######################################################################################################### -->
								</div>
								<!-- PANEL END -->
								<hr />
								<!-- Increment counter after -->
								% ider.inc()
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





		<!-- ######################################################################################################### -->			
		<!-- ######################################################################################################### -->
		<!-- LIST CONTROL BUTTONS START -->
		% record_string = ""
		% for r in records:
			% record_string += "<p>" + r.emailFormat() + "</p>"
		% end
		% print("PRINTING RECORD_STRING")
		% print(record_string)
		% print("GOT TO THE END OF THAT")
		% include('hours_control_buttons.tpl', name=name, record_string=record_string)
		<!-- LIST CONTROL BUTTONS END -->
		<!-- ######################################################################################################### -->
		<!-- ######################################################################################################### -->

	</div> <!-- /.container -->

<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
<script src="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
<!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script> -->
<script>
	// $(document).ready(function() {
	// 	$("button[name=collapseToggle]").click(function() {
	// 		var id = "#start" + $(this).val();
	// 		$(id).focus();
	// 		console.log(id + " should be focused");
	// 	});
	// });
</script>



</body>

</html>

