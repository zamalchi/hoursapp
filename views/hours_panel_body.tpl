<!-- ######################################################################################################### -->


<!-- TO BE INSERTED INTO A PANEL ELEMENT (*BEFORE*/AFTER) A PANEL-HEADING -->

<!-- ######################################################################################################### -->

<!-- REQUIRES -->
<!-- i: index of record and suffix of elem ids -->
<!-- name: name cookie, if it is set -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for focusing) -->

<!-- ######################################################################################################### -->

<!-- TODO: determine if this import is needed -->
% from Record import Record


<!-- times must match 15-minute interval pattern -->
% # TIME_REGEX = "(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45)"
% TIME_REGEX = "(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))"

% NAME_REGEX = "[a-zA-Z]{2,}"

<!-- PROVIDE NAMES AND IDS FOR ELEMENTS (IDS INCLUDE THE INDEX OF THE RECORD) -->
% namer = Labeler()
% ider = Labeler(i)

<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->




<!-- START OF PANEL-BODY HTML -->

<div class="panel-body">
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-12">
	
				<!-- ######################################################################################################### -->
				<!-- ********************************************************************************************************* -->
				<!-- ********************************************************************************************************* -->
				<!-- ######################################################################################################### -->

				<form action="/hours" method="post" enctype="multipart/form-data">
					<fieldset class="inputs form-group">

						<!-- ######################################################################################################### -->
						<!-- SINGLE LINE -->
						<div class="form-inline">
							<!-- NAME : TEXT -->
							<input name={{namer.name()}} id={{ider.name()}} type="text" class="form-control third-width" placeholder="Name" pattern={{NAME_REGEX}} required value="{{name}}" />

							<!-- ************************************************************************** -->
							<!-- START TIME -->
							% if is_initial_record:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control quarter-width" placeholder="Start Time" pattern={{TIME_REGEX}} required autofocus />

							% elif (is_new_record) and (prev_start != Record.PENDING_CHAR):
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control quarter-width" placeholder="Start Time" pattern={{TIME_REGEX}} value="{{prev_start}}" required />

							% elif is_new_record:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control quarter-width" placeholder="Start Time" pattern={{TIME_REGEX}} value="" autofocus required />

							% else:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control quarter-width" placeholder="Start Time" pattern={{TIME_REGEX}} required />
							% end
							<!-- ************************************************************************** -->


							<!-- ************************************************************************** -->
							<!-- END TIME -->
							% if is_initial_record:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control quarter-width" placeholder="End Time" pattern={{TIME_REGEX}} value="{{prev_end}}" />
							% elif is_new_record:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control quarter-width" placeholder="End Time" pattern={{TIME_REGEX}} autofocus value="" />
							% else:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control quarter-width" placeholder="End Time" pattern={{TIME_REGEX}} value="{{prev_end}}" required />
							% end
							<!-- ************************************************************************** -->

						</div>
						<!-- END OF SINGLE LINE -->
						<!-- ######################################################################################################### -->
						<hr />
						<!-- ######################################################################################################### -->
						<!-- SINGLE LINE -->
						<div class="form-inline">
							<!-- <input name={{namer.label()}} id={{ider.label()}} type="text" class="form-control quarter-width" placeholder="Label" required/> -->
							<!-- LABEL : TEXT -->
							<div class="dropdown form-control">
								<!-- INITIAL VALUES USED FOR DEFAULT AND INDEX OFFSET -->
								% ls_name = [""]
								% ls_billable = ["Y"]
								% ls_emergency = ["N"]

								% for each in labels:
							   	% l = each.split(" | ")
							   	% ls_name.append(l[0])
							   	% ls_billable.append(l[1])
							   	% ls_emergency.append(l[2])
								% end

								<select class="dropdownSelect" data-index="{{ider.i}}" onchange="dropdownChangeSelect(this)">
								   % for i, each in enumerate(ls_name):
								   	<option value="{{each}}" data-billable="{{ls_billable[i]}}" data-emergency="{{ls_emergency[i]}}">{{each}}</option>
								   % end
								</select>
								<input class="dropdownInput" name="{{namer.dropdown()}}" placeholder="Label" id="{{ider.dropdown()}}" onfocus="this.select()" type="text" onchange="dropdownChangeType(this)" data-name="{{ls_name}}" data-billable="{{ls_billable}}" data-emergency="{{ls_emergency}}" data-index="{{ider.i}}" required style="text-transform: uppercase;" />
								<input name="{{namer.label()}}" id="{{ider.label()}}" type="hidden">
							</div>
							
							<!-- DESCRIPTION : TEXT // not required (ex. lunch) -->
							<input  name={{namer.description()}} id={{ider.description()}} type="text" class="form-control" placeholder="Notes" required />
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
								<input name={{namer.duration()}} id={{ider.duration()}} type="text" class="form-control quarter-width" placeholder="Duration" />
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
			
				<!-- ######################################################################################################### -->
				<!-- ********************************************************************************************************* -->
				<!-- ********************************************************************************************************* -->
				<!-- ######################################################################################################### -->

			</div>
		</div>
	</div>
</div>

<!-- END OF PANEL-BODY HTML -->
