<%
import modu.labeler as labeler
import modu.recorder as recorder
%>

<div class="panel-collapse collapse" name="record" id="record{{FORM.index}}" >
<div class="panel-body">
<div class="container-fluid">
<div class="row">
<div class="col-md-12">

<form action="/hours" method="post" enctype="multipart/form-data">
	<fieldset class="inputs form-group" name="inputs">

		<!-- SINGLE LINE : ROW 1 -->
		<div class="form-inline" name="row1">
			
			<!-- NAME : TEXT -->
			<input type="text" name="name" id="name{{FORM.index}}" class="form-control record-form-name"
				value="{{DATA.name}}" pattern="{{REGEX.NAME}}" placeholder="Name"
				tabindex="1" required />
			
			<!-- START TIME : TEXT -->
 			<input type="text" name="start" id="start{{FORM.index}}" class="form-control record-form-start"
				value="{{FORM.start}}" pattern="{{REGEX.TIME}}" placeholder="Start Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				required tabindex="2"
				onblur="checkTime(this);" />

			<!-- END TIME : TEXT -->
			<input type="text" name="end" id="end{{FORM.index}}" class="form-control record-form-end"
				value="{{FORM.end}}" pattern="{{REGEX.TIME}}" placeholder="End Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				tabindex="3" 
				onblur="checkTime(this);" />
		
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 2 -->
		<div class="form-inline" name="row2">

			<!-- LABEL : TEXT/DROPDOWN -->
			% include("dropdown_labels.tpl", recordIndex=FORM.index)

			<!-- NOTES : TEXT -->
			<div name="notes-wrapper">
				<input type="text" name="{{HTML_LABELS.NOTES}}" class="form-control record-form-notes"
					value="{{FORM.notes}}" placeholder="Notes" 
					required tabindex="6" />
			</div>
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 3 -->
		<div class="form-inline" name="row3">

			<div name="left">
				<!-- DURATION : TEXT -->
				<div name="duration-wrapper">
					<input type="text" name="{{HTML_LABELS.DURATION}}" class="form-control"
						pattern="{{REGEX.FLOAT}}" placeholder="Duration"
						tabindex="7" />
				</div>

				<!-- BILLABLE : BUTTON -->
				% include("toggle_form_billable.tpl")
				
				<!-- EMERGENCY : BUTTON -->
				% include("toggle_form_emergency.tpl")
			</div>

			<div name="right">
				<!-- SUBMIT BUTTON : SUBMIT -->
				<button type="submit" name="{{HTML_LABELS.SUBMIT}}" class="btn btn-default" tabindex="10">Add Record</button>
			</div>

		</div>

		<!-- INDEX FOR NEXT RECORD : HIDDEN -->
		<input type="hidden" name="index" value="{{FORM.index}}" />

	</fieldset>
</form>


</div>
</div>
</div>
</div>
</div>
