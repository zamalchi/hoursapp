<%
"""
This sub-template displays data for a single record
It contains forms for modifying certain record fields

div.panel-heading.record-display
div.media
	div.media-left.media-middle.record-controls
		include ("button_collapse.tpl")
		include ("button_delete.tpl")
	div.media-body
		a[name="{{index}}"]
		h4.panel-title.record-display-string
			div.record-content.start
			include ("complete_end_form.tpl") || div.record-content.end
			div.record-content.duration
				span.negative-duration
			div.record-content.label
			include ("toggle_display_billable.tpl")
			include ("toggle_display_emergency.tpl")
			include ("update_notes_form.tpl")


"""
import modu.recorder as recorder
%>

<!-- START OF PANEL-HEADING HTML -->
<div class="panel-heading record-display" id="record-display{{str(DISPLAY.index)}}">

	<div class="media">

		<div class="media-left media-middle record-controls">
			% include("button_collapse.tpl", target="record-form"+str(DISPLAY.index))
			
			% include("button_delete.tpl", recordIndex=DISPLAY.index)
		</div>

		
		<div class="media-body">

			<!-- anchor tag for adjusting page after editing a record -->
			<a name="{{DISPLAY.index}}"></a>

			<h4 class="panel-title pull-left record-display-string">

				{{DISPLAY.record.name}} | {{DISPLAY.record.date}}

				<div name="start" class="record-content start"><strong><u>{{DISPLAY.record.fstart}}</u></strong></div>

				| {{DISPLAY.record.date}}

				% if DISPLAY.record.isPending():
						
					% include("complete_end_form.tpl", recordIndex=DISPLAY.index)

					| {{DISPLAY.record.duration}}

				% else:

					<div name="end" class="record-content end"><strong><u>{{DISPLAY.record.fend}}</u></strong></div> |
					
					<div name="duration" class="record-content duration">

						% if float(DISPLAY.record.duration) <= 0:
							<span class="negative">{{DISPLAY.record.duration}}</span>
						% else:
							{{DISPLAY.record.duration}}
						% end

					</div>

				% end

				|
				<div name="label" class="record-content label">{{DISPLAY.record.label}}</div>
				|
				% include("toggle_display_billable.tpl", record=DISPLAY.record, recordIndex=DISPLAY.index)
				| 
				% include("toggle_display_emergency.tpl", record=DISPLAY.record, recordIndex=DISPLAY.index)				
				|
				<br>
				% include("update_notes_form.tpl", record=DISPLAY.record, recordIndex=DISPLAY.index)
				
			</h4>

		</div> <!-- /.media-body -->
	</div> <!-- /.media -->

</div>
</div>
</div>
</div>
