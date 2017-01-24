<!-- BILLABLE TOGGLE FORM -->
<form action="/toggleBillable" method="post" name="toggleBillable" class="form-inline" enctype="multipart/form-data">
	<input type="hidden" name="billable" value="{{record.billable}}" />
	<input type="hidden" name="index" value="{{recordIndex}}" />
	<button type="submit">
		<span>
			{{record.billable}}
		</span>
	</button>
</form>