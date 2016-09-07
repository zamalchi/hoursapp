<!-- ######################################################################################################### -->


<!-- TO BE INSERTED INTO A PANEL ELEMENT (*BEFORE*/AFTER) A PANEL-DISPLAY -->

<!-- ######################################################################################################### -->

<!-- REQUIRES -->
<!-- i: index of record and suffix of elem ids -->
<!-- name: name cookie, if it is set -->
<!-- is_new_record: boolean for differentiating 'New Record' part (for focusing) -->

<!-- ######################################################################################################### -->

<!-- TODO: determine if this import is needed -->
% from classes.Record import Record


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
					<fieldset class="inputs form-group" name="inputs">

						<!-- ######################################################################################################### -->
						<!-- SINGLE LINE -->
						<div class="form-inline" name="row1">
							<!-- NAME : TEXT -->
							<input name={{namer.name()}} id={{ider.name()}} type="text" class="form-control" placeholder="Name" pattern={{NAME_REGEX}} required value="{{name}}" />

							<!-- ************************************************************************** -->
							<!-- START TIME -->
							% if is_initial_record:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} required autofocus />

							% elif (is_new_record) and (prev_start != Record.PENDING_CHAR):
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} value="{{prev_start}}" required />

							% elif is_new_record:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} value="" autofocus required />

							% else:
								<input name={{namer.start()}} id={{ider.start()}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} required />
							% end
							<!-- ************************************************************************** -->


							<!-- ************************************************************************** -->
							<!-- END TIME -->
							% if is_initial_record:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control" placeholder="End Time" pattern={{TIME_REGEX}} value="{{prev_end}}" />
							% elif is_new_record:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control" placeholder="End Time" pattern={{TIME_REGEX}} autofocus value="" />
							% else:
								<input name={{namer.end()}} id={{ider.end()}} type="text" class="form-control" placeholder="End Time" pattern={{TIME_REGEX}} value="{{prev_end}}" required />
							% end
							<!-- ************************************************************************** -->

						</div>
						<!-- END OF SINGLE LINE -->
						<!-- ######################################################################################################### -->
						<hr />
						<!-- ######################################################################################################### -->
						<!-- SINGLE LINE -->
						<div class="form-inline" name="row2">
							<!-- <input name={{namer.label()}} id={{ider.label()}} type="text" class="form-control quarter-width" placeholder="Label" required/> -->
							<!-- LABEL : TEXT -->
							<div name="dropdown-wrapper">
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
							</div>
							
							<div name="notes-wrapper">
								<!-- NOTES : TEXT // not required (ex. lunch) -->
								<input  name={{namer.notes()}} id={{ider.notes()}} type="text" class="form-control" placeholder="Notes" required />
							</div>

						</div>
						<!-- END OF SINGLE LINE -->
						<!-- ######################################################################################################### -->
						<hr />
						<!-- ######################################################################################################### -->
						<!-- SINGLE LINE -->
						<div class="form-inline" name="row3">
							
							<!-- LEFT SIDE -->
							<div name="left">
								<!-- DURATION : TEXT -->
								<div name="duration-wrapper">
									<input type="text" name={{namer.duration()}} id={{ider.duration()}}
										class="form-control" placeholder="Duration" pattern="{{FLOAT_REGEX}}" />
								</div>
								
								<!-- BILLABLE BUTTON -->
								<div name="{{namer.billable()}}" id="{{ider.billable()}}" class="billable btn btn-default" onclick="toggleBE(this);">
									<span class="checkboxtext">Billable:</span>
									<span class="checkboxtext"><strong>Y</strong></span>
									<input type="hidden" name="{{namer.billable()}}" value="Y" />
								</div>
								
								<!-- EMERGENCY BUTTON -->
								<div name="{{namer.emergency()}}" id="{{ider.emergency()}}" class="emergency btn btn-default" onclick="toggleBE(this);">
									<span class="checkboxtext">Emergency:</span>
									<span class="checkboxtext"><strong>N</strong></span>
									<input type="hidden" name="{{namer.emergency()}}" value="N" />
								</div>

							</div>

							<!-- RIGHT SIDE -->
							<div name="right">
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
