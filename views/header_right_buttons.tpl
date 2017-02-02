<div class="btn-group right">
		
	<!-- VIEW RAW RECORDS -->
	<div class="button-wrapper">
		<input id="view" name="view" type="submit" value="Raw" class="control-button btn btn-info btn-sm"
			onclick="openViewer()" />
		<input id="view-records" name="viewRecords" type="hidden" value="{{!DATA.recordString}}" />
	</div>

	<!-- VIEW README/UPDATES -->
	<div class="button-wrapper">
		<a href="/viewUpdates" target="__blank" class="control-button btn btn-default btn-sm updates">Help / Updates</a>
	</div>


	<!-- DELETE RECORDS -->
	<form action="/delete" method="post" class="button-wrapper" enctype="multipart/form-data">						
		<div class="form-group">
			
			<input id="delete" name="delete" type="submit" value="Delete" class="control-button btn btn-danger btn-sm delete"
				onclick="confirmDelete()" />
			
			<input id="comfirm-delete-all" name="deleteConfirm" type="hidden" value="false" />
		</div>
	</form>

	<!-- SEND RECORDS -->
	<form action="/email" method="post" class="button-wrapper" enctype="multipart/form-data">
		<div class="form-group full-width">						
			
			<input id="email" name="email" type="submit" value="Email" class="control-button btn btn-success btn-sm email"
				onclick="confirmEmail(this)" data-sender="{{DATA.SENDER}}" data-receivers="{{DATA.RECEIVERS}}" />
			
			<input id="confirm-email" name="emailConfirm" type="hidden" value="false" />
		</div>
	</form>

</div>