
<!-- ######################################################################################################### -->

<!-- PROVIDES A PANEL HEADING CONTAINING A DISPLAY OF THE RECORD WITH CONTROLS AND SOME MODIFYABLE FIELDS -->
<!-- TO BE INSERTED INTO A PANEL ELEMENT (BEFORE/*AFTER*) A PANEL-BODY -->

<!-- ######################################################################################################### -->

<!-- REQUIRES -->
<!-- r: Record object for populating the record label -->
<!-- i: index of record and suffix of elem ids -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for record label) -->

<!-- ######################################################################################################### -->

<!-- TODO: determine if this import is needed -->
% from Record import Record

<!-- PROVIDE NAMES AND IDS FOR ELEMENTS (IDS INCLUDE THE INDEX OF THE RECORD) -->
% namer = Labeler()
% ider = Labeler(i)

<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->




<!-- START OF PANEL-HEADING HTML -->

<div class="panel-heading"> 				
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-12">
				<div class="media">

					<!-- ######################################################################################################### -->
					<!-- ********************************************************************************************************* -->
					<!-- ********************************************************************************************************* -->
					<!-- ######################################################################################################### -->

					<div class="media-left media-middle" name="recordControls">
						<!-- ######################################################################################################### -->
						<!-- INSERT BUTTON -->
		  			<button name="collapseToggle" value={{ider.i}} class="btn btn-success btn-xs media-object" type="button" data-toggle="collapse" data-target="#{{ider.record()}}" data-parent="#accordion">
		  				<span class="glyphicon glyphicon-chevron-down"></span>
		  			</button>
						<!-- ######################################################################################################### -->

						<!-- ######################################################################################################### -->
						% if not is_new_record:

							<!-- EDIT BUTTON -->
							<form class="form-inline" action="/editRecord" method="post" enctype="multipart/form-data">
				  			<button type="submit" name="editButton" id="{{ider.edit()}}" value={{ider.i}} class="btn btn-primary btn-xs media-object" type="button" disabled >
									<input type="hidden" name="recordIndex" value="{{ider.i}}" />
									<input type="hidden" id="{{ider.new_description()}}" name="newDescription" value="" />
									<input type="hidden" id="{{ider.complete_end_time()}}" name="completeEndTime" value="" />
				  				<span class="glyphicon glyphicon-edit"></span>
				  			</button>
			  			</form>

							<!-- DELETE RECORD FORM -->
							<form class="form-inline" action="/deleteOne" method="post" enctype="multipart/form-data">
									<div class="form-group">
									<!-- INDEX FOR DELETING RECORD : HIDDEN -->
									<input type="hidden" name="recordIndex" value="{{ider.i}}" />
									<button name="deleteButton" class="btn btn-default x-button btn-xs media-object" type="button" ondblclick="this.parentElement.parentElement.submit();" >
									<span class="glyphicon glyphicon-remove"></span>
									</button>
								</div>
							</form>
						% end
						<!-- ######################################################################################################### -->
					
					</div>
							
					<!-- ######################################################################################################### -->
					<!-- ********************************************************************************************************* -->
					<!-- ********************************************************************************************************* -->
					<!-- ######################################################################################################### -->
					
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
							<!-- name|date <start>|date <end>|duration|label|billable|emergency|<description> -->

							<h4 class="panel-title pull-left" name="record-display-string">

							{{r.name}} | {{r.date}}

							<!-- START TIME -->
							<div name="start" class="record-content"><strong><u>{{r.fstart}}</u></strong></div>

							| {{r.date}}

							<!-- ##################################################### -->
							<!-- ##################################################### -->
							<!-- IF INCOMPLETE RECORD (END TIME AND DURATION) -->
							% if (r.duration == Record.PENDING_CHAR):
								
								<!-- COMPLETE END TIME FORM -->
								<form action="/completeEndTime" method="post" class="form-inline" enctype="multipart/form-data" >
									<div class="form-group">
											<!-- END TIME : input able to submit form -->
											<input type="text" name="completeEndTime"
														 class="form-control input-sm" placeholder="     " 
														 onkeyup="enableSaveButton(event, this);" 
														 data-index="{{ider.i}}" />
									</div>
								</form>
		
								<!-- ##################################################### -->

								<!-- INCOMPLETE DURATION -->
								| <span class="negative-duration">{{r.duration}}</span>

							<!-- ##################################################### -->
							<!-- ##################################################### -->
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

							<!-- ##################################################### -->
							<!-- ##################################################### -->
							% end

							<!-- LABEL -->
							| <div name="label" class="record-content">{{r.label}}</div>
							
							<!-- BILLABLE | EMERGENCY -->
							| {{r.billable}} | {{r.emergency}} |
							
							<!-- ##################################################### -->

							<!-- COMPLETE NOTES FORM -->
							<form action="/completeNotes" method="post" name="completeNotes" class="form-inline" enctype="multipart/form-data">
								<div class="form-group">
									<!-- NOTES : editable, submits on (keydown === enter) -->
									<span name="notes" contenteditable="true"
												data-index="{{ider.i}}" class="record-content"
												onkeyup="enableSaveButton(this);"
												onkeydown="submitOnEnterPressed(event, this.parentElement.parentElement);">
										{{r.description}}
									</span>
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