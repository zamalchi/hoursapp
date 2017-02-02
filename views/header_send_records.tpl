<form action="/send" method="post" class="inline-block button-wrapper" enctype="multipart/form-data">
	<div class="form-group full-width">						
		
		<input type="text" id="serverAddress" name="address" value="{{DATA.LOGGING_SERVER_ADDRESS}}" placeholder="Logging Server Address" class="form-control input-sm" />
		<strong>:</strong>
		<input type="text" id="serverPort" name="port" value="{{DATA.LOGGING_SERVER_PORT}}" placeholder="Port" class="form-control input-sm">

		<input id="send" name="send" type="submit" value="Send" class="control-button btn btn-success btn-sm"
			onclick="confirmSend(this)" />
		
		<input id="sendConfirm" name="confirm" type="hidden" value="false" />
	</div>
</form>