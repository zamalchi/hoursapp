<%
"""
This sub-template provides a dropdown/text-input field for a record's label
Inputting text will match the value against REGEX.LABELS (which only allows an existing label)
"""
%>

<div name="dropdown-wrapper">
	<div class="dropdown form-control">
		<%
		"""
		Splits each label entry into its components: name, billable y/n, and emergency y/n
		"""
		ls_name = [""]
		ls_billable = ["Y"]
		ls_emergency = ["N"]

		for each in DATA.LABELS:
	  	l = each.split(" | ")
	  	ls_name.append(l[0])
	  	ls_billable.append(l[1])
	  	ls_emergency.append(l[2])
	  end
		%>

		<select class="dropdown-select" data-index="{{recordIndex}}" tabindex="4"
			onchange="dropdownChangeSelect(this)">

			% for i, each in enumerate(ls_name):
				<option value="{{each}}" data-billable="{{ls_billable[i]}}" data-emergency="{{ls_emergency[i]}}">{{each}}</option>
			% end

		</select>
		
		<input type="text" name="{{HTML_LABELS.DROPDOWN}}" id="{{HTML_LABELS.DROPDOWN+str(recordIndex)}}" class="dropdown-input"
			pattern="{{REGEX.LABELS}}" placeholder="Label"
			data-name="{{ls_name}}" data-billable="{{ls_billable}}" data-emergency="{{ls_emergency}}" data-index="{{recordIndex}}"
			onfocus="this.select()" onchange="dropdownChangeType(this)"
			style="text-transform: uppercase;"
			tabindex="5" required />
		
		<input type="hidden" name="{{HTML_LABELS.LABEL}}" id="{{HTML_LABELS.LABEL+recordIndex}}" />

	</div>
</div>