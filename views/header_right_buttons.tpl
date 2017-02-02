<div class="btn-group">
		
	<!-- VIEW RAW RECORDS -->
	<div class="form-group inline-block button-wrapper">
		<input id="view" name="view" type="submit" value="Raw" class="control-button btn btn-info btn-sm"
			onclick="openViewer()" />
		<input id="viewRecords" name="viewRecords" type="hidden" value="{{!DATA.recordString}}" />
	</div>

	<!-- VIEW README/UPDATES -->
	<div class="form-group inline-block button-wrapper">
		<a name="updates" href="/viewUpdates" target="__blank" class="control-button btn btn-default btn-sm">Help / Updates</a>
	</div>


	<!-- DELETE RECORDS -->
	<form action="/delete" method="post" class="inline-block button-wrapper" enctype="multipart/form-data">						
		<div class="form-group full-width">
			
			<input id="delete" name="delete" type="submit" value="Delete" class="control-button btn btn-danger btn-sm"
				onclick="confirmDelete()" />
			
			<input id="deleteConfirm" name="deleteConfirm" type="hidden" value="false" />
		</div>
	</form>

	<!-- SEND RECORDS -->
	<form action="/email" method="post" class="inline-block button-wrapper" enctype="multipart/form-data">
		<div class="form-group full-width">						
			
			<input id="email" name="email" type="submit" value="Email" class="control-button btn btn-success btn-sm"
				onclick="confirmEmail(this)" data-sender="{{DATA.SENDER}}" data-receivers="{{DATA.RECEIVERS}}" />
			
			<input id="emailConfirm" name="emailConfirm" type="hidden" value="false" />
		</div>
	</form>

</div>