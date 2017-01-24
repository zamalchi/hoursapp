<form class="form-inline" action="/deleteOne" method="post" enctype="multipart/form-data">
		<div class="form-group">

			<!-- RECORD INDEX : *value* is passed back via form -->
			<input name="index" type="hidden" value="{{recordIndex}}" />

			<!-- DELETE BUTTON : submits form on double-click -->
			<button name="delete" type="button"
				class="btn btn-default x-button btn-xs media-object"
				ondblclick="this.parentElement.parentElement.submit();" >
				
				<span class="glyphicon glyphicon-remove"></span>
			</button>
		</div>
</form>