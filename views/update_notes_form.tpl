<!-- COMPLETE NOTES FORM -->
<form action="/updateNotes" method="post" name="updateNotes" class="form-inline" enctype="multipart/form-data">
	<div class="form-group full-width">

		<!-- RECORD INDEX : *value* is passed back via form -->
		<input name="index" type="hidden" value="{{recordIndex}}" />

		<!-- NOTES : submits on (keydown === enter) ; value is passed back via form -->
		<input name="notesDisplay" class="record-content" value="{{record.notes}}" />

	</div>
</form>