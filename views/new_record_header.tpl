
<div class="panel-heading" id="record-display{{str(index)}}">
<div class="media">

	<div class="media-left media-middle" name="record-controls">
		% include("button_collapse.tpl", target="record-form"+str(index))
	</div>


	<div class="media-body" name="recordDisplay">
		<h4 class="panel-title"><strong>Insert new record: #{{len(DATA.records)+1}}</strong></h4>
	</div>

</div>
</div>
</div>
</div>
</div>