
<!-- ##################### -->
<!-- REQUIRES -->
<!-- r: Record object for populating the record label -->
<!-- i: index of record and suffix of elem ids -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for record label) -->
<!-- ##################### -->
% from Record import Record

% namer = Labeler()
% ider = Labeler(i)

<div class="panel-heading"> 				
	<div class="container-fluid">
		<div class="row">
			<div class="media" name="recordControlButtons">
				<div class="media-left media-middle">
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
			  				<span class="glyphicon glyphicon-save"></span>
			  			</button>
		  			</form>

						<!-- DELETE RECORD FORM -->
						<form class="form-inline" action="/deleteOne" method="post" enctype="multipart/form-data">
								<div class="form-group">
								<!-- INDEX FOR DELETING RECORD : HIDDEN -->
								<input type="hidden" name="recordIndex" value="{{ider.i}}" />
								<button class="btn btn-default x-button btn-xs media-object inline" type="submit">
								<span class="glyphicon glyphicon-remove"></span>
								</button>
							</div>
						</form>
					% end
					<!-- ######################################################################################################### -->
				</div>
			
				<div class="media-body">
					% if is_new_record:

						<h4 class="panel-title"><strong>Insert new record: #{{ider.i+1}}</strong></h4>


					% else:

						<!-- ######################################################################################################### -->
						<!-- FORMATTED RECORD TEXT -->
						<h4 class="panel-title pull-left">

						<form class="form-inline" action="/saveRecord" method="post" enctype="multipart/form-data">

							<!-- FORMAT RECORD START/END/DESCRIPTION -->

							<!-- name|date <start>|date <end>|duration|label|billable|emergency|<description> -->
							{{r.name}} |
							{{r.date}}
							<div name="start" class="record-content"><strong><u>{{r.fstart}}</u></strong></div> |
							{{r.date}}

							% if (r.duration == Record.PENDING_CHAR):
								<form class="form-inline" action="/completeRecord" method="post" enctype="multipart/form-data">
									<div class="form-group">
										<a href="#" onclick="this.parentElement.parentElement.submit();">
											<strong><span class="pending-text">{{r.fend}}</span></strong> |
											<span class="negative-duration">{{r.duration}}</span>
											<input type="hidden" name="completeIndex" id="{{ider.complete()}}" value="{{ider.i}}" />
										</a>
									</div>
								</form>
							% else:
								<div name="start" class="record-content"><strong><u>{{r.fend}}</u></strong></div> |
								<div name="duration" class="record-content">
								% if (float(r.duration) <= 0):
									<span class="negative-duration">{{r.duration}}</span>
								% else:
									{{r.duration}}
								% end
								</div>
							% end
							<div name="label" class="record-content">{{r.label}}</div> | {{r.billable}} | {{r.emergency}} |
							<div name="description" class="record-content" onkeyup="enableSaveButton(this);" >
								<input type="hidden" name="recordIndex" value="{{ider.i}}" contenteditable="false" />
								<strong contenteditable="true" >{{r.description}}</strong>
							</div>
							<!-- END OF FORMAT -->

						</form>

						</h4>

					% end

					<!-- ######################################################################################################### -->
				</div>
			</div>
		</div>
	</div>
</div>
