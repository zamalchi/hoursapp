

<!-- ##################### -->
<!-- REQUIRES -->
<!-- i: index of record and suffix of elem ids -->
<!-- name: name cookie, if it is set -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for focusing) -->
<!-- ##################### -->


<!-- times must match 15-minute interval pattern -->
% TIME_REGEX = "(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45)"

% NAME_REGEX = "[a-zA-Z]{2,}"


% namer = Labeler()
% ider = Labeler(i)


<div class="panel-body">
	<form action="/hours" method="post" enctype="multipart/form-data">
		<fieldset class="inputs form-group">
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline">
				<!-- NAME : TEXT -->
				% if name:
					<input name={{namer.name()}} id={{ider.name()}} type="text" value={{name}} class="form-control quarter-width" placeholder="Name" pattern={{NAME_REGEX}} required />
				% else:
					<input name={{namer.name()}} id={{ider.name()}} type="text" class="form-control quarter-width" placeholder="Name" pattern={{NAME_REGEX}} required />
				% end
				<!-- START TIME -->
				% if is_new_record:
					<input name={{namer.start()}} id={{ider.start()}} type="text" value={{prev_start}} class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} autofocus />
				
				% elif is_initial_record:
					<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} required />
				
				% elif prev_start:
					<input name={{namer.start()}} id={{ider.start()}} type="text" value={{prev_start}} class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} />
				
				% else:
					<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} required />
				% end


				<!-- END TIME -->
				<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control" placeholder="End Time" pattern={{TIME_REGEX}} required />
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline">
				<!-- LABEL : TEXT -->
				<input name={{namer.label()}} id={{ider.label()}} type="text" class="form-control" placeholder="Label" required/>
				<!-- DESCRIPTION : TEXT // not required (ex. lunch) -->
				<input name={{namer.description()}} id={{ider.description()}} type="text" class="form-control half-width" placeholder="Description" required />
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline padded-top">
				<!-- LEFT SIDE -->
				<div class="pull-left">
					<!-- DURATION : TEXT -->
					<input name={{namer.duration()}} id={{ider.duration()}} type="text" class="form-control" placeholder="Duration" />
					<!-- BILLABLE CHECKBOX -->
					<div class="billable">
						<span class="checkboxtext">Billable: </span>
						<input type="checkbox" name={{namer.billable()}} id={{ider.billable()}} checked />
					</div>
					<!-- EMERGENCY CHECKBOX -->
					<div class="emergency">
						<span class="checkboxtext">Emergency: </span>
						<input type="checkbox" name={{namer.emergency()}} id={{ider.emergency()}} />
					</div>
				</div>
				<!-- RIGHT SIDE -->
				<div class="pull-right">
					<!-- SUBMIT BUTTON : SUBMIT -->
					<button type="submit" name={{namer.submit()}} id={{ider.submit()}} class="btn btn-default">Add Record</button>
					<!-- ######################################################################################################### -->
				</div>
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->

			<!-- INDEX FOR NEXT RECORD : HIDDEN -->
			<input type="hidden" name={{namer.insert()}} id={{ider.insert()}} value={{ider.i}} />
		</fieldset>
	</form>
</div> <!-- /.panel-body -->