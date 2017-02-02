
<!-- ######################################################################################################### -->

<!-- PROVIDES A PANEL HEADING CONTAINING A DISPLAY OF THE RECORD WITH CONTROLS AND SOME MODIFYABLE FIELDS -->
<!-- TO BE INSERTED INTO A PANEL ELEMENT (BEFORE/*AFTER*) A PANEL-FORM -->

<!-- ######################################################################################################### -->

<!-- REQUIRES -->
<!-- r: Record object for populating the record label -->
<!-- i: index of record and suffix of elem ids -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for record label) -->

<!-- ######################################################################################################### -->

<%
import modu.labeler as labeler
import modu.recorder as recorder

# PROVIDE NAMES AND IDS FOR ELEMENTS (IDS INCLUDE THE INDEX OF THE RECORD)
# TODO: check if these are needed or if the sub-template can access the existing global objects
namer = labeler.Labeler()
ider = labeler.Labeler(i)

TIME_REGEX = "(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))"
%>

<!-- START OF PANEL-HEADING HTML -->

<div class="panel-heading"> 				
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-12" name="record-display-col">
				<div class="media">


					<div class="media-left media-middle" name="recordControls">

						<!-- TODO: needed in button? : data-index="{{ider.i}}" -->
		  			% include("button_collapse.tpl", record_id=ider.record())
						
						% include("button_delete.tpl", record_index=ider.i)
						
					</div>

					
					<!-- MEDIA-BODY -->
					<div class="media-body" name="recordDisplay">

						<!-- IF NEW RECORD -->
						% if is_new_record:

							<!-- RECORD COUNTER -->
							<h4 class="panel-title"><strong>Insert new record: #{{ider.i+1}}</strong></h4>

						<!-- ELSE NOT NEW RECORD -->
						% else:

							<!-- ######################################################################################################### -->
							<!-- ********************************************************************************************************* -->
							<!-- ######################################################################################################### -->
							<!-- FORMATTED RECORD TEXT -->
							<!-- name|date <start>|date <end>|duration|label|billable|emergency|<notes> -->

							<!-- anchor tag for adjusting page after editing a record -->
							<a name="{{ider.i}}"></a>

							<h4 class="panel-title pull-left" name="record-display-string">

							{{r.name}} | {{r.date}}

							<!-- START TIME -->
							<div name="start" class="record-content"><strong><u>{{r.fstart}}</u></strong></div>

							| {{r.date}}

							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->
	
							<!-- IF INCOMPLETE RECORD (END TIME AND DURATION) -->
							% if (r.fend == recorder.PENDING_CHAR):
								
								<!-- COMPLETE END TIME FORM -->
								<form action="/completeEndTime" method="post" class="form-inline" enctype="multipart/form-data" >
									<div class="form-group">

											<!-- RECORD INDEX : *value* is passed back via form -->
											<input name="index" type="hidden" value="{{ider.i}}" />

											<!-- END TIME : input able to submit form ; value is passed back -->
											<input type="text" name="completeEnd" class="form-control input-sm"
												placeholder="     " pattern={{TIME_REGEX}} />
									</div>
								</form>

								<!-- ######################################################################################################### -->

								<!-- INCOMPLETE DURATION -->
								| {{r.duration}}

							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->

							<!-- ELSE COMPLETE RECORD (END TIME AND DURATION) -->
							% else:

								<!-- END TIME -->
								<div name="end" class="record-content"><strong><u>{{r.fend}}</u></strong></div> |
								
								<!-- DURATION -->
								<div name="duration" class="record-content">
									<!-- check if negative -> error -->
									% if (float(r.duration) <= 0):
										<span class="negative-duration">{{r.duration}}</span>
									% else:
										{{r.duration}}
									% end
								</div>

							<!-- ######################################################################################################### -->
							<!-- ######################################################################################################### -->

							% end

							|
							
							<!-- LABEL -->
							<div name="label" class="record-content">{{r.label}}</div>
							
							|
						
							<!-- BILLABLE TOGGLE FORM -->
							<form action="/toggleBillable" method="post" name="toggleBillable" class="form-inline" enctype="multipart/form-data">
								<input type="hidden" name="billable" value="{{r.billable}}" />
								<input type="hidden" name="index" value="{{ider.i}}" />
								<button type="submit">
									<span>
										{{r.billable}}
									</span>
								</button>
							</form>

							| 
							
							<!-- EMERGENCY TOGGLE FORM -->
							<form action="/toggleEmergency" method="post" name="toggleEmergency" class="form-inline" enctype="multipart/form-data">
								<input type="hidden" name="emergency" value="{{r.emergency}}" />
								<input type="hidden" name="index" value="{{ider.i}}" />
								<button type="submit">
									<span>
										{{r.emergency}}
									</span>
								</button>
							</form>

							|
	
							<br>

							<!-- ######################################################################################################### -->

							<!-- COMPLETE NOTES FORM -->
							<form action="/completeNotes" method="post" name="completeNotes" class="form-inline" enctype="multipart/form-data">
								<div class="form-group full-width">

									<!-- RECORD INDEX : *value* is passed back via form -->
									<input name="index" type="hidden" value="{{ider.i}}" />

									<!-- NOTES : submits on (keydown === enter) ; value is passed back via form -->
									<input name="notesDisplay" class="record-content" value="{{r.notes}}" />

								</div>
							</form>

							</h4>

							<!-- END OF FORMAT -->
							<!-- ######################################################################################################### -->
							<!-- ********************************************************************************************************* -->
							<!-- ######################################################################################################### -->

						% end

					</div>

					<!-- ######################################################################################################### -->
					<!-- ********************************************************************************************************* -->
					<!-- ********************************************************************************************************* -->
					<!-- ######################################################################################################### -->

				</div>
			</div>
		</div>
	</div>
</div>

<!-- END OF PANEL-HEADING HTML -->