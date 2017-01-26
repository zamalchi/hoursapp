<!-- COMPLETE NOTES FORM -->
<form action="/updateNotes" method="post" name="update-notes" class="form-inline" enctype="multipart/form-data">

		<!-- RECORD INDEX : *value* is passed back via form -->
		<input name="index" type="hidden" value="{{recordIndex}}" />

		<!-- NOTES : submits on (keydown === enter) ; value is passed back via form -->
		<input name="notes" class="record-content notes" value="{{record.notes}}" />

</form>