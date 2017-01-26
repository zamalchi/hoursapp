<%
"""
This sub-template provides a collapsable form for adding a record
A form is generated for each existing record,
	plus one for inserting at the end of the list

div.panel-collapse.record-form
div.panel-body
form (POST /hours)
	fieldset.inputs ("inputs")
		div.form-inline ("row1")
			input.name ("name")
			input.start ("start")
			input.end ("end")
		div.form-inline ("row2")
			include ("dropdown_labels.tpl")
			input.notes ("notes")
		div.form-inline ("row3")
			div ("left")
				input.duration ("duration")
				include ("toggle_form_billable.tpl")
				include ("toggle_form_emergency.tpl")
			div ("right")
				input.submit ("submit")
		input.index ("index")
"""
import modu.recorder as recorder
%>

<div class="panel-collapse collapse record-form" id="record-form{{str(FORM.index)}}" >
<div class="panel-body">

<form action="/hours" method="post" enctype="multipart/form-data">
	<fieldset class="form-group">

		<!-- INDEX FOR NEXT RECORD : HIDDEN -->
		<input type="hidden" name="index" value="{{FORM.index}}" />

		<!-- SINGLE LINE : ROW 1 -->
		<div name="row1" class="form-inline">
			
			<!-- NAME : TEXT -->
			<input type="text" name="name" class="form-control name"
				value="{{DATA.name}}" pattern="{{REGEX.NAME}}" placeholder="Name"
				tabindex="1" required />
			
			<!-- START TIME : TEXT -->
 			<input type="text" name="start" class="form-control start"
				value="{{FORM.start}}" pattern="{{REGEX.TIME}}" placeholder="Start Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				required tabindex="2"
				onblur="checkTime(this);" />

			<!-- END TIME : TEXT -->
			<input type="text" name="end" class="form-control end"
				value="{{FORM.end}}" pattern="{{REGEX.TIME}}" placeholder="End Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				tabindex="3" 
				onblur="checkTime(this);" />
		
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 2 -->
		<div name="row2" class="form-inline">

			<!-- LABEL : TEXT/DROPDOWN -->
			% include("dropdown_labels.tpl", recordIndex=FORM.index)

			<!-- NOTES : TEXT -->
			<input type="text" name="notes" class="form-control notes"
				value="{{FORM.notes}}" placeholder="Notes" 
				required tabindex="6" />

		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 3 -->
		<div name="row3" class="form-inline">

			<div class="left">
				<!-- DURATION : TEXT -->
				<input type="text" name="duration" class="form-control"
					pattern="{{REGEX.FLOAT}}" placeholder="Duration"
					tabindex="7" />

				<!-- BILLABLE : BUTTON -->
				% include("toggle_form_billable.tpl")
				
				<!-- EMERGENCY : BUTTON -->
				% include("toggle_form_emergency.tpl")
			</div>

			<div class="right">
				<!-- SUBMIT BUTTON : SUBMIT -->
				<button type="submit" class="btn btn-default submit" tabindex="10">Add Record</button>
			</div>

		</div>

	</fieldset>
</form>


</div>
</div>
