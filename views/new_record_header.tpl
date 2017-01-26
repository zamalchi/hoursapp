
<div class="panel-heading" id="{{HTML_LABELS.RECORD_DISPLAY+str(index)}}">
<div class="container-fluid">
<div class="row">
<div class="col-md-12" name="record-display-col">
<div class="media">

	<div class="media-left media-middle" name="record-controls">
		% include("button_collapse.tpl", recordFormId=HTML_LABELS.RECORD_FORM+str(index))
	</div>


	<div class="media-body" name="recordDisplay">
		<h4 class="panel-title"><strong>Insert new record: #{{len(DATA.records)+1}}</strong></h4>
	</div>

</div>
</div>
</div>
</div>
</div>