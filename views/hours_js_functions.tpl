

<script type="text/javascript">


function confirmDelete() {
	var choice = confirm("Are you sure you want to delete records?");
	if (choice) {
		document.getElementById("deleteConfirm").value = "true";
	}
}

function emailRecords() {
	confirm("Are you sure you want to email records?");
}


// gets element with provided id, sets value to "", and gives focus
function focusAndClearField(id) {
	var elem = document.getElementById(id);
	elem.value = "";
	elem.focus();
}


function adjustNextIndex(insertID, recordIndex) {
	document.getElementById(insertID).value = recordIndex;
}


function openViewer() {
	var str = document.getElementById("viewRecords").value;
	OpenWindow=window.open("", "newwin", "width=550, height=750, toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.moveTo(0,0);
	OpenWindow.document.write(`
	<html>
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
	 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
		<title>Hours</title>
	</head>
	<body>
	<div class="container" id="viewerContents">
		<div class="row">
			<div class="col-md-6 col-md-offset-3">
				<div class="panel panel-default">
					<div class="panel-body">`);
	OpenWindow.document.write(str);
	OpenWindow.document.write(`
					</div>
				</div>
			</div>
		</div>
	</div>
	</body>
	</html>
	`);
	var contents = document.getElementById("viewerContents");
	console.log("width: " + contents.offsetWidth + " height: " + contents.offsetHeight)
	OpenWindow.resizeTo(contents.offsetWidth, contents.offsetHeight);
	OpenWindow.document.close();
	self.name="main"
}


function openUpdateViewer(self) {
	OpenWindow=window.open("", "newwin", "width=750, height=750, toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.moveTo(0,0);
// 	OpenWindow.document.write(`
// <html>
// <head>
// 	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
// 	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
//  	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
// 	<title>Updates</title>
// </head>
// <body>
// <div class="container" id="viewerContents">
// 	<div class="row">
// 		<div class="col-md-6 col-md-offset-3">
// 			<div class="panel">
// 				<div class="panel-heading">
// 					<h4>Updates</h4>
// 				</div>
// 				<div class="panel-body">
// 					<ol>`);
// 		for (line in self.attributes["data-updates"].value.split("\n")) {
// 			OpenWindow.document.write(`<li>` + line + `</li>`);
// 		}
// 		OpenWindow.document.write(`
// 					</ol>
// 				</div>
// 			</div>
// 		</div>
// 	</div>
// </div>
// </body>
// </html>
// `);
	OpenWindow.document.write(`
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
	<title>Updates</title>
</head>
<body>
<div class="container" id="viewerContents">
	<div class="row">
		<div class="col-md-6 col-md-offset-3">
			<div class="panel">
				<div class="panel-heading">
					<h4>Updates</h4>
				</div>
				<div class="panel-body">
					<ol>
						<li>
							<span class="bugfix">BUGFIX</span> : monthly subtotal used to be wrongly incremented when a record's notes were changed
						</li>
						<li>
							Incomplete records now have an input field AND a button that will insert current rounded time
						<li>
							Checkboxes are modified based on the value of the label select/input elem
							<ul>
								<li>
									Selecting a value will match the presets on file
								</li>
								<li>
									Typing in a value will dynamically check if it matches an option
							</ul>
						</li>
						<li>
							Incomplete records now have an input field for the end time
							<ul>
								<li>
									End time can be saved with the save button OR by pressing enter
								</li>
								<li>
									Entered time must conform to 15-minute intervals (this is checked)
								</li>
							</ul>
						</li>
						<li>
							Deleting a record requires a double-click on the delete button
						</li>
						<li>
							Notes/description can be edited and saved with the save button OR by pressing enter
						</li>
						<li>
							Pulling records with an empty date defaults to the current date
						</li>
					</ol>
				</div>
			</div>
		</div>
	</div>
</div>
</body>
</html>
`);
	OpenWindow.document.close();
	self.name="main"
}



function setCheckboxes(index, billable, emergency) {
	if (billable === "Y") {
		// console.log("SETTING BILLABLE TO TRUE");
		document.getElementById("billable" + index).checked = true;
	} else {
		// console.log("SETTING BILLABLE TO FALSE");
		document.getElementById("billable" + index).checked = false;
	}

	if (emergency === "Y") {
		// console.log("SETTING EMERGENCY TO TRUE");
		document.getElementById("emergency" + index).checked = true;
	} else {
		// console.log("SETTING EMERGENCY TO FALSE");
		document.getElementById("emergency" + index).checked = false;
	}
}


function dropdownChangeSelect(self) {
	var index = self.attributes["data-index"].value;
	var selected = self.options[self.selectedIndex];

	var billable = selected.attributes["data-billable"].value
	var emergency = selected.attributes["data-emergency"].value

	setCheckboxes(index, billable, emergency);

	// console.log(index, billable, emergency);
	// console.log(selected);

	var input = self.parentElement.querySelector("[name='dropdown']");
	input.value = self.options[self.selectedIndex].text;

	var value = self.parentElement.querySelector("[name='label']");
	value.value = self.options[self.selectedIndex].value;
}

function dropdownChangeType(self) {
	var index = self.attributes["data-index"].value;
	var names = self.attributes["data-name"].value;
	var billable = self.attributes["data-billable"].value;
	var emergency = self.attributes["data-emergency"].value;
	

	names = names.replace(/,|'|\[|\]/g, '').split(" ");
	billable = billable.replace(/,|'|\[|\]/g, '').split(" ");
	emergency = emergency.replace(/,|'|\[|\]/g, '').split(" ");

	var selected_index = names.indexOf(self.value.toUpperCase());

	if (selected_index >= 0) {
		setCheckboxes(index, billable[selected_index], emergency[selected_index]);
	} else {
		setCheckboxes(index, billable[0], emergency[0]);
	}


	var input = self.parentElement.querySelector("[name='dropdown']");
	var value = self.parentElement.querySelector("[name='label']");

	value.value = input.value;
}


function submitOnEnterPressed(event, formElem) {

	// if enter button was pressed, submit the form
	if (event.keyCode === 13) {
		formElem.submit();
	}
}

function setValueFromInnerText(self) {
	self.value = self.innerText;
}


</script>