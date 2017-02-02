<!-- EMERGENCY TOGGLE FORM -->
<form action="/toggleEmergency" method="post" name="toggleEmergency" class="form-inline" enctype="multipart/form-data">
	<input type="hidden" name="emergency" value="{{record.emergency}}" />
	<input type="hidden" name="index" value="{{recordIndex}}" />
	<button type="submit">
		<span>
			{{record.emergency}}
		</span>
	</button>
</form>