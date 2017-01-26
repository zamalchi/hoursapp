
<div id="billable{{str(FORM.index)}}" class="btn btn-default billable" 
	onclick="toggleBE(this);"
	onkeypress="toggleButtonPress(event, this);"
	tabindex="8">
	
	<span class="checkboxtext">Billable:</span>
	<span class="checkboxtext"><strong>Y</strong></span>
	<input type="hidden" name="billable" value="Y" />
</div>