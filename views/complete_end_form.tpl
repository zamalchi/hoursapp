<form action="/completeEndTime" method="post" class="form-inline complete-end" enctype="multipart/form-data" >
	<div class="form-group">

		<!-- RECORD INDEX : HIDDEN -->
		<input type="hidden" name="index" value="{{recordIndex}}" />

		<!-- TODO: finish here -->
		<!-- END TIME : TEXT : input able to submit form ; value is passed back -->
		<input type="text" name="end" class="form-control input-sm"
			placeholder="     " pattern={{REGEX.TIME}} />
	</div>
</form>