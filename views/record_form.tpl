<%
import modu.labeler as labeler
import modu.recorder as recorder
%>

<div class="panel-collapse collapse" name="{{HTML_LABEL.RECORD}}" id="{{HTML_LABEL.RECORD+FORM.index}}" >
<div class="panel-body">
<div class="container-fluid">
<div class="row">
<div class="col-md-12">

<form action="/hours" method="post" enctype="multipart/form-data">
	<fieldset class="inputs form-group" name="inputs">

		<!-- SINGLE LINE : ROW 1 -->
		<div class="form-inline" name="row1">
			
			<!-- NAME : TEXT -->
			<!-- <input name={{namer.name()}} id={{ider.name()}} type="text" class="form-control" placeholder="Name" pattern={{REGEX.NAME}} required value="{{name}}" tabindex="1" /> -->
			<input type="text" name="{{HTML_LABEL.NAME}}" class="form-control"
				value="{{DATA.name}}" pattern="{{REGEX.NAME}}" placeholder="Name"
				tabindex="1" required />
			
			<!-- START TIME -->
<!-- 			<input type="tsext" name={{namer.start()}} id={{ider.start()}}
				class="form-control" pattern={{REGEX.TIME}}
				value="{{FORM.start}}" data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				placeholder="Start Time" required tabindex="2"
				onblur="checkTime(this);" />
 -->		
 			<input type="text" name="{{HTML_LABEL.START}}" class="form-control"
				value="{{FORM.start}}" pattern="{{REGEX.TIME}}" placeholder="Start Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				required tabindex="2"
				onblur="checkTime(this);" />

			<!-- END TIME -->
<!-- 			<input type="text" name={{namer.end()}} id={{ider.end()}}
				class="form-control" pattern={{REGEX.TIME}}
				value="{{FORM.end}}" data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				placeholder="End Time" tabindex="3" 
				onblur="checkTime(this);" /> -->
			<input type="text" name="{{HTML_LABEL.END}}" class="form-control"
				value="{{FORM.end}}" pattern="{{REGEX.TIME}}" placeholder="End Time"
				data-min="{{FORM.min}}" data-max="{{FORM.max}}"
				tabindex="3" 
				onblur="checkTime(this);" />
		
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 2 -->
		<div class="form-inline" name="row2">

			<!-- LABEL : TEXT -->
			% include("dropdown_labels.tpl")

			<!-- NOTES : TEXT -->
			<div name="notes-wrapper">
				<input type="text" name="{{HTML_LABEL.NOTES}}" class="form-control"
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
					<input type="text" name="{{HTML_LABEL.DURATION}}" class="form-control"
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
				<button type="submit" name="{{HTML_LABEL.SUBMIT}}" class="btn btn-default" tabindex="10">Add Record</button>
			</div>

		</div>

		<!-- INDEX FOR NEXT RECORD : HIDDEN -->
<!-- 		<input type="hidden" name={{namer.insert()}} id={{ider.insert()}} value={{FORM.index}} />-->
		<input type="hidden" name="{{HTML_LABEL.INSERT}}" value="{{FORM.index}}" />

	</fieldset>
</form>


</div>
</div>
</div>
</div>
</div>
