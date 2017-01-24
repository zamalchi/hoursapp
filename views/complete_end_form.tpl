<form action="/completeEndTime" method="post" class="form-inline" enctype="multipart/form-data" >
	<div class="form-group">
		<!-- RECORD INDEX : *value* is passed back via form -->
		<input name="index" type="hidden" value="{{recordIndex}}" />

		<!-- END TIME : input able to submit form ; value is passed back -->
		<input type="text" name="completeEnd" class="form-control input-sm"
			placeholder="     " pattern={{REGEX.TIME}} />
	</div>
</form>