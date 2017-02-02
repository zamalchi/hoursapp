<form action="/send" method="post" class="inline-block button-wrapper send" enctype="multipart/form-data">
	<div class="form-group full-width">						
		
		<input type="text" name="address" value="{{DATA.LOGGING_SERVER_ADDRESS}}" placeholder="Logging Server Address" class="form-control input-sm address" />
		<strong>:</strong>
		<input type="text" name="port" value="{{DATA.LOGGING_SERVER_PORT}}" placeholder="Port" class="form-control input-sm port">

		<input id="send" name="send" type="submit" value="Send" class="control-button btn btn-success btn-sm"
			onclick="confirmSend(this)" />
		
		<input id="confirm-send" name="confirm" class="confirm" type="hidden" value="false" />
	</div>
</form>