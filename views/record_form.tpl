<%
import modu.labeler as labeler
import modu.recorder as recorder

name = record.name if record else ""

form_start = form_end = ""

min = "0000"
max = "2345"

prev_record = recorder.getPrevRecord(DATA.records, ider.i)
	
if prev_record:
	if (prev_record.end != recorder.PENDING_CHAR):
		form_start = prev_record.fend
	end

	min = prev_record.start 
end

form_notes = ""
if DATA.anchor == "-1":
	form_notes = DATA.notes
%>

<div class="panel-collapse collapse" name={{namer.record()}} id={{ider.record()}} >
<div class="panel-body">
<div class="container-fluid">
<div class="row">
<div class="col-md-12">

<form action="/hours" method="post" enctype="multipart/form-data">
	<fieldset class="inputs form-group" name="inputs">

		<!-- SINGLE LINE : ROW 1 -->
		<div class="form-inline" name="row1">
			<!-- NAME : TEXT -->
			<input name={{namer.name()}} id={{ider.name()}} type="text" class="form-control" placeholder="Name" pattern={{REGEX.NAME}} required value="{{name}}" tabindex="1" />
			<!-- START TIME -->
			<input type="text" name={{namer.start()}} id={{ider.start()}}
				class="form-control" pattern={{REGEX.TIME}}
				value="{{form_start}}" data-min="{{min}}" data-max="{{max}}"
				placeholder="Start Time" required tabindex="2"
				onblur="checkTime(this);" />
			<!-- END TIME -->
			<input type="text" name={{namer.end()}} id={{ider.end()}}
				class="form-control" pattern={{REGEX.TIME}}
				value="{{form_end}}" data-min="{{min}}" data-max="{{max}}"
				placeholder="End Time" tabindex="3" 
				onblur="checkTime(this);" />
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 2 -->
		<div class="form-inline" name="row2">
			<!-- LABEL : TEXT -->
			% include("dropdown_labels.tpl")
			<!-- NOTES : TEXT -->
			<div name="notes-wrapper">
				<input  name={{namer.notes()}} id={{ider.notes()}} type="text" value="{{DATA.notes}}" class="form-control" placeholder="Notes" required tabindex="6" />
			</div>
		</div>

		<hr />
		
		<!-- SINGLE LINE : ROW 3 -->
		<div class="form-inline" name="row3">

			<div name="left">
				<!-- DURATION : TEXT -->
				<div name="duration-wrapper">
					<input type="text" name={{namer.duration()}} id={{ider.duration()}}
						class="form-control" placeholder="Duration" pattern="{{REGEX.FLOAT}}" tabindex="7" />
				</div>
				<!-- BILLABLE : BUTTON -->
				% include("toggle_form_billable.tpl")
				<!-- EMERGENCY : BUTTON -->
				% include("toggle_form_emergency.tpl")
			</div>

			<div name="right">
				<!-- SUBMIT BUTTON : SUBMIT -->
				<button type="submit" name={{namer.submit()}} id={{ider.submit()}} class="btn btn-default" tabindex="10" >Add Record</button>
			</div>

		</div>

		<!-- INDEX FOR NEXT RECORD : HIDDEN -->
		<input type="hidden" name={{namer.insert()}} id={{ider.insert()}} value={{ider.i}} />
	</fieldset>
</form>


</div>
</div>
</div>
</div>
</div>
