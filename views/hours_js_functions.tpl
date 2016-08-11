

<script type="text/javascript">

/*
// come back to this maybe
function focusEndTime(endID) {
	console.log("In focusEndTime()")
	console.log("endID:", endID)
	document.getElementById(endID).focus();
}
*/


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

// @param recordID: id of record that should stay open
// loops through and closes all of the records; then opens the one specified by recordID
function openForm(recordID) {
	var i = 0
	var form = document.getElementById('record' + i)
	while (form != null) {
		form.classList.remove('in');
		form.classList.add('collapse');
		// get next record
		form = document.getElementById('record' + (++i))
	}
	// set specified record to be open
	var form = document.getElementById(recordID);
	form.classList.remove('collapse');
	form.classList.add('in');
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


function openUpdateViewer() {
	OpenWindow=window.open("", "newwin", "width=750, height=750, toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.moveTo(0,0);
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






function dropdownChangeSelect(self) {
	var input = self.parentElement.querySelector("[name='dropdown']");
	input.value = self.options[self.selectedIndex].text;

	var value = self.parentElement.querySelector("[name='label']");
	value.value = self.options[self.selectedIndex].value;
}

function dropdownChangeType(self) {
	var input = self.parentElement.querySelector("[name='dropdown']");
	var value = self.parentElement.querySelector("[name='label']");

	value.value = input.value;
}


function enableSaveButton(event, self) {

	// get i value from hidden child
	var i = self.children[0].value;

	// get ith edit button
	var btn = document.getElementById("edit" + i);

	// if enter button was pressed, submit the form
	if (event.keyCode === 13) {
		btn.parentElement.submit();
	}

	// enable btn
	btn.disabled = false;
	
	if (self.attributes["name"].value === "description") {
		// get element where new description text will be submitted
		var new_description = document.getElementById("newDescription" + i);
		// console.log("NEW DESC: " + new_description)
		// get text from description field
		var text = self.children[1].innerHTML;
		// console.log("TEXT: " + text);
		// set new text to form element
		new_description.value = text;
	
	} else if (self.attributes["name"].value === "completeEndTime") {
		
		var new_end_time = document.getElementById("completeEndTime" + i);

		var text = self.children[1].value;

		new_end_time.value = text;
	}
	
}

</script>